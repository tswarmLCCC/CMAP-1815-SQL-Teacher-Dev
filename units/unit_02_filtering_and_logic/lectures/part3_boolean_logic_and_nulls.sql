/*
====================================================================
CMAP 1815 - Unit 2: Lecture Walkthrough Part 3
Topic: Boolean Logic, The NULL Mystery, & Result Limiting
Video Duration: ~8 minutes
====================================================================
*/

-- 1. Boolean Gates: AND vs. OR
-- Both conditions must be met:
SELECT first_name, last_name, department, salary
FROM employees
WHERE department = 'Security' 
  AND salary >= 65000;

-- 2. [DEMO TRAP: Operator Precedence without Parentheses]
-- AND executes before OR!
-- This query returns high earners in Sales... PLUS ANYONE in Security (even dogs earning $20k!)
SELECT first_name, last_name, department, salary
FROM employees
WHERE department = 'Security' 
   OR department = 'Sales' 
  AND salary >= 70000;

-- The Fix: Enforce intended logic with parentheses!
SELECT first_name, last_name, department, salary
FROM employees
WHERE (department = 'Security' OR department = 'Sales')
  AND salary >= 70000;

-- 3. [DEMO TRAP: The = NULL Disaster]
-- This query returns ZERO rows because nothing equals UNKNOWN!
SELECT first_name, last_name, bonus
FROM employees
WHERE bonus = NULL; -- ❌ NEVER USE!

-- The Correct Approach: IS NULL and IS NOT NULL
-- Finds employees who do NOT receive an annual bonus:
SELECT first_name, last_name, department, salary, bonus
FROM employees
WHERE bonus IS NULL;

-- Finds employees who DO receive an annual bonus:
SELECT first_name, last_name, department, salary, bonus
FROM employees
WHERE bonus IS NOT NULL
ORDER BY bonus DESC;

-- 4. Result Limiting & Web Pagination: LIMIT and OFFSET
-- Page 1: Top 5 Highest Paid Employees
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5 OFFSET 0;

-- Page 2: Next 5 Highest Paid Employees (Skip 5, take 5)
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5 OFFSET 5;
