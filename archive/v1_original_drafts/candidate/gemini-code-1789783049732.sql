/*
====================================================================
Module 8: Performance, Auditing, and Capstone
File: week_8_performance_final.sql
Focus: Indexes, Execution Plans, Synthesis of all course concepts.
====================================================================
*/

/* 
--------------------------------------------------------------------
Part 1: Instructor Demonstration Queries
Use these during Periods 1 & 2 to explain optimization.
--------------------------------------------------------------------
*/

-- Demo 1: Indexing for Performance
-- Goal: Create a non-clustered index on a column frequently used in WHERE clauses 
-- to speed up data retrieval.
CREATE INDEX idx_products_category ON products(category);

-- Demo 2: Reading an Execution Plan
-- Goal: Show the database engine's step-by-step strategy for executing a query.
-- Note: 'EXPLAIN ANALYZE' physically runs the query and returns the performance metrics.
EXPLAIN ANALYZE 
SELECT * 
FROM products 
WHERE category = 'Gaming';


/* 
--------------------------------------------------------------------
Part 2: Student Assessment (Capstone Project)
Periods 3 & 4 Independent Practice
--------------------------------------------------------------------
*/

-- 1. Optimization: The HR department runs frequent reports filtering by the 'title' column. 
-- Create an index on the 'title' column in the employees table to optimize these queries.
CREATE INDEX idx_employees_title ON employees(title);

-- 2. Capstone Synthesis Query: The business needs an executive revenue report.
-- Write a single query that meets all the following requirements:
--   A. Uses a Common Table Expression (CTE) to calculate the total revenue generated 
--      by each order (sum of quantity * unit_price).
--   B. Uses a main query that joins your CTE to the orders, employees, and locations tables.
--   C. Displays the employee's last name, the location city, the order_date, and the total revenue.
--   D. Filters the final results to only show orders that generated strictly more than $100.
--   E. Sorts the results so the highest revenue orders appear at the top.

WITH OrderRevenue AS (
    SELECT 
        order_id, 
        SUM(quantity * unit_price) AS total_order_value
    FROM order_lines
    GROUP BY order_id
)
SELECT 
    e.last_name, 
    l.city, 
    o.order_date, 
    orv.total_order_value
FROM orders o
INNER JOIN OrderRevenue orv ON o.order_id = orv.order_id
INNER JOIN employees e ON o.employee_id = e.employee_id
INNER JOIN locations l ON e.location_id = l.location_id
WHERE orv.total_order_value > 100.00
ORDER BY orv.total_order_value DESC;

-- 3. Data Cleanup (End of Term): Write a DROP TABLE statement to remove the 
-- 'equipment_checkouts' table you created in Week 7.
DROP TABLE IF EXISTS equipment_checkouts;