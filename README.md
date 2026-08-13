# 🛡️ AI-Based Smart Exam Proctoring and Malpractice Detection System

An advanced, AI-powered online examination platform designed to ensure academic integrity during remote assessments. This system combines a secure online examination environment with real-time computer vision, browser behavior monitoring, automated evidence collection, and dynamic risk analysis to detect and deter malpractice.

---

## 2. Badges

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-yellow)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 3. Features

| Feature | Description |
| ------- | ----------- |
| **Real-Time Webcam Monitoring** | Continuous background analysis of the student's webcam feed during the exam. |
| **Face Detection** | Identifies the presence of a face in the frame. |
| **Face Absence Detection** | Flags an event when no face is visible in the frame. |
| **Multiple Face Detection** | Detects if more than one person is present in front of the camera. |
| **Looking-Away Detection** | Identifies when the student is not looking at the screen by analyzing facial profiles. |
| **Mobile Phone Detection** | Uses AI to detect unauthorized objects, specifically mobile phones. |
| **Suspicious Audio Detection** | Analyzes microphone volume to detect loud noises or potential communication. |
| **Tab Switching Detection** | Alerts and records when a user switches browser tabs or loses focus. |
| **Fullscreen Exit Detection** | Enforces fullscreen mode and flags if the user attempts to exit it. |
| **Right Click Prevention** | Disables context menus to prevent copying and pasting. |
| **Evidence Capture** | Automatically saves webcam snapshots for medium to high-severity events. |
| **Risk Score Engine** | Dynamically calculates a risk score and categorizes the attempt (Low/Medium/High Risk). |
| **Automatic Examination Evaluation** | Instantly grades the exam and calculates the percentage upon submission. |
| **Randomized Questions** | Randomly selects 50 questions for each exam attempt and shuffles options. |
| **Admin Portal** | A secure dashboard for administrators to review attempts, scores, and proctoring logs. |
| **Student Portal** | Interface for students to log in, read instructions, and take the exam. |

---

## 4. Project Architecture / Folder Structure

```text
Project/
├── source code/           # Main application source code directory
│   ├── app.py             # Main Flask application and server entry point
│   ├── init_db.py         # Database initialization and question seeding script
│   ├── config.py          # Application configuration (Keys, Paths)
│   ├── routes/            # Blueprint routes for different application modules
│   │   ├── auth.py        # Authentication routes (Login, Instructions, etc.)
│   │   ├── exam.py        # Examination logic (Load questions, save answers, submit)
│   │   ├── proctoring.py  # AI processing and event logging APIs
│   │   └── admin.py       # Admin dashboard and review logic
│   ├── utils/
│   │   └── database.py    # Database connection and schema definitions
│   ├── templates/         # HTML Jinja2 templates (Frontend)
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── exam.html
│   │   ├── result.html
│   │   └── ...
│   └── static/            # Static assets (CSS, JS, Images)
├── requirements.txt       # Project dependencies
├── yolov8n.pt             # Pre-trained YOLOv8 Nano model for object detection
├── database/              # Directory containing the SQLite database (database.db)
├── evidence/              # Directory where captured webcam snapshots are saved
└── flask_session/         # Server-side session storage directory
```

---

## 5. Technology Stack

### AI / Computer Vision
| Component | Technology |
| --------- | ---------- |
| Face Detection | OpenCV (Haar Cascades - Frontal & Profile) |
| Object Detection | YOLOv8 (Ultralytics) |
| Image Processing | OpenCV (`cv2`), NumPy, Pillow |

### Backend
| Component | Technology |
| --------- | ---------- |
| Web Framework | Flask |
| Session Management | Flask-Session |
| Password Hashing | Werkzeug Security |

### Frontend
| Component | Technology |
| --------- | ---------- |
| Structure / Styling | HTML, CSS |
| Interactivity | Vanilla JavaScript |
| Webcam/Mic Access | HTML5 MediaDevices API (`getUserMedia`) |

### Database
| Component | Technology |
| --------- | ---------- |
| Relational DB | SQLite |

---

## 6. System Architecture

