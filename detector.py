import cv2
import mediapipe as mp
import time
from threading import Thread

class FaceDetector:
    def __init__(self, callback_trigger, safe_face_count=1):
        """
        :param callback_trigger: Function to call when status changes (True=Unsafe, False=Safe)
        :param safe_face_count: Number of allowed faces (usually 1)
        """
        self.callback = callback_trigger
        self.safe_face_count = safe_face_count
        self.running = False
        self.cap = None
        
        # MediaPipe Setup
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

        # Logic Controls
        self.last_state_unsafe = False
        self.persistence_counter = 0
        self.persistence_threshold = 3  # Needs 3 consecutive frames to switch state (prevents flickering)

    def start(self):
        if self.running: return
        self.running = True
        self.thread = Thread(target=self._process_video, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def _process_video(self):
        self.cap = cv2.VideoCapture(0)
        
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            # Performance optimization: Resize frame slightly to speed up processing
            # frame = cv2.resize(frame, (640, 480))

            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb_frame)

            face_count = 0
            if results.detections:
                face_count = len(results.detections)

            # --- LOGIC CORE ---
            # If faces > 1, we have a surfer.
            # You can also add logic here: if face_count == 0, lock screen (user left).
            is_unsafe = face_count > self.safe_face_count

            # Stabilization Logic (Debouncing)
            # We don't want the screen to flash if the camera glitches for 1 millisecond.
            if is_unsafe != self.last_state_unsafe:
                self.persistence_counter += 1
            else:
                self.persistence_counter = 0

            if self.persistence_counter >= self.persistence_threshold:
                self.last_state_unsafe = is_unsafe
                # Trigger the callback (update UI)
                self.callback(is_unsafe)
                self.persistence_counter = 0

            # Sleep slightly to save CPU resource (approx 30 fps)
            time.sleep(0.03)

        self.cap.release()