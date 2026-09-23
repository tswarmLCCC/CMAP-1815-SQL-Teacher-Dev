# Unit 4 Assessment: Summarization, Aggregation & Pivoting Quiz

**Total Questions:** 15  
**Points Possible:** 30 (2 points per question)  
**Time Limit:** 30 Minutes  
**Format:** Multiple Choice & Code Analysis  
**Aligned Learning Outcomes:** CLO 2, Competencies 2.1–2.4

---

## Part 1: Conceptual Foundations & Grouping Semantics (Questions 1–5)

### Question 1
In SQL, what is the fundamental difference between `COUNT(*)` and `COUNT(column_name)`?
* A) `COUNT(*)` only counts primary keys; `COUNT(column_name)` counts any column.
* B) `COUNT(*)` counts all physical rows, whereas `COUNT(column_name)` ignores rows where the specified column contains a `NULL` value.
* C) `COUNT(*)` is an ANSI standard aggregate, while `COUNT(column_name)` is a proprietary PostgreSQL extension.
* D) `COUNT(*)` calculates the sum of all numerical values in the table.

---

### Question 2
What is the "Golden Rule of Aggregation" when writing a query with a `GROUP BY` clause?
* A) All aggregate functions must be listed before the `FROM` clause.
* B) Any column appearing in the `SELECT` list that is not wrapped inside an aggregate function must be explicitly included in the `GROUP BY` clause.
* C) The `GROUP BY` clause can only group by columns that have unique primary key indexes.
* D) You cannot use `WHERE` and `GROUP BY` within the same query statement.

---

### Question 3
Why does attempting to filter aggregate results using the `WHERE` clause (e.g. `WHERE AVG(salary) > 50000`) produce a syntax error?
* A) Aggregate functions are only valid in the `ORDER BY` clause.
* B) In the query execution pipeline, `WHERE` evaluates individual rows before groups and aggregate metrics are calculated.
* C) The `AVG` function only works with integer data types in PostgreSQL.
* D) Column names inside aggregate functions cannot be referenced in filter conditions.

---

### Question 4
What is the primary difference between `UNION` and `UNION ALL`?
* A) `UNION` joins tables horizontally; `UNION ALL` joins tables vertically.
* B) `UNION` eliminates duplicate rows between the result sets, whereas `UNION ALL` retains all rows including duplicates.
* C) `UNION ALL` sorts the final output in ascending order automatically.
* D) `UNION` requires both queries to come from the exact same table.

---

### Question 5
How does the `HAVING` clause differ from the `WHERE` clause in SQL query processing?
* A) `WHERE` filters individual rows prior to grouping; `HAVING` filters aggregated group buckets after grouping.
* B) `HAVING` filters individual rows prior to grouping; `WHERE` filters summary rows after grouping.
* C) `HAVING` can only be used with text columns, while `WHERE` only works with numbers.
* D) There is no difference; they are interchangeable synonyms in modern PostgreSQL.

---

## Part 2: Syntax Traps & Query Analysis (Questions 6–10)

### Question 6
Examine the following SQL statement:
```sql
SELECT department, job_title, AVG(salary) AS avg_sal
FROM employees
GROUP BY department;
```
What will happen when this query is executed in PostgreSQL?
* A) It will succeed and pick the first `job_title` alphabetically for each department.
* B) It will fail with an error stating that `job_title` must appear in the `GROUP BY` clause or be used in an aggregate function.
* C) It will succeed and return `NULL` for the `job_title` column.
* D) It will fail because `AVG(salary)` cannot have a column alias.

---

### Question 7
A table named `orders` contains 100 rows. In 10 of these rows, `ship_date` is `NULL`. What will the following query return?
```sql
SELECT COUNT(*), COUNT(ship_date)
FROM orders;
```
* A) `100, 100`
* B) `100, 90`
* C) `90, 90`
* D) `100, 10`

---

### Question 8
Consider the following query:
```sql
SELECT department, COUNT(*) AS staff_count
FROM employees
WHERE department <> 'Executive'
GROUP BY department
HAVING COUNT(*) >= 5;
```
In what sequence does PostgreSQL process these operations?
* A) `FROM` $\rightarrow$ `SELECT` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING`
* B) `FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `SELECT`
* C) `FROM` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `WHERE` $\rightarrow$ `SELECT`
* D) `SELECT` $\rightarrow$ `FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING`

---

### Question 9
Why is `UNION ALL` typically preferred over `UNION` in high-performance production queries when duplicate rows are known not to exist?
* A) `UNION ALL` bypasses the disk write cache.
* B) `UNION ALL` avoids an expensive sort or hash deduplication step required by `UNION`.
* C) `UNION` converts all numbers to floating-point values.
* D) `UNION ALL` executes in parallel across all CPU cores automatically.

---

