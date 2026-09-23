# Unit 5 Assessment: Safe DML, Transactions & Temporary Tables Quiz

**Total Questions:** 15  
**Points Possible:** 30 (2 points per question)  
**Time Limit:** 30 Minutes  
**Format:** Multiple Choice & Code Analysis  
**Aligned Learning Outcomes:** CLO 4, Competencies 4.1–4.4

---

## Part 1: Conceptual Foundations & DML Semantics (Questions 1–5)

### Question 1
Why is writing an explicit column list (e.g. `INSERT INTO table (col1, col2) VALUES (...)`) strongly recommended over positional insertion (`INSERT INTO table VALUES (...)`)?
* A) Positional inserts run much slower because PostgreSQL must infer data types.
* B) Positional inserts break if new columns are added to the table or if existing column orders change in the schema.
* C) PostgreSQL deprecated positional inserts in version 12.
* D) Explicit column lists bypass all constraint validation checks.

---

### Question 2
What will happen if an `UPDATE` statement is executed without a `WHERE` clause?
* A) PostgreSQL displays a confirmation prompt asking the user to confirm the update.
* B) Only the first row in the table is updated.
* C) Every single row in the targeted table is updated.
* D) The query produces a syntax error because `WHERE` is mandatory on updates.

---

### Question 3
In PostgreSQL, what does the `EXCLUDED` pseudo-table represent inside an `ON CONFLICT DO UPDATE` clause?
* A) The existing row stored on disk that caused the conflict.
* B) The proposed new row values that were submitted in the `INSERT` statement.
* C) Rows that failed database constraint checks and were discarded.
* D) Records that have been archived to cold storage.

---

### Question 4
Which ACID property guarantees that either all SQL operations within a transaction complete successfully, or all changes are completely aborted and undone?
* A) Atomicity
* B) Consistency
* C) Isolation
* D) Durability

---

### Question 5
What is the lifecycle and visibility of a table created with `CREATE TEMPORARY TABLE`?
* A) It is visible to all database users and persists until explicitly dropped.
* B) It is visible only to the current user connection session and is automatically dropped when the session ends.
* C) It exists only for the duration of a single `SELECT` query.
* D) It is stored permanently in the server's cache directory.

---

## Part 2: Syntax Traps & Behavioral Analysis (Questions 6–10)

### Question 6
Examine the following code block:
```sql
BEGIN;
DELETE FROM products WHERE stock_quantity = 0;
ROLLBACK;
```
What is the final state of the `products` table after this block executes?
* A) All products with zero stock are permanently deleted.
* B) The table is dropped from the database.
* C) Zero rows are deleted; the table is in the exact state it was in prior to `BEGIN`.
* D) The table is converted to a temporary table.

---

### Question 7
Look at the following query:
```sql
UPDATE employees
SET salary = salary * 1.05
WHERE department = 'Research'
RETURNING employee_id, first_name, salary;
```
What is the purpose of the `RETURNING` clause here?
* A) It restores previous salary values if an error occurs.
* B) It projects the modified rows back to the client immediately without requiring a separate `SELECT` query.
* C) It writes the updated salaries to a log file on the database server.
* D) It rolls back the update after displaying the rows.

---

### Question 8
Consider this query:
```sql
INSERT INTO products (product_id, product_name, retail_price)
VALUES (42, 'Wireless Ergonomic Mouse', 59.99)
ON CONFLICT (product_id) DO NOTHING;
```
If a product with `product_id = 42` already exists in the table, what happens?
* A) The existing product's price is updated to $59.99.
* B) PostgreSQL throws a primary key violation error.
* C) The insert is silently ignored, no error is thrown, and existing data remains unchanged.
* D) A duplicate row with ID 42 is inserted.

---

### Question 9
Why does the following statement produce an error in PostgreSQL?
```sql
DELETE FROM employees e
WHERE e.department = 'Sales'
ORDER BY e.salary DESC;
```
* A) In SQL standard and PostgreSQL, `DELETE` does not support an `ORDER BY` clause.
* B) You cannot delete rows from the `employees` table.
* C) The table alias `e` is prohibited in `DELETE` statements.
* D) The `salary` column is protected by a foreign key constraint.

---

### Question 10
What is the recommended professional safety practice to perform immediately before running an `UPDATE` or `DELETE` query against a database?
* A) Restart the database server.
* B) Run a `SELECT` query with the identical `WHERE` condition to verify the exact rows and count of records that will be affected.
* C) Drop all indexes on the table to speed up the operation.
* D) Convert the target table to read-only mode.

---

## Part 3: Applied Scenario Calculations (Questions 11–15)

