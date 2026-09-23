-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 4: Summarization, Aggregation & Pivoting
-- Script 2: WHERE vs. HAVING Filtering & Set Operations
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Row Filtering (WHERE) vs. Group Filtering (HAVING)
-- WHERE filters raw rows before grouping occurs.
-- HAVING filters aggregated summary rows after grouping is completed.
-- ----------------------------------------------------------------------------

-- 1.1 The Complete Filtering Pipeline
SELECT 
    department,
    COUNT(*) AS active_staff,
    ROUND(AVG(salary), 2) AS avg_active_salary
FROM employees
WHERE is_active = TRUE              -- Step 1: Discard inactive staff rows
GROUP BY department                 -- Step 2: Form department groups
HAVING COUNT(*) >= 3                -- Step 3: Keep groups with at least 3 active staff
   AND AVG(salary) >= 65000         -- Step 4: Keep groups with average salary >= $65,000
ORDER BY avg_active_salary DESC;    -- Step 5: Sort final results

-- 1.2 Performance Best Practice: Put non-aggregate filters in WHERE, not HAVING
-- BAD PRACTICE (Computes aggregates for all departments then discards):
-- SELECT department, AVG(salary) FROM employees GROUP BY department HAVING department <> 'Executive';
-- GOOD PRACTICE (Prunes 'Executive' before hash aggregation):
SELECT department, ROUND(AVG(salary), 2) AS avg_sal
FROM employees
WHERE department <> 'Executive'
GROUP BY department;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Set Operations (UNION and UNION ALL)
-- Stacking datasets vertically.
-- Requirement: Same number of columns, compatible data types.
-- ----------------------------------------------------------------------------

-- 2.1 UNION ALL (Retains all rows - Fast!)
SELECT 
    'Wyoming Branch' AS facility_source,
    first_name,
    last_name,
    department
FROM employees
WHERE location_id = 1

UNION ALL

SELECT 
    'Remote / Satellite' AS facility_source,
    first_name,
    last_name,
    department
FROM employees
WHERE location_id IS NULL OR location_id <> 1
ORDER BY last_name;

-- 2.2 UNION vs. UNION ALL (Deduplication)
-- Notice that UNION eliminates duplicates by performing an internal sort/hash.
SELECT department FROM employees WHERE salary > 80000
UNION
SELECT department FROM employees WHERE hire_date < '2021-01-01';

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: INTERSECT and EXCEPT
-- Finding commonalities and discrepancies between datasets.
-- ----------------------------------------------------------------------------

-- 3.1 INTERSECT: Departments with high earners AND tenured staff
SELECT department FROM employees WHERE salary > 80000
INTERSECT
SELECT department FROM employees WHERE hire_date < '2021-01-01';

-- 3.2 EXCEPT: Departments with high earners that have NO staff hired before 2021
SELECT department FROM employees WHERE salary > 80000
EXCEPT
SELECT department FROM employees WHERE hire_date < '2021-01-01';
