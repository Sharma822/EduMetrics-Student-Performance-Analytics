-- Database Schema for Student Performance Tracker
CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    math_score INT,
    science_score INT,
    english_score INT,
    attendance INT,
    total_score INT,
    average_score FLOAT,
    grade VARCHAR(5),
    status VARCHAR(10)
);

-- Sample Data Insertion
INSERT INTO students (roll_no, name, gender, math_score, science_score, english_score, attendance, total_score, average_score, grade, status)
VALUES 
('101', 'Aarav Sharma', 'Male', 85, 90, 78, 92, 253, 84.33, 'A', 'Pass'),
('102', 'Priya Patel', 'Female', 92, 95, 89, 96, 276, 92.00, 'A+', 'Pass'),
('103', 'Rohan Verma', 'Male', 45, 52, 40, 75, 137, 45.67, 'C', 'Pass'),
('104', 'Sneha Gupta', 'Female', 78, 82, 85, 88, 245, 81.67, 'A', 'Pass'),
('105', 'Amit Kumar', 'Male', 32, 28, 35, 62, 95, 31.67, 'F', 'Fail');
