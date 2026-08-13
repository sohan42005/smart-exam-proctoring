import cv2
import numpy as np
from ultralytics import YOLO
from flask import Blueprint, request, jsonify, session
from utils.database import get_db_connection
import os
import datetime
from config import Config
import base64

proctoring_bp = Blueprint('proctoring', __name__)

# Load YOLO model for phone detection
yolo_model = YOLO(os.path.join(Config.PROJECT_ROOT, 'yolov8n.pt')) 

# Load OpenCV Haar Cascades for face detection
# Using the default frontal face and profile face cascades included in opencv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

RISK_SCORES = {
    'TAB_SWITCH': 5,
    'FULLSCREEN_EXIT': 5,
    'NO_FACE': 10,
    'MULTIPLE_FACES': 20,
    'MOBILE_PHONE_DETECTED': 30,
    'SUSPICIOUS_AUDIO': 10,
    'LOOKING_AWAY': 5
}

def save_evidence(image_data, attempt_id, event_type):
    # Decode base64 image
    img_data = image_data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{event_type}_{timestamp}.jpg"
    folder = os.path.join(Config.EVIDENCE_DIR, attempt_id)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    cv2.imwrite(filepath, img)
    return filepath

def log_event(attempt_id, event_type, description, severity, image_data=None):
    student_id = session.get('student_id')
    evidence_path = None
    if image_data and severity >= 10: # Only save evidence for medium/high risk
        evidence_path = save_evidence(image_data, attempt_id, event_type)
        
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO proctoring_events (attempt_id, student_id, event_type, timestamp, description, severity, evidence_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (attempt_id, student_id, event_type, datetime.datetime.now(), description, severity, evidence_path))
    
    # Update risk score
    score_increment = RISK_SCORES.get(event_type, 0)
    conn.execute('UPDATE exam_attempts SET risk_score = risk_score + ? WHERE attempt_id = ?', (score_increment, attempt_id))
    
    # Update risk status
    attempt = conn.execute('SELECT risk_score FROM exam_attempts WHERE attempt_id = ?', (attempt_id,)).fetchone()
    current_score = attempt['risk_score']
    status = 'Low Risk'
    if current_score > 50:
        status = 'High Risk'
    elif current_score > 20:
        status = 'Medium Risk'
    conn.execute('UPDATE exam_attempts SET risk_status = ? WHERE attempt_id = ?', (status, attempt_id))
        
    conn.commit()
    conn.close()

@proctoring_bp.route('/api/proctor/event', methods=['POST'])
def handle_browser_event():
    if 'attempt_id' not in session:
        return jsonify({'status': 'error'})
        
    data = request.json
    event_type = data.get('event_type')
    log_event(session['attempt_id'], event_type, f"Browser event: {event_type}", RISK_SCORES.get(event_type, 5))
    return jsonify({'status': 'logged'})

@proctoring_bp.route('/api/proctor/analyze', methods=['POST'])
def analyze_frame():
    if 'attempt_id' not in session:
        return jsonify({'status': 'error'})
        
    data = request.json
    image_data = data.get('image')
    attempt_id = session['attempt_id']
    
    if not image_data:
        return jsonify({'status': 'no_image'})
        
    # Decode image for OpenCV processing
    img_data_decoded = base64.b64decode(image_data.split(',')[1])
    nparr = np.frombuffer(img_data_decoded, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return jsonify({'status': 'error_decoding'})

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    events_detected = []

    # 1. Phone Detection using YOLOv8
    results = yolo_model(frame, verbose=False)
    phone_detected = False
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            name = yolo_model.names[cls]
            if name == 'cell phone':
                phone_detected = True
                events_detected.append('MOBILE_PHONE_DETECTED')
                break
        if phone_detected: break
        
    if phone_detected:
        log_event(attempt_id, 'MOBILE_PHONE_DETECTED', 'Mobile phone detected in frame', RISK_SCORES['MOBILE_PHONE_DETECTED'], image_data)

    # 2. Face Detection
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    profiles = profile_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # We combine frontal and profile face detection to accurately count faces
    num_frontal = len(faces)
    num_profiles = len(profiles)
    
    num_total_faces = max(num_frontal, num_profiles)

    if num_total_faces == 0:
        events_detected.append('NO_FACE')
        log_event(attempt_id, 'NO_FACE', 'No face detected in frame', RISK_SCORES['NO_FACE'], image_data)
    elif num_total_faces > 1:
        events_detected.append('MULTIPLE_FACES')
        log_event(attempt_id, 'MULTIPLE_FACES', f'Multiple faces detected', RISK_SCORES['MULTIPLE_FACES'], image_data)
    else:
        # If no frontal face but profile face exists, they might be looking away
        if num_frontal == 0 and num_profiles > 0:
            events_detected.append('LOOKING_AWAY')
            log_event(attempt_id, 'LOOKING_AWAY', 'Looking away from screen', RISK_SCORES['LOOKING_AWAY'])

    return jsonify({'status': 'processed', 'events': events_detected})
