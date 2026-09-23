/*
====================================================================
CMAP 1815 - Unit 3: In-Class Active Learning Challenges
Session Hands-on Practice
====================================================================

Instructions:
Work with your assigned lab partner. Ensure all SQL keywords are 
in UPPERCASE, table aliases are short and meaningful, and every projected 
column is explicitly prefixed (e.g. e.first_name, l.city).
*/

-- ==================================================================
-- CHALLENGE 1: Staff Facility Directory (2-Table INNER JOIN)
-- ==================================================================
-- Management needs a list of all employees and the facility details 
-- of their primary assignment.
-- Write a query joining 'employees' and 'locations' that displays:
--   - e.first_name, e.last_name
--   - e.department
--   - l.city
--   - l.state
--   - l.facility_type
-- Sort by l.state ascending, then by e.last_name ascending.

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 2: Order Revenue Itemization (3-Table INNER JOIN)
-- ==================================================================
-- Reconstruct detailed sales records by joining 'orders', 'order_lines', 
-- and 'products'.
-- Display:
--   - o.order_id
--   - o.order_date
--   - p.product_name
--   - ol.quantity
--   - ol.unit_price
--   - A calculated column 'item_subtotal' (quantity * unit_price)
-- Filter for orders placed in the year 2023 or later.
-- Sort by o.order_id ascending, then by item_subtotal descending.

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 3: Complete Product Catalog Audit (LEFT JOIN)
-- ==================================================================
-- The merchandising team wants to view ALL products, along with any 
-- order line items associated with them.
-- Use a LEFT JOIN from 'products' to 'order_lines'.
-- Display:
--   - p.product_id
--   - p.product_name
--   - p.stock_quantity
--   - ol.order_id
--   - ol.quantity
-- Notice which products return NULL for order_id and quantity!

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 4: Dead Inventory Anomaly Detection (The ANTI-JOIN)
-- ==================================================================
-- Find all products in our catalog that have NEVER been sold in an order.
-- Combine a LEFT JOIN with a WHERE clause checking for NULL.
-- Display:
--   - p.product_id
--   - p.sku
--   - p.product_name
--   - p.stock_quantity
--   - p.retail_price
-- Order by stock_quantity descending (identifying highest capital tied up).

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 5: Four-Table Executive Sales Trail
-- ==================================================================
-- Trace an order completely from sales rep facility to line item.
-- Join: locations -> employees -> orders -> order_lines
-- Display:
--   - o.order_id
--   - l.city AS sales_office_city
--   - e.last_name AS rep_last_name
--   - ol.quantity
--   - ol.unit_price
-- Filter for orders with status = 'Completed'.
-- Sort by o.order_id ASC.

-- [YOUR QUERY HERE]

