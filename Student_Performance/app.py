import io
import base64
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for web servers
import matplotlib.pyplot as plt
from database import init_db, get_db_connection, calculate_grade_and_status

app = Flask(__name__)
app.secret_key = "student_performance_secret_key"

# Database initialization
init_db()

def generate_matplotlib_charts(df):
    """Generates charts using pure Matplotlib and returns base64 image strings."""
    if df.empty:
        return None, None, None

    # Chart 1: Pass vs Fail Distribution (Pie Chart)
    fig1, ax1 = plt.subplots(figsize=(4.5, 4.0))
    status_counts = df['status'].value_counts()
    labels = status_counts.index.tolist()
    counts = status_counts.values.tolist()
    colors = ['#2ecc71' if l == 'Pass' else '#e74c3c' for l in labels]
    
    ax1.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, 
            wedgeprops={'edgecolor': '#ffffff', 'linewidth': 2},
            textprops={'fontsize': 11, 'weight': 'bold'})
    ax1.set_title("Pass vs Fail Ratio", fontsize=13, weight='bold', pad=15)
    fig1.tight_layout()

    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png", dpi=100, bbox_inches='tight', transparent=True)
    buf1.seek(0)
    pass_fail_chart = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)

    # Chart 2: Grade Distribution (Bar Chart)
    fig2, ax2 = plt.subplots(figsize=(5.5, 4.0))
    grades = ['A+', 'A', 'B', 'C', 'D', 'F']
    grade_counts = [df[df['grade'] == g].shape[0] for g in grades]
    bar_colors = ['#3498db', '#2980b9', '#f39c12', '#e67e22', '#d35400', '#c0392b']

    bars = ax2.bar(grades, grade_counts, color=bar_colors, edgecolor='#ffffff', width=0.6)
    ax2.set_title("Grade Distribution", fontsize=13, weight='bold', pad=15)
    ax2.set_xlabel("Grades", fontsize=11, weight='bold')
    ax2.set_ylabel("Student Count", fontsize=11, weight='bold')
    ax2.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in bars:
        yval = bar.get_height()
        if yval > 0:
            ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, int(yval), ha='center', va='bottom', weight='bold')

    fig2.tight_layout()
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format="png", dpi=100, bbox_inches='tight', transparent=True)
    buf2.seek(0)
    grade_chart = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)

    # Chart 3: Subject-wise Average Marks (Horizontal Bar Chart)
    fig3, ax3 = plt.subplots(figsize=(5.0, 4.0))
    subjects = ['Math', 'Science', 'English']
    avg_scores = [df['math_score'].mean(), df['science_score'].mean(), df['english_score'].mean()]
    colors_subj = ['#9b59b6', '#1abc9c', '#e67e22']

    bars3 = ax3.barh(subjects, avg_scores, color=colors_subj, edgecolor='#ffffff', height=0.55)
    ax3.set_xlim(0, 100)
    ax3.set_title("Average Subject Scores", fontsize=13, weight='bold', pad=15)
    ax3.set_xlabel("Mean Score (0-100)", fontsize=11, weight='bold')
    ax3.grid(axis='x', linestyle='--', alpha=0.5)

    for bar in bars3:
        width = bar.get_width()
        ax3.text(width + 1.5, bar.get_y() + bar.get_height()/2.0, f'{width:.1f}', ha='left', va='center', weight='bold')

    fig3.tight_layout()
    buf3 = io.BytesIO()
    fig3.savefig(buf3, format="png", dpi=100, bbox_inches='tight', transparent=True)
    buf3.seek(0)
    subject_chart = base64.b64encode(buf3.getvalue()).decode('utf-8')
    plt.close(fig3)

    return pass_fail_chart, grade_chart, subject_chart

@app.route("/")
def index():
    search = request.args.get("search", "").strip()
    sort_by = request.args.get("sort_by", "id")
    filter_status = request.args.get("filter_status", "All")

    conn = get_db_connection()
    query = "SELECT * FROM students"
    conditions = []
    params = []

    if search:
        conditions.append("(name LIKE ? OR roll_no LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])

    if filter_status and filter_status != "All":
        conditions.append("status = ?")
        params.append(filter_status)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Allowed sorting fields
    allowed_sorts = {
        "id": "id ASC",
        "roll_no": "CAST(roll_no AS INTEGER) ASC",
        "name": "name ASC",
        "total_score_desc": "total_score DESC",
        "attendance_desc": "attendance DESC"
    }
    query += " ORDER BY " + allowed_sorts.get(sort_by, "id ASC")

    students = conn.execute(query, params).fetchall()

    # Load all students into Pandas DataFrame for statistical insights
    all_df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()

    # Analytics calculation using Pandas & NumPy
    if not all_df.empty:
        total_students = int(len(all_df))
        avg_overall = float(np.round(all_df['average_score'].mean(), 2))
        avg_attendance = float(np.round(all_df['attendance'].mean(), 2))
        pass_count = int((all_df['status'] == 'Pass').sum())
        fail_count = int((all_df['status'] == 'Fail').sum())
        top_student = all_df.loc[all_df['total_score'].idxmax()].to_dict()
    else:
        total_students = avg_overall = avg_attendance = pass_count = fail_count = 0
        top_student = None

    # Generate Matplotlib charts
    pass_fail_chart, grade_chart, subject_chart = generate_matplotlib_charts(all_df)

    stats = {
        "total_students": total_students,
        "avg_overall": avg_overall,
        "avg_attendance": avg_attendance,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "top_student": top_student
    }

    return render_template(
        "index.html",
        students=students,
        stats=stats,
        search=search,
        sort_by=sort_by,
        filter_status=filter_status,
        pass_fail_chart=pass_fail_chart,
        grade_chart=grade_chart,
        subject_chart=subject_chart
    )

@app.route("/add", methods=["POST"])
def add_student():
    roll_no = request.form["roll_no"].strip()
    name = request.form["name"].strip()
    gender = request.form["gender"]
    math_score = int(request.form["math_score"])
    science_score = int(request.form["science_score"])
    english_score = int(request.form["english_score"])
    attendance = int(request.form["attendance"])

    total = math_score + science_score + english_score
    avg = round(total / 3.0, 2)
    grade, status = calculate_grade_and_status(math_score, science_score, english_score)

    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO students (roll_no, name, gender, math_score, science_score, english_score, attendance, total_score, average_score, grade, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (roll_no, name, gender, math_score, science_score, english_score, attendance, total, avg, grade, status))
        conn.commit()
        flash("Student record added successfully!", "success")
    except Exception as e:
        flash(f"Error adding student: {e}", "danger")
    finally:
        conn.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    conn = get_db_connection()
    if request.method == "POST":
        roll_no = request.form["roll_no"].strip()
        name = request.form["name"].strip()
        gender = request.form["gender"]
        math_score = int(request.form["math_score"])
        science_score = int(request.form["science_score"])
        english_score = int(request.form["english_score"])
        attendance = int(request.form["attendance"])

        total = math_score + science_score + english_score
        avg = round(total / 3.0, 2)
        grade, status = calculate_grade_and_status(math_score, science_score, english_score)

        conn.execute("""
            UPDATE students 
            SET roll_no=?, name=?, gender=?, math_score=?, science_score=?, english_score=?, attendance=?, total_score=?, average_score=?, grade=?, status=?
            WHERE id=?
        """, (roll_no, name, gender, math_score, science_score, english_score, attendance, total, avg, grade, status, id))
        conn.commit()
        conn.close()
        flash("Student record updated successfully!", "success")
        return redirect(url_for("index"))

    student = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("index"))
    return render_template("edit.html", student=student)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully!", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
