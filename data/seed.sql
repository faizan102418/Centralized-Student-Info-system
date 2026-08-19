-- Sample schema and synthetic data for local development.
-- Run this after creating the database, e.g.:
--   mysql -u root -p project_data < data/seed.sql
-- All names below are fictional.

CREATE TABLE IF NOT EXISTS student_general_data (
    roll_number VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    discipline VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS student_scholarship (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scholarship_name VARCHAR(100),
    enrollment_status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS student_fee_submission (
    registration_number VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    fee_status VARCHAR(50)
);

INSERT INTO student_general_data (roll_number, name, discipline) VALUES
    ('2023-CS-001', 'Alice Smith', 'Computer Science'),
    ('2023-EE-005', 'Bob Johnson', 'Electrical Engineering'),
    ('2023-ME-010', 'Charlie Brown', 'Mechanical Engineering'),
    ('2023-CS-002', 'Diana Prince', 'Computer Science');

INSERT INTO student_scholarship (name, scholarship_name, enrollment_status) VALUES
    ('Alice Smith', 'Merit Scholarship', 'Enrolled'),
    ('Bob Johnson', 'Need-Based Grant', 'Pending'),
    ('Diana Prince', 'Athletic Scholarship', 'Enrolled');

INSERT INTO student_fee_submission (registration_number, name, fee_status) VALUES
    ('REG-CS-001', 'Alice Smith', 'Paid'),
    ('REG-EE-005', 'Bob Johnson', 'Pending'),
    ('REG-ME-010', 'Charlie Brown', 'Paid'),
    ('REG-CS-002', 'Diana Prince', 'Overdue');
