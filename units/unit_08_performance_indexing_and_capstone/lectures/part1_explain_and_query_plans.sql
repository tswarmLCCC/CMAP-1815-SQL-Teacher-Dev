-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 8: Query Performance, Indexing & Capstone Defense
-- Script 1: Query Execution Profiling with EXPLAIN & EXPLAIN ANALYZE
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Reading Query Plans (EXPLAIN vs. EXPLAIN ANALYZE)
-- EXPLAIN: Query plan estimate without executing.
-- EXPLAIN ANALYZE: Real execution timing and exact row count metrics.
-- ----------------------------------------------------------------------------

-- 1.1 Estimated query plan
EXPLAIN
SELECT * 
FROM employees 
WHERE salary > 85000.00;

-- 1.2 Real execution metrics (Note the actual time and loops)
EXPLAIN ANALYZE
SELECT * 
FROM employees 
WHERE salary > 85000.00;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Analyzing Join Performance Plans
-- Observing how the query planner chooses join algorithms:
-- Hash Join, Nested Loop, or Merge Join.
-- ----------------------------------------------------------------------------

EXPLAIN ANALYZE
SELECT 
    o.order_id,
    o.order_date,
    c.customer_id,
    c.first_name,
    c.last_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2023-01-01';

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Profiling Aggregation and Window Performance
-- ----------------------------------------------------------------------------

EXPLAIN ANALYZE
SELECT 
    department,
    COUNT(*) AS total_staff,
    ROUND(AVG(salary), 2) AS avg_sal,
    DENSE_RANK() OVER(ORDER BY AVG(salary) DESC) AS rank_by_avg_salary
FROM employees
GROUP BY department;