```text
Student
   ↓
Login (Authentication)
   ↓
Online Examination (Fullscreen enforced)
   ↓
Background Proctoring (JS MediaDevices)
   ↓
   ├── Browser Events (Tab Switch, Fullscreen Exit)
   ├── Audio Monitoring (Volume Threshold)
   └── Frame Capture (Every 4 seconds)
         ↓
    AI Detection (Flask Backend)
         ├── Face Detection (Haar Cascades)
         ├── Looking-Away Detection
         ├── Multiple Face Detection
         └── Object Detection (YOLOv8 Phone Detection)
         ↓
Suspicious Event Engine (Log to DB)
         ↓
Evidence Capture (Save snapshot to disk)
         ↓
Risk Score Update (Low/Medium/High)
         ↓
Admin Dashboard (Chronological Review & Analytics)
```

---

## 7. How the AI Proctoring Works

```text
Webcam Frame (Browser)
      ↓
Base64 Encoded Image sent via AJAX
      ↓
OpenCV Frame Decoding (Backend)
      ↓
Grayscale Conversion
      ↓
Face Detection (Haar Frontal + Profile Cascades)
      ↓
YOLOv8 Inference (Phone detection)
      ↓
Determine Proctoring Event (No Face, Phone, etc.)
      ↓
Save Snapshot to /evidence (if severity >= 10)
      ↓
Update Student Risk Score in Database
```

---

## 8. Face Monitoring

The system uses **OpenCV's Haar Cascades** for face monitoring:
- **Face Presence**: Detects if a student is actively in front of the camera.
- **Face Absence (`NO_FACE`)**: Flagged when no faces are detected in the current frame.
- **Multiple Faces (`MULTIPLE_FACES`)**: Flagged when the detection algorithm finds more than one bounding box, indicating potential unauthorized assistance.

---

## 9. Head Movement / Looking-Away Detection

The system intelligently detects if a user is looking away from the screen by analyzing facial profiles.

- It runs both `haarcascade_frontalface_default` and `haarcascade_profileface`.
- **Logic**: If the system detects `0` frontal faces but `>0` profile faces, it triggers a `LOOKING_AWAY` event, indicating the student has turned their head significantly away from the monitor.

---

## 10. Object Detection

The system utilizes **YOLOv8** (`yolov8n.pt` - Nano model) from Ultralytics.
- Each incoming frame is passed through the YOLO model.
- It specifically checks for the `cell phone` class.
- If a phone is detected in the frame, a high-severity `MOBILE_PHONE_DETECTED` event is triggered.

---

## 11. Browser Monitoring

Client-side JavaScript actively monitors the examination environment:
- **Tab Switching / Focus Lost**: Uses `visibilitychange` and `blur` events. Triggers a `TAB_SWITCH` event if the student navigates away.
- **Fullscreen Exit**: Enforces the Fullscreen API. If `fullscreenchange` indicates an exit, a `FULLSCREEN_EXIT` event is logged, and an overlay blocks the exam until fullscreen is restored.
- **Right-Click Prevention**: Blocks `contextmenu` to prevent easy copying of questions.
- **Suspicious Audio**: Monitors microphone input using `AudioContext` and `AnalyserNode`. If the average volume exceeds a threshold, a `SUSPICIOUS_AUDIO` event is flagged.

---

## 12. Suspicious Event Management

When a suspicious activity is detected, it is logged in the `proctoring_events` database table with the following fields:
- `event_id`
- `attempt_id` (Link to the specific exam session)
- `student_id`
- `event_type` (e.g., MOBILE_PHONE_DETECTED, TAB_SWITCH)
- `timestamp`
- `description`
- `severity` (Weighted impact on the risk score)
- `evidence_path` (Path to the saved image snapshot, if applicable)

---

## 13. Risk Scoring

Each event type has an associated severity weight:
- `TAB_SWITCH`: 5
- `FULLSCREEN_EXIT`: 5
- `LOOKING_AWAY`: 5
- `NO_FACE`: 10
- `SUSPICIOUS_AUDIO`: 10
- `MULTIPLE_FACES`: 20
- `MOBILE_PHONE_DETECTED`: 30

