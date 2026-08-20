-- Adds query_logs for evaluation/research purposes.
-- See docs/RESEARCH_METHODOLOGY.md for the full logging protocol.
-- Run once: mysql -u root -p project_data < data/add_query_logs.sql

CREATE TABLE IF NOT EXISTS query_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(64) NOT NULL,
    user_role ENUM('admin', 'faculty', 'student', 'dev_test') NOT NULL,
    query_text TEXT NOT NULL,
    detected_intent VARCHAR(50),
    extracted_entities JSON,
    system_variant VARCHAR(20) NOT NULL,
    retrieved_chunk_ids JSON,
    response_text TEXT,
    latency_ms INT,
    access_denied BOOLEAN DEFAULT FALSE,
    user_feedback ENUM('up', 'down', 'none') DEFAULT 'none',
    human_label ENUM('correct', 'partial', 'incorrect', 'not_rated') DEFAULT 'not_rated',
    notes TEXT
);
