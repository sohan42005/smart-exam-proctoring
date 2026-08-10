from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import check_password_hash
from utils.database import get_db_connection
import os
import uuid
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        password = request.form.get('password')
        
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
        conn.close()
        
        if student and check_password_hash(student['password_hash'], password):
            session['student_id'] = student['student_id']
            session['student_name'] = student['name']
            
            # Create a new exam attempt upon login (or after instructions)
            # We'll create it here for simplicity
            attempt_id = str(uuid.uuid4())
            session['attempt_id'] = attempt_id
            
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO exam_attempts (attempt_id, student_id, start_time) 
                VALUES (?, ?, ?)
            ''', (attempt_id, student_id, datetime.datetime.now()))
            conn.commit()
            conn.close()
            
            return redirect(url_for('auth.instructions'))
        else:
            flash('Invalid Student ID or Password')
            
    return render_template('login.html')

@auth_bp.route('/instructions')
def instructions():
    if 'student_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('instructions.html')

@auth_bp.route('/selfie')
def selfie():
    if 'student_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('selfie.html')

@auth_bp.route('/system-check')
def system_check():
    if 'student_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('system_check.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
