import sys
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal
from PIL import Image, ImageDraw

# Import our custom modules
from overlay import PrivacyShield
from detector import FaceDetector
import pystray

# We need a Signal Handler to communicate between the Detector Thread and the GUI Thread
class Signaller(QObject):
    update_shield = pyqtSignal(bool)

def create_tray_icon(app_reference, detector_reference):
    # Create a simple icon image programmatically
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill="blue") # A simple blue square icon

    def on_exit(icon, item):
        detector_reference.stop()
        icon.stop()
        app_reference.quit()

    menu = (
        pystray.MenuItem('Status: Running', lambda icon, item: None, enabled=False),
        pystray.MenuItem('Exit Privacy Shield', on_exit)
    )

    icon = pystray.Icon("PrivacyShield", image, "Privacy Shield", menu)
    icon.run()

def main():
    # 1. Setup PyQt Application
    app = QApplication(sys.argv)
    
    # Prevent the app from quitting when the window is hidden (since we run in background)
    app.setQuitOnLastWindowClosed(False)

    # 2. Setup the Visual Shield
    shield = PrivacyShield()

    # 3. Setup Logic Bridge
    # PyQt widgets can only be updated by the Main Thread. 
    # The Detector runs in a background thread.
    # We use this signal to bridge the gap safely.
    bridge = Signaller()
    
    def gui_update(is_unsafe):
        if is_unsafe:
            shield.activate_shield()
        else:
            shield.deactivate_shield()
            
    # Connect signal to the function
    bridge.update_shield.connect(gui_update)

    # 4. Setup Detector
    # This callback is executed by the background thread, which emits the signal
    def detector_callback(is_unsafe):
        bridge.update_shield.emit(is_unsafe)

    detector = FaceDetector(callback_trigger=detector_callback, safe_face_count=1)
    detector.start()

    # 5. Setup System Tray (in a separate thread so it doesn't block Qt)
    tray_thread = threading.Thread(target=create_tray_icon, args=(app, detector))
    tray_thread.start()

    # 6. Run the App
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()