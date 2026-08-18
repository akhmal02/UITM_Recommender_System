CREATE DATABASE IF NOT EXISTS recsystem CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE recsystem;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    faculty VARCHAR(20) NOT NULL DEFAULT 'FSKM',
    difficulty_level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL DEFAULT 'Beginner',
    duration_preference ENUM('Short', 'Medium', 'Long') NOT NULL DEFAULT 'Medium',
    format_preference ENUM('Online', 'In-Person', 'Hybrid', 'Any') NOT NULL DEFAULT 'Any',
    interests TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    faculty VARCHAR(20) NOT NULL,
    difficulty ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    duration_weeks INT NOT NULL,
    format ENUM('Online', 'In-Person', 'Hybrid') NOT NULL,
    credits INT NOT NULL DEFAULT 3,
    tags VARCHAR(255) NOT NULL DEFAULT '',
    rating DECIMAL(3,2) NOT NULL DEFAULT 4.00,
    instructor VARCHAR(100) NOT NULL DEFAULT 'TBA',
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS course_schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    day ENUM('Monday','Tuesday','Wednesday','Thursday','Friday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    venue VARCHAR(80) NOT NULL,
    session_type VARCHAR(30) NOT NULL DEFAULT 'Kuliah',
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_enrollment (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Courses and schedules are seeded via seed_courses.py (72 courses, 12 per faculty)
