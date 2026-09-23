-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 4: Summarization, Aggregation & Pivoting
-- Script 1: Core Aggregate Functions and The GROUP BY Clause
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: The Big Five Aggregate Functions
-- Aggregates collapse multiple rows into a single scalar value.
-- Notice the critical difference between COUNT(*) and COUNT(column_name):
-- COUNT(*) counts all rows; COUNT(column) ignores NULLs.
-- ----------------------------------------------------------------------------

-- 1.1 Company-wide salary and headcount metrics
SELECT 
    COUNT(*) AS total_headcount,
    COUNT(location_id) AS assigned_to_locations,
    ROUND(AVG(salary), 2) AS average_salary,
    SUM(salary) AS total_payroll,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary
FROM employees;

-- 1.2 Demonstrating NULL handling in mathematical aggregates
-- Notice that AVG() divides by the count of non-null rows, NOT total rows.
SELECT 
    COUNT(*) AS total_products,
    COUNT(retail_price) AS products_with_prices,
    ROUND(AVG(retail_price), 2) AS avg_retail_price,
    ROUND(SUM(retail_price) / COUNT(*), 2) AS avg_price_if_null_were_zero
FROM products;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: The GROUP BY Clause
-- Collapses rows into distinct categorical buckets.
-- ----------------------------------------------------------------------------

-- 2.1 Departmental salary distribution
SELECT 
    department,
    COUNT(*) AS employee_count,
    ROUND(AVG(salary), 2) AS avg_dept_salary,
    MIN(salary) AS min_dept_salary,
    MAX(salary) AS max_dept_salary
FROM employees
GROUP BY department
ORDER BY employee_count DESC;

-- 2.2 Multi-column grouping: Aggregating across hierarchical categories
SELECT 
    department,
    job_title,
    COUNT(*) AS role_count,
    ROUND(AVG(salary), 2) AS avg_role_salary
FROM employees
GROUP BY department, job_title
ORDER BY department, avg_role_salary DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: The Golden Rule of Aggregation
-- Every non-aggregated column in the SELECT clause MUST appear in GROUP BY!
-- ----------------------------------------------------------------------------

-- 3.1 DELIBERATE ERROR DEMONSTRATION (Uncomment to inspect the PostgreSQL error):
-- SELECT department, first_name, AVG(salary)
-- FROM employees
-- GROUP BY department;
-- ERROR: column "employees.first_name" must appear in the GROUP BY clause or be used in an aggregate function

-- 3.2 Correct implementation:
SELECT 
    department,
    COUNT(*) AS total_staff,
    STRING_AGG(first_name, ', ' ORDER BY salary DESC) AS top_earners
FROM employees
GROUP BY department;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 4: Aggregating Across Relational Joins
-- Joining tables before grouping to produce business intelligence reports.
-- ----------------------------------------------------------------------------

-- 4.1 Order volume and revenue by customer/order header
SELECT 
    o.order_id,
    o.order_date,
    COUNT(ol.line_id) AS distinct_items_ordered,
    SUM(ol.quantity) AS total_units_ordered,
    ROUND(SUM(ol.quantity * ol.unit_price), 2) AS total_order_amount
FROM orders o
JOIN order_lines ol ON o.order_id = ol.order_id
GROUP BY o.order_id, o.order_date
ORDER BY total_order_amount DESC
LIMIT 10;
