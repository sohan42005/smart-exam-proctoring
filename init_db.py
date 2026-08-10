import json
import random
import werkzeug.security as security
from utils.database import init_db_schema, get_db_connection

def generate_questions(num=1000):
    questions = []
    
    # Templates for Quantitative Aptitude
    def gen_train_q():
        distance = random.randint(10, 50) * 10
        time = random.randint(2, 8)
        speed = distance // time
        wrong_speeds = [speed + random.choice([5, 10, -5, -10]), speed * 2, speed + random.randint(1, 15)]
        opts = [f"{speed} km/h", f"{wrong_speeds[0]} km/h", f"{wrong_speeds[1]} km/h", f"{wrong_speeds[2]} km/h"]
        return {
            'question': f"A train travels {distance} km in {time} hours. What is its average speed?",
            'options': opts, 'correct_idx': 0, 'category': 'Quantitative Aptitude', 'difficulty': 'Easy'
        }
        
    def gen_percentage_q():
        total = random.choice([100, 200, 500, 1000, 2000])
        pct = random.randint(5, 45) * 2
        ans = (total * pct) // 100
        opts = [f"{ans}", f"{ans + total//10}", f"{ans - 10}", f"{ans + 20}"]
        return {
            'question': f"What is {pct}% of {total}?",
            'options': opts, 'correct_idx': 0, 'category': 'Quantitative Aptitude', 'difficulty': 'Easy'
        }
        
    def gen_algebra_q():
        x = random.randint(2, 12)
        y = random.randint(2, 12)
        ans = (x * 2) + y
        opts = [f"{ans}", f"{ans + 2}", f"{ans - 2}", f"{ans + x}"]
        return {
            'question': f"If x = {x} and y = {y}, what is the value of 2x + y?",
            'options': opts, 'correct_idx': 0, 'category': 'Numerical Ability', 'difficulty': 'Easy'
        }
        
    def gen_series_q():
        start = random.randint(2, 10)
        step = random.randint(2, 5)
        seq = [start + (step * i) for i in range(4)]
        ans = start + (step * 4)
        opts = [f"{ans}", f"{ans + step}", f"{ans - step + 1}", f"{ans * 2}"]
        return {
            'question': f"Find the next number in the series: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ...",
            'options': opts, 'correct_idx': 0, 'category': 'Logical Reasoning', 'difficulty': 'Medium'
        }
        
    def gen_work_q():
        a = random.choice([10, 12, 15, 20])
        b = random.choice([20, 30, 60])
        # 1/a + 1/b = (b+a)/ab => ab/(a+b)
        ans = (a * b) / (a + b)
        opts = [f"{ans:.2f} days", f"{ans + 2:.2f} days", f"{(a+b)/2:.2f} days", f"{min(a,b)/2:.2f} days"]
        return {
            'question': f"A can do a piece of work in {a} days and B can do it in {b} days. How long will they take if they work together?",
            'options': opts, 'correct_idx': 0, 'category': 'Quantitative Aptitude', 'difficulty': 'Medium'
        }
        
    generators = [gen_train_q, gen_percentage_q, gen_algebra_q, gen_series_q, gen_work_q]
    
    # Generate requested number of questions
    while len(questions) < num:
        q_gen = random.choice(generators)()
        q_data = {
            'question': q_gen['question'],
            'option_a': q_gen['options'][0],
            'option_b': q_gen['options'][1],
            'option_c': q_gen['options'][2],
            'option_d': q_gen['options'][3],
            'correct_answer': 'A', # It is always A here, we shuffle during the exam
            'category': q_gen['category'],
            'difficulty': q_gen['difficulty'],
            'marks': 1 if q_gen['difficulty'] == 'Easy' else 2
        }
        questions.append(q_data)
            
    return questions

def seed_database():
    conn = get_db_connection()
    c = conn.cursor()
    
    # 1. Add demo student
    student_id = "student001"
    student_pw = "student123"
    hashed_student_pw = security.generate_password_hash(student_pw)
    c.execute("INSERT OR IGNORE INTO students (student_id, password_hash, name) VALUES (?, ?, ?)", 
              (student_id, hashed_student_pw, "Demo Student"))
    
    # 2. Add demo admin
    admin_id = "admin"
    admin_pw = "admin123"
    hashed_admin_pw = security.generate_password_hash(admin_pw)
    c.execute("INSERT OR IGNORE INTO admins (username, password_hash) VALUES (?, ?)", 
              (admin_id, hashed_admin_pw))
              
    # 3. Drop old questions to ensure real questions are used
    c.execute("DELETE FROM questions")
    
    # 4. Add questions
    c.execute("SELECT COUNT(*) as cnt FROM questions")
    count = c.fetchone()['cnt']
    if count < 1000:
        print(f"Generating questions. Currently have {count} questions.")
        questions = generate_questions(1000 - count)
        for q in questions:
            c.execute('''
                INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer, category, difficulty, marks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (q['question'], q['option_a'], q['option_b'], q['option_c'], q['option_d'], q['correct_answer'], q['category'], q['difficulty'], q['marks']))
            
    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == '__main__':
    print("Initializing database schema...")
    init_db_schema()
    print("Seeding database...")
    seed_database()