### Question 11
A table `accounts` has two rows:
* Account 1: Balance = $1,000
* Account 2: Balance = $500

A developer runs:
```sql
BEGIN;
UPDATE accounts SET balance = balance - 200 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 200 WHERE account_id = 2;
-- Connection suddenly crashes before COMMIT or ROLLBACK is issued!
```
When the database recovers and a new session connects, what will the balances be?
* A) Account 1: $800, Account 2: $700
* B) Account 1: $1,000, Account 2: $500
* C) Account 1: $800, Account 2: $500
* D) Both balances will be `NULL`

---

### Question 12
A products table has 5 items in category `'Office Supplies'`, 3 of which have `stock_quantity = 0`.  
A user runs:
```sql
DELETE FROM products
WHERE category = 'Office Supplies' AND stock_quantity = 0
RETURNING product_id;
```
How many rows will this command return in its result set?
* A) 0
* B) 2
* C) 3
* D) 5

---

### Question 13
An ETL engineer needs to populate a `dim_customers` table from an external file without stopping if a duplicate `customer_id` is encountered. Which construct achieves this?
* A) `INSERT INTO dim_customers ... ON DUPLICATE ESCAPE;`
* B) `INSERT INTO dim_customers ... ON CONFLICT (customer_id) DO NOTHING;`
* C) `INSERT INTO dim_customers ... IGNORE ALL;`
* D) `MERGE INTO dim_customers OVERWRITE;`

---

### Question 14
Look at the following query:
```sql
INSERT INTO products (product_name, category, retail_price)
SELECT product_name, category, sales / quantity
FROM superstore
WHERE quantity > 0;
```
What type of operation is this?
* A) A bulk insert that streams filtered and calculated rows from `superstore` directly into `products`.
* B) An update query that links `products` and `superstore` via a foreign key.
* C) A temporary table creation script.
* D) A recursive query that replaces the `products` table.

---

### Question 15
Why is a "Soft Delete" (setting `is_active = FALSE` or setting `deleted_at = CURRENT_TIMESTAMP`) often preferred in enterprise applications over a "Hard Delete" (`DELETE FROM table`)?
* A) Hard deletes require restarting the PostgreSQL service.
* B) Soft deletes preserve historical integrity, auditability, and avoid cascading foreign key deletion errors.
* C) Hard deletes can only be executed by superusers.
* D) Soft deletes take up zero bytes of disk space.

---

# Answer Key & Pedagogical Rationales

| Q# | Correct Answer | Rationale / Explanation |
| :---: | :---: | :--- |
| **1** | **B** | Schema evolution: adding or reordering columns causes positional inserts (`INSERT INTO table VALUES (...)`) to misalign data types and fail. Explicit column lists are resilient. |
| **2** | **C** | In declarative SQL, omitting `WHERE` applies the modification to the entire table. An unconstrained `UPDATE` modifies every row. |
| **3** | **B** | `EXCLUDED` contains the values from the `VALUES` clause that conflicted with the existing row, allowing you to update the target row with the incoming data. |
| **4** | **A** | **Atomicity** ensures an all-or-nothing outcome: if any statement in a transaction fails, all preceding statements in the block can be rolled back. |
| **5** | **B** | Temporary tables exist exclusively for the client session that created them and are automatically cleaned up when the connection terminates. |
| **6** | **C** | `ROLLBACK` completely reverses all mutations executed since the `BEGIN` statement, leaving the database unchanged. |
| **7** | **B** | `RETURNING` immediately outputs the affected rows to the client, providing real-time feedback and eliminating redundant verification queries. |
| **8** | **C** | `ON CONFLICT (col) DO NOTHING` catches uniqueness constraint violations and silently skips insertion without throwing an error. |
| **9** | **A** | PostgreSQL `DELETE` statements do not support `ORDER BY`. Deletion targets must be filtered via `WHERE` predicates. |
| **10** | **B** | The 3-Step Pre-Execution Protocol requires verifying the target set and row count via `SELECT` before issuing destructive commands. |
| **11** | **B** | Incomplete transactions that are not explicitly committed before a crash or disconnection are automatically rolled back by the database recovery process. |
| **12** | **C** | Only the 3 rows matching both criteria (`Office Supplies` and `stock_quantity = 0`) are deleted and returned. |
| **13** | **B** | `ON CONFLICT (customer_id) DO NOTHING` safely handles duplicate keys during ingestion by bypassing collisions. |
| **14** | **A** | `INSERT INTO ... SELECT` is SQL's bulk data pipeline mechanism, piping query results directly into a destination table. |
| **15** | **B** | Soft deletes maintain audit trails, allow records to be restored, and prevent foreign key violations in related child tables (e.g. order history). |
