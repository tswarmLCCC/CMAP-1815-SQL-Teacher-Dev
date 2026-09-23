-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 6: Query Modularity, CTEs & Window Functions
-- Script 3: Running Totals, Moving Averages & The Deduplication Pattern
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Cumulative Running Totals (Ordered Window Frames)
-- Calculating financial progression over time.
-- ----------------------------------------------------------------------------

-- Cumulative daily revenue tracking
SELECT 
    order_id,
    order_date,
    total_amount,
    -- Running total over time:
    SUM(total_amount) OVER(
        ORDER BY order_date, order_id
    ) AS cumulative_revenue,
    -- Running count of orders:
    COUNT(*) OVER(
        ORDER BY order_date, order_id
    ) AS running_order_count
FROM orders
ORDER BY order_date, order_id;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Moving Averages (Explicit Window Framing)
-- Smoothing out volatile transactional trends.
-- ----------------------------------------------------------------------------

SELECT 
    order_id,
    order_date,
    total_amount,
    -- 3-order moving average: current order + 2 prior orders
    ROUND(AVG(total_amount) OVER(
        ORDER BY order_date, order_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3_orders
FROM orders
ORDER BY order_date, order_id;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: The Golden Deduplication Pattern
-- Isolating the most recent or highest-priority record per entity.
-- ----------------------------------------------------------------------------

-- Scenario: Finding the most recent order placed by each customer
WITH customer_orders_ranked AS (
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
FROM customer_orders_ranked
WHERE recency_rank = 1
ORDER BY customer_id;
