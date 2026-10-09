/* ============================================================================
   CMAP 1815: Introduction to Modern SQL
   MASTER INSTRUCTOR SOLUTIONS SUITE — ALL UNITS (1 TO 8)
   ============================================================================
   Author / Instructor: Trevor Swarm, LCCC
   Database Engine:     PostgreSQL 16 (GitHub Codespaces / Docker Sandbox)
   Target Database:     cmap1815 (or postgres)
   
   HOW TO USE THIS MASTER VERIFICATION SCRIPT:
   ----------------------------------------------------------------------------
   1. Initialize or reset your database using the master seed script:
      psql -U postgres -d cmap1815 -f datasets/setup_chap1.sql
      (or in terminal: ./reset_database.sh)
      
   2. You can execute this file section-by-section to walk through each lab,
      or run specific queries to check database outputs against student submissions.
      
   3. This script contains EVERY question/prompt asked of students in the 
      lab guides, paired directly with the official instructor solution query.
   ============================================================================ */

-- Defensive schema compatibility check (ensures clean runs on any database state)
DO $$
BEGIN
    -- Ensure products columns exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'products' AND column_name = 'wholesale_cost') THEN
        ALTER TABLE products ADD COLUMN wholesale_cost DECIMAL(10, 2);
        UPDATE products SET wholesale_cost = cost_to_produce;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'products' AND column_name = 'is_discontinued') THEN
        ALTER TABLE products ADD COLUMN is_discontinued BOOLEAN DEFAULT FALSE;
        UPDATE products SET is_discontinued = (discontinued_date IS NOT NULL);
    END IF;
    -- Ensure orders columns exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'orders' AND column_name = 'customer_id') THEN
        ALTER TABLE orders ADD COLUMN customer_id INT DEFAULT 101;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'orders' AND column_name = 'total_amount') THEN
        ALTER TABLE orders ADD COLUMN total_amount DECIMAL(10, 2) DEFAULT 0.00;
        UPDATE orders o SET total_amount = sub.sum_amt FROM (
            SELECT order_id, ROUND(SUM(quantity * unit_price), 2) AS sum_amt FROM order_lines GROUP BY order_id
        ) sub WHERE o.order_id = sub.order_id;
    END IF;
    -- Ensure order_lines line_id exists
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'order_lines' AND column_name = 'line_id') THEN
        ALTER TABLE order_lines ADD COLUMN line_id INT;
        UPDATE order_lines SET line_id = order_line_id;
    END IF;
END $$;


/* ============================================================================
   UNIT 1: SELECTION & RELATIONAL FUNDAMENTALS
   Lab: Data Exploration & Orientation
   ============================================================================ */

-- ----------------------------------------------------------------------------
-- Part 1: Environment & System Catalogs (20 Points)
-- ----------------------------------------------------------------------------

-- Prompt 1: Server Version
-- Write a query to display the exact version of PostgreSQL running on your server.
SELECT version();

-- Prompt 2: Current Session
-- Write a query to display your current active database user and the database name you are connected to.
SELECT current_user, current_database();

-- Prompt 3: Table Discovery
-- Query the information_schema.tables catalog to list all base table names in the 
-- public schema, sorted alphabetically by table name.
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name ASC;

-- Prompt 4: Column Inspector
-- Query information_schema.columns to find all column names and data types for the 
-- employees table, sorted by ordinal_position.
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'employees'
ORDER BY ordinal_position ASC;


-- ----------------------------------------------------------------------------
-- Part 2: Precision Projection & Data Exploration (40 Points)
-- ----------------------------------------------------------------------------

-- Prompt 5: Staff Directory
-- From the employees table, retrieve the first_name, last_name, and title. 
-- Sort alphabetically by last_name.
SELECT first_name, last_name, title
FROM employees
ORDER BY last_name ASC;

-- Prompt 6: Executive Compensation Roster
-- Retrieve the first_name, last_name, and salary of all employees. 
-- Sort from highest paid to lowest paid.
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC;

-- Prompt 7: Unique Departments
-- Write a query that returns a list of all distinct departments in the company, 
-- sorted alphabetically from A to Z.
SELECT DISTINCT department
FROM employees
ORDER BY department ASC;

-- Prompt 8: Department-Title Roster
-- Find all unique combinations of department and title across the company. 
-- Order by department first, then by title.
SELECT DISTINCT department, title
FROM employees
ORDER BY department ASC, title ASC;


-- ----------------------------------------------------------------------------
-- Part 3: Expressions, Aliases & Mathematical Projections (40 Points)
-- ----------------------------------------------------------------------------

