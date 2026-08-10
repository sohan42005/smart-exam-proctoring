# AI-Based Smart Online Exam Proctoring and Malpractice Detection System

This is a complete, working Online Aptitude/Placement Examination platform with continuous AI proctoring in the background. It is built using Python, Flask, SQLite, and computer vision models (OpenCV, MediaPipe, YOLOv8).

## Features

- **Student Login & Authentication**: Secure login system.
- **Pre-Exam Verification**: Checks camera and microphone access, and requires a student selfie capture before the exam.
- **Randomized Question Bank**: Automatically selects 50 random aptitude questions from a generated pool of 1000+ questions. Questions and options are presented cleanly.
- **Continuous AI Proctoring**:
    - **Face Detection**: Detects if the student's face is missing from the frame (MediaPipe).
    - **Multiple Faces**: Detects if multiple people are in the frame (MediaPipe).
    - **Head Pose Estimation**: Detects if the student is looking away from the screen (MediaPipe / OpenCV).
    - **Mobile Phone Detection**: Detects if a mobile phone is visible (YOLOv8n).
- **Audio Monitoring**: Detects suspicious background noise or talking using the browser's Web Audio API.
- **Browser Monitoring**: Detects tab switching, window blurring, and exiting Fullscreen mode. Right-click is also disabled.
- **Evidence Capture**: Automatically captures webcam snapshots (evidence) when medium or high severity events occur (like phone detection or multiple faces).
- **Risk Engine**: Calculates a risk score based on proctoring events and categorizes the attempt as Low, Medium, or High Risk.
- **Admin Dashboard**: View total students, exams completed, average scores, and detailed proctoring logs (with evidence images) for each student attempt.

## Technology Stack

- **Backend**: Python, Flask, Flask-Session
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite3
- **Computer Vision**: OpenCV, MediaPipe (Face Mesh/Detection)
- **Object Detection**: Ultralytics YOLOv8 (yolov8n.pt)

## Folder Structure

```text
exam_test/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── init_db.py              # Script to initialize database and generate 1000+ questions
├── requirements.txt        # Python dependencies
├── database/               # SQLite database directory
├── evidence/               # Captured snapshots from proctoring
├── logs/                   # System logs
├── utils/                  # Database helpers
├── routes/                 # Blueprint routes
│   ├── auth.py             # Login, Instructions, System Check
│   ├── exam.py             # Exam core logic, Timer, Submit
│   ├── proctoring.py       # AI analysis of webcam frames
│   └── admin.py            # Admin Dashboard
├── static/                 # CSS & JS
└── templates/              # HTML Templates
```

## Installation & Running on Windows

1. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database:**
   This step will create the database, add demo users, and generate 1000 random questions.
   ```bash
   python init_db.py
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will start on `http://127.0.0.1:5000/`.

## Demo Credentials

**Student Login:**
- **Student ID:** student001
- **Password:** student123

**Admin Login:**
- **Username:** admin
- **Password:** admin123

## How the AI Proctoring Works

- The frontend continuously requests webcam and microphone access.
- Every 4 seconds, the frontend takes a snapshot of the `<video>` element, converts it to a Base64 string, and sends it to `/api/proctor/analyze`.
- The backend uses **MediaPipe** to detect faces. If 0 faces or >1 faces are found, it logs an event. If exactly 1 face is found, it calculates the head pose (pitch/yaw) to detect if the student is looking away.
- The backend uses **YOLOv8** to scan the frame for a "cell phone" object. If detected, it logs a severe event.
- Snapshots are saved to the `/evidence/<attempt_id>` folder if a severe event triggers.
- Browser events (fullscreen exit, tab switch) are detected via JavaScript (`visibilitychange`, `blur`, `fullscreenchange`) and sent directly to the backend logging API.
- Microphone activity is analyzed on the frontend using `AudioContext.createAnalyser()`. If the volume exceeds a threshold, an event is sent to the backend.

## Limitations & Security Note
- While this system employs robust AI checking, browser-based JavaScript cannot provide absolute control over the student's operating system (e.g., they could run a virtual machine). The strongest practical detection is implemented, but a truly secure exam often requires a dedicated desktop client.
