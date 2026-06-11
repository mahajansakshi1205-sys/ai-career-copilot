import sqlite3
import os
import pandas as pd

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'careers.db')

def init_database():
    """Create database and tables if not exist"""
    
    # Create data folder if not exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            job_link TEXT,
            date_applied TEXT,
            status TEXT DEFAULT 'Applied',
            notes TEXT,
            salary_range TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def add_job_application(company, title, link, 
                        date, status, notes, 
                        salary, location):
    """Add a new job application"""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO job_applications 
        (company_name, job_title, job_link, 
         date_applied, status, notes, 
         salary_range, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (company, title, link, date, 
          status, notes, salary, location))
    
    conn.commit()
    conn.close()


def get_all_applications():
    """Get all job applications"""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    
    df = pd.read_sql_query('''
        SELECT * FROM job_applications 
        ORDER BY created_at DESC
    ''', conn)
    
    conn.close()
    return df


def update_application_status(app_id, new_status):
    """Update status of a job application"""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE job_applications 
        SET status = ? 
        WHERE id = ?
    ''', (new_status, app_id))
    
    conn.commit()
    conn.close()


def delete_application(app_id):
    """Delete a job application"""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM job_applications 
        WHERE id = ?
    ''', (app_id,))
    
    conn.commit()
    conn.close()


def get_stats():
    """Get statistics for dashboard"""
    df = get_all_applications()
    
    if df.empty:
        return {
            'total': 0,
            'applied': 0,
            'interview': 0,
            'offer': 0,
            'rejected': 0
        }
    
    return {
        'total': len(df),
        'applied': len(df[df['status'] == 'Applied']),
        'interview': len(df[df['status'] == 'Interview']),
        'offer': len(df[df['status'] == 'Offer']),
        'rejected': len(df[df['status'] == 'Rejected'])
    }