-- Prompt 9: Polished Full Name
-- Write a query against employees that combines first_name and last_name into a 
-- single column aliased as full_name using string concatenation (||), along with 
-- their department. Sort by department ascending, then by full_name ascending.
SELECT 
    first_name || ' ' || last_name AS full_name,
    department
FROM employees
ORDER BY department ASC, full_name ASC;

-- Prompt 10: Bonus Simulation
-- Many employees receive an annual bonus. Write a query against employees displaying:
-- - last_name
-- - salary (aliased as base_salary)
-- - bonus (aliased as annual_bonus)
-- - A calculated column adding salary + bonus aliased as total_compensation.
-- Note: If bonus is NULL, the result of (salary + bonus) is NULL. This introduces Three-Valued Logic!
SELECT 
    last_name,
    salary AS base_salary,
    bonus AS annual_bonus,
    salary + bonus AS total_compensation
FROM employees;

-- Prompt 11: Retail Product Margins
-- From the products table, retrieve product_name, retail_price, cost_to_produce,
-- and a calculated column retail_price - cost_to_produce aliased as estimated_unit_profit.
-- Sort so the most profitable products appear first.
SELECT 
    product_name,
    retail_price,
    cost_to_produce,
    retail_price - cost_to_produce AS estimated_unit_profit
FROM products
ORDER BY estimated_unit_profit DESC;

-- Prompt 12: Inventory Value Analysis
-- From products, project product_name, stock_quantity, retail_price, and a calculated 
-- column stock_quantity * retail_price aliased as total_inventory_value.
-- Sort from highest inventory value to lowest.
SELECT 
    product_name,
    stock_quantity,
    retail_price,
    stock_quantity * retail_price AS total_inventory_value
FROM products
ORDER BY total_inventory_value DESC;



/* ============================================================================
   UNIT 2: TARGETED RETRIEVAL & THREE-VALUED LOGIC
   Lab: Targeted Retrieval & Logic Audits
   ============================================================================ */

-- ----------------------------------------------------------------------------
-- Part 1: Numerical Boundaries & Inclusive Ranges (25 Points)
-- ----------------------------------------------------------------------------

-- Prompt 1: Premium Inventory
-- Write a query against products retrieving product_name, retail_price, and 
-- stock_quantity for all items priced at or above $100.00. Sort from highest to lowest price.
SELECT product_name, retail_price, stock_quantity
FROM products
WHERE retail_price >= 100.00
ORDER BY retail_price DESC;

-- Prompt 2: Mid-Tier Catalog
-- Find all products whose retail_price is between $30.00 and $80.00 (inclusive). 
-- Display product_name, category, and retail_price. Sort by price ascending.
SELECT product_name, category, retail_price
FROM products
WHERE retail_price BETWEEN 30.00 AND 80.00
ORDER BY retail_price ASC;

-- Prompt 3: Critical Stock Alert
-- Management needs an urgent reorder list. Find all products where stock_quantity 
-- is strictly less than 25 units. Display product_name, stock_quantity, and category, 
-- sorted with the lowest inventory at the top.
SELECT product_name, stock_quantity, category
FROM products
WHERE stock_quantity < 25
ORDER BY stock_quantity ASC;


-- ----------------------------------------------------------------------------
-- Part 2: Categorical Sets & Pattern Matching (25 Points)
-- ----------------------------------------------------------------------------

-- Prompt 4: Key Departments Roster
-- Retrieve first_name, last_name, department, and salary for all employees who 
-- work in Research, Security, or Engineering. Sort by department alphabetically, 
-- then by salary descending.
SELECT first_name, last_name, department, salary
FROM employees
WHERE department IN ('Research', 'Security', 'Engineering')
ORDER BY department ASC, salary DESC;

-- Prompt 5: Non-Technical Staff
-- Find all employees who do NOT work in Security, Engineering, or Research. 
-- Project full_name (first and last concatenated) and department.
SELECT 
    first_name || ' ' || last_name AS full_name,
    department
FROM employees
WHERE department NOT IN ('Security', 'Engineering', 'Research')
ORDER BY department ASC;

-- Prompt 6: SKU Prefix Audit
-- Find all products whose sku starts with the prefix 'ELEC' using LIKE. 
-- Display sku, product_name, and retail_price.
SELECT sku, product_name, retail_price
FROM products
WHERE sku LIKE 'ELEC%'
ORDER BY sku ASC;

-- Prompt 7: Description Keyword Search
-- Find all products where description contains the word 'heavy' (case-insensitive) using ILIKE. 
-- Display product_name and description.
SELECT product_name, description
FROM products
WHERE description ILIKE '%heavy%';


