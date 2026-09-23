# Unit 8: Instructor Lecture Notes & Pedagogical Guide

## Module Overview & Objectives
Unit 8 serves as the capstone and performance tuning culmination of CMAP 1815. Students bridge the gap between mathematical query correctness and physical database engine execution. They master the use of `EXPLAIN` and `EXPLAIN ANALYZE`, understand the cost-based query planner, evaluate Sequential Scans vs. Index Scans, evaluate the trade-offs of B-Tree indexing (the "Write Penalty"), design audit trail tracking schemas, and defend their comprehensive Capstone Architecture.

### Aligned Course Learning Outcomes
* **CLO 6:** Profile query performance using `EXPLAIN ANALYZE`, create effective B-Tree indexes, and defend architectural choices in a comprehensive capstone.
* **CLO 1–5:** Unified synthesis across all course competencies.

---

## 1. Pedagogical Roadmap & Common Student Traps

### A. Reading EXPLAIN and EXPLAIN ANALYZE
* **EXPLAIN vs. EXPLAIN ANALYZE:**
  * `EXPLAIN`: Shows the optimizer's cost estimate and chosen algorithm *without running the query*. Safe to run on mutating queries in theory, but always caution students.
  * `EXPLAIN ANALYZE`: Actually executes the statement, measures actual run-time in milliseconds, and compares estimated row counts against actual rows returned.
* **Key Plan Node Types:**
  * `Seq Scan`: Full table scan. Optimal for small tables or when a query retrieves >20% of the table. Pathological for highly selective queries on large tables.
  * `Index Scan`: Traverses B-Tree index to retrieve heap tuples.
  * `Index Only Scan`: Retrieves all requested columns directly from the index leaf pages without visiting the table heap (fastest!).
  * `Bitmap Index Scan`: Collects matching pointers into a bitmap before fetching heap pages in physical disk order.

### B. The B-Tree Index Architecture & The Write Penalty
* **How B-Trees Work:** Balanced search tree maintaining sorted order ($O(\log N)$ search complexity).
* **The Write Penalty:** Emphasize that indexing is not free. Every `INSERT`, `UPDATE`, and `DELETE` must maintain all indexes on that table.
  * *Rule of Thumb:* Index foreign keys and high-cardinality filter columns. Avoid indexing low-cardinality columns (e.g. boolean flags) unless using a partial index (`WHERE is_active = TRUE`).

### C. The Capstone Defense Framework
* The Capstone brings together all course threads:
  1. Data Modeling: Normalized 3NF entity-relationship architecture.
  2. Integrity: Strict constraints (`PK`, `FK`, `CHECK`, `UNIQUE`, `NOT NULL`).
  3. ETL Staging: Loading and cleaning dirty data via `TEMP TABLE`.
  4. Advanced Analytics: Modular CTEs and Window Functions.
  5. Optimization: Profiling bottlenecks and implementing B-Tree indexes.

---

## 2. In-Class Live Coding & Demonstration Script

### Demo 1: Profiling with EXPLAIN ANALYZE (`part1_explain_and_query_plans.sql`)
1. Run `EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 90000;`.
2. Break down each line of output: `Seq Scan`, `cost=0.00..18.50`, `actual time=0.015..0.028 ms`.
3. Explain how PostgreSQL measures cost in unitless I/O block fetch units.

### Demo 2: The Before-and-After Index Transformation (`part2_b_tree_indexing_strategies.sql`)
1. Profile a selective query on unindexed `superstore` or `products`. Note the `Seq Scan`.
2. Create a B-Tree index: `CREATE INDEX idx_products_category ON products(category);`.
3. Re-run `EXPLAIN ANALYZE` and show the switch to `Bitmap Index Scan` or `Index Scan`.
4. Demonstrate creating a Composite Index for multi-column filters.

### Demo 3: Audit Logging & Capstone Architecture (`part3_audit_logging_and_capstone.sql`)
1. Create an `audit_log` table with timestamps and session user.
2. Simulate a business transaction that inserts an audit record.
3. Review the rubric and expectations for the Capstone project defense.

---

## 3. Formative Check Questions (Think-Pair-Share)
1. *Why might PostgreSQL choose a Sequential Scan over an Index Scan on a small 100-row table, even if an index exists on the searched column?*
   * Answer: Because reading 1 or 2 small disk blocks sequentially is faster than loading the B-Tree index page and then jumping to the table heap (the overhead of the index lookup exceeds the cost of a full table read).
2. *What happens to index leaf nodes when an existing row is updated in PostgreSQL?*
   * Answer: PostgreSQL uses Multi-Version Concurrency Control (MVCC), creating a new tuple version in the heap and inserting a new entry into the index, contributing to index bloat and write overhead.
