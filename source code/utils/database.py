import sqlite3
import os
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db_schema():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            name TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            category TEXT,
            difficulty TEXT,
            marks INTEGER DEFAULT 1
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS exam_attempts (
            attempt_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME,
            status TEXT DEFAULT 'IN_PROGRESS',
            risk_score INTEGER DEFAULT 0,
            risk_status TEXT DEFAULT 'Low Risk',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS exam_questions (
            attempt_id TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            question_order INTEGER NOT NULL,
            PRIMARY KEY (attempt_id, question_id),
            FOREIGN KEY (attempt_id) REFERENCES exam_attempts(attempt_id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS student_answers (
            attempt_id TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            selected_option TEXT,
            is_correct BOOLEAN,
            PRIMARY KEY (attempt_id, question_id),
            FOREIGN KEY (attempt_id) REFERENCES exam_attempts(attempt_id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS exam_results (
            attempt_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            total_questions INTEGER,
            attempted INTEGER,
            correct INTEGER,
            wrong INTEGER,
            unanswered INTEGER,
            score INTEGER,
            percentage REAL,
            FOREIGN KEY (attempt_id) REFERENCES exam_attempts(attempt_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS proctoring_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id TEXT NOT NULL,
            student_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            description TEXT,
            severity INTEGER DEFAULT 1,
            evidence_path TEXT,
            FOREIGN KEY (attempt_id) REFERENCES exam_attempts(attempt_id)
        )
    ''')
    
    conn.commit()
    conn.close()
