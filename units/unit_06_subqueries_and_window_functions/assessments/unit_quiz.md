# Unit 6 Assessment: Query Modularity, CTEs & Window Functions Quiz

**Total Questions:** 15  
**Points Possible:** 30 (2 points per question)  
**Time Limit:** 30 Minutes  
**Format:** Multiple Choice & Code Analysis  
**Aligned Learning Outcomes:** CLO 2, Competencies 2.5–2.8

---

## Part 1: Conceptual Foundations & Modular Architecture (Questions 1–5)

### Question 1
What is the primary architectural and readability advantage of a Common Table Expression (CTE) over a deeply nested subquery in the `FROM` clause?
* A) CTEs are automatically indexed by the database query planner.
* B) CTEs read top-to-bottom and can be chained sequentially, making complex multi-step pipelines significantly more readable and maintainable.
* C) CTEs allow write operations (`INSERT`, `UPDATE`) directly inside the `SELECT` list.
* D) CTEs persist permanently on disk across database restarts.

---

### Question 2
What is the fundamental difference between standard aggregation with `GROUP BY` and an analytical calculation using a Window Function with `OVER()`?
* A) Window functions only execute on numerical columns, while `GROUP BY` works only on text.
* B) `GROUP BY` collapses individual rows into summary buckets, whereas Window Functions compute metrics across subsets of rows while preserving all individual granular rows.
* C) Window functions can only be used in SQLite, not PostgreSQL.
* D) `GROUP BY` runs in the client application, while window functions run on the database server.

---

### Question 3
What does the `PARTITION BY` clause do inside a window function?
* A) It physically partitions the table on disk across multiple storage volumes.
* B) It divides the rows into logical calculation groups or windows without collapsing the rows.
* C) It deletes all rows that do not match the partition criteria.
* D) It enforces a unique primary key constraint on the partitioned column.

---

### Question 4
How does `RANK()` differ from `DENSE_RANK()` when multiple rows share identical sort values (a tie)?
* A) `RANK()` leaves gaps in the sequence following ties; `DENSE_RANK()` produces continuous, gapless rankings.
* B) `DENSE_RANK()` leaves gaps in the sequence; `RANK()` produces gapless rankings.
* C) `RANK()` breaks ties randomly; `DENSE_RANK()` throws an error on ties.
* D) There is no difference; they are exact synonyms in PostgreSQL.

---

### Question 5
Why does placing a window function directly inside a `WHERE` clause (e.g. `WHERE ROW_NUMBER() OVER(...) <= 3`) result in a syntax error?
* A) Window functions can only be used in the `ORDER BY` clause.
* B) In the SQL logical execution pipeline, the `WHERE` clause is evaluated before window functions in the `SELECT` phase are computed.
* C) Window functions require superuser permissions to filter rows.
* D) The `WHERE` clause only allows boolean comparisons between table columns.

---

## Part 2: Syntax Traps & Behavioral Analysis (Questions 6–10)

### Question 6
Look at the following CTE query:
```sql
WITH step1 AS (
    SELECT * FROM employees WHERE salary > 50000
),
step2 AS (
    SELECT department, AVG(salary) AS avg_sal
    FROM step1
    GROUP BY department
)
SELECT * FROM step2;
```
How are multiple CTEs separated in the `WITH` block?
* A) Each CTE must begin with the keyword `WITH`.
* B) CTEs are separated by commas, with only a single `WITH` keyword at the beginning.
* C) CTEs must be separated by semicolons.
* D) Multiple CTEs cannot be defined in a single query.

---

### Question 7
Consider three employees who all earn the exact same salary of $85,000, tied for the highest salary in the company.  
What values will `ROW_NUMBER() OVER(ORDER BY salary DESC)` assign to these three employees?
* A) `1, 1, 1`
* B) `1, 2, 3`
* C) `1, 1, 3`
* D) `NULL, NULL, NULL`

---

### Question 8
In the same scenario with three employees tied for 1st place with $85,000, what rank will the 4th employee (earning $80,000) receive under `RANK() OVER(ORDER BY salary DESC)`?
* A) 2
* B) 3
* C) 4
* D) 1

---

### Question 9
In the same scenario, what rank will that 4th employee receive under `DENSE_RANK() OVER(ORDER BY salary DESC)`?
* A) 2
* B) 3
* C) 4
* D) 1

---

