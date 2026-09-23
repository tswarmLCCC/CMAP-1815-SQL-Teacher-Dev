/*
====================================================================
CMAP 1815 - Unit 1: Lecture Walkthrough Part 3
Topic: Expressions, Column Aliases, DISTINCT & ORDER BY
Video Duration: ~8 minutes
====================================================================
*/

-- 1. Using SQL as a Calculator: Scalar Expressions
-- Projecting a 5% raise for each employee
SELECT first_name, last_name, salary, salary * 1.05
FROM employees;

-- 2. Providing Clean Output Headers: Column Aliasing with AS
SELECT 
    first_name, 
    last_name, 
    salary AS current_salary,
    salary * 1.05 AS projected_salary
FROM employees;

-- 3. String Concatenation: Merging Text with ||
SELECT 
    first_name || ' ' || last_name AS full_name,
    department,
    title
FROM employees;

-- 4. De-duplicating Result Sets: The DISTINCT Keyword
-- Without DISTINCT (Shows repetitions):
SELECT department FROM employees;

-- With DISTINCT (Shows unique department categories):
SELECT DISTINCT department 
FROM employees;

-- 5. Sorting Results: ORDER BY
-- Ascending (default: A to Z, lowest to highest)
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary ASC;

-- Descending (highest earners first)
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC;

-- 6. Multi-Column Sorting: Nested Hierarchy
-- First sort by department ascending, then by salary descending within each department
SELECT department, last_name, first_name, salary
FROM employees
ORDER BY department ASC, salary DESC;
