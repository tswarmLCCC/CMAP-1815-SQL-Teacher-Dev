/*
====================================================================
Module 3: Data Integration and Joins
====================================================================
File: week_3_joins_lab.sql
Focus: INNER JOIN, LEFT/RIGHT JOIN, Multiple Tables, and NULL tracking.
====================================================================
*/

/* --- INSTRUCTOR DEMONSTRATION --- */

-- Demo 1: Basic INNER JOIN (Matching records only)
-- Show employees alongside their physical work locations.
SELECT e.first_name, e.last_name, e.department, l.city, l.state
FROM employees e
INNER JOIN locations l ON e.location_id = l.location_id;

-- Demo 2: LEFT JOIN (Keeping unmatched records)
-- Show all locations, even if no employees are currently assigned there.
SELECT l.city, l.facility_type, e.first_name, e.last_name
FROM locations l
LEFT JOIN employees e ON l.location_id = e.location_id;

/* --- STUDENT ASSESSMENT --- */

-- 1. Write an INNER JOIN to connect orders to employees. 
-- Display the order_date, status, employee first name, and last name.
SELECT o.order_date, o.status, e.first_name, e.last_name
FROM orders o
INNER JOIN employees e ON o.employee_id = e.employee_id;

-- 2. Join three tables: orders, order_lines, and products.
-- Display the order_date, product_name, quantity, and unit_price.
SELECT o.order_date, p.product_name, ol.quantity, ol.unit_price
FROM orders o
INNER JOIN order_lines ol ON o.order_id = ol.order_id
INNER JOIN products p ON ol.product_id = p.product_id;

-- 3. The "Missing Data" Audit: Write a LEFT JOIN to find products 
-- that have NEVER been ordered. (Hint: Look for NULLs in the right table).
SELECT p.product_name, p.sku
FROM products p
LEFT JOIN order_lines ol ON p.product_id = ol.product_id
WHERE ol.order_line_id IS NULL;

-- 4. Reconstruct the full sales receipt for Order #6.
-- Include employee name, location city, product name, quantity, and historical unit price.
SELECT e.last_name, l.city, p.product_name, ol.quantity, ol.unit_price
FROM orders o
INNER JOIN employees e ON o.employee_id = e.employee_id
INNER JOIN locations l ON e.location_id = l.location_id
INNER JOIN order_lines ol ON o.order_id = ol.order_id
INNER JOIN products p ON ol.product_id = p.product_id
WHERE o.order_id = 6;