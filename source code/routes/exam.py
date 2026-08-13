from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from utils.database import get_db_connection
import random
import datetime

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/exam')
def exam():
    if 'student_id' not in session or 'attempt_id' not in session:
        return redirect(url_for('auth.login'))
        
    attempt_id = session['attempt_id']
    conn = get_db_connection()
    
    # Check if exam is already submitted
    attempt = conn.execute('SELECT status, start_time FROM exam_attempts WHERE attempt_id = ?', (attempt_id,)).fetchone()
    if attempt['status'] == 'COMPLETED':
        conn.close()
        return redirect(url_for('exam.result'))
        
    # Check if questions exist for this attempt
    exam_qs = conn.execute('''
        SELECT q.id, q.question, q.option_a, q.option_b, q.option_c, q.option_d, eq.question_order, sa.selected_option
        FROM exam_questions eq
        JOIN questions q ON eq.question_id = q.id
        LEFT JOIN student_answers sa ON sa.attempt_id = eq.attempt_id AND sa.question_id = q.id
        WHERE eq.attempt_id = ?
        ORDER BY eq.question_order
    ''', (attempt_id,)).fetchall()
    
    if not exam_qs:
        # Generate 50 random questions
        all_qs = conn.execute('SELECT id FROM questions').fetchall()
        selected_qs = random.sample(all_qs, min(50, len(all_qs)))
        
        for i, q in enumerate(selected_qs):
            conn.execute('''
                INSERT INTO exam_questions (attempt_id, question_id, question_order)
                VALUES (?, ?, ?)
            ''', (attempt_id, q['id'], i+1))
        conn.commit()
        
        exam_qs = conn.execute('''
            SELECT q.id, q.question, q.option_a, q.option_b, q.option_c, q.option_d, eq.question_order, sa.selected_option
            FROM exam_questions eq
            JOIN questions q ON eq.question_id = q.id
            LEFT JOIN student_answers sa ON sa.attempt_id = eq.attempt_id AND sa.question_id = q.id
            WHERE eq.attempt_id = ?
            ORDER BY eq.question_order
        ''', (attempt_id,)).fetchall()
        
    # Calculate time remaining
    start_time_str = attempt['start_time']
    try:
        start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
    except:
        start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        
    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    time_remaining = max(0, 3600 - int(elapsed)) # 60 minutes
    
    conn.close()
    
    questions_list = []
    for q in exam_qs:
        q_dict = dict(q)
        
        # Deterministic shuffle so refresh keeps the same order
        r = random.Random(attempt_id + str(q['id']))
        opts = [
            {'key': 'A', 'text': q['option_a']},
            {'key': 'B', 'text': q['option_b']},
            {'key': 'C', 'text': q['option_c']},
            {'key': 'D', 'text': q['option_d']}
        ]
        r.shuffle(opts)
        q_dict['shuffled_options'] = opts
        questions_list.append(q_dict)
        
    return render_template('exam.html', questions=questions_list, time_remaining=time_remaining)

@exam_bp.route('/api/save-answer', methods=['POST'])
def save_answer():
    if 'attempt_id' not in session:
        return jsonify({'status': 'error'})
        
    data = request.json
    question_id = data.get('question_id')
    selected_option = data.get('selected_option')
    attempt_id = session['attempt_id']
    
    conn = get_db_connection()
    
    # Check correctness
    q = conn.execute('SELECT correct_answer FROM questions WHERE id = ?', (question_id,)).fetchone()
    is_correct = (q['correct_answer'] == selected_option)
    
    conn.execute('''
        INSERT INTO student_answers (attempt_id, question_id, selected_option, is_correct)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(attempt_id, question_id) 
        DO UPDATE SET selected_option=excluded.selected_option, is_correct=excluded.is_correct
    ''', (attempt_id, question_id, selected_option, is_correct))
    
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@exam_bp.route('/submit-exam', methods=['POST'])
def submit_exam():
    if 'attempt_id' not in session:
        return redirect(url_for('auth.login'))
        
    attempt_id = session['attempt_id']
    student_id = session['student_id']
    
    conn = get_db_connection()
    conn.execute("UPDATE exam_attempts SET status = 'COMPLETED', end_time = ? WHERE attempt_id = ?", (datetime.datetime.now(), attempt_id))
    
    # Evaluate
    total_qs = conn.execute('SELECT COUNT(*) as cnt FROM exam_questions WHERE attempt_id = ?', (attempt_id,)).fetchone()['cnt']
    answers = conn.execute('SELECT * FROM student_answers WHERE attempt_id = ?', (attempt_id,)).fetchall()
    
    attempted = len(answers)
    correct = sum(1 for a in answers if a['is_correct'])
    wrong = attempted - correct
    unanswered = total_qs - attempted
    score = correct # assuming 1 mark each for simplicity, though DB has marks
    percentage = (score / total_qs) * 100 if total_qs > 0 else 0
    
    conn.execute('''
        INSERT OR REPLACE INTO exam_results 
        (attempt_id, student_id, total_questions, attempted, correct, wrong, unanswered, score, percentage)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (attempt_id, student_id, total_qs, attempted, correct, wrong, unanswered, score, percentage))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('exam.result'))

@exam_bp.route('/result')
def result():
    if 'attempt_id' not in session:
        return redirect(url_for('auth.login'))
        
    attempt_id = session['attempt_id']
    conn = get_db_connection()
    result_data = conn.execute('SELECT * FROM exam_results WHERE attempt_id = ?', (attempt_id,)).fetchone()
    attempt = conn.execute('SELECT risk_score, risk_status FROM exam_attempts WHERE attempt_id = ?', (attempt_id,)).fetchone()
    conn.close()
    
    return render_template('result.html', result=result_data, attempt=attempt)
