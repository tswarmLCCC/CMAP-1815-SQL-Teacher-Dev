/*
====================================================================
CMAP 1815 - Unit 2: Lecture Walkthrough Part 2
Topic: Pattern Matching (LIKE/ILIKE) & The IN Operator
Video Duration: ~7 minutes
====================================================================
*/

-- 1. Discrete Set Filtering: The IN Operator
-- Retrieve employees in Sales, Research, or Support
SELECT first_name, last_name, department, salary
FROM employees
WHERE department IN ('Sales', 'Research', 'Support')
ORDER BY department ASC, salary DESC;

-- 2. Negating the Set: NOT IN
-- Find all employees OUTSIDE of Management and Operations
SELECT first_name, last_name, department
FROM employees
WHERE department NOT IN ('Management', 'Operations')
ORDER BY department ASC;

-- 3. Wildcard Searching with LIKE: The Percent Symbol (%)
-- Finds all locations in cities starting with the letter 'C'
SELECT city, state, facility_type
FROM locations
WHERE city LIKE 'C%';

-- Finds any product containing the word 'Widget' anywhere in the name
SELECT product_name, category, retail_price
FROM products
WHERE product_name LIKE '%Widget%';

-- 4. Case-Insensitive Pattern Matching: ILIKE (PostgreSQL)
-- Matches 'widget', 'Widget', or 'WIDGET'
SELECT product_name, description
FROM products
WHERE description ILIKE '%heavy%';

-- 5. Exact Character Placeholder: The Underscore (_)
-- Finds states with exact two-letter pattern starting with 'C'
SELECT city, state
FROM locations
WHERE state LIKE 'C_';
