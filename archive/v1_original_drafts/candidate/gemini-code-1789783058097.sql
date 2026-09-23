/*
====================================================================
Module 2: Restricting and Sorting Data
File: week_2_filtering_lab.sql
Focus: WHERE clause, AND/OR logic, IN, LIKE, IS NULL, ORDER BY
====================================================================
*/

/* 
--------------------------------------------------------------------
Part 1: Instructor Demonstration Queries
Use these during Periods 1 & 2 to explain row-level filtering.
--------------------------------------------------------------------
*/

-- Demo 1: Basic Filtering and Boolean Logic
-- Goal: Restrict data using conditions.
SELECT first_name, last_name, department 
FROM employees 
WHERE department = 'Security' OR department = 'Research';

-- Demo 2: Pattern Matching and Missing Data
-- Goal: Find text fragments and handle NULL values safely.
SELECT product_name, description 
FROM products 
WHERE description LIKE '%Bluetooth%' OR discontinued_date IS NULL;

-- Demo 3: Sorting and Limiting
-- Goal: Order the final result set and restrict row count.
SELECT product_name, retail_price 
FROM products 
ORDER BY retail_price DESC 
LIMIT 3;


/* 
--------------------------------------------------------------------
Part 2: Student Assessment (Targeted Retrieval Lab)
Periods 3 & 4 Independent Practice
--------------------------------------------------------------------
*/

-- 1. Find all products that cost strictly more than $100.
SELECT product_name, retail_price 
FROM products 
WHERE retail_price > 100.00;

-- 2. Find all products in the 'Home Automation' category that currently have a stock quantity greater than 0.
SELECT product_name, stock_quantity 
FROM products 
WHERE category = 'Home Automation' AND stock_quantity > 0;

-- 3. Identify all employees who have not been assigned a bonus. (Hint: Look for missing data).
SELECT first_name, last_name, bonus 
FROM employees 
WHERE bonus IS NULL;

-- 4. List all products that contain the word 'Key' anywhere in their product name.
SELECT product_name, category 
FROM products 
WHERE product_name LIKE '%Key%';

-- 5. Retrieve all employees hired between January 1, 2018, and December 31, 2021.
SELECT first_name, last_name, hire_date 
FROM employees 
WHERE hire_date BETWEEN '2018-01-01' AND '2021-12-31';

-- 6. Use the IN operator to list all products in the 'Audio', 'Gaming', or 'Electronics' categories.
SELECT product_name, category 
FROM products 
WHERE category IN ('Audio', 'Gaming', 'Electronics');

-- 7. Generate a list of all active employees, sorted by their salary from highest to lowest.
SELECT first_name, last_name, salary 
FROM employees 
WHERE is_active = TRUE 
ORDER BY salary DESC;

-- 8. Find the top 5 most expensive products currently in stock. 
-- Sort the results descending by price, and use a limit clause to restrict the output.
SELECT product_name, retail_price, stock_quantity 
FROM products 
WHERE stock_quantity > 0 
ORDER BY retail_price DESC 
LIMIT 5;