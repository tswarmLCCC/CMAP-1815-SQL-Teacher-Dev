/*
====================================================================
CMAP 1815 - Unit 1: Instructor Solution Key
Lab: Data Exploration & Orientation
====================================================================
*/

-- ==================================================================
-- Part 1: Environment & System Catalogs
-- ==================================================================

-- 1. Server Version
SELECT version();

-- 2. Current Session
SELECT current_user, current_database();

-- 3. Table Discovery in Public Schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name ASC;

-- 4. Column Inspector for Employees Table
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'employees'
ORDER BY ordinal_position ASC;


-- ==================================================================
-- Part 2: Precision Projection & Data Exploration
-- ==================================================================

-- 5. Staff Directory
SELECT first_name, last_name, title
FROM employees
ORDER BY last_name ASC;

-- 6. Executive Compensation Roster
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC;

-- 7. Unique Departments
SELECT DISTINCT department
FROM employees
ORDER BY department ASC;

-- 8. Department-Title Roster
SELECT DISTINCT department, title
FROM employees
ORDER BY department ASC, title ASC;


-- ==================================================================
-- Part 3: Expressions, Aliases & Mathematical Projections
-- ==================================================================

-- 9. Polished Full Name with String Concatenation
SELECT 
    first_name || ' ' || last_name AS full_name,
    department
FROM employees
ORDER BY department ASC, full_name ASC;

-- 10. Bonus Simulation
-- Teaching Note: Highlight that if bonus is NULL, the result of (salary + bonus) is NULL!
-- This is intentional and sets up Three-Valued Logic and COALESCE for Unit 2.
SELECT 
    last_name,
    salary AS base_salary,
    bonus AS annual_bonus,
    salary + bonus AS total_compensation
FROM employees;

-- 11. Retail Product Margins
SELECT 
    product_name,
    retail_price,
    cost_to_produce,
    retail_price - cost_to_produce AS estimated_unit_profit
FROM products
ORDER BY estimated_unit_profit DESC;

-- 12. Inventory Value Analysis
SELECT 
    product_name,
    stock_quantity,
    retail_price,
    stock_quantity * retail_price AS total_inventory_value
FROM products
ORDER BY total_inventory_value DESC;