-- ----------------------------------------------------------------------------
-- Part 3: Boolean Gates & Parentheses Discipline (25 Points)
-- ----------------------------------------------------------------------------

-- Prompt 8: Senior High-Earners
-- Find all employees who earn a salary of $80,000 or more AND were hired prior 
-- to January 1, 2018. Display first_name, last_name, salary, and hire_date.
SELECT first_name, last_name, salary, hire_date
FROM employees
WHERE salary >= 80000.00
  AND hire_date < '2018-01-01'
ORDER BY salary DESC;

-- Prompt 9: The Branch Security/Sales Filter
-- HR wants a list of staff in either Security OR Sales who also earn at least $60,000.
-- CRITICAL: Must use parentheses around the OR condition to prevent logic leakage!
SELECT last_name, department, salary
FROM employees
WHERE (department = 'Security' OR department = 'Sales')
  AND salary >= 60000.00
ORDER BY department ASC, salary DESC;

-- Prompt 10: Active Operations Exception
-- Find all employees who work in Operations AND whose is_active status is TRUE, 
-- but whose salary is strictly less than $60,000.
SELECT first_name, last_name, department, salary
FROM employees
WHERE department = 'Operations'
  AND is_active = TRUE
  AND salary < 60000.00;


-- ----------------------------------------------------------------------------
-- Part 4: The Mystery of NULL & Web Pagination (25 Points)
-- ----------------------------------------------------------------------------

-- Prompt 11: The Missing Bonus Report
-- Retrieve all employees whose bonus is currently missing (IS NULL). 
-- Display first_name, last_name, department, salary, and bonus. Order by salary descending.
SELECT first_name, last_name, department, salary, bonus
FROM employees
WHERE bonus IS NULL
ORDER BY salary DESC;

-- Prompt 12: Catalog Web Pagination (Page 2)
-- Simulate web pagination. Retrieve Page 2 of the product catalog where each page 
-- displays 5 products, ordered by retail_price descending. (Skip 5, take 5).
SELECT product_name, category, retail_price
FROM products
ORDER BY retail_price DESC
LIMIT 5 OFFSET 5;



/* ============================================================================
   UNIT 3: RELATIONAL JOINS & SET RELATIONSHIPS
   Lab: Multi-Table Relational Integration & Anomaly Audits
   ============================================================================ */

-- ----------------------------------------------------------------------------
-- Part 1: Two-Table INNER JOINs & Disambiguation (25 Points)
-- ----------------------------------------------------------------------------

-- Prompt 1: Staff Regional Roster
-- Join employees and locations. Retrieve first_name, last_name, title, and the 
-- city and state of their assigned location. Sort by state ASC, then last_name ASC.
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

-- Prompt 2: Headquarters Staff Directory (Wyoming Facilities)
-- Modify Challenge 1 to display only employees assigned to facilities in state 'WY'. 
-- Project full_name (combined), department, city, and facility_type.
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

-- Prompt 3: Order Ownership Audit
-- Join orders and employees. Retrieve order_id, order_date, status, and the full name 
-- of the employee who processed the order. Sort by order_date descending.
SELECT 
    o.order_id,
    o.order_date,
    o.status,
    e.first_name || ' ' || e.last_name AS processed_by
FROM orders o
INNER JOIN employees e 
    ON o.employee_id = e.employee_id
ORDER BY o.order_date DESC;


-- ----------------------------------------------------------------------------
-- Part 2: Multi-Table Transaction Reconstructions (30 Points)
-- ----------------------------------------------------------------------------

-- Prompt 4: Order Line Subtotals (3 Tables)
-- Join orders, order_lines, and products. Display:
-- - o.order_id, o.order_date, p.product_name, p.category, ol.quantity, ol.unit_price
-- - calculated column line_subtotal (ol.quantity * ol.unit_price)
-- Sort by order_id ascending, then line_subtotal descending.
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

-- Prompt 5: High-Value Item Sales
-- Filter the 3-table join for individual line items where line_subtotal > $150.00. 
-- Order from highest subtotal to lowest.
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

-- Prompt 6: Full Operational Audit Trail (4 Tables)
-- Trace transactions from the sales rep's physical office to the line item.
-- Join locations -> employees -> orders -> order_lines. 
-- Filter for orders with status = 'Completed'. Sort by order_id ascending.
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


-- ----------------------------------------------------------------------------
-- Part 3: Outer Joins & Data Loss Prevention (25 Points)
-- ----------------------------------------------------------------------------

