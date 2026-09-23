-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 6: Query Modularity, CTEs & Window Functions
-- Script 1: Subqueries vs. Common Table Expressions (CTEs)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Subqueries in WHERE & FROM Clauses
-- ----------------------------------------------------------------------------

-- 1.1 Scalar Subquery in WHERE: Employees earning above company average
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;

-- 1.2 Correlated Subquery: Employees earning above their own department's average
SELECT e.employee_id, e.first_name, e.department, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(sub.salary)
    FROM employees sub
    WHERE sub.department = e.department
)
ORDER BY e.department, e.salary DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Refactoring into Common Table Expressions (WITH)
-- CTEs make query logic modular, top-down, and easy to maintain.
-- ----------------------------------------------------------------------------

-- 2.1 Clean CTE alternative to the correlated subquery above
WITH dept_averages AS (
    SELECT 
        department, 
        ROUND(AVG(salary), 2) AS avg_dept_salary
    FROM employees
    GROUP BY department
)
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.department,
    e.salary,
    d.avg_dept_salary,
    e.salary - d.avg_dept_salary AS salary_premium
FROM employees e
JOIN dept_averages d ON e.department = d.department
WHERE e.salary > d.avg_dept_salary
ORDER BY e.department, salary_premium DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Chaining Multiple CTEs in a Data Pipeline
-- ----------------------------------------------------------------------------

-- Multi-step customer analysis pipeline
WITH order_aggregates AS (
    -- Step 1: Calculate total spend per order
    SELECT 
        order_id,
        customer_id,
        SUM(quantity * unit_price) AS order_total
    FROM order_lines
    GROUP BY order_id, customer_id
),
customer_lifetime_value AS (
    -- Step 2: Aggregate lifetime spend per customer
    SELECT 
        customer_id,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(order_total), 2) AS lifetime_spend
    FROM order_aggregates
    GROUP BY customer_id
),
tiered_customers AS (
    -- Step 3: Segment customers into loyalty tiers
    SELECT 
        customer_id,
        total_orders,
        lifetime_spend,
        CASE 
            WHEN lifetime_spend >= 1000.00 THEN 'Platinum'
            WHEN lifetime_spend >= 500.00 THEN 'Gold'
            ELSE 'Standard'
        END AS loyalty_tier
    FROM customer_lifetime_value
)
-- Step 4: Final presentation query
SELECT *
FROM tiered_customers
ORDER BY lifetime_spend DESC;
