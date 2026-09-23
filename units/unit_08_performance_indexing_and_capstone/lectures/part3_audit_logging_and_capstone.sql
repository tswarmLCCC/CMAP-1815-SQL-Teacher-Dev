-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 8: Query Performance, Indexing & Capstone Defense
-- Script 3: Enterprise Audit Trails & Capstone Synthesis
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Enterprise Audit Logging Table
-- Creating immutable compliance logs for regulatory tracking.
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS enterprise_audit_trail (
    audit_id SERIAL PRIMARY KEY,
    entity_name VARCHAR(50) NOT NULL,
    operation_type VARCHAR(10) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    record_id INT NOT NULL,
    executed_by VARCHAR(50) NOT NULL DEFAULT CURRENT_USER,
    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    change_summary JSONB
);

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Capturing Audit Events Inside Transactions
-- Simulating a production state change with synchronous audit logging.
-- ----------------------------------------------------------------------------

BEGIN;

-- Step 1: Execute production state change
UPDATE products
SET retail_price = 89.99
WHERE product_id = 5;

-- Step 2: Record change in audit trail
INSERT INTO enterprise_audit_trail (
    entity_name, 
    operation_type, 
    record_id, 
    change_summary
) VALUES (
    'products',
    'UPDATE',
    5,
    '{"field": "retail_price", "old_value": 79.99, "new_value": 89.99}'::jsonb
);

-- Step 3: Atomic commit
COMMIT;

-- Verify the audit log
SELECT * FROM enterprise_audit_trail;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Complete Course Capstone Synthesis
-- A unified pipeline combining DDL, Constraints, Staging, CTEs, and Indexes.
-- ----------------------------------------------------------------------------

-- Checkpoint Query: Executive Performance Ledger with Window Metrics
WITH monthly_revenue AS (
    SELECT 
        DATE_TRUNC('month', order_date)::DATE AS sales_month,
        COUNT(order_id) AS order_volume,
        ROUND(SUM(total_amount), 2) AS monthly_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    sales_month,
    order_volume,
    monthly_sales,
    SUM(monthly_sales) OVER(ORDER BY sales_month) AS cumulative_annual_revenue,
    ROUND(AVG(monthly_sales) OVER(
        ORDER BY sales_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3_month_sales
FROM monthly_revenue
ORDER BY sales_month;
