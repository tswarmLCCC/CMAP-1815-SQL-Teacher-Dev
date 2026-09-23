-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 6: Query Modularity, CTEs & Window Functions
-- Script 2: Window Functions, Partitioning & Ranking Semantics
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Basic Window Functions with OVER()
-- Aggregation metrics without row collapse!
-- ----------------------------------------------------------------------------

-- 1.1 Company average and departmental average on every employee row
SELECT 
    employee_id,
    first_name,
    department,
    salary,
    -- Total company average (entire table window):
    ROUND(AVG(salary) OVER(), 2) AS company_avg_salary,
    -- Departmental average (partitioned window):
    ROUND(AVG(salary) OVER(PARTITION BY department), 2) AS dept_avg_salary,
    -- Difference from departmental average:
    ROUND(salary - AVG(salary) OVER(PARTITION BY department), 2) AS diff_from_dept_avg
FROM employees
ORDER BY department, salary DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Ranking Functions (ROW_NUMBER vs. RANK vs. DENSE_RANK)
-- Understanding how ties are handled in analytical ranking.
-- ----------------------------------------------------------------------------

SELECT 
    first_name,
    last_name,
    department,
    salary,
    -- ROW_NUMBER: Strictly sequential, never ties (1, 2, 3, 4)
    ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary DESC) AS seq_num,
    -- RANK: Leaves gaps after ties (1, 2, 2, 4)
    RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS std_rank,
    -- DENSE_RANK: No gaps after ties (1, 2, 2, 3)
    DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS dense_rank
FROM employees
ORDER BY department, salary DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Filtering Window Functions (The CTE Requirement)
-- You CANNOT use window functions in WHERE directly!
-- We wrap the window query inside a CTE to filter for top-N performers.
-- ----------------------------------------------------------------------------

-- Top 2 highest earners in every department:
WITH ranked_staff AS (
    SELECT 
        employee_id,
        first_name,
        last_name,
        department,
        salary,
        DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS dept_salary_rank
    FROM employees
)
SELECT 
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    dept_salary_rank
FROM ranked_staff
WHERE dept_salary_rank <= 2
ORDER BY department, dept_salary_rank;
