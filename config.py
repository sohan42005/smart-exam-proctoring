import os

class Config:
    SECRET_KEY = 'super_secret_exam_key_for_development'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'database.db')
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(BASE_DIR, 'flask_session')
    
    EVIDENCE_DIR = os.path.join(BASE_DIR, 'evidence')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Ensure directories exist
    os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)
    os.makedirs(SESSION_FILE_DIR, exist_ok=True)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
