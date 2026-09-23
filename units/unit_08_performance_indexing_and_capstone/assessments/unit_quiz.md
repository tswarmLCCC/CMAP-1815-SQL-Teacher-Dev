# Unit 8 Assessment: Performance Tuning, Indexing & Capstone Quiz

**Total Questions:** 15  
**Points Possible:** 30 (2 points per question)  
**Time Limit:** 30 Minutes  
**Format:** Multiple Choice & Code Analysis  
**Aligned Learning Outcomes:** CLO 6, Competencies 6.1–6.4

---

## Part 1: Conceptual Foundations & Execution Plans (Questions 1–5)

### Question 1
What is the fundamental operational difference between running `EXPLAIN` and running `EXPLAIN ANALYZE` on a SQL statement?
* A) `EXPLAIN` optimizes the query, while `EXPLAIN ANALYZE` drops the table.
* B) `EXPLAIN` only displays the query planner's estimated cost and plan without executing the query, whereas `EXPLAIN ANALYZE` actually executes the query to measure real runtime and row counts.
* C) `EXPLAIN` is for `SELECT` queries only, while `EXPLAIN ANALYZE` is for `INSERT` statements.
* D) `EXPLAIN ANALYZE` runs in the cloud, while `EXPLAIN` runs locally.

---

### Question 2
What is a **Sequential Scan (`Seq Scan`)** in PostgreSQL?
* A) A fast search that jumps directly to the matching row using a B-Tree pointer.
* B) A brute-force traversal where the database reads every single physical block of the table from beginning to end.
* C) A query that processes only even-numbered rows.
* D) An asynchronous background index rebuild.

---

### Question 3
Under what condition is a Sequential Scan typically faster and preferred by the PostgreSQL query planner over an Index Scan?
* A) When the table has more than 100 million rows.
* B) When the table is very small (fitting entirely on 1 or 2 disk pages) or when the query retrieves a large percentage of the table (>25%).
* C) When the column contains encrypted text.
* D) Sequential scans are never preferred over index scans.

---

### Question 4
What is the **Write Penalty** in database indexing?
* A) A monetary fine imposed by cloud providers when tables exceed 1 GB.
* B) The performance overhead incurred during `INSERT`, `UPDATE`, and `DELETE` operations because all indexes on a table must be synchronously updated alongside the physical data heap.
* C) An error that occurs when writing to a read-only replica.
* D) The time it takes to compile a `CREATE TABLE` statement.

---

### Question 5
What data structure is used by default when you run `CREATE INDEX` in PostgreSQL?
* A) Hash Table
* B) B-Tree (Balanced Tree)
* C) Linked List
* D) Binary Heap

---

## Part 2: Syntax Traps & Indexing Engineering (Questions 6–10)

### Question 6
Look at the following index definition:
```sql
CREATE INDEX idx_emp_dept_salary ON employees(department, salary);
```
Which of the following queries will be able to utilize this composite index most effectively?
* A) `SELECT * FROM employees WHERE salary > 80000;`
* B) `SELECT * FROM employees WHERE department = 'Research' AND salary > 80000;`
* C) `SELECT * FROM employees WHERE hire_date > '2023-01-01';`
* D) `SELECT * FROM employees WHERE first_name = 'Alice';`

---

### Question 7
In the composite index `(department, salary)`, why does a query filtering solely on `WHERE salary > 80000` fail to utilize the index efficiently?
* A) `salary` is an unsupported data type for B-Trees.
* B) The index is sorted first by the leading column (`department`). Without a filter on the leading column, PostgreSQL cannot jump directly to a subtree.
* C) Composite indexes can only be used by `JOIN` statements.
* D) B-Trees do not support range comparisons like `>`.

---

### Question 8
What is a **Partial Index** in PostgreSQL?
* A) An index that stores only the first 5 characters of a string column.
* B) An index built with a `WHERE` clause that indexes only rows satisfying a specific condition, saving disk space and reducing write penalty.
* C) An index that is half-completed and corrupted.
* D) An index that only indexes primary keys.

---

### Question 9
Examine the following DDL statement:
```sql
CREATE INDEX idx_active_orders ON orders(order_date) WHERE order_status = 'Pending';
```
When will PostgreSQL's query optimizer consider using this index?
* A) For any query on `orders`, regardless of `WHERE` conditions.
* B) Only for queries that explicitly filter on `WHERE order_status = 'Pending'`.
* C) Only when deleting rows from `orders`.
* D) Only when `orders` is joined to `customers`.

---

### Question 10
Look at this output snippet from `EXPLAIN ANALYZE`:
```
Index Only Scan using idx_cust_email on customers  (cost=0.15..8.17 rows=1 width=32)
```
What makes an **Index Only Scan** faster than a regular **Index Scan**?
* A) It avoids reading data from the main table heap pages entirely, because all required projected columns are satisfied directly from the index leaf nodes.
* B) It runs in RAM without using CPU cycles.
* C) It bypasses all database security checks.
* D) It only returns the first letter of each column.

