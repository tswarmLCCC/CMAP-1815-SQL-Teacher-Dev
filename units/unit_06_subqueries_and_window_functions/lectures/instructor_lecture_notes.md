# Unit 6: Instructor Lecture Notes & Pedagogical Guide

## Module Overview & Objectives
Unit 6 represents the pinnacle of analytical SQL query design. Students transition from monolithic, nested procedural thinking to **declarative modular pipelines (CTEs)** and **non-collapsing analytical computations (Window Functions)**. Mastery of `PARTITION BY`, ranking semantics (`ROW_NUMBER` vs. `RANK` vs. `DENSE_RANK`), running accumulators, and deduplication patterns equips students for senior analytics and data engineering roles.

### Aligned Course Learning Outcomes
* **CLO 2:** Write modular subqueries, Common Table Expressions (CTEs), and window functions to manipulate result sets.
* **CLO 3:** Translate real-world business questions into performant and well-structured analytical SQL.

---

## 1. Pedagogical Roadmap & Common Student Traps

### A. Subqueries vs. CTEs: The Readability Revolution
* **The Concept:** Traditional nested subqueries in `FROM` clauses read from the inside out and bottom to top. CTEs (`WITH`) structure queries from top to bottom, mirroring procedural variable assignment.
* **Teaching Tip:** Present an unformatted, 3-level nested subquery on the projector. Challenge students to identify the business logic. Then, show the identical logic refactored into two named CTEs (`WITH active_customers AS (...), customer_ltv AS (...)`). The contrast immediately proves the value of CTEs.

### B. Aggregation vs. Window Functions (The "Collapse" Trap)
* **The Key Distinction:**
  * `GROUP BY` collapses $N$ rows into $K$ categorical rows ($K \le N$). Granular row identity is destroyed.
  * `OVER(PARTITION BY ...)` computes aggregate metrics in memory across partitions while leaving all $N$ original rows completely intact.
* **Student Trap 1: Trying to filter window functions in WHERE.**
  Students often write:
  ```sql
  SELECT name, salary, ROW_NUMBER() OVER(ORDER BY salary DESC) AS rn
  FROM employees
  WHERE ROW_NUMBER() OVER(ORDER BY salary DESC) <= 3; -- ERROR!
  ```
  *Teaching Remedy:* Remind students of the SQL execution pipeline: `WHERE` executes *before* `SELECT` and window functions! To filter on a window metric, the query must be wrapped in a CTE or subquery.

### C. Ranking Semantics: ROW_NUMBER, RANK, and DENSE_RANK
* **The Differences:**
  * `ROW_NUMBER()`: Strictly unique sequential integer ($1, 2, 3, 4$). Deterministic tie-breaking requires secondary sort keys.
  * `RANK()`: Ties share a rank, subsequent rank skips ($1, 2, 2, 4$).
  * `DENSE_RANK()`: Ties share a rank, subsequent rank does not skip ($1, 2, 2, 3$).

### D. The Golden Deduplication Pattern
* **The Industry Standard:**
  ```sql
  WITH ranked AS (
      SELECT *, ROW_NUMBER() OVER (PARTITION BY business_key ORDER BY updated_at DESC) AS rn
      FROM messy_table
  )
  SELECT * FROM ranked WHERE rn = 1;
  ```
  Highlight why `ROW_NUMBER()` is used here instead of `RANK()`: if two duplicate records share the exact same timestamp, `RANK()` produces two rows with `rn = 1`, failing deduplication! `ROW_NUMBER()` guarantees exactly one winning record.

---

## 2. In-Class Live Coding & Demonstration Script

### Demo 1: Refactoring Subqueries into CTEs (`part1_subqueries_and_ctes.sql`)
1. Write a query finding employees earning more than their department's average using a correlated subquery.
2. Refactor into a clean, readable CTE pipeline.
3. Demonstrate chaining multiple CTEs together.

### Demo 2: The Power of PARTITION BY & Ranking (`part2_window_functions_and_ranking.sql`)
1. Compare `COUNT(*) OVER()` (table total) with `COUNT(*) OVER(PARTITION BY department)` (department total).
2. Compute salary variance from departmental average: `salary - AVG(salary) OVER(PARTITION BY department)`.
3. Demonstrate ranking side-by-side: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`.

### Demo 3: Running Balances & Deduplication (`part3_running_totals_and_deduplication.sql`)
1. Create a running cumulative revenue ledger: `SUM(amount) OVER(ORDER BY order_date)`.
2. Demonstrate a 3-period moving average with `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`.
3. Execute the `ROW_NUMBER() = 1` deduplication pattern on a duplicate-laden table.

---

## 3. Formative Check Questions (Think-Pair-Share)
1. *Can a window function appear in a `WHERE` or `HAVING` clause?*
   * Answer: No. Window functions are evaluated in the `SELECT` phase, after `WHERE`, `GROUP BY`, and `HAVING`.
2. *If three athletes tie for 1st place in a race, what rank will the 4th athlete receive under `RANK()`? Under `DENSE_RANK()`?*
   * Answer: Under `RANK()`: 4. Under `DENSE_RANK()`: 2.
