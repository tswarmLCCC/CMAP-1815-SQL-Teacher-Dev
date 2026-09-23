# Unit 6 Student Lab Guide: Advanced Analytics, CTEs & Deduplication Pipelines

## Lab Overview
In this lab, you assume the role of Senior Analytics Engineer for Global Logistics & Supply. The business intelligence team requires advanced analytical reporting: refactoring legacy nested subqueries into modular pipelines, computing employee compensation variance without collapsing rows, identifying top performers per department, building a cumulative financial ledger, and implementing an automated record deduplication routine.

All work must be conducted in PostgreSQL 16.

---

## Deliverables & Submission Guidelines
1. Create a script named `lab6_submission.sql`.
2. Follow standard SQL formatting: UPPERCASE keywords, snake_case aliases.
3. Every analytical calculation must be labeled with an informative column alias.
4. Test execution in `psql`:
   ```bash
   psql -U postgres -d postgres -f lab6_submission.sql
   ```

---

## Lab Tasks

### Task 1: Refactoring Legacy Nested Subqueries into Modular CTEs
A legacy report contains an unreadable nested subquery in the `FROM` clause:
```sql
SELECT * FROM (
    SELECT department, AVG(salary) AS avg_sal
    FROM employees
    WHERE is_active = TRUE
    GROUP BY department
) sub WHERE avg_sal > 65000.00;
```
* **Requirements:**
  1. Refactor this query into a Common Table Expression named `active_dept_averages`.
  2. Include `department`, `headcount` (count of active staff), and `avg_salary` (rounded to 2 decimal places).
  3. Filter in the main query for departments with `avg_salary > 65000.00`.
  4. Sort by `avg_salary` in descending order.

### Task 2: Individual Compensation Variance via Window Functions
Management needs to compare each employee's salary against their department's average, without collapsing the 50 employee records.
* **Requirements:**
  1. From `employees`, project `employee_id`, `first_name`, `last_name`, `department`, and `salary`.
  2. Use `AVG(salary) OVER(PARTITION BY department)` to calculate `dept_avg_salary` rounded to 2 decimal places.
  3. Calculate `salary_variance`: the employee's salary minus `dept_avg_salary`.
  4. Calculate `company_avg_salary` using `AVG(salary) OVER()` across the entire table.
  5. Order results by `department` alphabetically, and `salary_variance` descending.

### Task 3: Top-N Departmental Earner Filter (CTE + Window Ranking)
HR wants to identify the top 2 highest earners in each department. If employees tie for a rank, no rank numbers should be skipped.
* **Requirements:**
  1. Write a CTE named `ranked_department_salaries`.
  2. Use `DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC)` to compute `salary_rank`.
  3. In the outer query, filter for `salary_rank <= 2`.
  4. Order by `department` and `salary_rank`.

### Task 4: Cumulative Financial Ledger (Running Totals)
Finance requires a daily cumulative revenue tracking report.
* **Requirements:**
  1. From `orders`, project `order_id`, `order_date`, and `total_amount`.
  2. Calculate `cumulative_revenue`: running total of `total_amount` ordered by `order_date` and `order_id`.
  3. Calculate `running_order_count`: running count of orders.
  4. Calculate `moving_avg_3_orders`: 3-order moving average using `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`, rounded to 2 decimal places.
  5. Order by `order_date`, `order_id`.

### Task 5: Golden Record Deduplication Pattern
Data pipelines often ingest multiple records per entity. Management needs a query that isolates each customer's single most recent order.
* **Requirements:**
  1. Write a CTE named `ranked_customer_orders`.
  2. Project `order_id`, `customer_id`, `order_date`, and `total_amount`.
  3. Use `ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC)` to assign `recency_rank`.
  4. In the main query, filter for `recency_rank = 1`.
  5. Output `customer_id`, `order_id AS latest_order_id`, `order_date AS latest_order_date`, and `total_amount AS latest_order_amount`.
  6. Order by `customer_id`.