### Question 10
Examine this query:
```sql
SELECT 
    order_date,
    total_amount,
    SUM(total_amount) OVER(ORDER BY order_date) AS running_rev
FROM orders;
```
Because `ORDER BY order_date` is specified without an explicit window frame clause, what default frame does PostgreSQL evaluate?
* A) The entire table from start to finish (`ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`).
* B) From the beginning of the partition up to the current row (`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).
* C) Only the current row (`ROWS BETWEEN CURRENT ROW AND CURRENT ROW`).
* D) The current row and the immediate next row.

---

## Part 3: Applied Scenario Solving (Questions 11–15)

### Question 11
An engineer writes the following deduplication query to find the single latest order for each customer:
```sql
WITH ranked_orders AS (
    SELECT 
        order_id, customer_id, order_date,
        ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn
    FROM orders
)
SELECT customer_id, order_id, order_date
FROM ranked_orders
WHERE rn = 1;
```
Why is `ROW_NUMBER()` preferred over `RANK()` in this deduplication pattern?
* A) `RANK()` runs significantly slower than `ROW_NUMBER()`.
* B) If a customer placed two orders with the exact same timestamp, `RANK()` would assign `1` to both rows, failing to deduplicate, whereas `ROW_NUMBER()` guarantees exactly one row per customer.
* C) `RANK()` cannot partition by foreign keys.
* D) `ROW_NUMBER()` automatically deletes the duplicate rows from disk.

---

### Question 12
Given a sales transaction table, which query correctly calculates each salesperson's contribution percentage toward their department's total sales?
* A) `sales_amount / SUM(sales_amount) OVER(PARTITION BY department) * 100`
* B) `sales_amount / SUM(sales_amount) GROUP BY department * 100`
* C) `AVG(sales_amount) OVER(ORDER BY department)`
* D) `COUNT(sales_amount) OVER(PARTITION BY department)`

---

### Question 13
Look at this query:
```sql
SELECT 
    order_date,
    order_amount,
    ROUND(AVG(order_amount) OVER(
        ORDER BY order_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg
FROM daily_sales;
```
For the 2nd row in the table (day 2), how many rows are included in the `moving_avg` calculation?
* A) 1 row (Day 2 only)
* B) 2 rows (Day 1 and Day 2)
* C) 3 rows (Day 1, Day 2, and Day 3)
* D) 0 rows (Requires at least 3 rows to start)

---

### Question 14
Which of the following clauses correctly computes an employee's salary rank within their department, restarting the ranking at 1 for each new department?
* A) `DENSE_RANK() OVER(ORDER BY department, salary DESC)`
* B) `DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC)`
* C) `DENSE_RANK() OVER(GROUP BY department ORDER BY salary DESC)`
* D) `DENSE_RANK(department) OVER(ORDER BY salary DESC)`

---

### Question 15
A data analyst wants to filter a report to show only employees whose salary is strictly greater than their department's average salary. Which approach is valid in PostgreSQL?
* A) `WHERE salary > AVG(salary) OVER(PARTITION BY department)`
* B) Compute the departmental average in a CTE or subquery, then filter `WHERE e.salary > d.avg_salary` in the outer query.
* C) `HAVING salary > AVG(salary) OVER(PARTITION BY department)`
* D) `WHERE salary > DEPARTMENT_AVG()`

---

# Answer Key & Pedagogical Rationales

| Q# | Correct Answer | Rationale / Explanation |
| :---: | :---: | :--- |
| **1** | **B** | CTEs structure complex multi-step queries from top-to-bottom, replacing deeply nested subqueries with readable, modular logic blocks. |
| **2** | **B** | `GROUP BY` collapses $N$ rows into summary groups. Window functions (`OVER`) calculate metrics across row sets while maintaining granular row identities. |
| **3** | **B** | `PARTITION BY` divides rows into analytical calculation windows, functioning like an in-memory `GROUP BY` without destroying individual rows. |
| **4** | **A** | `RANK()` skips ranks after ties (e.g. 1, 2, 2, 4). `DENSE_RANK()` maintains a continuous numerical sequence without gaps (e.g. 1, 2, 2, 3). |
| **5** | **B** | Standard execution order: `WHERE` runs before `SELECT`. Because window functions are evaluated in `SELECT`, they cannot be referenced in `WHERE`. |
| **6** | **B** | Multiple CTE definitions in a single statement are comma-delimited after the initial `WITH` keyword. |
| **7** | **B** | `ROW_NUMBER()` is strictly unique and sequential: it arbitrarily assigns 1, 2, and 3 to the three tied records. |
| **8** | **C** | Because three records tied for rank 1 (1, 1, 1), `RANK()` skips ranks 2 and 3, assigning rank 4 to the next distinct value. |
| **9** | **A** | `DENSE_RANK()` does not skip ranks after ties. After rank 1 (1, 1, 1), the next distinct value receives rank 2. |
| **10** | **B** | When `ORDER BY` is provided without an explicit frame, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, producing a cumulative sum. |
| **11** | **B** | If ties occur on the sort key, `RANK()` produces duplicate 1s, defeating deduplication. `ROW_NUMBER()` guarantees exactly one unique winner per partition. |
| **12** | **A** | Dividing the row-level `sales_amount` by the partitioned total `SUM(sales_amount) OVER(PARTITION BY department)` computes individual revenue contribution. |
| **13** | **B** | On Day 2, only 1 preceding row exists (Day 1). The window includes 2 rows total (Day 1 and Day 2). |
| **14** | **B** | `PARTITION BY department` resets the ranking bucket for each department; `ORDER BY salary DESC` sorts highest to lowest. |
| **15** | **B** | Window functions cannot appear in `WHERE` or `HAVING`. Wrapping the calculation in a CTE allows the outer query to filter against the resulting column. |