**Risk Calculation:**
The total risk score is the sum of all event weights during the attempt.
- **Low Risk**: Score ≤ 20
- **Medium Risk**: 20 < Score ≤ 50
- **High Risk**: Score > 50

---

## 14. Evidence Collection

- **Trigger**: Evidence (an image snapshot) is captured for events with a severity score of `10` or higher (e.g., Phone detected, multiple faces).
- **Storage**: The Base64 image from the frontend is decoded and saved as a `.jpg` using `cv2.imwrite()` in the `evidence/<attempt_id>/` directory.
- **Linkage**: The file path is saved in the `evidence_path` column of the event log, allowing admins to view the exact moment the infraction occurred.

---

## 15. Examination System

```text
Student Login
   ↓
Read Instructions & System Check
   ↓
Start Exam (Attempt Created)
   ↓
50 Randomized Questions Loaded
   ↓
Answer Submission via AJAX
   ↓
Submit Exam
   ↓
Automatic Evaluation (Correct/Wrong/Percentage)
   ↓
Results Page
```

---

## 16. Admin Portal

Administrators have access to a dedicated portal (`/admin/dashboard`):
- **Dashboard**: High-level statistics and a list of recent exam attempts.
- **Review Attempt**: Detailed view of a specific student's exam, including score, percentage, and risk status.
- **Events Log**: A chronological timeline of all proctoring events triggered during that specific attempt, including direct links to view image evidence.

---

## 17. Analytics Dashboard

The admin dashboard provides immediate statistical insights:
- Total registered students.
- Total exams completed.
- Average score percentage across all students.
- Total count of "High Risk" attempts requiring review.

---

## 18. Exam Replay (Chronological Event Review)

Administrators can review an attempt chronologically via the Events Log table.

```text
Exam Started
     ↓
Tab Switch (10:15 AM)
     ↓
Looking Away (10:18 AM)
     ↓
Phone Detected [View Image] (10:22 AM)
     ↓
Exam Submitted
```

---

## 19. API Reference

| Group | Endpoint | Method | Description |
| ----- | -------- | ------ | ----------- |
| **Auth** | `/login` | GET/POST | Student login |
| | `/logout` | GET | Clear session |
| **Exam** | `/exam` | GET | Load examination interface |
| | `/api/save-answer` | POST | Auto-save selected option |
| | `/submit-exam` | POST | Finalize and grade exam |
| | `/result` | GET | View exam score |
| **Proctor** | `/api/proctor/event` | POST | Log browser-based events (tab switch) |
| | `/api/proctor/analyze` | POST | Process webcam frame for AI detection |
| **Admin** | `/admin/login` | GET/POST | Administrator login |
| | `/admin/dashboard` | GET | Admin overview statistics |
| | `/admin/attempt/<id>` | GET | View specific exam attempt and logs |
| | `/evidence/<id>/<file>`| GET | Securely serve evidence images |

---

## 20. Database

The system uses **SQLite** with the following primary tables:

| Table | Purpose |
| ----- | ------- |
| `students` | Stores student credentials and hashed passwords. |
| `admins` | Stores admin credentials. |
| `questions` | Bank of all available examination questions. |
| `exam_attempts` | Tracks a specific exam session, start/end times, and risk score. |
| `exam_questions`| Maps the randomly selected 50 questions to an attempt. |
| `student_answers`| Records the option selected by the student. |
| `exam_results` | Stores final calculated scores and percentages. |
| `proctoring_events`| Logs every suspicious activity and links to evidence. |

---

## 21. Installation

### Prerequisites
- Python 3.8+
- Webcam and Microphone (for client-side testing)

### Clone the Repository
```bash
git clone <repository-url>
cd <project-folder>
```

### Create a Virtual Environment (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Initialize the Database
This will create `database.db`, seed it with questions, and create demo accounts:
- Student: `student001` / `student123`
- Admin: `admin` / `admin123`
```bash
python init_db.py
```

### Run the Application
```bash
python app.py
```
Access the application at: `http://localhost:5000`

---

## 22. Configuration

The application is configured via `config.py`. 
Directories for `database/`, `evidence/`, `logs/`, and `flask_session/` are automatically created on startup.