-- Prompt 7: Complete Inventory Visibility (LEFT JOIN)
-- List ALL products alongside order line items using LEFT JOIN from products to order_lines.
-- Note NULL values for products that have never been purchased.
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

-- Prompt 8: Locations Staffing Overview (LEFT JOIN)
-- Show every facility in the company and any employees assigned to it using LEFT JOIN 
-- from locations to employees. Sort by city ascending.
SELECT 
    l.city,
    l.facility_type,
    e.first_name,
    e.last_name
FROM locations l
LEFT JOIN employees e 
    ON l.location_id = e.location_id
ORDER BY l.city ASC, e.last_name ASC;


-- ----------------------------------------------------------------------------
-- Part 4: Anomaly Audits via Anti-Joins (20 Points)
-- ----------------------------------------------------------------------------

-- Prompt 9: Dead Inventory Detection (The Anti-Join)
-- Find all products that have NEVER appeared in any customer order.
-- Project product_id, sku, product_name, stock_quantity, retail_price.
-- Order by stock_quantity descending to highlight tied-up warehouse capital.
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

-- Prompt 10: Unstaffed Facility Audit (The Anti-Join)
-- Find facilities that currently have zero employees assigned.
-- Display location_id, city, state, facility_type.
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



/* ============================================================================
   UNIT 4: SUMMARIZATION, AGGREGATION & PIVOTING
   Lab: Corporate Summarization & Executive Matrix Audit
   ============================================================================ */

-- Prompt 1: Departmental Headcount & Salary Distribution
-- From employees, group by department. Calculate total_headcount, avg_salary (rounded to 2),
-- min_salary, max_salary, and salary_range (max - min). Sort by avg_salary descending.
SELECT 
    department,
    COUNT(*) AS total_headcount,
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    MAX(salary) - MIN(salary) AS salary_range
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;

-- Prompt 2: Warehouse Inventory Valuation & Capital Risk Filter
-- From products, filter for active products only (is_discontinued = FALSE). Group by category.
-- Calculate: total_sku_count, total_units_stocked, inventory_valuation_cost (sum of stock_quantity * wholesale_cost),
-- and expected_retail_value (sum of stock_quantity * retail_price).
-- Use HAVING to filter categories where total_units_stocked >= 100 AND inventory_valuation_cost > 1000.00.
SELECT 
    category,
    COUNT(*) AS total_sku_count,
    SUM(stock_quantity) AS total_units_stocked,
    ROUND(SUM(stock_quantity * COALESCE(wholesale_cost, cost_to_produce)), 2) AS inventory_valuation_cost,
    ROUND(SUM(stock_quantity * retail_price), 2) AS expected_retail_value
FROM products
WHERE is_discontinued = FALSE
GROUP BY category
HAVING SUM(stock_quantity) >= 100 
   AND SUM(stock_quantity * COALESCE(wholesale_cost, cost_to_produce)) > 1000.00
ORDER BY inventory_valuation_cost DESC;

-- Prompt 3: Multi-Table Order Summary & Basket Analysis
-- Perform INNER JOIN between orders and order_lines. Group by order_id, customer_id, and order_date.
-- Calculate: unique_items (count of order lines), total_units_purchased, order_subtotal.
-- Filter with HAVING for orders with subtotal >= $150.00. Sort by subtotal descending.
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    COUNT(ol.order_line_id) AS unique_items,
    SUM(ol.quantity) AS total_units_purchased,
    ROUND(SUM(ol.quantity * ol.unit_price), 2) AS order_subtotal
FROM orders o
JOIN order_lines ol ON o.order_id = ol.order_id
GROUP BY o.order_id, o.customer_id, o.order_date
HAVING SUM(ol.quantity * ol.unit_price) >= 150.00
ORDER BY order_subtotal DESC;

-- Prompt 4: Facility Staffing Reconciliation (Set Operations)
-- Select all location_id from locations. Use EXCEPT to subtract all distinct location_id 
-- present in employees where location_id IS NOT NULL.
SELECT location_id FROM locations
EXCEPT
SELECT DISTINCT location_id FROM employees WHERE location_id IS NOT NULL
ORDER BY location_id;

-- Business Insight Explanation:
-- Facilities returned have zero assigned staff, alerting real estate management to sub-lease or repurpose.

