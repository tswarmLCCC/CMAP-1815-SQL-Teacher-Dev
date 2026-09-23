-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 5: Safe DML, Transaction Integrity & Temporary Tables
-- Script 3: ACID Transactions & Temporary Staging Tables
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: ACID Transaction Blocks (BEGIN, COMMIT, ROLLBACK)
-- A transaction guarantees that multi-step operations execute atomically.
-- ----------------------------------------------------------------------------

-- 1.1 The ROLLBACK Time Machine: Simulating and catching a mistake
BEGIN;

-- Intentionally erroneous update (forgot WHERE clause!)
UPDATE employees
SET salary = 120000;

-- Inspect our disaster:
SELECT COUNT(*), AVG(salary) FROM employees;

-- Undo everything completely:
ROLLBACK;

-- Verify that our data was completely preserved:
SELECT MIN(salary), MAX(salary), ROUND(AVG(salary), 2) FROM employees;

-- 1.2 Multi-step transaction with successful COMMIT
BEGIN;

-- Step A: Deactivate an employee
UPDATE employees
SET is_active = FALSE
WHERE employee_id = 10;

-- Step B: Insert an audit log entry (sandbox table)
CREATE TABLE IF NOT EXISTS hr_audit_log (
    log_id SERIAL PRIMARY KEY,
    action_type VARCHAR(50),
    target_id INT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO hr_audit_log (action_type, target_id)
VALUES ('DEACTIVATE_EMPLOYEE', 10);

-- All steps succeeded, so permanently commit:
COMMIT;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Temporary Staging Tables (Data Engineering ETL)
-- CREATE TEMPORARY TABLE creates a private, fast, session-scoped scratchpad.
-- ----------------------------------------------------------------------------

-- 2.1 Create a temporary staging table for incoming dirty vendor data
CREATE TEMPORARY TABLE stage_vendor_catalog (
    raw_sku VARCHAR(50),
    raw_name VARCHAR(100),
    raw_price VARCHAR(50),
    raw_stock VARCHAR(50)
);

-- 2.2 Ingest raw dirty data
INSERT INTO stage_vendor_catalog (raw_sku, raw_name, raw_price, raw_stock)
VALUES 
    ('SKU-1001', '  Ergonomic Desk Mat  ', '$29.99', '150'),
    ('SKU-1002', 'USB-C Cable (6ft)', '14.50', '500'),
    ('SKU-1003', 'Mechanical Keyboard Red ', ' $89.00 ', ' 75 '),
    ('SKU-INVALID', 'Corrupt Record', 'N/A', 'UNKNOWN');

-- 2.3 Inspect raw staging table
SELECT * FROM stage_vendor_catalog;

-- 2.4 Clean and validate data inside the staging table
-- Remove dollar signs, trim whitespace, and validate numerical integrity
SELECT 
    raw_sku,
    TRIM(raw_name) AS clean_name,
    CAST(REPLACE(TRIM(raw_price), '$', '') AS NUMERIC(10,2)) AS clean_price,
    CAST(TRIM(raw_stock) AS INT) AS clean_stock
FROM stage_vendor_catalog
WHERE raw_price ~ '^\s*\$?[0-9]+(\.[0-9]+)?\s*$'
  AND raw_stock ~ '^\s*[0-9]+\s*$';

-- Clean records can now be safely inserted into production using INSERT INTO ... SELECT!
