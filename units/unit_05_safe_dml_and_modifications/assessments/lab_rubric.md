# Unit 5 Lab Rubric: Safe Data Ingestion, Staging & Modification Protocols

**Total Points:** 100  
**Submission Format:** Single verified SQL script (`lab5_submission.sql`) executed against PostgreSQL 16.

---

## Grading Criteria Breakdown

| Dimension | Points Possible | Exemplary (100%) | Proficient (80%) | Developing (60%) | Unsatisfactory (0%) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Task 1: Explicit Batch Insertion** | 20 | Explicitly specifies column names; inserts multi-row catalog items correctly; uses proper data types. | Minor syntax flaw or omitted column in `RETURNING`. | Uses positional insert without explicit column list. | Fails to execute or omitted. |
| **Task 2: Atomic Upsert Operation** | 20 | Implements `ON CONFLICT (product_id) DO UPDATE SET` using `EXCLUDED` references; handles collisions cleanly. | Upsert syntax works but hardcoded values used instead of `EXCLUDED`. | Missing conflict target or wrong clause. | Syntax error or omitted. |
| **Task 3: Safe Targeted UPDATE with RETURNING** | 20 | Includes pre-validation `SELECT` query in comments or code; executes `UPDATE` with exact `WHERE` filter; uses `RETURNING` to display before/after values. | Update works and returns data, but missing pre-validation check. | Missing `RETURNING` clause or overly broad `WHERE` condition. | Unconstrained update or syntax failure. |
| **Task 4: Transaction Rollback & Commit Control** | 20 | Demonstrates atomic multi-step operations using `BEGIN`, `COMMIT`, and `ROLLBACK`; correctly handles failure simulation. | Transaction blocks used, but minor logical ordering issue. | Missing `COMMIT` or improper transaction scope. | Failed execution or omitted. |
| **Task 5: Staging & Scrubbing Pipeline (TEMP TABLE)** | 20 | Creates `TEMPORARY TABLE`; loads raw data; writes clean transformation query removing currency symbols and whitespace; executes `INSERT INTO ... SELECT`. | Staging table created and transformed, but minor regex or string cleanup flaw. | Modified production table directly without staging. | Failed execution or omitted. |

---

## Deduction Penalties
* **-10 Points:** Executing an unconstrained `UPDATE` or `DELETE` without a `WHERE` clause.
* **-10 Points:** Lowercase keywords (SQL style guide violation).
* **-10 Points:** Syntax errors terminating script execution in `psql`.