-- Prompt 5: Executive Regional Performance Matrix (Conditional Pivoting)
-- Transform superstore transactional records into an executive matrix.
-- Group by region (COALESCE NULL to 'Unassigned'). Calculate total_orders, total_revenue,
-- furniture_revenue, office_supplies_revenue, technology_revenue (using CASE WHEN inside SUM),
-- and tech_revenue_share_pct (percentage of revenue from Technology, rounded to 1 decimal place).
SELECT 
    COALESCE(region, 'Unassigned') AS region,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN category = 'Furniture' THEN sales ELSE 0 END), 2) AS furniture_revenue,
    ROUND(SUM(CASE WHEN category = 'Office Supplies' THEN sales ELSE 0 END), 2) AS office_supplies_revenue,
    ROUND(SUM(CASE WHEN category = 'Technology' THEN sales ELSE 0 END), 2) AS technology_revenue,
    ROUND(
        100.0 * SUM(CASE WHEN category = 'Technology' THEN sales ELSE 0 END) / NULLIF(SUM(sales), 0),
        1
    ) AS tech_revenue_share_pct
FROM superstore
GROUP BY region
ORDER BY total_revenue DESC;



/* ============================================================================
   UNIT 5: SAFE DATA INGESTION, STAGING & MODIFICATION PROTOCOLS
   Lab: Safe Data Ingestion, Staging & Modification Protocols
   ============================================================================ */

-- Prompt 1: Explicit Multi-Row Product Ingestion
-- Write an INSERT INTO statement with explicit columns (product_name, category, 
-- retail_price, wholesale_cost, stock_quantity, is_discontinued) inserting 3 batch records.
-- Include RETURNING product_id, product_name, retail_price.
INSERT INTO products (
    product_name, 
    category, 
    retail_price, 
    wholesale_cost, 
    stock_quantity, 
    is_discontinued
) VALUES 
    ('Ergonomic High-Back Mesh Chair', 'Furniture', 249.99, 115.00, 25, FALSE),
    ('USB-C 10-in-1 Dual 4K Dock', 'Technology', 129.99, 58.00, 60, FALSE),
    ('Heavy-Duty Cable Conduit (25ft)', 'Office Supplies', 34.50, 12.00, 150, FALSE)
RETURNING product_id, product_name, retail_price;

-- Prompt 2: Atomic Catalog Upsert (ON CONFLICT)
-- Write an INSERT targeting product_id = 2 with ON CONFLICT (product_id) DO UPDATE SET:
-- Update retail_price and stock_quantity to EXCLUDED values. Use RETURNING *.
INSERT INTO products (product_id, product_name, retail_price, stock_quantity)
VALUES (2, 'Premium Ballpoint Gel Pen (12-Pack)', 18.99, 200)
ON CONFLICT (product_id) 
DO UPDATE SET 
    product_name = EXCLUDED.product_name,
    retail_price = EXCLUDED.retail_price,
    stock_quantity = EXCLUDED.stock_quantity
RETURNING *;

-- Prompt 3: Safe Compensation Adjustment with Pre-Validation
-- Corporate HR authorizes 5% salary increase for active Operations employees earning < $70,000.
-- Step 1: Pre-validation SELECT query
SELECT employee_id, first_name, last_name, department, salary
FROM employees
WHERE department = 'Operations' 
  AND is_active = TRUE 
  AND salary < 70000.00;

-- Step 2: Safe targeted UPDATE with RETURNING
UPDATE employees
SET salary = ROUND(salary * 1.05, 2)
WHERE department = 'Operations' 
  AND is_active = TRUE 
  AND salary < 70000.00
RETURNING 
    employee_id, 
    first_name, 
    last_name, 
    ROUND(salary / 1.05, 2) AS previous_salary,
    salary AS new_salary;

-- Prompt 4: Transaction Sandbox & Safe Rollback Verification
-- Verify an emergency purge routine using BEGIN and ROLLBACK.
BEGIN;

-- Check count before delete inside transaction
SELECT COUNT(*) AS count_before_delete FROM products WHERE is_discontinued = TRUE;

-- Delete discontinued records
DELETE FROM products
WHERE is_discontinued = TRUE;

-- Verify deletion inside transaction
SELECT COUNT(*) AS count_inside_transaction FROM products WHERE is_discontinued = TRUE;

-- Abort transaction to restore all rows
ROLLBACK;

-- Verify all records preserved outside transaction
SELECT COUNT(*) AS count_after_rollback FROM products WHERE is_discontinued = TRUE;

-- Prompt 5: Staging & Data Scrubbing Pipeline (TEMP TABLE)
-- Create temporary table stage_partner_feed, ingest 3 raw dirty rows, and write 
-- a cleaning SELECT query casting prices and quantities and filtering invalid rows via regex.
CREATE TEMPORARY TABLE stage_partner_feed (
    raw_sku VARCHAR(50),
    raw_item_name VARCHAR(100),
    raw_price_str VARCHAR(50),
    raw_qty_str VARCHAR(50)
);

