-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 6: Query Modularity, CTEs & Window Functions
-- In-Class Paired Coding Challenges
-- ============================================================================

-- ----------------------------------------------------------------------------
-- CHALLENGE 1: Refactoring Nested Subqueries into CTEs (Session 1)
-- Scenario: Refactor this messy nested query into a clean, readable CTE pipeline:
-- SELECT * FROM (
--     SELECT department, AVG(salary) as avg_sal
--     FROM employees
--     WHERE is_active = TRUE
--     GROUP BY department
-- ) sub WHERE avg_sal > 65000;
-- ----------------------------------------------------------------------------

-- Write your modular CTE solution below:
WITH active_department_averages AS (
    SELECT 
        department,
        COUNT(*) AS active_headcount,
        ROUND(AVG(salary), 2) AS avg_sal
    FROM employees
    WHERE is_active = TRUE
    GROUP BY department
)
SELECT department, active_headcount, avg_sal
FROM active_department_averages
WHERE avg_sal > 65000.00
ORDER BY avg_sal DESC;


-- ----------------------------------------------------------------------------
-- CHALLENGE 2: Multi-Tier Customer Spend Pipeline (Session 1)
-- Scenario: The Marketing Director wants customer lifetime metrics.
-- Task:
-- 1. CTE 1 (order_totals): Join orders and order_lines to calculate total
--    spend per order (order_id, customer_id, order_subtotal).
-- 2. CTE 2 (customer_spends): Aggregate by customer_id to find total_orders
--    and total_spend.
-- 3. Main Query: Filter for customers with total_spend >= 500, sorted descending.
-- ----------------------------------------------------------------------------

WITH order_totals AS (
    SELECT 
        o.order_id,
        o.customer_id,
        ROUND(SUM(ol.quantity * ol.unit_price), 2) AS order_subtotal
    FROM orders o
    JOIN order_lines ol ON o.order_id = ol.order_id
    GROUP BY o.order_id, o.customer_id
),
customer_spends AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(order_subtotal), 2) AS total_spend
    FROM order_totals
    GROUP BY customer_id
)
SELECT customer_id, total_orders, total_spend
FROM customer_spends
WHERE total_spend >= 500.00
ORDER BY total_spend DESC;


-- ----------------------------------------------------------------------------
-- CHALLENGE 3: Department Salary Variance via Window Functions (Session 2)
-- Scenario: HR needs to identify individual compensation anomalies compared
-- to departmental averages without collapsing rows.
-- Task:
-- 1. Display employee_id, first_name, last_name, department, salary.
-- 2. Calculate dept_avg_salary using AVG(salary) OVER(PARTITION BY department).
-- 3. Calculate salary_variance as (salary - dept_avg_salary).
-- 4. Order by department, salary_variance DESC.
-- ----------------------------------------------------------------------------

SELECT 
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    ROUND(AVG(salary) OVER(PARTITION BY department), 2) AS dept_avg_salary,
    ROUND(salary - AVG(salary) OVER(PARTITION BY department), 2) AS salary_variance
FROM employees
ORDER BY department, salary_variance DESC;


-- ----------------------------------------------------------------------------
-- CHALLENGE 4: Top-N Performer Filter with CTE (Session 2)
-- Scenario: Management wants to identify the top 2 highest-paid employees in
-- every department, handling ties gracefully without skipping ranks.
-- Task:
-- 1. Use DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC).
-- 2. Wrap the window query in a CTE.
-- 3. In the outer query, filter for rank <= 2.
-- ----------------------------------------------------------------------------

WITH ranked_department_salaries AS (
    SELECT 
        employee_id,
        first_name,
        last_name,
        department,
        salary,
        DENSE_RANK() OVER(
            PARTITION BY department 
            ORDER BY salary DESC
        ) AS salary_rank
    FROM employees
)
SELECT 
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    salary_rank
FROM ranked_department_salaries
WHERE salary_rank <= 2
ORDER BY department, salary_rank;


-- ----------------------------------------------------------------------------
-- CHALLENGE 5: The Golden Order Deduplication Pattern (Session 2)
-- Scenario: Find each customer's single most recent order.
-- Task:
-- 1. Use ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC).
-- 2. Wrap in a CTE named ranked_orders.
-- 3. Filter WHERE rn = 1.
-- ----------------------------------------------------------------------------

WITH ranked_orders AS (
    SELECT 
        order_id,
        customer_id,
        order_date,
        total_amount,
        ROW_NUMBER() OVER(
            PARTITION BY customer_id 
            ORDER BY order_date DESC, order_id DESC
        ) AS rn
    FROM orders
)
SELECT 
    customer_id,
    order_id AS latest_order_id,
    order_date AS latest_order_date,
    total_amount AS latest_order_amount
FROM ranked_orders
WHERE rn = 1
ORDER BY customer_id;
