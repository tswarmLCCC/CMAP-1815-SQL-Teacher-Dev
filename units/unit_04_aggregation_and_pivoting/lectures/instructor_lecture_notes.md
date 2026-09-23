# Unit 4: Instructor Lecture Notes & Pedagogical Guide

## Module Overview & Objectives
Unit 4 represents the primary transition in relational database fluency: moving from **row-level inspection** to **metric calculation and reporting**. Students master aggregate functions, grouping semantics, post-aggregation filtering (`HAVING`), vertical set concatenation (`UNION`/`UNION ALL`), and horizontal data pivoting via conditional aggregation (`CASE WHEN` inside aggregates).

### Aligned Course Learning Outcomes
* **CLO 2:** Group and aggregate data, write subqueries, and manipulate result sets using set operations.
* **CLO 3:** Translate real-world business questions into correct, performant, and well-structured SQL queries.

---

## 1. Pedagogical Roadmap & Common Student Traps

### A. The "Funnel" Mental Model
* **The Concept:** Emphasize that aggregation collapses rows. A table with 10,000 rows grouped by 4 regions will always yield at most 4 rows.
* **Student Trap 1: The Missing Column in GROUP BY.**
  Students frequently attempt:
  ```sql
  SELECT department, job_title, AVG(salary)
  FROM employees
  GROUP BY department; -- Error!
  ```
  *Teaching Remedy:* Have students visualize the output grid. If there are 5 departments and 25 job titles, what would go in the `job_title` cell for an aggregated department row? Force students to articulate why a 2D relational grid cannot hold multiple unrelated rows in a single cell without explicit grouping or aggregation.
* **The Invariant Rule:** Every column in `SELECT` must either be in an aggregate function or in the `GROUP BY` clause.

### B. WHERE vs. HAVING Order of Operations
* **The Concept:** Query execution order is:
  1. `FROM`
  2. `WHERE` (filters base rows)
  3. `GROUP BY` (creates buckets)
  4. `HAVING` (filters buckets)
  5. `SELECT` (formats output)
  6. `ORDER BY` (sorts result)
* **Student Trap 2: Using Aggregates in WHERE.**
  `WHERE AVG(salary) > 50000` is impossible because averages do not exist until groups are formed.
* **Student Trap 3: Putting Non-Aggregated Filters in HAVING.**
  ```sql
  SELECT department, AVG(salary)
  FROM employees
  GROUP BY department
  HAVING department <> 'Executive'; -- Inefficient!
  ```
  *Teaching Remedy:* Explain database query planning. Filtering in `WHERE` prunes rows before memory is allocated for hash aggregation, drastically improving query performance.

### C. NULL Handling in Aggregates
* **The Distinction:**
  * `COUNT(*)` counts physical rows, including rows containing `NULL` values.
  * `COUNT(column_name)` counts non-NULL entries only.
  * `AVG(column_name)` divides `SUM(column_name)` by `COUNT(column_name)`, NOT by `COUNT(*)`. Missing values are omitted from the denominator!

### D. Set Operations vs. Joins
* **The Distinction:**
  * **Joins** combine tables horizontally (adding columns side-by-side based on foreign key relationships).
  * **Set Operations** (`UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`) stack tables vertically (adding rows underneath each other).
* **Performance Note:** Emphasize defaulting to `UNION ALL`. `UNION` incurs an expensive background `Sort` and `Unique` operation to eliminate duplicate rows.

### E. Pivoting with Conditional Aggregations
* **The Concept:** Students often ask how to create Excel-style pivot tables in SQL. Demonstrating `COUNT(CASE WHEN ... THEN 1 END)` or `SUM(CASE WHEN ... THEN amount ELSE 0 END)` bridges the gap between database query logic and business intelligence reporting.

---

## 2. In-Class Live Coding & Demonstration Script

### Demo 1: The Big Five & The Golden Rule (`part1_aggregations_and_groupby.sql`)
1. Run `COUNT(*)` vs `COUNT(commission_pct)` to demonstrate NULL exclusion.
2. Group by `department` and show `MIN`, `MAX`, `AVG`, and `SUM`.
3. Deliberately trigger the `must appear in the GROUP BY clause` error and ask the class to diagnose the failure before fixing it.

### Demo 2: WHERE vs. HAVING Pipeline (`part2_having_and_set_operations.sql`)
1. Show how `WHERE is_active = TRUE` reduces input rows.
2. Add `HAVING COUNT(*) >= 3` to filter out small departments.
3. Demonstrate a `UNION ALL` combining active employees with archived contractors. Show why column count and types must align.

### Demo 3: Cross-Tab Pivoting (`part3_case_and_pivoting.sql`)
1. Run a standard vertical group by (`region`, `category`, `SUM(sales)`).
2. Rewrite into a single wide row per region with columns `furniture_sales`, `office_sales`, `tech_sales`.
3. Introduce PostgreSQL's native `FILTER (WHERE ...)` clause as a modern alternative.

---

## 3. Formative Check Questions (Think-Pair-Share)
1. *If a table has 10 rows and all values in column `x` are `NULL`, what does `COUNT(*)` return? What does `COUNT(x)` return? What does `SUM(x)` return?*
   * Answer: `COUNT(*)` = 10, `COUNT(x)` = 0, `SUM(x)` = `NULL`.
2. *Can a query have a `HAVING` clause without a `GROUP BY` clause?*
   * Answer: Yes! The entire table is treated as a single implicit group (e.g. `SELECT AVG(salary) FROM employees HAVING AVG(salary) > 50000;`).