INSERT INTO stage_partner_feed (raw_sku, raw_item_name, raw_price_str, raw_qty_str)
VALUES 
    ('PART-001', '  Industrial Label Maker  ', ' $79.99 ', ' 45 '),
    ('PART-002', 'Label Tape Cartridge 3-Pack', '$19.50', '200'),
    ('PART-ERR', 'Damaged Packaging Return', 'N/A', 'UNKNOWN');

SELECT 
    raw_sku,
    TRIM(raw_item_name) AS clean_item_name,
    CAST(REPLACE(TRIM(raw_price_str), '$', '') AS NUMERIC(10,2)) AS clean_retail_price,
    CAST(TRIM(raw_qty_str) AS INT) AS clean_stock_quantity
FROM stage_partner_feed
WHERE raw_price_str ~ '^\s*\$?[0-9]+(\.[0-9]+)?\s*$'
  AND raw_qty_str ~ '^\s*[0-9]+\s*$';



/* ============================================================================
   UNIT 6: ADVANCED ANALYTICS, CTES & WINDOW FUNCTIONS
   Lab: Advanced Analytics, CTEs & Deduplication Pipelines
   ============================================================================ */

-- Prompt 1: Refactoring Legacy Nested Subqueries into Modular CTEs
-- Refactor nested subquery into a Common Table Expression named active_dept_averages.
-- Filter in outer query for avg_salary > 65000.00 and sort descending.
WITH active_dept_averages AS (
    SELECT 
        department,
        COUNT(*) AS headcount,
        ROUND(AVG(salary), 2) AS avg_salary
    FROM employees
    WHERE is_active = TRUE
    GROUP BY department
)
SELECT 
    department,
    headcount,
    avg_salary
FROM active_dept_averages
WHERE avg_salary > 65000.00
ORDER BY avg_salary DESC;

-- Prompt 2: Individual Compensation Variance via Window Functions
-- Compare each employee's salary against their department average without collapsing rows.
-- Output dept_avg_salary, salary_variance (salary - dept_avg), and company_avg_salary.
SELECT 
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    ROUND(AVG(salary) OVER(PARTITION BY department), 2) AS dept_avg_salary,
    ROUND(salary - AVG(salary) OVER(PARTITION BY department), 2) AS salary_variance,
    ROUND(AVG(salary) OVER(), 2) AS company_avg_salary
FROM employees
ORDER BY department, salary_variance DESC;

-- Prompt 3: Top-N Departmental Earner Filter (CTE + Window Ranking)
-- Identify top 2 highest earners in each department using DENSE_RANK without skipping ranks.
WITH ranked_department_salaries AS (
    SELECT 
        employee_id,
        first_name,
        last_name,
        department,
        salary,
        DENSE_RANK() OVER(
            PARTITION BY department 
            ORDER BY salary DESC
        ) AS salary_rank
    FROM employees
)
SELECT 
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    salary_rank
FROM ranked_department_salaries
WHERE salary_rank <= 2
ORDER BY department, salary_rank;

