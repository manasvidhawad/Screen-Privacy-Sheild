import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

class PrivacyShield(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Remove window borders and keep on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # Set opacity (0.0 to 1.0). 0.95 makes it almost black but visible.
        self.setWindowOpacity(0.95)
        
        # Set Full Screen
        self.showFullScreen()
        
        # Set Background Color to Black
        self.setStyleSheet("background-color: black;")

        # Create the Warning Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Warning Text
        self.label = QLabel("PRIVACY ALERT\nSHOULDER SURFER DETECTED")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: red; font-weight: bold;")
        self.label.setFont(QFont('Arial', 40))
        
        # Subtext
        self.sub_label = QLabel("Please ensure you are alone before continuing.")
        self.sub_label.setAlignment(Qt.AlignCenter)
        self.sub_label.setStyleSheet("color: white;")
        self.sub_label.setFont(QFont('Arial', 14))

        layout.addWidget(self.label)
        layout.addWidget(self.sub_label)
        self.setLayout(layout)

        # Start Hidden
        self.hide()

    def activate_shield(self):
        if not self.isVisible():
            self.showFullScreen()
            self.raise_()
            self.repaint()

    def deactivate_shield(self):
        if self.isVisible():
            self.hide()

# For testing this file independently
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrivacyShield()
    window.activate_shield()
    sys.exit(app.exec_())