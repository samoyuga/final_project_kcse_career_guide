import sqlite3
import json
import pandas as pd
from datetime import datetime

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Subjects table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject_name TEXT NOT NULL,
            grade TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Skills table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            skill TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Interests table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_interests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            interest TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Payments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            mpesa_code TEXT,
            checkout_request_id TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Results table
    c.execute('''
        CREATE TABLE IF NOT EXISTS career_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            recommendations TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_user_data(student_info, subjects_grades, skills_interests):
    """Save user data to database and return user ID"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    try:
        # Insert user
        c.execute(
            'INSERT INTO users (name, phone, email) VALUES (?, ?, ?)',
            (student_info['name'], student_info['phone'], student_info.get('email', ''))
        )
        user_id = c.lastrowid
        
        # Insert subjects
        for subject, grade in subjects_grades.items():
            if grade != "Not Taken" and grade != "Select Grade":
                c.execute(
                    'INSERT INTO user_subjects (user_id, subject_name, grade) VALUES (?, ?, ?)',
                    (user_id, subject, grade)
                )
        
        # Insert skills
        for skill in skills_interests.get('skills', []):
            c.execute(
                'INSERT INTO user_skills (user_id, skill) VALUES (?, ?)',
                (user_id, skill)
            )
        
        # Insert interests
        for interest in skills_interests.get('interests', []):
            c.execute(
                'INSERT INTO user_interests (user_id, interest) VALUES (?, ?)',
                (user_id, interest)
            )
        
        conn.commit()
        return user_id
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def save_payment(user_id, amount, mpesa_code, status, checkout_request_id=None):
    """Save payment information"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    try:
        c.execute(
            'INSERT INTO payments (user_id, amount, mpesa_code, checkout_request_id, status) VALUES (?, ?, ?, ?, ?)',
            (user_id, amount, mpesa_code, checkout_request_id, status)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def save_career_results(user_id, recommendations):
    """Save career recommendations"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    try:
        c.execute(
            'INSERT INTO career_results (user_id, recommendations) VALUES (?, ?)',
            (user_id, json.dumps(recommendations))
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def check_payment_status(user_id):
    """Check if user has completed payment"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    try:
        c.execute(
            'SELECT status FROM payments WHERE user_id = ? AND status = "completed"',
            (user_id,)
        )
        result = c.fetchone()
        return result is not None
    finally:
        conn.close()

def get_user_data(user_id):
    """Get user data by ID"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    try:
        # Get user info
        c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        
        if not user:
            return None
        
        # Get subjects
        c.execute('SELECT subject_name, grade FROM user_subjects WHERE user_id = ?', (user_id,))
        subjects = {row[0]: row[1] for row in c.fetchall()}
        
        # Get skills
        c.execute('SELECT skill FROM user_skills WHERE user_id = ?', (user_id,))
        skills = [row[0] for row in c.fetchall()]
        
        # Get interests
        c.execute('SELECT interest FROM user_interests WHERE user_id = ?', (user_id,))
        interests = [row[0] for row in c.fetchall()]
        
        return {
            'user_info': {
                'id': user[0],
                'name': user[1],
                'phone': user[2],
                'email': user[3],
                'created_at': user[4]
            },
            'subjects': subjects,
            'skills': skills,
            'interests': interests
        }
    finally:
        conn.close()

def get_payment_history(user_id):
    """Get payment history for a user"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    try:
        c.execute(
            'SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        )
        payments = c.fetchall()
        
        payment_list = []
        for payment in payments:
            payment_list.append({
                'id': payment[0],
                'user_id': payment[1],
                'amount': payment[2],
                'mpesa_code': payment[3],
                'checkout_request_id': payment[4],
                'status': payment[5],
                'created_at': payment[6]
            })
        
        return payment_list
    finally:
        conn.close()

def get_career_results(user_id):
    """Get career results for a user"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    try:
        c.execute(
            'SELECT recommendations, generated_at FROM career_results WHERE user_id = ? ORDER BY generated_at DESC LIMIT 1',
            (user_id,)
        )
        result = c.fetchone()
        
        if result:
            return {
                'recommendations': json.loads(result[0]),
                'generated_at': result[1]
            }
        return None
    finally:
        conn.close()

def cleanup_old_data(days_old=30):
    """Clean up data older than specified days (for maintenance)"""
    conn = sqlite3.connect('career_guide.db')
    c = conn.cursor()
    
    try:
        cutoff_date = f"datetime('now', '-{days_old} days')"
        
        # Delete old career results
        c.execute(f'DELETE FROM career_results WHERE generated_at < {cutoff_date}')
        
        # Delete old payments
        c.execute(f'DELETE FROM payments WHERE created_at < {cutoff_date}')
        
        # Find users with no recent activity
        c.execute(f'''
            DELETE FROM users 
            WHERE id NOT IN (
                SELECT DISTINCT user_id FROM payments WHERE created_at >= {cutoff_date}
                UNION 
                SELECT DISTINCT user_id FROM career_results WHERE generated_at >= {cutoff_date}
            ) AND created_at < {cutoff_date}
        ''')
        
        conn.commit()
        return c.rowcount  # Number of rows affected
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()