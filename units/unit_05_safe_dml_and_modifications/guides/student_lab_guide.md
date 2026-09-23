# Unit 5 Student Lab Guide: Safe Data Ingestion, Staging & Modification Protocols

## Lab Overview
In this lab, you assume the role of Database Operations Engineer for Global Logistics & Supply. You are responsible for executing catalog expansions, performing targeted compensation updates, testing fail-safe rollbacks, and building an automated staging pipeline to scrub dirty vendor data before inserting it into production.

All work must be conducted in PostgreSQL 16.

---

## Deliverables & Submission Guidelines
1. Create a single script named `lab5_submission.sql`.
2. Adhere strictly to the SQL Style Guide: UPPERCASE keywords, snake_case identifiers.
3. Every modification (`UPDATE`, `DELETE`) must be preceded by a pre-validation `SELECT` query.
4. Test execution in `psql`:
   ```bash
   psql -U postgres -d postgres -f lab5_submission.sql
   ```

---

## Lab Tasks

### Task 1: Explicit Multi-Row Product Ingestion
Procurement has secured three new inventory items that must be inserted into the `products` table.
* **Requirements:**
  1. Write an `INSERT INTO` statement with an explicit column list:
     - `product_name`, `category`, `retail_price`, `wholesale_cost`, `stock_quantity`, `is_discontinued`.
  2. Insert the following 3 records in a single batch statement:
     * `'Ergonomic High-Back Mesh Chair'`, `'Furniture'`, `249.99`, `115.00`, `25`, `FALSE`
     * `'USB-C 10-in-1 Dual 4K Dock'`, `'Technology'`, `129.99`, `58.00`, `60`, `FALSE`
     * `'Heavy-Duty Cable Conduit (25ft)'`, `'Office Supplies'`, `34.50`, `12.00`, `150`, `FALSE`
  3. Include a `RETURNING product_id, product_name, retail_price` clause to verify the auto-generated primary keys.

### Task 2: Atomic Catalog Upsert (ON CONFLICT)
Vendor data feeds often include both new items and price/stock updates for existing items.
* **Requirements:**
  1. Write an `INSERT` statement targeting `product_id = 2` (or a known product in your database):
     - `product_name`: `'Premium Ballpoint Gel Pen (12-Pack)'`
     - `retail_price`: `18.99`
     - `stock_quantity`: `200`
  2. Implement `ON CONFLICT (product_id) DO UPDATE SET`:
     - Update `retail_price` to `EXCLUDED.retail_price`.
     - Update `stock_quantity` to `EXCLUDED.stock_quantity`.
  3. Use `RETURNING *` to display the resulting state of the row.

### Task 3: Safe Compensation Adjustment with Pre-Validation
Corporate HR has authorized a 5% bonus adjustment for all active employees in the `'Operations'` department earning less than `$70,000`.
* **Requirements:**
  1. **Pre-Validation:** Write a `SELECT` query that displays `employee_id`, `first_name`, `last_name`, `department`, and `salary` for this targeted group.
  2. **Safe Update:** Write an `UPDATE` statement that increases their `salary` by 5% (rounded to 2 decimal places).
  3. Use `RETURNING employee_id, first_name, salary AS new_salary` to audit the change.

### Task 4: Transaction Sandbox & Safe Rollback Verification
You must verify that an emergency purge routine works as expected without permanently destroying live data.
* **Requirements:**
  1. Start a transaction using `BEGIN;`.
  2. Execute a `DELETE` targeting all discontinued products (`is_discontinued = TRUE`).
  3. Run a `SELECT COUNT(*)` to verify the remaining count inside the transaction.
  4. Immediately abort the transaction using `ROLLBACK;`.
  5. Run a `SELECT COUNT(*)` outside the transaction to prove that all discontinued records were preserved.

### Task 5: Staging & Data Scrubbing Pipeline (TEMP TABLE)
A third-party partner provides a raw batch feed with unformatted currency symbols and extra whitespace.
* **Requirements:**
  1. Create a `CREATE TEMPORARY TABLE stage_partner_feed` with:
     - `raw_sku VARCHAR(50)`
     - `raw_item_name VARCHAR(100)`
     - `raw_price_str VARCHAR(50)`
     - `raw_qty_str VARCHAR(50)`
  2. Insert the following 3 dirty rows:
     * `('PART-001', '  Industrial Label Maker  ', ' $79.99 ', ' 45 ')`
     * `('PART-002', 'Label Tape Cartridge 3-Pack', '$19.50', '200')`
     * `('PART-ERR', 'Damaged Packaging Return', 'N/A', 'UNKNOWN')`
  3. Write a cleaning `SELECT` query that:
     - Trims whitespace from `raw_item_name`.
     - Removes `$` and trims `raw_price_str`, casting it to `NUMERIC(10,2)`.
     - Trims and casts `raw_qty_str` to `INT`.
     - Filters out non-numeric invalid rows using regex (`raw_price_str ~ '^\s*\$?[0-9]+(\.[0-9]+)?\s*$'`).
  4. Document with a comment how this cleaned staging data would be promoted into the live `products` table.