-- Prompt 4: Cumulative Financial Ledger (Running Totals)
-- Calculate cumulative_revenue, running_order_count, and 3-order moving average from orders.
SELECT 
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER(
        ORDER BY order_date, order_id
    ) AS cumulative_revenue,
    COUNT(*) OVER(
        ORDER BY order_date, order_id
    ) AS running_order_count,
    ROUND(AVG(total_amount) OVER(
        ORDER BY order_date, order_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3_orders
FROM orders
ORDER BY order_date, order_id;

-- Prompt 5: Golden Record Deduplication Pattern
-- Isolate each customer's single most recent order using ROW_NUMBER() OVER(PARTITION BY customer_id).
WITH ranked_customer_orders AS (
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
FROM ranked_customer_orders
WHERE recency_rank = 1
ORDER BY customer_id;



/* ============================================================================
   UNIT 7: NORMALIZED SCHEMA DESIGN & CONSTRAINT ARCHITECTURE
   Lab: Normalized Schema Design & Constraint Architecture
   ============================================================================ */

-- Clean environment
DROP VIEW IF EXISTS v_active_trial_roster CASCADE;
DROP TABLE IF EXISTS trial_medications CASCADE;
DROP TABLE IF EXISTS clinical_trials CASCADE;
DROP TABLE IF EXISTS physicians CASCADE;
DROP TABLE IF EXISTS patients CASCADE;

-- Prompts 1, 2, 3: 3NF Relational Decomposition, DDL & Constraints
-- Implement 4 tables: patients, physicians, clinical_trials, trial_medications
-- Constraints: UNIQUE email, CHECK status IN (...), CHECK dosage not empty, ON DELETE RESTRICT & CASCADE

CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    patient_email VARCHAR(255) NOT NULL,
    patient_dob DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_patients_email UNIQUE (patient_email)
);

CREATE TABLE physicians (
    physician_id SERIAL PRIMARY KEY,
    physician_name VARCHAR(100) NOT NULL,
    physician_pager VARCHAR(20) NOT NULL,
    hospital_wing VARCHAR(50) NOT NULL
);

CREATE TABLE clinical_trials (
    trial_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    physician_id INT NOT NULL,
    start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    trial_status VARCHAR(20) NOT NULL DEFAULT 'Enrolled',
    CONSTRAINT fk_trials_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE RESTRICT,
    CONSTRAINT fk_trials_physician FOREIGN KEY (physician_id) REFERENCES physicians(physician_id) ON DELETE RESTRICT,
    CONSTRAINT chk_trials_status CHECK (trial_status IN ('Enrolled', 'Active', 'Completed', 'Withdrawn'))
);

CREATE TABLE trial_medications (
    trial_med_id SERIAL PRIMARY KEY,
    trial_id INT NOT NULL,
    drug_code VARCHAR(50) NOT NULL,
    drug_dosage VARCHAR(50) NOT NULL,
    CONSTRAINT fk_meds_trial FOREIGN KEY (trial_id) REFERENCES clinical_trials(trial_id) ON DELETE CASCADE,
    CONSTRAINT chk_meds_dosage_not_empty CHECK (LENGTH(TRIM(drug_dosage)) > 0)
);

-- Seed Sample Verification Data
INSERT INTO patients (patient_name, patient_email, patient_dob) VALUES 
('Sarah Connor', 'sconnor@cyberdyne.org', '1985-05-12'),
('Kyle Reese', 'kreese@resistance.net', '1990-11-23');

INSERT INTO physicians (physician_name, physician_pager, hospital_wing) VALUES 
('Dr. Peter Silberman', 'PAGER-801', 'Psychiatry Wing B'),
('Dr. Miles Dyson', 'PAGER-404', 'Advanced Technology Wing');

INSERT INTO clinical_trials (patient_id, physician_id, trial_status) VALUES 
(1, 1, 'Active'),
(2, 2, 'Enrolled');

INSERT INTO trial_medications (trial_id, drug_code, drug_dosage) VALUES 
(1, 'MED-902', '50mg daily'),
(1, 'MED-104', '10mg as needed'),
(2, 'MED-330', '100mg twice daily');

-- Prompt 4: Constraint Stress Testing Proof
-- Test 1 (Invalid Status):
-- INSERT INTO clinical_trials (patient_id, physician_id, trial_status) VALUES (1, 1, 'Terminated');
-- EXPECTED: violates check constraint "chk_trials_status"
-- Test 2 (Duplicate Email):
-- INSERT INTO patients (patient_name, patient_email, patient_dob) VALUES ('Sarah Imposter', 'sconnor@cyberdyne.org', '1992-01-01');
-- EXPECTED: duplicate key violates unique constraint "uq_patients_email"

-- Prompt 5: Security & Executive Reporting View
-- Analytical view joining 4 tables, active trials only, masking patient email/DOB for HIPAA compliance.
CREATE OR REPLACE VIEW v_active_trial_roster AS
SELECT 
    t.trial_id,
    p.patient_name,
    doc.physician_name,
    doc.hospital_wing,
    m.drug_code,
    m.drug_dosage
FROM clinical_trials t
JOIN patients p ON t.patient_id = p.patient_id
JOIN physicians doc ON t.physician_id = doc.physician_id
JOIN trial_medications m ON t.trial_id = m.trial_id
WHERE t.trial_status = 'Active';

SELECT * FROM v_active_trial_roster;



/* ============================================================================
   UNIT 8 & CAPSTONE: PERFORMANCE ENGINEERING & INDEXING DEFENSE
   Lab: Comprehensive Engineering & Performance Defense
   ============================================================================ */

-- Clean environment
DROP TABLE IF EXISTS shipment_audit_log CASCADE;
DROP TABLE IF EXISTS freight_shipments CASCADE;
DROP TABLE IF EXISTS logistics_hubs CASCADE;

-- Part 1: Schema Architecture & Declarative Integrity (3NF)
CREATE TABLE logistics_hubs (
    hub_id SERIAL PRIMARY KEY,
    hub_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE freight_shipments (
    shipment_id SERIAL PRIMARY KEY,
    hub_id INT NOT NULL REFERENCES logistics_hubs(hub_id) ON DELETE RESTRICT,
    tracking_code VARCHAR(50) NOT NULL UNIQUE,
    declared_value NUMERIC(10,2) NOT NULL CHECK (declared_value >= 0.00),
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'In Transit', 'Delivered', 'Cancelled')),
    shipped_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE shipment_audit_log (
    audit_id SERIAL PRIMARY KEY,
    shipment_id INT NOT NULL,
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    modified_by VARCHAR(50) NOT NULL DEFAULT CURRENT_USER,
    modified_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO logistics_hubs (hub_name, region) VALUES 
('Cheyenne Central Gateway', 'Mountain West'),
('Denver Cargo Facility', 'Mountain West'),
('Salt Lake Logistics Center', 'Mountain West'),
('Seattle Marine Freight', 'Pacific Northwest'),
('Portland Distribution Hub', 'Pacific Northwest');

-- Part 2: Safe Ingestion Pipeline via Temporary Staging Table
CREATE TEMPORARY TABLE stage_vendor_freight (
    raw_hub_id VARCHAR(20),
    raw_tracking VARCHAR(50),
    raw_value VARCHAR(50),
    raw_status VARCHAR(50)
);

INSERT INTO stage_vendor_freight (raw_hub_id, raw_tracking, raw_value, raw_status) VALUES 
('1', '  TRK-9001  ', ' $1250.50 ', 'In Transit'),
('2', 'TRK-9002', '$450.00', 'In Transit'),
('1', 'TRK-9003', '$3200.00', 'In Transit'),
('4', 'TRK-9004', ' $850.75 ', 'In Transit');

BEGIN;
INSERT INTO freight_shipments (hub_id, tracking_code, declared_value, status)
SELECT 
    CAST(TRIM(raw_hub_id) AS INT),
    TRIM(raw_tracking),
    CAST(REPLACE(TRIM(raw_value), '$', '') AS NUMERIC(10,2)),
    TRIM(raw_status)
FROM stage_vendor_freight
RETURNING shipment_id, tracking_code, declared_value, status;
COMMIT;

-- Part 3: Advanced Analytical Intelligence (CTEs & Windows)
WITH regional_shipment_metrics AS (
    SELECT 
        h.region,
        h.hub_name,
        COUNT(s.shipment_id) AS total_shipments,
        ROUND(COALESCE(SUM(s.declared_value), 0.00), 2) AS total_declared_value
    FROM logistics_hubs h
    LEFT JOIN freight_shipments s ON h.hub_id = s.hub_id
    GROUP BY h.region, h.hub_name
)
SELECT 
    region,
    hub_name,
    total_shipments,
    total_declared_value,
    DENSE_RANK() OVER(PARTITION BY region ORDER BY total_declared_value DESC) AS regional_rank,
    ROUND(AVG(total_declared_value) OVER(PARTITION BY region), 2) AS region_avg_value,
    ROUND(total_declared_value - AVG(total_declared_value) OVER(PARTITION BY region), 2) AS variance_from_reg_avg
FROM regional_shipment_metrics
ORDER BY region, regional_rank;

-- Part 4: Performance Profiling & B-Tree Index Engineering
-- Baseline query execution plan
EXPLAIN ANALYZE
SELECT shipment_id, tracking_code, declared_value
FROM freight_shipments
WHERE status = 'In Transit' AND shipped_date >= CURRENT_DATE;

-- Engineer composite B-Tree index
CREATE INDEX IF NOT EXISTS idx_shipments_status_date 
ON freight_shipments(status, shipped_date);

-- Post-index execution plan verification
EXPLAIN ANALYZE
SELECT shipment_id, tracking_code, declared_value
FROM freight_shipments
WHERE status = 'In Transit' AND shipped_date >= CURRENT_DATE;

-- Write Penalty Architecture Note:
-- Indexes accelerate read queries by maintaining balanced trees, but every INSERT, UPDATE,
-- and DELETE pays a Write Penalty to keep the index balanced. Drop unused indexes when
-- table write volume dominates read traffic.

-- Part 5: Transactional Audit Event Capture
BEGIN;
UPDATE freight_shipments
SET status = 'Delivered'
WHERE tracking_code = 'TRK-9001';

INSERT INTO shipment_audit_log (shipment_id, old_status, new_status)
VALUES (1, 'In Transit', 'Delivered');
COMMIT;

SELECT * FROM shipment_audit_log;

-- ============================================================================
-- END OF MASTER INSTRUCTOR SOLUTION SUITE (CMAP 1815)
-- ============================================================================
