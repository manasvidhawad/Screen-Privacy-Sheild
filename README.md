# Screen-Privacy-Sheild

-> Overview

The Privacy Shield is a real-time AI-powered privacy alert system that protects users from shoulder surfing in public environments. Using a webcam and face detection, the application monitors the area behind the user and instantly displays a privacy alert overlay when unauthorized viewers are detected.

This project demonstrates the integration of Computer Vision, Multithreading, and GUI systems for practical cybersecurity applications.

-> Problem Statement

Working in public places like libraries, cafés, or classrooms exposes sensitive information to nearby onlookers. Users often remain unaware when someone is watching their screen, leading to privacy breaches.

-> Solution

The Privacy Shield runs silently in the background and continuously analyzes webcam input.
If more than one face is detected in the frame, the system immediately activates a warning overlay with a privacy alert message, ensuring instant user awareness.

-> How It Works

The webcam captures live video feed

MediaPipe Face Detection detects faces in each frame

If detected faces exceed the allowed limit (default: 1), the environment is marked unsafe

A Privacy Alert overlay is displayed

When the environment becomes safe again, the overlay disappears

To prevent flickering due to brief detection errors, a frame persistence mechanism is used before changing states.

-> Key Features

Real-time face detection using MediaPipe

Privacy alert overlay

Background execution with system tray support

Multi-threaded architecture for smooth performance

Debouncing logic to avoid false alerts

Cross-platform Python implementation

🛠️ Tech Stack

Python

OpenCV

MediaPipe

PyQt5

PyStray

PIL (Pillow)

Multithreading

-> Project Structure
Privacy-Shield/
│
├── main.py            # Application entry point
├── detector.py        # Face detection and logic processing
├── overlay.py         # Full-screen privacy alert UI
├── requirements.txt   # Project dependencies
└── README.md

-> How to Run

Clone the repository

git clone https://github.com/your-username/privacy-shield.git
cd privacy-shield


Install dependencies

pip install -r requirements.txt


Run the application

python main.py


The application will run in the background and appear in the system tray.

-> Use Cases

Working in libraries or cafés

Classrooms and exam environments

Office desks in shared workspaces

Handling passwords, banking, or private messages

-> Future Enhancements

Gaze direction detection

Custom alert messages

Sound or notification-based alerts

User authentication (detect owner’s face)

Logging and alert history

-> License

This project is open-source and available for educational and personal use.
