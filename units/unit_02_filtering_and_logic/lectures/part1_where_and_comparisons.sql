/*
====================================================================
CMAP 1815 - Unit 2: Lecture Walkthrough Part 1
Topic: The WHERE Clause & Comparison Operators
Video Duration: ~7 minutes
====================================================================
*/

-- 1. Numerical Filtering: Finding Premium Products
-- Filters rows where retail_price is strictly 100.00 or greater
SELECT product_name, category, retail_price
FROM products
WHERE retail_price >= 100.00
ORDER BY retail_price DESC;

-- 2. Exact Text Matching (Case-Sensitive)
-- Finds employees specifically assigned to 'Security'
SELECT first_name, last_name, department, title
FROM employees
WHERE department = 'Security';

-- 3. Date Filtering: ISO 8601 Format (YYYY-MM-DD)
-- Identifies employees hired on or after January 1, 2020
SELECT first_name, last_name, hire_date
FROM employees
WHERE hire_date >= '2020-01-01'
ORDER BY hire_date ASC;

-- 4. Inclusive Range Filtering: The BETWEEN Operator
-- Finds products priced between $25.00 and $75.00 inclusive
SELECT product_name, retail_price, stock_quantity
FROM products
WHERE retail_price BETWEEN 25.00 AND 75.00
ORDER BY retail_price ASC;

-- 5. [DEMO TRAP: The Alias in WHERE Trap]
-- Uncomment the query below to show the error:
-- SELECT product_name, retail_price * 0.90 AS sale_price
-- FROM products
-- WHERE sale_price < 50.00;
-- ERROR: column "sale_price" does not exist

-- Correct Approach (Repeat the expression):
SELECT product_name, retail_price * 0.90 AS sale_price
FROM products
WHERE retail_price * 0.90 < 50.00;
