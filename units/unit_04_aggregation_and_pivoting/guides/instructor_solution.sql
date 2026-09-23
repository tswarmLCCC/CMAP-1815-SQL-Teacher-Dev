-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 4: Summarization, Aggregation & Pivoting
-- Instructor Master Solution
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TASK 1: Departmental Headcount & Salary Distribution
-- ----------------------------------------------------------------------------
SELECT 
    department,
    COUNT(*) AS total_headcount,
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    MAX(salary) - MIN(salary) AS salary_range
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;


-- ----------------------------------------------------------------------------
-- TASK 2: Warehouse Inventory Valuation & Capital Risk Filter
-- ----------------------------------------------------------------------------
SELECT 
    category,
    COUNT(*) AS total_sku_count,
    SUM(stock_quantity) AS total_units_stocked,
    ROUND(SUM(stock_quantity * wholesale_cost), 2) AS inventory_valuation_cost,
    ROUND(SUM(stock_quantity * retail_price), 2) AS expected_retail_value
FROM products
WHERE is_discontinued = FALSE
GROUP BY category
HAVING SUM(stock_quantity) >= 100 
   AND SUM(stock_quantity * wholesale_cost) > 1000.00
ORDER BY inventory_valuation_cost DESC;


-- ----------------------------------------------------------------------------
-- TASK 3: Multi-Table Order Summary & Basket Analysis
-- ----------------------------------------------------------------------------
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    COUNT(ol.line_id) AS unique_items,
    SUM(ol.quantity) AS total_units_purchased,
    ROUND(SUM(ol.quantity * ol.unit_price), 2) AS order_subtotal
FROM orders o
JOIN order_lines ol ON o.order_id = ol.order_id
GROUP BY o.order_id, o.customer_id, o.order_date
HAVING SUM(ol.quantity * ol.unit_price) >= 150.00
ORDER BY order_subtotal DESC;


-- ----------------------------------------------------------------------------
-- TASK 4: Facility Staffing Reconciliation (Set Operations)
-- ----------------------------------------------------------------------------
SELECT location_id FROM locations
EXCEPT
SELECT DISTINCT location_id FROM employees WHERE location_id IS NOT NULL
ORDER BY location_id;

-- Business Insight Explanation:
-- Locations returned by this query represent corporate real estate assets
-- that currently have zero assigned staff. Management can evaluate these
-- facilities for sub-leasing, decommissioning, or priority hiring reallocations.


-- ----------------------------------------------------------------------------
-- TASK 5: Executive Regional Performance Matrix (Conditional Pivoting)
-- ----------------------------------------------------------------------------
SELECT 
    COALESCE(region, 'Unassigned') AS region,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN category = 'Furniture' THEN sales ELSE 0 END), 2) AS furniture_revenue,
    ROUND(SUM(CASE WHEN category = 'Office Supplies' THEN sales ELSE 0 END), 2) AS office_supplies_revenue,
    ROUND(SUM(CASE WHEN category = 'Technology' THEN sales ELSE 0 END), 2) AS technology_revenue,
    ROUND(
        100.0 * SUM(CASE WHEN category = 'Technology' THEN sales ELSE 0 END) / NULLIF(SUM(sales), 0),
        1
    ) AS tech_revenue_share_pct
FROM superstore
GROUP BY region
ORDER BY total_revenue DESC;
