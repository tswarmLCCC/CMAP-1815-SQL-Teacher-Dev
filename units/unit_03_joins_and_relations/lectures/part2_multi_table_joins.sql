/*
====================================================================
CMAP 1815 - Unit 3: Lecture Walkthrough Part 2
Topic: Multi-Table Joins & The Cartesian Product Disaster
Video Duration: ~8 minutes
====================================================================
*/

-- 1. Chaining 3 Tables: orders -> order_lines -> products
-- Reconstruct customer transactions with full product details
SELECT 
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    ol.quantity,
    ol.unit_price,
    ol.quantity * ol.unit_price AS line_item_total
FROM orders o
INNER JOIN order_lines ol 
    ON o.order_id = ol.order_id
INNER JOIN products p 
    ON ol.product_id = p.product_id
ORDER BY o.order_id ASC, ol.line_item_total DESC;

-- 2. Chaining 4 Tables: Adding Employee Sales Rep Info
-- locations -> employees -> orders -> order_lines
SELECT 
    o.order_id,
    o.order_date,
    e.first_name || ' ' || e.last_name AS sales_rep,
    l.city AS sales_office_city,
    ol.quantity,
    ol.unit_price
FROM orders o
INNER JOIN employees e 
    ON o.employee_id = e.employee_id
INNER JOIN locations l 
    ON e.location_id = l.location_id
INNER JOIN order_lines ol 
    ON o.order_id = ol.order_id
ORDER BY o.order_id ASC;

-- 3. [DEMO TRAP: The Cartesian Disaster (CROSS JOIN)]
-- Notice what happens if you forget the ON clause in old-style joins:
-- SELECT count(*) FROM employees, locations;
-- Returns 26 * 8 = 208 rows instead of 26!
