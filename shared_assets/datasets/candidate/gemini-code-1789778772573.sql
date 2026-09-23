/*
====================================================================
Module 6: Advanced Analytics (CTEs and Window Functions)
====================================================================
File: week_6_window_ctes_lab.sql
Focus: WITH clause, OVER(), PARTITION BY, ROW_NUMBER.
====================================================================
*/

/* --- INSTRUCTOR DEMONSTRATION --- */

-- Demo 1: Common Table Expression (CTE)
-- Refactoring a query to make finding high-value orders readable.
WITH OrderTotals AS (
    SELECT order_id, SUM(quantity * unit_price) AS total_revenue
    FROM order_lines
    GROUP BY order_id
)
SELECT o.order_date, ot.total_revenue
FROM orders o
INNER JOIN OrderTotals ot ON o.order_id = ot.order_id
WHERE ot.total_revenue > 500;

-- Demo 2: Window Function - Ranking
-- Rank employees by salary within their specific departments.
SELECT first_name, last_name, department, salary,
       RANK() OVER(PARTITION BY department ORDER BY salary DESC) as dept_salary_rank
FROM employees;

/* --- STUDENT ASSESSMENT --- */

-- 1. CTE Refactor: Write a CTE named 'CategoryStats' that calculates the average 
-- retail price per category. Then query that CTE to show only categories averaging over $50.
WITH CategoryStats AS (
    SELECT category, AVG(retail_price) as avg_price
    FROM products
    GROUP BY category
)
SELECT category, avg_price 
FROM CategoryStats 
WHERE avg_price > 50;

-- 2. Running Totals: Use a Window Function to calculate a running total of stock_quantity 
-- ordered by the product release_date.
SELECT product_name, release_date, stock_quantity,
       SUM(stock_quantity) OVER(ORDER BY release_date ASC) as running_stock_total
FROM products
WHERE release_date IS NOT NULL;

-- 3. Deduplication Prep: Use ROW_NUMBER() to assign a unique ID (1, 2, 3...) to 
-- employees in each location, ordered by their hire_date.
SELECT first_name, last_name, location_id, hire_date,
       ROW_NUMBER() OVER(PARTITION BY location_id ORDER BY hire_date ASC) as seniority_rank
FROM employees;