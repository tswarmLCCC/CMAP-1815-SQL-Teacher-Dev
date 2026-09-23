# Unit 5: Instructor Lecture Notes & Pedagogical Guide

## Module Overview & Objectives
Unit 5 represents the critical transition in database systems education: moving from **declarative read operations (`SELECT`)** to **destructive state modification (`INSERT`, `UPDATE`, `DELETE`)**. The core instructional imperative is instilling **defensive data engineering habits**: pre-execution validation queries, ACID transaction containment, automated change inspection with `RETURNING`, and isolated data staging via `TEMP TABLE`s.

### Aligned Course Learning Outcomes
* **CLO 4:** Execute safe data manipulation operations (`INSERT`, `UPDATE`, `DELETE`), manage transactions, and stage data transformations using temporary tables.
* **CLO 3:** Translate real-world business requirements into verified, robust database workflows.

---

## 1. Pedagogical Roadmap & Common Student Traps

### A. The "Runaway Mutation" Risk
* **The Concept:** SQL was designed with declarative semantics. A command like `DELETE FROM employees;` has valid syntax, so the database will happily execute it and truncate the entire table without prompt.
* **Student Trap 1: Forgetting the WHERE clause on UPDATE/DELETE.**
  *Teaching Remedy:* Drill the **3-Step Pre-Execution Protocol**:
  1. Write `SELECT * FROM table WHERE condition;`
  2. Inspect matching rows and check count.
  3. Replace `SELECT *` with `DELETE` or `UPDATE table SET ...`
* **Student Trap 2: Omission of Column Lists on INSERT.**
  Students often write `INSERT INTO products VALUES (1, 'Widget', ...);`. Emphasize that schema evolution (adding a column) breaks positional inserts. Require explicit column declarations at all times.

### B. Transaction Management (ACID)
* **The Concept:** A transaction is an atomic sandbox (`BEGIN ... COMMIT / ROLLBACK`).
* **Teaching Tip:** Conduct a live "disaster simulation" in class:
  1. Open a transaction: `BEGIN;`
  2. Execute an intentionally flawed query: `DELETE FROM employees WHERE department = 'Sales';`
  3. Show the empty table: `SELECT COUNT(*) FROM employees;`
  4. Type `ROLLBACK;` and show that all records were restored unharmed!
  This demo creates an indelible emotional impression on students regarding the protective power of transactions.

### C. Upsert Semantics (ON CONFLICT)
* **The Concept:** Traditional databases required two round-trips: a `SELECT` to see if a record existed, followed by an `INSERT` or `UPDATE`.
* **PostgreSQL Innovation:** `ON CONFLICT (target_column) DO UPDATE SET ...` allows atomic upserts without race conditions. Introduce the `EXCLUDED` pseudo-table representing incoming row values.

### D. Staging Pipelines via Temporary Tables
* **The Concept:** Professional ETL (Extract, Transform, Load) processes ingest raw data into temporary tables before moving clean records into production tables.
* **Key Properties:**
  * Created with `CREATE TEMPORARY TABLE ...` (or `CREATE TEMP TABLE ...`).
  * Visible only to the current database session.
  * Automatically dropped when the session disconnects.
  * Completely bypasses write contention on production tables.

---

## 2. In-Class Live Coding & Demonstration Script

### Demo 1: The Explicit INSERT & Upsert (`part1_insert_and_copy.sql`)
1. Demonstrate positional insert failure vs. explicit column insert success.
2. Demonstrate `INSERT INTO ... SELECT` bulk migration from `superstore`.
3. Demonstrate `ON CONFLICT (product_id) DO UPDATE SET ...` using `EXCLUDED.price`.

### Demo 2: Safe UPDATE, DELETE & RETURNING (`part2_update_delete_and_returning.sql`)
1. Demonstrate the 3-step safety check before modifying salaries.
2. Run an `UPDATE` with `RETURNING employee_id, first_name, salary AS new_salary`.
3. Run a `DELETE` with `RETURNING *` to display purged records in real-time.

### Demo 3: ACID Transactions & Temp Staging (`part3_transactions_and_temp_tables.sql`)
1. Execute `BEGIN`, make changes, inspect, and then run `ROLLBACK`.
2. Create a `TEMP TABLE stage_products`, load dirty data, perform string cleaning, and promote clean rows to `products`.

---

## 3. Formative Check Questions (Think-Pair-Share)
1. *What happens to unmentioned columns when you run `INSERT INTO table (col_a) VALUES ('val');`?*
   * Answer: They are populated with their column default values, or `NULL` if no default is declared.
2. *If you execute an `UPDATE` statement inside a transaction and your computer loses power before you type `COMMIT`, what state is the database in when it reboots?*
   * Answer: The database automatically rolls back to the pre-transaction state, ensuring data consistency (Atomicity).
