import os

class Config:
    SECRET_KEY = 'super_secret_exam_key_for_development'
    # Resolves to the parent directory of 'source code', i.e., the project root
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    DATABASE_PATH = os.path.join(PROJECT_ROOT, 'database', 'database.db')
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(PROJECT_ROOT, 'flask_session')
    
    EVIDENCE_DIR = os.path.join(PROJECT_ROOT, 'evidence')
    LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
    
    # Ensure directories exist
    os.makedirs(os.path.join(PROJECT_ROOT, 'database'), exist_ok=True)
    os.makedirs(SESSION_FILE_DIR, exist_ok=True)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
