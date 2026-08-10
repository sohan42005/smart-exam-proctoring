# WORK PROGRESS

## 1. Detailed Work Progress

**1. Project Planning and Requirement Analysis**
*   **Work Completed:** The requirements for an AI-based online examination and proctoring system were identified. The core constraints (webcam/microphone access, strict examination environment) and necessary modules (AI proctoring, exam engine, admin dashboard) were defined.
*   **Technology Used:** N/A (Planning phase)
*   **Status:** COMPLETED

**2. System Design and Architecture**
*   **Work Completed:** The relational database schema and application routing structure were designed. A client-server architecture was finalized where the browser handles continuous frame capture and the backend performs AI analysis.
*   **Technology Used:** Python, SQLite, HTML/CSS
*   **Status:** COMPLETED

**3. Database Development**
*   **Work Completed:** The SQLite database was implemented with normalized tables for students, administrators, aptitude questions, examination attempts, student answers, exam results, proctoring events, and photographic evidence.
*   **Technology Used:** SQLite, Python sqlite3
*   **Status:** COMPLETED

**4. Student and Admin Authentication**
*   **Work Completed:** Distinct, secure login portals were created for students and administrators using hashed passwords and session management.
*   **Technology Used:** Flask, Werkzeug Security, HTML/CSS
*   **Status:** COMPLETED

**5. Examination Module**
*   **Work Completed:** The main examination interface was developed featuring a question display area, a dynamic question palette for navigation, and a secure countdown timer.
*   **Technology Used:** HTML, CSS, JavaScript, Flask
*   **Status:** COMPLETED

**6. Aptitude Question Bank Generation**
*   **Work Completed:** A programmatic question generator was implemented to dynamically create over 1,000 distinct mathematical, quantitative, and logical aptitude questions with accurately calculated distractors (wrong options).
*   **Technology Used:** Python (random module)
*   **Status:** COMPLETED

**7. Question Randomization and Shuffling**
*   **Work Completed:** The backend was configured to randomly select 50 questions per examination attempt. A deterministic shuffling algorithm was implemented to randomize the order of options (A, B, C, D) uniquely for each attempt while preserving the correct answer mapping.
*   **Technology Used:** Python
*   **Status:** COMPLETED

**8. Pre-Exam System Verification and Selfie Capture**
*   **Work Completed:** Modules were developed to explicitly request and verify webcam and microphone permissions. A selfie capture mechanism was integrated to serve as baseline identity verification evidence prior to exam commencement.
*   **Technology Used:** JavaScript (MediaDevices API), Flask
*   **Status:** COMPLETED

**9. Camera-Based AI Proctoring**
*   **Work Completed:** A continuous background monitoring system was implemented. The frontend silently captures video frames every 4 seconds and transmits them to the backend for computer vision analysis without interrupting the student.
*   **Technology Used:** JavaScript (Canvas API), Python, OpenCV
*   **Status:** COMPLETED

**10. Face and Multiple-Face Detection**
*   **Work Completed:** Face detection was implemented using OpenCV Haar Cascades to reliably identify the presence of a face, absence of a face (NO_FACE), and the presence of unauthorized individuals (MULTIPLE_FACES) in the camera frame.
*   **Technology Used:** Python, OpenCV (Haar Cascades)
*   **Status:** COMPLETED

**11. Mobile Phone Detection**
*   **Work Completed:** A deep learning object detection model was integrated to specifically scan video frames for unauthorized devices (e.g., mobile phones or smart devices) during the examination.
*   **Technology Used:** Python, YOLOv8 (Ultralytics)
*   **Status:** COMPLETED

**12. Microphone Monitoring**
*   **Work Completed:** Background audio processing was implemented in the browser using the Web Audio API to analyze frequency and volume levels. Sustained loud noises or talking trigger a SUSPICIOUS_AUDIO event.
*   **Technology Used:** JavaScript (Web Audio API)
*   **Status:** COMPLETED

**13. Fullscreen and Browser Monitoring**
*   **Work Completed:** The examination engine strictly enforces the Fullscreen API. If a student attempts to exit fullscreen, switch tabs, or minimize the browser, the system immediately blocks the examination interface and records the violation.
*   **Technology Used:** JavaScript (Fullscreen API, Page Visibility API)
*   **Status:** COMPLETED

**14. Malpractice Detection and Risk Score Logging**
*   **Work Completed:** A centralized proctoring event logger was developed. Detected infractions are assigned a severity weight (Low, Medium, High) which aggregates into a total Risk Score for the examination attempt, ultimately categorizing the attempt as Low, Medium, or High Risk.
*   **Technology Used:** Python, SQLite
*   **Status:** COMPLETED

