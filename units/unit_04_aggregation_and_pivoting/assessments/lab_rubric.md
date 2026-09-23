# Unit 4 Lab Rubric: Corporate Summarization & Executive Matrix Audit

**Total Points:** 100  
**Submission Format:** Single verified SQL script (`lab4_submission.sql`) executed against PostgreSQL 16.

---

## Grading Criteria Breakdown

| Dimension | Points Possible | Exemplary (100%) | Proficient (80%) | Developing (60%) | Unsatisfactory (0%) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Task 1: Departmental Metric Distribution** | 20 | Correctly groups by `department`, calculates `headcount`, `avg_salary`, `min_salary`, `max_salary` with proper rounding (`ROUND(..., 2)`). | Minor calculation or rounding error; logic is sound. | Missing `GROUP BY` column or incorrect aggregate function used. | Query fails to execute or omitted. |
| **Task 2: Inventory Valuation & Threshold Filtering** | 20 | Correctly calculates total stock, valuation cost, and retail potential; correctly filters active items in `WHERE` and uses `HAVING` for inventory valuation thresholds. | Used `HAVING` for row-level filter or minor math discrepancy. | Grouping errors or improper aggregate filtering. | Syntax error or omitted. |
| **Task 3: Multi-Table Revenue Aggregation** | 20 | Joins `orders` and `order_lines`, groups by `order_id` and `order_date`, calculates item count and total order amount correctly. | Join syntax correct but missing rounding or minor alias flaw. | Incomplete join or grouping on unprojected keys. | Query fails to execute or omitted. |
| **Task 4: Facility Staffing Reconciliation (Set Ops)** | 20 | Uses `EXCEPT` or `INTERSECT` correctly to reconcile corporate facility IDs with active employee assignments; explains business insight in comments. | Correct set operator but missing comment explanation. | Used incorrect set operator (`UNION` instead of `EXCEPT`). | Syntax error or omitted. |
| **Task 5: Executive Regional Matrix Pivot** | 20 | Implements conditional aggregation using `CASE WHEN` inside `SUM` or `COUNT` (or `FILTER`) to pivot categories into horizontal columns; formats nulls cleanly. | Pivots data correctly but has null formatting or minor percentage rounding issue. | Attempted pivot without aggregate wrapping or incorrect `CASE` logic. | Query fails to execute or omitted. |

---

## Deduction Penalties
* **-10 Points:** Using lowercase keywords (must follow SQL style guide: uppercase keywords, snake_case identifiers).
* **-10 Points:** Trailing syntax errors that prevent script execution in `psql`.
* **-5 Points:** Unformatted output (omitting column aliases such as `AS total_revenue`).
