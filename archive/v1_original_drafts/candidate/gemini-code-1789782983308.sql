/*
====================================================================
Module 5: Safe Data Manipulation and Validation
File: week_5_dml_temp_tables_lab.sql
Focus: INSERT, UPDATE, DELETE, Validation Protocols, Temp Tables.
====================================================================
*/

/* 
--------------------------------------------------------------------
Part 1: Instructor Demonstration Queries
Use these during Periods 1 & 2 to emphasize the "Safe Update Protocol".
--------------------------------------------------------------------
*/

-- Demo 1: The Safe Update Protocol
-- Goal: Increase the price of all 'Books' by 10%.
-- Step A: ALWAYS write the SELECT first to verify the target rows.
SELECT product_name, retail_price 
FROM products 
WHERE category = 'Books';

-- Step B: Execute the UPDATE using the exact same WHERE clause.
UPDATE products 
SET retail_price = retail_price * 1.10 
WHERE category = 'Books';

-- Demo 2: Temporary Tables
-- Goal: Stage a specific subset of active sales staff for a complex operation.
CREATE TEMP TABLE active_sales AS
SELECT employee_id, first_name, last_name, location_id 
FROM employees 
WHERE department = 'Sales' AND is_active = TRUE;

-- Verify the temp table was created and populated.
SELECT * FROM active_sales;


/* 
--------------------------------------------------------------------
Part 2: Student Assessment (Data Cleanup Lab)
Periods 3 & 4 Independent Practice
--------------------------------------------------------------------
*/

-- 1. Write an INSERT statement to add a new employee to the database.
-- Supply values for first_name, last_name, department, title, hire_date, 
-- salary, location_id, and set is_active to TRUE.
INSERT INTO employees (first_name, last_name, department, title, hire_date, salary, location_id, is_active) 
VALUES ('Sarah', 'Connor', 'Security', 'Tactical Advisor', CURRENT_DATE, 88000.00, 10, TRUE);

-- 2. The Safe Update: The 'Fitness' category is having a 15% off inventory clearance.
-- Step A: Write the SELECT statement to verify the current products and prices.
SELECT product_name, retail_price 
FROM products 
WHERE category = 'Fitness';

-- Step B: Write the UPDATE statement to reduce the retail_price by 15%.
UPDATE products 
SET retail_price = retail_price * 0.85 
WHERE category = 'Fitness';

-- Step C: Write the SELECT statement again to validate the changes took effect.
SELECT product_name, retail_price 
FROM products 
WHERE category = 'Fitness';

-- 3. Data Archiving with Temp Tables
-- We need to clean up discontinued products, but we don't want to lose the record entirely yet.
-- Step A: Create a temp table named 'discontinued_archive' and populate it with 
-- all products that have a discontinued_date.
CREATE TEMP TABLE discontinued_archive AS
SELECT * 
FROM products 
WHERE discontinued_date IS NOT NULL;

-- Step B: Write a SELECT statement to count how many rows are in your temp table.
SELECT COUNT(*) FROM discontinued_archive;

-- Step C: Safely DELETE those records from the main products table using the exact same logic.
DELETE FROM products 
WHERE discontinued_date IS NOT NULL;