**Important Note for Deployment:**
Always change the `SECRET_KEY` in `config.py` (or load it from an environment variable `.env`) before deploying to production. Do not expose secret keys in public repositories.

---

## 23. Running the System

### Student Workflow
```text
Login (student001)
 ↓
Read Instructions & System Check (Allow Camera/Mic)
 ↓
Enter Fullscreen & Start Examination
 ↓
Answer Questions (Background Proctoring Active)
 ↓
Submit Exam -> View Score
```

### Admin Workflow
```text
Admin Login (admin)
 ↓
Dashboard (View global stats)
 ↓
Select a Recent Attempt
 ↓
Review Final Score & Risk Status
 ↓
Analyze Proctoring Events Log
 ↓
Click "View Image" on Evidence
```

---

## 24. Screenshots

> *Placeholder for project screenshots. Add images to this section later.*
>
> - **Login Screen:** `[Add Screenshot Here]`
> - **Examination Interface:** `[Add Screenshot Here]`
> - **Admin Dashboard:** `[Add Screenshot Here]`
> - **Proctoring Evidence Log:** `[Add Screenshot Here]`

---

## 25. Project Results / Capabilities

This system successfully demonstrates the integration of a web-based examination platform with real-time AI computer vision. It is capable of autonomously monitoring a student, detecting physical unauthorized items (phones), tracking behavioral anomalies (looking away, leaving the screen, tab switching), and aggregating this data into a structured risk profile for administrative review.

---

## 26. Security and Privacy

- **Data Privacy:** Webcam frames are processed continuously, but images are **only** saved to the disk if a medium-to-high severity anomaly is detected.
- **Review Process:** AI detections are indicators of potential malpractice. All flagged events and risk scores should be reviewed by authorized administrative personnel before any disciplinary action is taken.

---

## 27. Limitations

- **Lighting Conditions:** Haar cascades and object detection models perform poorly in low light or extreme backlighting.
- **False Positives:** Haar cascades may occasionally misidentify background patterns as faces. YOLOv8 might misclassify objects resembling a phone.
- **Browser APIs:** Tab switching and fullscreen detection rely on browser-specific APIs, which can sometimes be circumvented by advanced users or browser extensions.
- **Processing Overhead:** Processing frames every 4 seconds on the backend server can introduce latency if scaled to hundreds of concurrent users.

---

## 28. Future Enhancements

- **Advanced Identity Verification:** Implementing facial recognition to verify the student matches their ID card.
- **Model Upgrades:** Replacing Haar Cascades with deep-learning-based facial landmark detection (e.g., MediaPipe) for highly accurate head pose estimation (Pitch, Yaw, Roll).
- **WebRTC Implementation:** Streaming video via WebRTC rather than sending Base64 images for lower latency and continuous recording capabilities.
- **More Robust False-Positive Reduction:** Implementing temporal logic (e.g., requiring an object to be visible for 3 consecutive frames before flagging).

---

## 29. Version Control

To push this project to GitHub:

```bash
git init
git add .
git commit -m "Initial project implementation"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

**Recommended `.gitignore`:**
```text
__pycache__/
venv/
*.db
evidence/*
!evidence/.gitkeep
flask_session/*
!flask_session/.gitkeep
```

---

## 30. Project Deliverables

| Deliverable | Location | Status |
| ----------- | -------- | ------ |
| Source Code | Root folder | ✅ |
| AI Models | `yolov8n.pt` | ✅ |
| Database Scripts | `init_db.py`, `utils/database.py` | ✅ |
| Frontend Templates | `templates/`, `static/` | ✅ |
| Documentation | `README.md` | ✅ |

---

## 31. Acknowledgements

This project utilizes several open-source technologies:
- **Ultralytics** for the YOLOv8 object detection model.
- **OpenCV** for image processing and Haar cascade face detection.
- **Flask** & **SQLite** for backend routing and data storage.

---

## 32. Disclaimer

This project is developed for educational and academic purposes.

AI-based proctoring systems can produce false positives. Suspicious events and risk scores should be treated as review indicators and should be evaluated by authorized personnel rather than being considered automatic proof of malpractice.