**15. Evidence Collection**
*   **Work Completed:** When the AI modules detect critical infractions (e.g., mobile phone detected, no face), the specific video frame is saved to the local file system as cryptographic evidence and linked directly to the event log in the database.
*   **Technology Used:** Python, Base64 Image Processing
*   **Status:** COMPLETED

**16. Automatic Exam Evaluation**
*   **Work Completed:** Upon submission or timer expiration, the backend immediately calculates the total attempted questions, correct answers, wrong answers, and final percentage, storing the results immutably in the database.
*   **Technology Used:** Python, SQLite
*   **Status:** COMPLETED

**17. Admin Dashboard**
*   **Work Completed:** A secure, premium administrative dashboard was designed. Administrators can review all student attempts, analyze final scores, view the aggregated risk status, read the detailed proctoring event log, and manually inspect captured photographic evidence.
*   **Technology Used:** Flask, HTML, CSS
*   **Status:** COMPLETED


---

## 2. Report-Ready Version

**WORK PROGRESS**

1. The project requirements were analyzed and the overall architecture of the AI-based online examination and proctoring system was designed.
2. A normalized SQLite database was established to manage student data, dynamic question banks, examination attempts, and proctoring event logs.
3. Secure, distinctly styled authentication portals were developed for both students and administrators.
4. An automated question generator was implemented to supply a repository of over 1,000 distinct mathematical and logical aptitude questions.
5. The core examination module was developed, featuring a secure countdown timer, dynamic question palette, and backend-driven deterministic option shuffling.
6. System check protocols were integrated to verify hardware access (webcam and microphone) and capture baseline selfie evidence prior to the examination.
7. Background video and audio processing logic was implemented to continually monitor the student without interrupting the examination interface.
8. Computer vision-based face monitoring was implemented using OpenCV Haar Cascades to reliably detect face absence, multiple faces, and profile orientations.
9. A YOLOv8 deep learning model was integrated into the backend pipeline to detect the presence of unauthorized objects, specifically mobile phones.
10. The Web Audio API was utilized to continuously sample microphone input and log instances of suspicious audio or talking.
11. Browser-level security constraints were enforced using the Fullscreen API and Page Visibility API to prevent tab-switching and mandate a locked testing environment.
12. A weighted risk-scoring algorithm was implemented to aggregate proctoring infractions and classify examination attempts into distinct risk categories.
13. An automated evaluation engine was constructed to grade the examination instantly upon submission or timer expiration.
14. A comprehensive administrative dashboard was developed, allowing proctors to review student scores, analyze detailed event logs, and inspect captured photographic evidence of malpractice.

---

## 3. Current Completed Features

*   **Student login:** COMPLETED
*   **Admin login:** COMPLETED
*   **Exam instructions:** COMPLETED
*   **Camera permission:** COMPLETED
*   **Microphone permission:** COMPLETED
*   **Selfie capture:** COMPLETED
*   **Face detection:** COMPLETED
*   **Multiple-face detection:** COMPLETED
*   **No-face detection:** COMPLETED
*   **Head movement / Looking-away detection:** PARTIALLY COMPLETED (Implemented via profile face cascades, but could be enhanced with advanced landmarking)
*   **YOLOv8 mobile-phone detection:** COMPLETED
*   **Microphone/audio monitoring:** COMPLETED
*   **Fullscreen monitoring:** COMPLETED
*   **Tab-switch detection:** COMPLETED
*   **Browser activity monitoring:** COMPLETED
*   **Risk score:** COMPLETED
*   **Suspicious event logging:** COMPLETED
*   **Evidence capture:** COMPLETED
*   **Random aptitude questions:** COMPLETED
*   **Question palette:** COMPLETED
*   **Exam timer:** COMPLETED
*   **Automatic evaluation:** COMPLETED
*   **Result generation:** COMPLETED
*   **Admin dashboard:** COMPLETED
*   **Evidence gallery:** COMPLETED

## 4. Features Still Requiring Improvement

*   **Analytics:** NOT IMPLEMENTED (Basic statistics exist, but deep data visualizations across cohorts are missing).
*   **Export functionality:** NOT IMPLEMENTED (No capability currently exists to export results to PDF or CSV).
*   **Head movement tracking:** PARTIALLY COMPLETED (Currently relies on basic OpenCV Haar Cascades; requires a complex 3D landmark mesh for high-precision gaze tracking).
