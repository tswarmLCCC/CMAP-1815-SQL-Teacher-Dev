-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 5: Safe DML, Transaction Integrity & Temporary Tables
-- Instructor Master Solution
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TASK 1: Explicit Multi-Row Product Ingestion
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- TASK 2: Atomic Catalog Upsert (ON CONFLICT)
-- ----------------------------------------------------------------------------
INSERT INTO products (product_id, product_name, retail_price, stock_quantity)
VALUES (2, 'Premium Ballpoint Gel Pen (12-Pack)', 18.99, 200)
ON CONFLICT (product_id) 
DO UPDATE SET 
    product_name = EXCLUDED.product_name,
    retail_price = EXCLUDED.retail_price,
    stock_quantity = EXCLUDED.stock_quantity
RETURNING *;


-- ----------------------------------------------------------------------------
-- TASK 3: Safe Compensation Adjustment with Pre-Validation
-- ----------------------------------------------------------------------------

-- Step 1: Pre-validation inspection query
SELECT employee_id, first_name, last_name, department, salary
FROM employees
WHERE department = 'Operations' 
  AND is_active = TRUE 
  AND salary < 70000.00;

-- Step 2: Safe targeted update with RETURNING
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


-- ----------------------------------------------------------------------------
-- TASK 4: Transaction Sandbox & Safe Rollback Verification
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- TASK 5: Staging & Data Scrubbing Pipeline (TEMP TABLE)
-- ----------------------------------------------------------------------------

-- Step 1: Create isolated temporary staging table
CREATE TEMPORARY TABLE stage_partner_feed (
    raw_sku VARCHAR(50),
    raw_item_name VARCHAR(100),
    raw_price_str VARCHAR(50),
    raw_qty_str VARCHAR(50)
);

-- Step 2: Ingest unformatted vendor batch
INSERT INTO stage_partner_feed (raw_sku, raw_item_name, raw_price_str, raw_qty_str)
VALUES 
    ('PART-001', '  Industrial Label Maker  ', ' $79.99 ', ' 45 '),
    ('PART-002', 'Label Tape Cartridge 3-Pack', '$19.50', '200'),
    ('PART-ERR', 'Damaged Packaging Return', 'N/A', 'UNKNOWN');

-- Step 3: Scrub and cast staging data
SELECT 
    raw_sku,
    TRIM(raw_item_name) AS clean_item_name,
    CAST(REPLACE(TRIM(raw_price_str), '$', '') AS NUMERIC(10,2)) AS clean_retail_price,
    CAST(TRIM(raw_qty_str) AS INT) AS clean_stock_quantity
FROM stage_partner_feed
WHERE raw_price_str ~ '^\s*\$?[0-9]+(\.[0-9]+)?\s*$'
  AND raw_qty_str ~ '^\s*[0-9]+\s*$';

-- Promotion Protocol Comment:
-- Clean records are promoted into production using an atomic bulk insert:
-- INSERT INTO products (product_name, retail_price, stock_quantity)
-- SELECT TRIM(raw_item_name), CAST(REPLACE(TRIM(raw_price_str), '$', '') AS NUMERIC(10,2)), CAST(TRIM(raw_qty_str) AS INT)
-- FROM stage_partner_feed
-- WHERE raw_price_str ~ '^\s*\$?[0-9]+(\.[0-9]+)?\s*$' AND raw_qty_str ~ '^\s*[0-9]+\s*$';
