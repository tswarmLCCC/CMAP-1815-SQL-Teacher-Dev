/*
====================================================================
CMAP 1815 - Unit 3: Lecture Walkthrough Part 3
Topic: Outer Joins (LEFT/RIGHT) & The Anti-Join Anomaly Audit
Video Duration: ~8 minutes
====================================================================
*/

-- 1. The Blind Spot of INNER JOIN
-- Only returns products that have appeared in at least one order!
SELECT 
    p.product_id, 
    p.product_name, 
    ol.quantity
FROM products p
INNER JOIN order_lines ol 
    ON p.product_id = ol.product_id;

-- 2. The Comprehensive View: LEFT JOIN
-- Keeps 100% of products, filling order fields with NULL if unsold
SELECT 
    p.product_id, 
    p.product_name, 
    p.stock_quantity,
    ol.order_id, 
    ol.quantity
FROM products p
LEFT JOIN order_lines ol 
    ON p.product_id = ol.product_id
ORDER BY ol.order_id ASC NULLS FIRST;

-- 3. The Power of the ANTI-JOIN: Anomaly Detection
-- Isolates products that have NEVER been ordered (Dead Inventory Audit)
SELECT 
    p.product_id, 
    p.sku, 
    p.product_name, 
    p.stock_quantity,
    p.retail_price
FROM products p
LEFT JOIN order_lines ol 
    ON p.product_id = ol.product_id
WHERE ol.order_line_id IS NULL
ORDER BY p.stock_quantity DESC;

-- 4. Facilities Without Staff Audit
-- Find any location where zero employees are assigned
SELECT 
    l.location_id, 
    l.city, 
    l.state, 
    l.facility_type
FROM locations l
LEFT JOIN employees e 
    ON l.location_id = e.location_id
WHERE e.employee_id IS NULL;
