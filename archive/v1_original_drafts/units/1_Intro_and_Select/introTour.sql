/* ============================================================================
   POSTGRESQL BEGINNER STARTER SCRIPT
   ----------------------------------------------------------------------------
   How to use:
   Run each section block-by-block (highlight the section and execute).
   Read the comments before running each query to understand what happens.
   ============================================================================ */


/* ============================================================================
   SECTION 1: CREATING TABLES (DDL - Data Definition Language)
   ----------------------------------------------------------------------------
   Before storing data, we must define the blueprint (columns and data types).
   We also establish constraints like PRIMARY KEY, NOT NULL, and UNIQUE.
   ============================================================================ */

-- Always clean up previous runs during practice so this script can rerun cleanly.
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

-- Create the parent table: students
CREATE TABLE students (
    -- GENERATED ALWAYS AS IDENTITY automatically generates unique numbers (1, 2, 3...)
    -- PRIMARY KEY ensures each student has a unique, non-null identifier.
    student_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- VARCHAR(n) holds text up to n characters. NOT NULL means it cannot be blank.
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    
    -- UNIQUE prevents duplicate email addresses across rows.
    email      VARCHAR(100) UNIQUE NOT NULL,
    
    -- DATE stores calendar dates (YYYY-MM-DD).
    enrollment_date DATE DEFAULT CURRENT_DATE,
    
    -- BOOLEAN holds TRUE or FALSE.
    is_active  BOOLEAN DEFAULT TRUE
);

-- Create a second table: courses
CREATE TABLE courses (
    course_id   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    title       VARCHAR(100) NOT NULL,
    credits     INT NOT NULL CHECK (credits > 0)  -- CHECK constraint enforces business rules
);


/* ============================================================================
   SECTION 2: INSERTING DATA (DML - Data Manipulation Language)
   ----------------------------------------------------------------------------
   Add records into the tables using INSERT INTO ... VALUES.
   ============================================================================ */

-- Insert a single student record
INSERT INTO students (first_name, last_name, email, enrollment_date)
VALUES ('Alice', 'Smith', 'alice.smith@example.edu', '2026-08-25');

-- Insert multiple records in a single query
INSERT INTO students (first_name, last_name, email, enrollment_date)
VALUES 
    ('Bob', 'Jones', 'bob.jones@example.edu', '2026-08-26'),
    ('Charlie', 'Brown', 'charlie.brown@example.edu', '2026-08-27'),
    ('Diana', 'Prince', 'diana.prince@example.edu', '2026-08-28');

-- Insert courses
INSERT INTO courses (course_code, title, credits)
VALUES 
    ('CS101', 'Introduction to Computer Science', 3),
    ('CS201', 'Data Structures & Algorithms', 4),
    ('MATH150', 'Discrete Mathematics', 3);


/* ============================================================================
   SECTION 3: QUERYING DATA (SELECT Statements)
   ----------------------------------------------------------------------------
   Retrieve records using filtering, sorting, and projection.
   ============================================================================ */

-- View all columns and all rows (* means "all columns")
SELECT * FROM students;

-- Projection: Select only specific columns (recommended practice)
SELECT first_name, last_name, email 
FROM students;

-- Filtering with WHERE: Retrieve specific rows matching a condition
SELECT first_name, last_name 
FROM students 
WHERE enrollment_date >= '2026-08-26';

-- Multiple conditions with AND / OR
SELECT * 
FROM students 
WHERE is_active = TRUE AND last_name = 'Smith';

-- Pattern matching with LIKE (% represents zero or more wildcard characters)
SELECT * 
FROM students 
WHERE email LIKE '%@example.edu';

-- Sorting results with ORDER BY (ASC for ascending, DESC for descending)
-- LIMIT restricts the total number of rows returned
SELECT first_name, last_name, enrollment_date 
FROM students 
ORDER BY last_name ASC 
LIMIT 2;


/* ============================================================================
   SECTION 4: UPDATING AND DELETING RECORDS
   ----------------------------------------------------------------------------
   Modifying or removing existing data.
   WARNING: Always use a WHERE clause unless you intend to update/delete every row!
   ============================================================================ */

