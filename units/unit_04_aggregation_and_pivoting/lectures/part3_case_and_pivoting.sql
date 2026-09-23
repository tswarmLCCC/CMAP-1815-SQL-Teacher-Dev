-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 4: Summarization, Aggregation & Pivoting
-- Script 3: Conditional Aggregations & Matrix Pivoting
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Conditional Aggregation Using CASE Inside COUNT
-- Turning vertical category rows into horizontal reporting columns.
-- ----------------------------------------------------------------------------

-- 1.1 Departmental headcount breakdown by status and location tier
SELECT 
    department,
    COUNT(*) AS total_staff,
    COUNT(CASE WHEN is_active = TRUE THEN 1 END) AS active_count,
    COUNT(CASE WHEN is_active = FALSE THEN 1 END) AS inactive_count,
    COUNT(CASE WHEN salary >= 80000 THEN 1 END) AS senior_tier_count,
    COUNT(CASE WHEN salary < 80000 THEN 1 END) AS junior_tier_count
FROM employees
GROUP BY department
ORDER BY total_staff DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Conditional Aggregation Using CASE Inside SUM
-- Pivoting financial metrics across categorical dimensions.
-- ----------------------------------------------------------------------------

-- 2.1 Department payroll allocation by active status
SELECT 
    department,
    SUM(salary) AS total_payroll,
    SUM(CASE WHEN is_active = TRUE THEN salary ELSE 0 END) AS active_payroll,
    SUM(CASE WHEN is_active = FALSE THEN salary ELSE 0 END) AS inactive_payroll,
    ROUND(
        100.0 * SUM(CASE WHEN is_active = TRUE THEN salary ELSE 0 END) / NULLIF(SUM(salary), 0),
        1
    ) AS pct_active_payroll
FROM employees
GROUP BY department
ORDER BY total_payroll DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Modern PostgreSQL Alternative: The FILTER Clause
-- PostgreSQL supports the ANSI SQL:2003 FILTER clause for cleaner syntax.
-- ----------------------------------------------------------------------------

-- 3.1 Headcount matrix using FILTER (WHERE ...)
SELECT 
    department,
    COUNT(*) AS total_staff,
    COUNT(*) FILTER (WHERE is_active = TRUE) AS active_count,
    COUNT(*) FILTER (WHERE is_active = FALSE) AS inactive_count,
    ROUND(AVG(salary) FILTER (WHERE is_active = TRUE), 2) AS avg_active_salary
FROM employees
GROUP BY department
ORDER BY total_staff DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 4: Executive Cross-Tab Matrix from Superstore Data
-- Pivoting sales categories across geographic regions into a spreadsheet matrix.
-- ----------------------------------------------------------------------------

-- 4.1 Regional Category Matrix
SELECT 
    COALESCE(region, 'Unknown') AS region,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN category = 'Furniture' THEN sales ELSE 0 END), 2) AS furniture_sales,
    ROUND(SUM(CASE WHEN category = 'Office Supplies' THEN sales ELSE 0 END), 2) AS office_supplies_sales,
    ROUND(SUM(CASE WHEN category = 'Technology' THEN sales ELSE 0 END), 2) AS technology_sales,
    ROUND(
        100.0 * SUM(CASE WHEN category = 'Technology' THEN sales ELSE 0 END) / NULLIF(SUM(sales), 0),
        1
    ) AS tech_revenue_share_pct
FROM superstore
GROUP BY region
ORDER BY total_revenue DESC;