### Question 10
Look at the following query intended to pivot customer orders into distinct columns:
```sql
SELECT 
    region,
    COUNT(CASE WHEN category = 'Technology' THEN 1 END) AS tech_orders
FROM superstore
GROUP BY region;
```
Why does this correctly count only Technology orders?
* A) When `category` is not 'Technology', the `CASE` statement returns `NULL`, and `COUNT` ignores `NULL`s.
* B) The `CASE` statement physically deletes all rows where category is not 'Technology'.
* C) `COUNT` automatically replaces any boolean `FALSE` with a value of `0`.
* D) Because 'Technology' is the first category in the table.

---

## Part 3: Applied Calculations & Scenario Solving (Questions 11–15)

### Question 11
Given a table `bonuses` with the following 4 values in column `amount`: `100, 200, NULL, 300`.  
What will `AVG(amount)` return?
* A) `150` (600 / 4)
* B) `200` (600 / 3)
* C) `NULL`
* D) An error because `NULL` cannot be divided

---

### Question 12
Query 1 returns the set `{1, 2, 3, 4}`.  
Query 2 returns the set `{3, 4, 5, 6}`.  
What will `Query 1 EXCEPT Query 2` return?
* A) `{1, 2, 3, 4, 5, 6}`
* B) `{3, 4}`
* C) `{1, 2}`
* D) `{5, 6}`

---

### Question 13
Query 1 returns `{10, 20, 30}`.  
Query 2 returns `{20, 30, 40}`.  
What will `Query 1 INTERSECT Query 2` return?
* A) `{10, 40}`
* B) `{20, 30}`
* C) `{10, 20, 30, 40}`
* D) `{}` (Empty Set)

---

### Question 14
A sales analyst wants to calculate the total dollar volume for 'Furniture' in each region, setting non-furniture sales to zero in the summation. Which expression accomplishes this?
* A) `SUM(CASE WHEN category = 'Furniture' THEN sales ELSE 0 END)`
* B) `COUNT(CASE WHEN category = 'Furniture' THEN sales END)`
* C) `AVG(CASE WHEN category = 'Furniture' THEN sales ELSE NULL END)`
* D) `SUM(sales) WHERE category = 'Furniture'`

---

### Question 15
Look at this query:
```sql
SELECT department, SUM(salary) AS total_payroll
FROM employees
WHERE is_active = TRUE
GROUP BY department
HAVING SUM(salary) > 200000;
```
If an inactive employee in the 'Research' department earns $150,000, and two active employees earn $110,000 each ($220,000 total active):
Will the 'Research' department appear in the final result?
* A) Yes, because the total active payroll ($220,000) exceeds the $200,000 threshold.
* B) No, because the inactive employee's salary is added and disqualifies the department.
* C) No, because the average salary is below $200,000.
* D) The query will return a syntax error because `SUM(salary)` is used twice.

---

# Answer Key & Pedagogical Rationales

| Q# | Correct Answer | Rationale / Explanation |
| :---: | :---: | :--- |
| **1** | **B** | `COUNT(*)` counts total records regardless of content. `COUNT(column)` strictly counts non-null entries in that specific column. |
| **2** | **B** | Relational projection integrity requires that every non-aggregated column in `SELECT` be defined in `GROUP BY` so the engine knows how to bucket rows. |
| **3** | **B** | In the standard query execution pipeline, `WHERE` filters rows before groups are established. Aggregates cannot be calculated until after rows pass the `WHERE` filter. |
| **4** | **B** | `UNION` executes a deduplication step (equivalent to `DISTINCT`), while `UNION ALL` stacks datasets without removing duplicates. |
| **5** | **A** | `WHERE` operates on individual rows *before* aggregation. `HAVING` operates on aggregated metric buckets *after* grouping has collapsed the rows. |
| **6** | **B** | PostgreSQL enforces strict aggregation semantics: because `job_title` is not in an aggregate function or in `GROUP BY`, the engine rejects the query. |
| **7** | **B** | `COUNT(*)` returns all 100 rows. `COUNT(ship_date)` ignores the 10 `NULL`s and returns 90. |
| **8** | **B** | Correct execution sequence: `FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `SELECT`. |
| **9** | **B** | `UNION` incurs an expensive sort and duplicate removal pass. If duplicates are impossible or acceptable, `UNION ALL` provides superior performance. |
| **10** | **A** | When the condition is false, `CASE` defaults to `NULL` (since no `ELSE` is specified). `COUNT` ignores `NULL`s, counting only true occurrences. |
| **11** | **B** | `AVG` ignores `NULL` values in both numerator and denominator: (100 + 200 + 300) / 3 = 200. |
| **12** | **C** | `EXCEPT` returns items in Query 1 that do NOT appear in Query 2. `{1, 2, 3, 4} \ {3, 4, 5, 6} = {1, 2}`. |
| **13** | **B** | `INTERSECT` returns the mathematical intersection (elements common to both sets): `{20, 30}`. |
| **14** | **A** | Placing a `CASE` statement inside `SUM` adds `sales` when the condition is met and `0` otherwise, cleanly aggregating category revenue. |
| **15** | **A** | `WHERE is_active = TRUE` discards the inactive employee first. The surviving active payroll ($110k + $110k = $220k) passes the `HAVING` check ($220k > $200k). |
