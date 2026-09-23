-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 8: Query Performance, Indexing & Capstone Defense
-- In-Class Paired Coding Challenges
-- ============================================================================

-- ----------------------------------------------------------------------------
-- CHALLENGE 1: Plan Profiling Clinic with EXPLAIN ANALYZE (Session 1)
-- Scenario: The reporting dashboard is running slowly when filtering products.
-- Task:
-- 1. Profile the following query using EXPLAIN ANALYZE:
--    SELECT product_id, product_name, retail_price
--    FROM products
--    WHERE category = 'Technology' AND retail_price >= 100.00;
-- 2. Inspect the scan type and total execution time.
-- ----------------------------------------------------------------------------

EXPLAIN ANALYZE
SELECT product_id, product_name, retail_price
FROM products
WHERE category = 'Technology' AND retail_price >= 100.00;


-- ----------------------------------------------------------------------------
-- CHALLENGE 2: Targeted Composite Index Engineering (Session 1)
-- Task:
-- 1. Build a composite B-Tree index named idx_products_cat_price on (category, retail_price).
-- 2. Re-run the EXPLAIN ANALYZE statement from Challenge 1.
-- 3. Document the before/after cost and execution time in a SQL comment.
-- ----------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_products_cat_price 
ON products(category, retail_price);

EXPLAIN ANALYZE
SELECT product_id, product_name, retail_price
FROM products
WHERE category = 'Technology' AND retail_price >= 100.00;


-- ----------------------------------------------------------------------------
-- CHALLENGE 3: Audit Trail Schema & Event Capture (Session 1)
-- Scenario: Security requires tracking all price modifications on products.
-- Task:
-- 1. Create a table named product_price_audit:
--    audit_id SERIAL PRIMARY KEY,
--    product_id INT NOT NULL,
--    old_price NUMERIC(10,2),
--    new_price NUMERIC(10,2),
--    modified_by VARCHAR(50) DEFAULT CURRENT_USER,
--    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- 2. Execute a transaction that updates a product price and inserts a companion audit row.
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS product_price_audit (
    audit_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    old_price NUMERIC(10,2),
    new_price NUMERIC(10,2),
    modified_by VARCHAR(50) DEFAULT CURRENT_USER,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

BEGIN;

UPDATE products
SET retail_price = 159.99
WHERE product_id = 1
RETURNING product_id, retail_price;

INSERT INTO product_price_audit (product_id, old_price, new_price)
VALUES (1, 149.99, 159.99);

COMMIT;

SELECT * FROM product_price_audit;


-- ----------------------------------------------------------------------------
-- CHALLENGE 4: Capstone Cross-Review Checkpoint (Session 2)
-- Synthesizing a comprehensive analytical report:
-- Monthly revenue breakdown with moving 3-month average.
-- ----------------------------------------------------------------------------

WITH monthly_sales_summary AS (
    SELECT 
        DATE_TRUNC('month', order_date)::DATE AS order_month,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(total_amount), 2) AS monthly_revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    order_month,
    total_orders,
    monthly_revenue,
    SUM(monthly_revenue) OVER(ORDER BY order_month) AS cumulative_revenue,
    ROUND(AVG(monthly_revenue) OVER(
        ORDER BY order_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_3mo_avg
FROM monthly_sales_summary
ORDER BY order_month;
