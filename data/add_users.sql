-- Run this once to add the users table and demo accounts, without
-- re-inserting student data that already exists in your database.
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty', 'student') NOT NULL DEFAULT 'student',
    student_name VARCHAR(100) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password_hash, role, student_name) VALUES
    ('admin', '$2b$12$zUy0IDfnuR/nCi4xuA5zOuAKNNLq7lOWXBeHmBA1j5XwcqrBjINzW', 'admin', NULL),
    ('faculty1', '$2b$12$SwgFIxh/om4DJph/0J5Y5urNk6DaIEGG4K2Y1c87j/Q0m37faT12e', 'faculty', NULL),
    ('alice', '$2b$12$D129EdNZ2KEnx2jNNZ4BaOeOvUuqaFHzUSof.4kGD35dqcrS90wUK', 'student', 'Alice Smith');
