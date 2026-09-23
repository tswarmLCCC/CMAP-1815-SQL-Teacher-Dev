/*
====================================================================
Module 5: Safe Data Manipulation and Validation
====================================================================
File: week_5_dml_temp_tables_lab.sql
Focus: INSERT, UPDATE, DELETE, Validation Protocols, Temp Tables.
====================================================================
*/

/* --- INSTRUCTOR DEMONSTRATION --- */

-- Demo 1: The Safe Update Protocol
-- Always write the SELECT first to verify the target rows.
SELECT product_name, retail_price FROM products WHERE category = 'Books';

-- Execute the UPDATE based on the exact same WHERE clause.
UPDATE products 
SET retail_price = retail_price * 1.10 
WHERE category = 'Books';

-- Demo 2: Temporary Tables
-- Staging active sales staff for a specific operation.
CREATE TEMP TABLE active_sales AS
SELECT employee_id, first_name, last_name 
FROM employees 
WHERE department = 'Sales' AND is_active = TRUE;

/* --- STUDENT ASSESSMENT --- */

-- 1. INSERT a new executive employee into the database. 
INSERT INTO employees (first_name, last_name, department, title, hire_date, salary, location_id, is_active) 
VALUES ('John', 'Elway', 'Management', 'Executive Director', CURRENT_DATE, 250000.00, 3, TRUE);

-- 2. The Safe Update: The 'Fitness' category is having a 15% off sale.
-- Step A: Write the SELECT statement to verify the current prices.
SELECT product_name, retail_price 
FROM products 
WHERE category = 'Fitness';

-- Step B: Write the UPDATE statement to reduce the retail_price by 15%.
UPDATE products 
SET retail_price = retail_price * 0.85 
WHERE category = 'Fitness';

-- 3. Data Archiving with Temp Tables
-- Step A: Create a temp table named 'discontinued_archive' and populate it with discontinued products.
CREATE TEMP TABLE discontinued_archive AS
SELECT * FROM products WHERE discontinued_date IS NOT NULL;

-- Step B: Safely DELETE those records from the main products table using the exact same logic.
DELETE FROM products 
WHERE discontinued_date IS NOT NULL;