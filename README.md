# 🎓 EduMetrics: Student Academic Performance Analytics & Record Management System

EduMetrics is a comprehensive, data-driven web dashboard built using **Python, Flask, MySQL, Pandas, and Matplotlib**. It streamlines academic record management and delivers visual performance insights, subject analytics, and pass/fail distribution without relying on client-side charting libraries.

---

## 🚀 Key Features

* **Student Records Management:** Full CRUD operations (Add, Edit, Update, Delete student profiles).
* **Academic Analytics:**
  * Auto-calculated Total Marks, Percentage/Average, and Grades (A+, A, B, C, D, F).
  * Overall performance telemetry and attendance tracking.
  * Real-time identification of top performers and pass/fail ratios.
* **Pure Python Visualizations (Matplotlib):**
  * Dynamic Pass vs. Fail distribution.
  * Grade frequency breakdown.
  * Subject-wise average performance comparison.
* **Search, Filter & Sorting:** Quick student search by name/roll number and multi-attribute sorting.
* **Modern UI:** Responsive dashboard design with integrated Dark/Light mode.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Data Processing & Analytics:** Pandas, NumPy
* **Visualization:** Matplotlib (Server-side dynamic base64 rendering)
* **Database:** MySQL / SQLite (`mysql-connector-python`)
* **Frontend:** HTML5, CSS3, JavaScript

---

## 📂 Project Structure

```text
EduMetrics-Student-Performance-Analytics/
├── Student_Performance/
│   ├── app.py                # Main Flask application and analytics routes
│   ├── database.py           # Database connection and helper queries
│   ├── static/
│   │   └── style.css         # UI stylesheet and Dark/Light mode theme
│   ├── templates/
│   │   ├── index.html        # Analytics dashboard & records table
│   │   └── edit.html         # Student record modification form
│   └── data/
│       └── students.csv      # Seed dataset for initial records
└── stud pro sql.sql          # MySQL database schema and sample data
