---
marp: true
theme: default
paginate: true
header: "CMAP 1815: Introduction to Modern SQL"
footer: "Unit 5: Safe DML, Transaction Integrity & Temporary Tables"
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 40px;
    background-color: #fdfdfd;
  }
  h1 {
    color: #1a365d;
  }
  h2 {
    color: #2b6cb0;
  }
  .highlight {
    background-color: #fffaf0;
    border-left: 5px solid #dd6b20;
    padding: 10px;
    border-radius: 4px;
  }
  .danger {
    background-color: #fff5f5;
    border-left: 5px solid #e53e3e;
    padding: 10px;
    border-radius: 4px;
  }
  code {
    background-color: #edf2f7;
    color: #c53030;
    padding: 2px 6px;
    border-radius: 4px;
  }
---

# CMAP 1815: Introduction to Modern SQL
## Unit 5: Safe DML, Transaction Integrity & Temporary Tables

**Instructor:** Department of Computer Applications  
**Environment:** PostgreSQL 16 & GitHub Codespaces  
**Focus:** INSERT, UPDATE, DELETE, RETURNING, Transaction Control (ACID), and Staging via TEMP TABLEs

---

## The Danger Zone: From Read-Only to Modification

Up to now, every query was a `SELECT` statement:
* **Zero risk:** Reading data never destroys data.
* **Safe experimentation:** Errors just printed error messages.

<div class="danger">
<b>Starting Today:</b> DML commands (<code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>) permanently mutate data stored on disk. A single missing <code>WHERE</code> clause in an <code>UPDATE</code> or <code>DELETE</code> can overwrite or wipe out an entire production database!
</div>

**Our Professional Creed:** *Never execute a mutating query without a pre-validation protocol!*

---

## Video 5.1: The Anatomy of INSERT

Inserting rows into relational tables:

```sql
-- 1. Explicit Column Mapping (Best Practice!)
INSERT INTO products (product_name, category, retail_price, stock_quantity)
VALUES ('Ergonomic Mouse', 'Office Supplies', 49.99, 120);

-- 2. Multi-Row Insertion (Batch Loading)
INSERT INTO products (product_name, category, retail_price, stock_quantity)
VALUES 
    ('Mechanical Keyboard', 'Office Supplies', 89.99, 50),
    ('Ultra-Wide Monitor', 'Technology', 399.99, 25);

-- 3. Bulk Insert from Query (INSERT INTO ... SELECT)
INSERT INTO products (product_name, category, retail_price)
SELECT product_name, category, sales / quantity
FROM superstore
WHERE quantity > 0;
```

---

## Upsert: ON CONFLICT DO UPDATE

What happens when an inserted primary key or unique key already exists?

```sql
INSERT INTO products (product_id, product_name, retail_price)
VALUES (101, 'Upgraded Keyboard', 99.99)
ON CONFLICT (product_id) 
DO UPDATE SET 
    product_name = EXCLUDED.product_name,
    retail_price = EXCLUDED.retail_price;
```

* **`ON CONFLICT (col) DO NOTHING`**: Ignores duplicates safely.
* **`ON CONFLICT (col) DO UPDATE`**: Modifies existing record (**Upsert**).
* **`EXCLUDED`**: Represents the incoming row values attempting to insert.

---

## Video 5.2: Safe UPDATE & DELETE Workflows

<div class="danger">
<b>The Career-Ending Mistake:</b><br>
<code>UPDATE employees SET salary = 100000;</code> &nbsp;&nbsp;&nbsp;&nbsp;-- Every employee now makes $100k!<br>
<code>DELETE FROM employees;</code> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-- The entire company roster is wiped out!
</div>

### The 3-Step Professional Safety Protocol
1. **Step 1: Write a `SELECT` query first** with the exact `WHERE` clause to verify targeted rows.
2. **Step 2: Wrap the modification in a Transaction block** with `BEGIN`.
3. **Step 3: Verify row count, then `COMMIT`** (or `ROLLBACK` if row count is wrong!).

---

## The Power of the RETURNING Clause

PostgreSQL gives us instant feedback on what was changed:

```sql
-- 1. See what was deleted:
DELETE FROM products
WHERE is_discontinued = TRUE AND stock_quantity = 0
RETURNING product_id, product_name, wholesale_cost;

-- 2. See before-and-after values on update:
UPDATE employees
SET salary = salary * 1.05
WHERE department = 'Research'
RETURNING employee_id, first_name, last_name, salary AS new_salary;
```

* Eliminates the need to run a separate query after modification!
* Invaluable for application audit trails and real-time confirmations.

---

## Video 5.3: Transactions (ACID) & Temporary Staging Tables

### What is a Database Transaction?
A single logical unit of work that must succeed completely or fail completely:
* **A**tomicity: All-or-nothing execution.
* **C**onsistency: Maintains database constraints and rules.
* **I**solation: Concurrent queries do not see uncommitted data.
* **D**urability: Once committed, changes survive server crashes.

```sql
BEGIN; -- Opens transaction

UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;

-- If balance check succeeds:
COMMIT;

-- If something fails:
ROLLBACK;
```

---

## Staging & Data Engineering with TEMP TABLEs

When transforming dirty datasets, never manipulate live production tables directly:

```sql
-- Creates a private scratch table that automatically drops when session ends:
CREATE TEMPORARY TABLE stage_inventory (
    sku VARCHAR(50),
    raw_price VARCHAR(50),
    qty_text VARCHAR(50)
);

-- 1. Load dirty raw data into TEMP table
-- 2. Scrub, clean, and cast data types in TEMP table
-- 3. Move validated rows into production using INSERT INTO ... SELECT
-- 4. Session disconnects -> TEMP table disappears cleanly!
```

---

## Unit 5 Summary Checklist

1. Always specify column names explicitly in `INSERT INTO`.
2. Use `ON CONFLICT` to handle key collisions cleanly (Upsert).
3. **Never run `UPDATE` or `DELETE` without testing a `SELECT` first!**
4. Always wrap DML operations in `BEGIN ... COMMIT / ROLLBACK` during manual updates.
5. Use `RETURNING` to inspect affected rows immediately.
6. Use `CREATE TEMPORARY TABLE` as a safe sandbox for data cleaning pipelines.
