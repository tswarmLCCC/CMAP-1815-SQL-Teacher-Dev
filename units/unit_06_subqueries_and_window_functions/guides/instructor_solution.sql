-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 6: Query Modularity, CTEs & Window Functions
-- Instructor Master Solution
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TASK 1: Refactoring Legacy Nested Subqueries into Modular CTEs
-- ----------------------------------------------------------------------------
WITH active_dept_averages AS (
    SELECT 
        department,
        COUNT(*) AS headcount,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM employees
    WHERE is_active = TRUE
    GROUP BY department
)
SELECT 
    department,
    headcount,
    avg_salary
FROM active_dept_averages
WHERE avg_salary > 65000.00
ORDER BY avg_salary DESC;


-- ----------------------------------------------------------------------------
-- TASK 2: Individual Compensation Variance via Window Functions
-- ----------------------------------------------------------------------------
SELECT 
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    ROUND(AVG(salary) OVER(PARTITION BY department), 2) AS dept_avg_salary,
    ROUND(salary - AVG(salary) OVER(PARTITION BY department), 2) AS salary_variance,
    ROUND(AVG(salary) OVER(), 2) AS company_avg_salary
FROM employees
ORDER BY department, salary_variance DESC;


-- ----------------------------------------------------------------------------
-- TASK 3: Top-N Departmental Earner Filter (CTE + Window Ranking)
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
-- TASK 4: Cumulative Financial Ledger (Running Totals)
-- ----------------------------------------------------------------------------
SELECT 
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER(
        ORDER BY order_date, order_id
    ) AS cumulative_revenue,
    COUNT(*) OVER(
        ORDER BY order_date, order_id
    ) AS running_order_count,
    ROUND(AVG(total_amount) OVER(
        ORDER BY order_date, order_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3_orders
FROM orders
ORDER BY order_date, order_id;


-- ----------------------------------------------------------------------------
-- TASK 5: Golden Record Deduplication Pattern
-- ----------------------------------------------------------------------------
WITH ranked_customer_orders AS (
    SELECT 
        order_id,
        customer_id,
        order_date,
        total_amount,
        ROW_NUMBER() OVER(
            PARTITION BY customer_id 
            ORDER BY order_date DESC, order_id DESC
        ) AS recency_rank
    FROM orders
)
SELECT 
    customer_id,
    order_id AS latest_order_id,
    order_date AS latest_order_date,
    total_amount AS latest_order_amount
FROM ranked_customer_orders
WHERE recency_rank = 1
ORDER BY customer_id;