-- Update an existing record
UPDATE students 
SET email = 'alice.newemail@example.edu',
    is_active = FALSE 
WHERE student_id = 1;

-- Verify the update
SELECT * FROM students WHERE student_id = 1;

-- Delete a specific record
DELETE FROM students 
WHERE email = 'charlie.brown@example.edu';

-- Verify deletion (Charlie should no longer appear)
SELECT * FROM students;


/* ============================================================================
   SECTION 5: RELATIONAL DATA & FOREIGN KEYS
   ----------------------------------------------------------------------------
   A junction table creates a Many-to-Many relationship between students & courses.
   ============================================================================ */

CREATE TABLE enrollments (
    enrollment_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- FOREIGN KEY links directly to a row in another table.
    -- ON DELETE CASCADE deletes the enrollment if the referenced student is deleted.
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_id  INT NOT NULL REFERENCES courses(course_id) ON DELETE RESTRICT,
    
    grade NUMERIC(3, 2), -- Stores numbers like 3.75 or 4.00
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent a student from enrolling in the exact same course twice
    UNIQUE (student_id, course_id)
);

-- Enroll students in courses (Alice is ID 1, Bob is ID 2, Diana is ID 4)
INSERT INTO enrollments (student_id, course_id, grade)
VALUES 
    (1, 1, 3.80), -- Alice in CS101
    (1, 2, 3.50), -- Alice in CS201
    (2, 1, 2.90), -- Bob in CS101
    (4, 3, 4.00); -- Diana in MATH150


/* ============================================================================
   SECTION 6: JOINS (Combining Related Tables)
   ----------------------------------------------------------------------------
   Connecting data across separate tables using keys.
   ============================================================================ */

-- INNER JOIN: Returns only rows where matching values exist in both tables
SELECT 
    s.first_name,
    s.last_name,
    c.course_code,
    c.title,
    e.grade
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c  ON e.course_id = c.course_id;

-- LEFT JOIN: Returns ALL rows from the left table, even if no match exists on the right
-- Useful for finding students who are NOT enrolled in any courses
SELECT 
    s.first_name,
    s.last_name,
    e.course_id
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id;


/* ============================================================================
   SECTION 7: AGGREGATE FUNCTIONS & GROUP BY
   ----------------------------------------------------------------------------
   Calculate summary metrics (COUNT, AVG, SUM, MIN, MAX).
   ============================================================================ */

-- Total count of students
SELECT COUNT(*) AS total_registered_students 
FROM students;

-- Average grade per course
-- GROUP BY collapses rows that share common values into summary rows
SELECT 
    c.course_code,
    c.title,
    ROUND(AVG(e.grade), 2) AS average_grade,
    COUNT(e.student_id)    AS total_enrolled
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_code, c.title;

-- HAVING: Filters groups AFTER aggregation (unlike WHERE, which filters before)
SELECT 
    course_id, 
    COUNT(*) AS total_students
FROM enrollments
GROUP BY course_id
HAVING COUNT(*) >= 2;


/* ============================================================================
   SECTION 8: TRANSACTIONS (ACID Compliance)
   ----------------------------------------------------------------------------
   Transactions guarantee that a series of commands either ALL succeed or ALL fail.
   ============================================================================ */

-- Example of a safe, reversible transaction:
BEGIN;

-- Insert a test student
INSERT INTO students (first_name, last_name, email)
VALUES ('Test', 'Student', 'temp.test@example.edu');

-- Check that the student exists inside this transaction
SELECT * FROM students WHERE email = 'temp.test@example.edu';

-- ROLLBACK cancels everything done since BEGIN
ROLLBACK;

-- Verify the rollback: the test student is gone
SELECT * FROM students WHERE email = 'temp.test@example.edu';

-- If you ran COMMIT instead of ROLLBACK, the changes would be permanently written.


/* ============================================================================
   SECTION 9: TEARDOWN / CLEANUP
   ----------------------------------------------------------------------------
   Remove all objects created during this tutorial.
   ============================================================================ */

-- Uncomment and run the lines below when you are finished practicing:
-- DROP TABLE IF EXISTS enrollments;
-- DROP TABLE IF EXISTS courses;
-- DROP TABLE IF EXISTS students;
