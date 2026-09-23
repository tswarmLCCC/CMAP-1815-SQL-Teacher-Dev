-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 8: Query Performance, Indexing & Capstone Defense
-- Script 2: B-Tree Indexing Strategies & The Write Penalty
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Single-Column B-Tree Indexing
-- Transforming slow Sequential Scans into fast Index Scans.
-- ----------------------------------------------------------------------------

-- Before indexing: Profile search by department
EXPLAIN ANALYZE
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE department = 'Research';

-- Create B-Tree Index
CREATE INDEX IF NOT EXISTS idx_employees_dept ON employees(department);

-- After indexing: Re-profile to observe index scan behavior
EXPLAIN ANALYZE
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE department = 'Research';

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Composite (Multi-Column) Indexing
-- Optimizing queries that filter on multiple columns simultaneously.
-- Rule: The index is most effective when queries filter on the leading column!
-- ----------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_employees_dept_salary ON employees(department, salary);

-- Query utilizing both leading and secondary index keys
EXPLAIN ANALYZE
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE department = 'Research' AND salary > 75000.00;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Partial Indexing (Storage & Write Optimization)
-- Index only the subset of rows that queries actually filter on.
-- ----------------------------------------------------------------------------

-- Instead of indexing all 50,000 rows, index only active employees:
CREATE INDEX IF NOT EXISTS idx_employees_active_salaries 
ON employees(salary) 
WHERE is_active = TRUE;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 4: Inspecting Index Usage & Catalog Metadata
-- ----------------------------------------------------------------------------

SELECT 
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS number_of_scans,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched
FROM pg_stat_user_indexes
WHERE relname IN ('employees', 'products', 'orders');
