from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from utils.database import get_db_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_user'] = admin['username']
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid Admin Credentials')
            
    return render_template('admin_login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_user', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
def dashboard():
    if 'admin_user' not in session:
        return redirect(url_for('admin.login'))
        
    conn = get_db_connection()
    
    # Stats
    total_students = conn.execute('SELECT COUNT(*) as cnt FROM students').fetchone()['cnt']
    exams_completed = conn.execute("SELECT COUNT(*) as cnt FROM exam_attempts WHERE status = 'COMPLETED'").fetchone()['cnt']
    avg_score_row = conn.execute('SELECT AVG(percentage) as avg_pct FROM exam_results').fetchone()
    avg_score = round(avg_score_row['avg_pct'] or 0, 2)
    high_risk = conn.execute("SELECT COUNT(*) as cnt FROM exam_attempts WHERE risk_status = 'High Risk'").fetchone()['cnt']
    
    # Recent Attempts
    attempts = conn.execute('''
        SELECT ea.attempt_id, ea.student_id, ea.start_time, ea.end_time, ea.status, ea.risk_score, ea.risk_status,
               er.score, er.percentage, s.name
        FROM exam_attempts ea
        LEFT JOIN exam_results er ON ea.attempt_id = er.attempt_id
        JOIN students s ON ea.student_id = s.student_id
        ORDER BY ea.start_time DESC
        LIMIT 20
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                           stats={'total_students': total_students, 'exams_completed': exams_completed, 'avg_score': avg_score, 'high_risk': high_risk},
                           attempts=[dict(a) for a in attempts])

@admin_bp.route('/attempt/<attempt_id>')
def view_attempt(attempt_id):
    if 'admin_user' not in session:
        return redirect(url_for('admin.login'))
        
    conn = get_db_connection()
    attempt = conn.execute('''
        SELECT ea.*, er.*, s.name 
        FROM exam_attempts ea 
        LEFT JOIN exam_results er ON ea.attempt_id = er.attempt_id
        JOIN students s ON ea.student_id = s.student_id
        WHERE ea.attempt_id = ?
    ''', (attempt_id,)).fetchone()
    
    events = conn.execute('SELECT * FROM proctoring_events WHERE attempt_id = ? ORDER BY timestamp DESC', (attempt_id,)).fetchall()
    conn.close()
    
    return render_template('admin_attempt.html', attempt=dict(attempt) if attempt else None, events=[dict(e) for e in events])
