-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 7: Schema Design, DDL & Data Integrity
-- In-Class Paired Coding Challenges
-- ============================================================================

-- ----------------------------------------------------------------------------
-- CHALLENGE 1: Normalizing a Flat Student Enrollment Sheet (Session 1)
-- Scenario: The college registrar tracks student course enrollment in a single
-- flat file with repeating records and transitive dependencies.
-- Columns: student_id, student_name, student_email, course_code, course_title,
--          instructor_name, instructor_office, grade.
-- Task: Decompose this into 3 distinct 3NF tables using DDL:
-- 1. students (student_id, student_name, student_email)
-- 2. courses (course_code, course_title, instructor_name, instructor_office)
-- 3. enrollments (enrollment_id, student_id, course_code, grade)
-- ----------------------------------------------------------------------------

-- Table 1: Students
CREATE TABLE IF NOT EXISTS challenge_students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    student_email VARCHAR(255) NOT NULL UNIQUE
);

-- Table 2: Courses
CREATE TABLE IF NOT EXISTS challenge_courses (
    course_code VARCHAR(10) PRIMARY KEY,
    course_title VARCHAR(150) NOT NULL,
    instructor_name VARCHAR(100) NOT NULL,
    instructor_office VARCHAR(50) NOT NULL
);

-- Table 3: Enrollments (Junction Table)
CREATE TABLE IF NOT EXISTS challenge_enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES challenge_students(student_id) ON DELETE CASCADE,
    course_code VARCHAR(10) NOT NULL REFERENCES challenge_courses(course_code) ON DELETE RESTRICT,
    grade VARCHAR(2) DEFAULT 'IP',
    CONSTRAINT uq_student_course UNIQUE (student_id, course_code)
);


-- ----------------------------------------------------------------------------
-- CHALLENGE 2: Declaring Domain Check Constraints (Session 2)
-- Scenario: Corporate HR wants an employees table where:
-- - salary cannot be negative
-- - department must be one of: 'Operations', 'Research', 'Security', 'Sales', 'Executive'
-- - is_active defaults to TRUE
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS challenge_staff (
    staff_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    CONSTRAINT chk_challenge_staff_salary 
        CHECK (salary >= 0.00),
        
    CONSTRAINT chk_challenge_staff_dept 
        CHECK (department IN ('Operations', 'Research', 'Security', 'Sales', 'Executive'))
);


-- ----------------------------------------------------------------------------
-- CHALLENGE 3: Testing Constraint Rejections (Session 2)
-- Task:
-- 1. Attempt to insert a staff member with department = 'Marketing'.
-- 2. Verify that PostgreSQL catches the check constraint violation.
-- 3. Attempt to insert a negative salary (-1000.00).
-- ----------------------------------------------------------------------------

-- Test 1: Invalid department (Should fail)
-- INSERT INTO challenge_staff (full_name, department, salary)
-- VALUES ('Alice Brown', 'Marketing', 60000.00);

-- Test 2: Negative salary (Should fail)
-- INSERT INTO challenge_staff (full_name, department, salary)
-- VALUES ('Bob Green', 'Security', -1000.00);


-- ----------------------------------------------------------------------------
-- CHALLENGE 4: Creating a Joined Executive View (Session 2)
-- Scenario: Management wants a clean virtual table named v_course_enrollment_roster
-- that presents student names, course codes, and grades without exposing IDs.
-- ----------------------------------------------------------------------------

CREATE OR REPLACE VIEW v_course_enrollment_roster AS
SELECT 
    s.student_name,
    s.student_email,
    c.course_code,
    c.course_title,
    c.instructor_name,
    e.grade
FROM challenge_enrollments e
JOIN challenge_students s ON e.student_id = s.student_id
JOIN challenge_courses c ON e.course_code = c.course_code;

-- Query the view:
SELECT * FROM v_course_enrollment_roster;
