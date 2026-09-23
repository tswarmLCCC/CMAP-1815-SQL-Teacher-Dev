/*
====================================================================
CMAP 1815 - Unit 3: Instructor Solution Key
Lab: Multi-Table Relational Integration & Anomaly Audits
====================================================================
*/

-- ==================================================================
-- Part 1: Two-Table INNER JOINs & Disambiguation
-- ==================================================================

-- 1. Staff Regional Roster
SELECT 
    e.first_name, 
    e.last_name, 
    e.title, 
    l.city, 
    l.state
FROM employees e
INNER JOIN locations l 
    ON e.location_id = l.location_id
ORDER BY l.state ASC, e.last_name ASC;

-- 2. Headquarters Staff Directory (Wyoming Facilities)
SELECT 
    e.first_name || ' ' || e.last_name AS full_name,
    e.department,
    l.city,
    l.facility_type
FROM employees e
INNER JOIN locations l 
    ON e.location_id = l.location_id
WHERE l.state = 'WY'
ORDER BY e.department ASC, full_name ASC;

-- 3. Order Ownership Audit
SELECT 
    o.order_id,
    o.order_date,
    o.status,
    e.first_name || ' ' || e.last_name AS processed_by
FROM orders o
INNER JOIN employees e 
    ON o.employee_id = e.employee_id
ORDER BY o.order_date DESC;


-- ==================================================================
-- Part 2: Multi-Table Transaction Reconstructions
-- ==================================================================

-- 4. Order Line Subtotals (3 Tables)
SELECT 
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    ol.quantity,
    ol.unit_price,
    ol.quantity * ol.unit_price AS line_subtotal
FROM orders o
INNER JOIN order_lines ol 
    ON o.order_id = ol.order_id
INNER JOIN products p 
    ON ol.product_id = p.product_id
ORDER BY o.order_id ASC, line_subtotal DESC;

-- 5. High-Value Item Sales (> $150.00)
SELECT 
    o.order_id,
    o.order_date,
    p.product_name,
    ol.quantity,
    ol.unit_price,
    ol.quantity * ol.unit_price AS line_subtotal
FROM orders o
INNER JOIN order_lines ol 
    ON o.order_id = ol.order_id
INNER JOIN products p 
    ON ol.product_id = p.product_id
WHERE ol.quantity * ol.unit_price > 150.00
ORDER BY line_subtotal DESC;

-- 6. Full Operational Audit Trail (4 Tables)
SELECT 
    o.order_id,
    l.city AS sales_office_city,
    e.last_name AS employee_last_name,
    ol.quantity,
    ol.unit_price
FROM locations l
INNER JOIN employees e 
    ON l.location_id = e.location_id
INNER JOIN orders o 
    ON e.employee_id = o.employee_id
INNER JOIN order_lines ol 
    ON o.order_id = ol.order_id
WHERE o.status = 'Completed'
ORDER BY o.order_id ASC;


-- ==================================================================
-- Part 3: Outer Joins & Data Loss Prevention
-- ==================================================================

-- 7. Complete Inventory Visibility (LEFT JOIN)
SELECT 
    p.product_id,
    p.product_name,
    p.stock_quantity,
    ol.order_id,
    ol.quantity
FROM products p
LEFT JOIN order_lines ol 
    ON p.product_id = ol.product_id
ORDER BY p.product_id ASC;

-- 8. Locations Staffing Overview (LEFT JOIN)
SELECT 
    l.city,
    l.facility_type,
    e.first_name,
    e.last_name
FROM locations l
LEFT JOIN employees e 
    ON l.location_id = e.location_id
ORDER BY l.city ASC, e.last_name ASC;


-- ==================================================================
-- Part 4: Anomaly Audits via Anti-Joins
-- ==================================================================

-- 9. Dead Inventory Detection (The Anti-Join)
-- Teaching Note: ol.order_line_id IS NULL isolates products with zero sales lines!
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

-- 10. Unstaffed Facility Audit (The Anti-Join)
SELECT 
    l.location_id,
    l.city,
    l.state,
    l.facility_type
FROM locations l
LEFT JOIN employees e 
    ON l.location_id = e.location_id
WHERE e.employee_id IS NULL
ORDER BY l.location_id ASC;
