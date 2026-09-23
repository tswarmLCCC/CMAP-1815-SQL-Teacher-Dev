-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 5: Safe DML, Transaction Integrity & Temporary Tables
-- In-Class Paired Coding Challenges
-- ============================================================================

-- ----------------------------------------------------------------------------
-- CHALLENGE 1: Catalog Expansion & Upsert (Session 1)
-- Scenario: Procurement is onboarding a new line of ergonomic office equipment.
-- Task:
-- 1. Insert two new items into products:
--    - ('Ultra-Quiet Mechanical Keyboard', 'Office Supplies', 119.99, 55.00, 40)
--    - ('Ergonomic Split Wrist Rest', 'Office Supplies', 29.99, 11.00, 100)
-- 2. Then, write an Upsert statement for product_id = 1:
--    If product_id = 1 exists, update its retail_price to 29.99 and
--    stock_quantity to 300 using EXCLUDED.
-- ----------------------------------------------------------------------------

-- Step 1: Batch Insert
INSERT INTO products (product_name, category, retail_price, wholesale_cost, stock_quantity)
VALUES 
    ('Ultra-Quiet Mechanical Keyboard', 'Office Supplies', 119.99, 55.00, 40),
    ('Ergonomic Split Wrist Rest', 'Office Supplies', 29.99, 11.00, 100);

-- Step 2: Atomic Upsert
INSERT INTO products (product_id, product_name, retail_price, stock_quantity)
VALUES (1, 'Executive Ballpoint Pen', 29.99, 300)
ON CONFLICT (product_id) 
DO UPDATE SET 
    retail_price = EXCLUDED.retail_price,
    stock_quantity = EXCLUDED.stock_quantity;


-- ----------------------------------------------------------------------------
-- CHALLENGE 2: Targeted Compensation Adjustment with RETURNING (Session 1)
-- Scenario: HR is issuing a 6.5% cost-of-living increase to all active staff in
-- 'Operations' whose salary is currently under $65,000.
-- Task:
-- 1. Run a pre-validation SELECT to inspect eligible employees.
-- 2. Execute the UPDATE statement and use RETURNING to project:
--    employee_id, first_name, last_name, old salary, and new salary.
-- ----------------------------------------------------------------------------

-- Step 1: Pre-validation SELECT
SELECT employee_id, first_name, last_name, department, salary
FROM employees
WHERE department = 'Operations' 
  AND is_active = TRUE 
  AND salary < 65000.00;

-- Step 2: Safe UPDATE with RETURNING
UPDATE employees
SET salary = ROUND(salary * 1.065, 2)
WHERE department = 'Operations' 
  AND is_active = TRUE 
  AND salary < 65000.00
RETURNING 
    employee_id, 
    first_name, 
    last_name, 
    ROUND(salary / 1.065, 2) AS old_salary, 
    salary AS new_salary;


-- ----------------------------------------------------------------------------
-- CHALLENGE 3: Transaction Rollback Clinic (Session 2)
-- Scenario: Simulating a catastrophic mistake in a sandbox transaction.
-- Task:
-- 1. Begin a transaction.
-- 2. Delete all records from products where stock_quantity < 50.
-- 3. Verify the deletion inside the transaction.
-- 4. Roll back the transaction.
-- 5. Verify that zero records were permanently deleted.
-- ----------------------------------------------------------------------------

BEGIN;

DELETE FROM products
WHERE stock_quantity < 50;

SELECT COUNT(*) AS remaining_products FROM products;

ROLLBACK;

SELECT COUNT(*) AS total_products_after_rollback FROM products;


-- ----------------------------------------------------------------------------
-- CHALLENGE 4: Vendor Feed Staging & Scrubbing (Session 2)
-- Scenario: Ingesting messy product feeds from an external vendor.
-- Task:
-- 1. Create a TEMPORARY TABLE named stage_vendor_items with columns:
--    vendor_sku VARCHAR(50), raw_title VARCHAR(100), raw_price VARCHAR(50), raw_stock VARCHAR(50).
-- 2. Insert 3 messy rows:
--    ('V-101', '  Desk Lamp LED  ', '$34.95', '120')
--    ('V-102', 'Monitor Stand Wooden', '$45.00', ' 85 ')
--    ('V-ERR', 'Defective Part', 'UNKNOWN', 'N/A')
-- 3. Write a cleaning SELECT query that strips dollar signs, trims strings,
--    and filters out non-numeric prices.
-- ----------------------------------------------------------------------------

CREATE TEMPORARY TABLE stage_vendor_items (
    vendor_sku VARCHAR(50),
    raw_title VARCHAR(100),
    raw_price VARCHAR(50),
    raw_stock VARCHAR(50)
);

INSERT INTO stage_vendor_items (vendor_sku, raw_title, raw_price, raw_stock)
VALUES 
    ('V-101', '  Desk Lamp LED  ', '$34.95', '120'),
    ('V-102', 'Monitor Stand Wooden', '$45.00', ' 85 '),
    ('V-ERR', 'Defective Part', 'UNKNOWN', 'N/A');

SELECT 
    vendor_sku,
    TRIM(raw_title) AS clean_title,
    CAST(REPLACE(TRIM(raw_price), '$', '') AS NUMERIC(10,2)) AS clean_price,
    CAST(TRIM(raw_stock) AS INT) AS clean_stock
FROM stage_vendor_items
WHERE raw_price ~ '^\s*\$?[0-9]+(\.[0-9]+)?\s*$'
  AND raw_stock ~ '^\s*[0-9]+\s*$';
