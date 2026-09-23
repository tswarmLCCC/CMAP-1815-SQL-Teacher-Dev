/*
====================================================================
CMAP 1815 - Unit 1: Lecture Walkthrough Part 2
Topic: Anatomy of SELECT & Projection (The Flashlight)
Video Duration: ~8 minutes
====================================================================
*/

-- 1. The Sledgehammer: SELECT *
-- Retrieves every single column in the employees table
SELECT * 
FROM employees;

-- 2. The Scalpel: Projecting Specific Columns
-- Turning on the flashlight to illuminate only first_name and last_name
SELECT first_name, last_name
FROM employees;

-- 3. Adding More Columns
-- Notice: commas separate columns, but NO comma after 'department'
SELECT first_name, last_name, department, title
FROM employees;

-- 4. [DEMO TRAP 1: The Missing Semicolon]
-- In your terminal, run this line without a semicolon to show the continuation prompt (mydb-#)
-- SELECT first_name FROM employees

-- 5. [DEMO TRAP 2: The Trailing Comma]
-- Uncomment the line below to show students PostgreSQL's syntax error:
-- SELECT first_name, last_name, FROM employees;
-- ERROR: syntax error at or near "FROM"
