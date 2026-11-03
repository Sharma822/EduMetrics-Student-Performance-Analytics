import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "students.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT,
            math_score INTEGER,
            science_score INTEGER,
            english_score INTEGER,
            attendance INTEGER,
            total_score INTEGER,
            average_score REAL,
            grade TEXT,
            status TEXT
        )
    """)
    conn.commit()

    # Check if empty, populate from CSV if available
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    if count == 0:
        csv_path = os.path.join(os.path.dirname(__file__), "data", "students.csv")
        if os.path.exists(csv_path):
            import pandas as pd
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                m, s, e = int(row['math_score']), int(row['science_score']), int(row['english_score'])
                total = m + s + e
                avg = round(total / 3.0, 2)
                grade, status = calculate_grade_and_status(m, s, e)
                cursor.execute("""
                    INSERT INTO students (roll_no, name, gender, math_score, science_score, english_score, attendance, total_score, average_score, grade, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (str(row['roll_no']), row['name'], row['gender'], m, s, e, int(row['attendance']), total, avg, grade, status))
            conn.commit()
    conn.close()

def calculate_grade_and_status(m, s, e):
    avg = (m + s + e) / 3.0
    if m < 35 or s < 35 or e < 35:
        status = "Fail"
    else:
        status = "Pass"

    if avg >= 90:
        grade = "A+"
    elif avg >= 80:
        grade = "A"
    elif avg >= 70:
        grade = "B"
    elif avg >= 60:
        grade = "C"
    elif avg >= 40:
        grade = "D"
    else:
        grade = "F"
    return grade, status
