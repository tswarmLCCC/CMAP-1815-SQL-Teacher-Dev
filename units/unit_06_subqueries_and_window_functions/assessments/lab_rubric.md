# Unit 6 Lab Rubric: Advanced Analytics, CTEs & Deduplication Pipelines

**Total Points:** 100  
**Submission Format:** Single verified SQL script (`lab6_submission.sql`) executed against PostgreSQL 16.

---

## Grading Criteria Breakdown

| Dimension | Points Possible | Exemplary (100%) | Proficient (80%) | Developing (60%) | Unsatisfactory (0%) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Task 1: Subquery Refactoring to CTE** | 20 | Elegantly refactors subquery into a named CTE; clean aliases; correct filtering. | CTE works, but retains minor nesting or formatting flaws. | Subquery used instead of CTE. | Query fails to execute or omitted. |
| **Task 2: Partitioned Variance & Contribution** | 20 | Correctly computes `AVG() OVER(PARTITION BY ...)` and `SUM() OVER(...)`; rounds currency variance cleanly. | Logic sound, but minor rounding or alias flaw. | Missing `PARTITION BY` or used `GROUP BY` instead of window. | Syntax error or omitted. |
| **Task 3: Departmental Top-N Performer Filter** | 20 | Implements `DENSE_RANK()` or `ROW_NUMBER()`; wraps in CTE; filters rank $\le N$ in outer query. | Ranking correct, but filters directly in `WHERE` without CTE wrapper initially. | Incorrect ranking function used (`RANK` with tie gaps). | Syntax error or omitted. |
| **Task 4: Cumulative Financial Ledger** | 20 | Computes running cumulative total using `SUM() OVER(ORDER BY ...)`; formats output clearly. | Cumulative total works, but ordering key omitted or duplicate date order flaw. | Missing `ORDER BY` inside `OVER()`. | Failed execution or omitted. |
| **Task 5: Golden Record Deduplication Pattern** | 20 | Implements `ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ... DESC) = 1` pattern inside a CTE; isolates golden records. | Deduplication logic sound, but used `RANK()` instead of `ROW_NUMBER()`. | Attempted `DISTINCT ON` without proper window understanding. | Syntax error or omitted. |

---

## Deduction Penalties
* **-10 Points:** Lowercase keywords (SQL Style Guide violation).
* **-10 Points:** Attempting to filter window functions in `WHERE` directly, resulting in syntax errors.
* **-5 Points:** Unformatted column calculations (missing aliases).