---

## Part 3: Applied Architecture & Capstone Synthesis (Questions 11–15)

### Question 11
A high-throughput e-commerce database processes 2,000 order insertions per second. A junior developer adds 12 separate single-column indexes to the `orders` table to speed up ad-hoc analytics. What is the most likely consequence?
* A) Read queries will become 10 times slower.
* B) Order insertion and checkout throughput will drop significantly due to massive write amplification and lock contention across the 12 indexes.
* C) PostgreSQL will automatically convert the table to unlogged mode.
* D) All primary key constraints will be disabled.

---

### Question 12
An enterprise database tracks customer profile changes for legal compliance. Which architectural design provides an immutable audit trail?
* A) Overwriting previous customer records in place using `UPDATE`.
* B) A dedicated `audit_log` table populated inside the same transaction with timestamps, user session metadata, action types, and before/after values.
* C) Writing changes to a temporary scratchpad table that drops upon disconnect.
* D) Relying on the server's crash log.

---

### Question 13
An analytical query running on a 10-million row `transactions` table contains:
`WHERE transaction_date >= '2024-01-01' AND account_id = 9482`
Assuming `account_id` has high selectivity (each account has ~20 rows), how should a composite index be ordered for maximum efficiency?
* A) `(transaction_date, account_id)`
* B) `(account_id, transaction_date)` (Equality filter column first, followed by range filter column)
* C) The column order in a composite index has no effect on performance.
* D) Indexes cannot contain both dates and integers.

---

### Question 14
Which view in PostgreSQL allows a database administrator to inspect how many times each user index has been scanned in production?
* A) `pg_stat_user_indexes`
* B) `pg_all_indexes_view`
* C) `information_schema.indexes`
* D) `pg_index_catalog`

---

### Question 15
In the context of the Course Capstone, which sequence represents the professional lifecycle of relational database development?
* A) Write queries $\rightarrow$ Guess indexes $\rightarrow$ Build tables $\rightarrow$ Normalize data
* B) Domain modeling & 3NF Normalization $\rightarrow$ DDL Schema with declarative constraints $\rightarrow$ Data Ingestion & Staging $\rightarrow$ Analytical Reporting (CTEs/Windows) $\rightarrow$ Profiling (`EXPLAIN`) & Index Tuning
* C) Load raw data into production $\rightarrow$ Add constraints later $\rightarrow$ Drop primary keys $\rightarrow$ Run `SELECT *`
* D) Build frontend $\rightarrow$ Let the ORM generate random tables $\rightarrow$ Never optimize

---

# Answer Key & Pedagogical Rationales

| Q# | Correct Answer | Rationale / Explanation |
| :---: | :---: | :--- |
| **1** | **B** | `EXPLAIN` displays static optimizer estimates. `EXPLAIN ANALYZE` executes the statement and captures actual runtime in milliseconds and true row counts. |
| **2** | **B** | A Sequential Scan inspects every disk page and tuple in the table heap sequentially from start to finish. |
| **3** | **B** | When a table fits in a couple of pages or a query fetches a massive percentage of rows, sequential I/O is faster than index pointer lookups. |
| **4** | **B** | The Write Penalty is the cumulative performance hit on mutating queries (`INSERT`, `UPDATE`, `DELETE`) caused by maintaining multiple index structures. |
| **5** | **B** | The default index type in PostgreSQL is the Balanced Tree (B-Tree), providing $O(\log N)$ search complexity for equality and range queries. |
| **6** | **B** | B-Tree composite indexes require filtering on the leading column (`department`) to navigate the tree structure effectively. |
| **7** | **B** | Without a predicate on the leading column (`department`), the optimizer cannot traverse the hierarchical branches of the composite B-Tree. |
| **8** | **B** | A Partial Index includes a `WHERE` predicate, indexing only rows meeting the criteria, saving disk storage and write overhead. |
| **9** | **B** | Partial indexes can only be used when a query's `WHERE` clause matches or subsumes the partial index predicate. |
| **10** | **A** | An Index Only Scan satisfies the entire projection from the index leaves, eliminating expensive visits to the physical table heap. |
| **11** | **B** | Excessive indexing severely throttles write throughput: every insert must update 12 B-Trees on disk, saturating storage I/O. |
| **12** | **B** | Enterprise compliance requires immutable audit tables recording timestamp, user ID, operation type, and modified payloads within ACID transactions. |
| **13** | **B** | Best practice for composite indexes: place equality filter columns first (`account_id`), followed by range/inequality columns (`transaction_date`). |
| **14** | **A** | `pg_stat_user_indexes` tracks operational index statistics, including `idx_scan` (number of index scans executed). |
| **15** | **B** | The engineering lifecycle moves from domain normalization to constraint DDL, safe staging, analytical reporting, and query tuning. |
