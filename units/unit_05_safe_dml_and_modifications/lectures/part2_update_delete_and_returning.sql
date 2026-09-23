-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 5: Safe DML, Transaction Integrity & Temporary Tables
-- Script 2: Safe UPDATE, DELETE & The RETURNING Clause
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: The Pre-Execution SELECT Protocol
-- NEVER run an UPDATE or DELETE without testing the WHERE clause first!
-- ----------------------------------------------------------------------------

-- Step 1: Pre-validation query
SELECT employee_id, first_name, last_name, department, salary
FROM employees
WHERE department = 'Research' AND is_active = TRUE;

-- Step 2: Safe UPDATE targeting the exact verified population
UPDATE employees
SET salary = salary * 1.06
WHERE department = 'Research' AND is_active = TRUE;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: The RETURNING Clause on UPDATE
-- Real-time visual confirmation of changes made.
-- ----------------------------------------------------------------------------

-- Give active employees in Security a $2,500 cost-of-living adjustment
UPDATE employees
SET salary = salary + 2500.00
WHERE department = 'Security' AND is_active = TRUE
RETURNING 
    employee_id, 
    first_name, 
    last_name, 
    department, 
    salary - 2500.00 AS previous_salary,
    salary AS updated_salary;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Safe DELETE with RETURNING
-- Purging records safely with an instant audit trail.
-- ----------------------------------------------------------------------------

-- Step 1: Inspect what we intend to delete
SELECT archive_id, product_name, category
FROM product_archive
WHERE category = 'Furniture';

-- Step 2: Delete with RETURNING to capture the purged rows
DELETE FROM product_archive
WHERE category = 'Furniture'
RETURNING 
    archive_id, 
    product_name, 
    category, 
    CURRENT_TIMESTAMP AS deleted_at;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 4: Cascading Logic & Soft Deletes vs. Hard Deletes
-- Best Practice in modern software engineering: Soft Deletes
-- ----------------------------------------------------------------------------

-- Instead of permanently deleting a customer order (Hard Delete),
-- modern systems set a flag or timestamp (Soft Delete):
ALTER TABLE products ADD COLUMN IF NOT EXISTS archived_at TIMESTAMP;

-- Execute Soft Delete
UPDATE products
SET is_discontinued = TRUE,
    archived_at = CURRENT_TIMESTAMP
WHERE stock_quantity = 0 AND is_discontinued = FALSE
RETURNING product_id, product_name, is_discontinued, archived_at;
