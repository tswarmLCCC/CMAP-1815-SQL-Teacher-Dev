/*
====================================================================
CMAP 1815 - Unit 2: In-Class Active Learning Challenges
Session Hands-on Practice
====================================================================

Instructions:
Work with your assigned lab partner. Ensure all SQL keywords are 
in UPPERCASE, string literals are in single quotes, and OR conditions 
are guarded with parentheses.
*/

-- ==================================================================
-- CHALLENGE 1: Targeted Inventory Search
-- ==================================================================
-- A retail manager needs to audit warehouse stock.
-- Write a query against the 'products' table that retrieves:
--   1. product_name
--   2. category
--   3. retail_price
--   4. stock_quantity
-- Filter for products where:
--   - The retail price is between $30.00 and $150.00 (inclusive)
--   - AND the stock quantity is less than 50 units.
-- Order by stock_quantity ascending (lowest stock first).

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 2: HR Tenure & Name Search
-- ==================================================================
-- The HR director is planning a recognition event.
-- Find all employees who:
--   1. Were hired before January 1, 2018 (hire_date < '2018-01-01')
--   2. AND whose last name starts with the letter 'M' or 'D' (use LIKE / ILIKE)
-- Display their first name, last name, department, and hire date.
-- Sort by hire_date from oldest to newest.

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 3: The Missing Bonus Audit
-- ==================================================================
-- Management wants to identify full-time staff who did NOT receive 
-- an annual bonus, but earn a base salary of at least $60,000.
-- Write a query against 'employees' displaying:
--   - full_name (first and last combined)
--   - department
--   - salary
--   - bonus
-- Filter for bonus IS NULL and salary >= 60000.
-- Sort by salary descending.

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 4: Multi-Department High Earner Screen
-- ==================================================================
-- Retrieve all employees who:
--   - Work in either the 'Research' OR 'Engineering' departments
--   - AND earn an annual salary strictly greater than $90,000.
-- (CRITICAL: Make sure to wrap your OR condition in parentheses!)
-- Display first_name, last_name, department, and salary.
-- Sort by department alphabetically, then by salary descending.

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 5: Web Store Pagination Simulation
-- ==================================================================
-- You are writing the backend query for an e-commerce catalog page.
-- The user is viewing "Page 2" of the catalog.
-- Each page shows exactly 4 products per page.
-- Products must be sorted by retail_price from highest to lowest.
-- Write a query using LIMIT and OFFSET to return the 4 products for Page 2
-- (i.e. products ranked 5th through 8th in price).

-- [YOUR QUERY HERE]

