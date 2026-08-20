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

-- Login accounts for the app. 'admin' and 'faculty' roles can query any
-- student; 'student' role accounts can only query their own record
-- (matched against student_name).
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty', 'student') NOT NULL DEFAULT 'student',
    student_name VARCHAR(100) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

-- Demo login accounts. Passwords below are for local development only —
-- change them (or remove these rows) before any real deployment.
--   admin    / admin123    (role: admin — full access)
--   faculty1 / faculty123  (role: faculty — full access)
--   alice    / alice123    (role: student — can only query Alice Smith's own record)
INSERT INTO users (username, password_hash, role, student_name) VALUES
    ('admin', '$2b$12$zUy0IDfnuR/nCi4xuA5zOuAKNNLq7lOWXBeHmBA1j5XwcqrBjINzW', 'admin', NULL),
    ('faculty1', '$2b$12$SwgFIxh/om4DJph/0J5Y5urNk6DaIEGG4K2Y1c87j/Q0m37faT12e', 'faculty', NULL),
    ('alice', '$2b$12$D129EdNZ2KEnx2jNNZ4BaOeOvUuqaFHzUSof.4kGD35dqcrS90wUK', 'student', 'Alice Smith');
