/*
====================================================================
Module 3: Data Integration and Joins
File: week_3_joins_lab.sql
Focus: INNER JOIN, LEFT/RIGHT JOIN, Multiple Tables, and NULL tracking.
====================================================================
*/

/* 
--------------------------------------------------------------------
Part 1: Instructor Demonstration Queries
Use these during Periods 1 & 2 to explain join mechanics.
--------------------------------------------------------------------
*/

-- Demo 1: The Basic INNER JOIN (Matching records only)
-- Goal: Show employees alongside their physical work locations.
SELECT 
    e.first_name, 
    e.last_name, 
    e.department, 
    l.city, 
    l.state
FROM employees e
INNER JOIN locations l ON e.location_id = l.location_id;

-- Demo 2: The LEFT JOIN (Keeping unmatched records)
-- Goal: Show all locations, even if no employees are currently assigned there.
-- Note the NULL values that appear for employees in locations like Austin or Seattle.
SELECT 
    l.city, 
    l.facility_type, 
    e.first_name, 
    e.last_name
FROM locations l
LEFT JOIN employees e ON l.location_id = e.location_id;

-- Demo 3: Joining Three Tables
-- Goal: Connect a transaction header to its details, and then to the product name.
SELECT 
    o.order_id,
    o.order_date, 
    p.product_name, 
    ol.quantity
FROM orders o
INNER JOIN order_lines ol ON o.order_id = ol.order_id
INNER JOIN products p ON ol.product_id = p.product_id
WHERE o.order_id = 1;


/* 
--------------------------------------------------------------------
Part 2: Student Assessment (Data Integration Lab)
Periods 3 & 4 Independent Practice
--------------------------------------------------------------------
*/

-- 1. Write an INNER JOIN to connect orders to the employees who placed them. 
-- Display the order_date, status, and the employee's first and last name.
SELECT 
    o.order_date, 
    o.status, 
    e.first_name, 
    e.last_name
FROM orders o
INNER JOIN employees e ON o.employee_id = e.employee_id;

-- 2. Write an INNER JOIN to find out which locations hold 'Security' personnel.
-- Display the city, state, and employee last name.
SELECT 
    l.city, 
    l.state, 
    e.last_name
FROM employees e
INNER JOIN locations l ON e.location_id = l.location_id
WHERE e.department = 'Security';

-- 3. Join three tables: orders, order_lines, and products.
-- Display the order_date, product_name, quantity purchased, and unit_price.
SELECT 
    o.order_date, 
    p.product_name, 
    ol.quantity, 
    ol.unit_price
FROM orders o
INNER JOIN order_lines ol ON o.order_id = ol.order_id
INNER JOIN products p ON ol.product_id = p.product_id;

-- 4. Reconstruct the full sales receipt for Order #6.
-- You will need to join four tables: orders, employees, order_lines, and products.
-- Include the employee's last name, product name, quantity, and historical unit price.
SELECT 
    e.last_name, 
    p.product_name, 
    ol.quantity, 
    ol.unit_price
FROM orders o
INNER JOIN employees e ON o.employee_id = e.employee_id
INNER JOIN order_lines ol ON o.order_id = ol.order_id
INNER JOIN products p ON ol.product_id = p.product_id
WHERE o.order_id = 6;

-- 5. The "Missing Data" Audit: We need to find products that are sitting in the catalog 
-- but have NEVER been ordered. Write a LEFT JOIN between products and order_lines. 
-- Filter the results to only show rows where the order_line_id IS NULL.
SELECT 
    p.sku,
    p.product_name, 
    p.retail_price
FROM products p
LEFT JOIN order_lines ol ON p.product_id = ol.product_id
WHERE ol.order_line_id IS NULL;

-- 6. Location Audit: Write a LEFT JOIN to find out if we have any active employees 
-- who have NOT been assigned to a location_id. 
SELECT 
    e.first_name, 
    e.last_name, 
    e.title
FROM employees e
LEFT JOIN locations l ON e.location_id = l.location_id
WHERE l.location_id IS NULL AND e.is_active = TRUE;