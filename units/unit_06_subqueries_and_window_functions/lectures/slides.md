---
marp: true
theme: default
paginate: true
header: "CMAP 1815: Introduction to Modern SQL"
footer: "Unit 6: Query Modularity, CTEs & Window Functions"
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 40px;
    background-color: #fdfdfd;
  }
  h1 {
    color: #1a365d;
  }
  h2 {
    color: #2b6cb0;
  }
  .highlight {
    background-color: #ebf8ff;
    border-left: 5px solid #3182ce;
    padding: 10px;
    border-radius: 4px;
  }
  code {
    background-color: #edf2f7;
    color: #c53030;
    padding: 2px 6px;
    border-radius: 4px;
  }
---

# CMAP 1815: Introduction to Modern SQL
## Unit 6: Query Modularity, CTEs & Window Functions

**Instructor:** Department of Computer Applications  
**Environment:** PostgreSQL 16 & GitHub Codespaces  
**Focus:** Subqueries, Common Table Expressions (`WITH`), Window Functions (`OVER`, `PARTITION BY`), Ranking, and Running Totals

---

## The Evolutionary Leap: Analytical SQL

* **Basic SQL (Units 1–4):** Filters rows, aggregates into buckets, joins tables.
* **Modern Analytical SQL (Unit 6):** Calculates rankings, running balances, rolling averages, and hierarchical deduplication **without collapsing rows!**

```
Basic Aggregation:           Window Function:
+--------+--------+          +--------+--------+-------------+
| Dept   | Salary |          | Dept   | Salary | Dept_Avg    |
+--------+--------+          +--------+--------+-------------+
| Sales  | 60000  |          | Sales  | 60000  | 65000       |
| Sales  | 70000  |  --->    | Sales  | 70000  | 65000       |
+--------+--------+          | Mktg   | 80000  | 80000       |
| Sales  | 65000  | (Collapsed) +--------+--------+-------------+
                             (Preserves individual rows!)
```

---

## Video 6.1: Subqueries vs. Common Table Expressions (CTEs)

### The Nightmare of Nested Subqueries:
```sql
SELECT * FROM (
    SELECT * FROM (
        SELECT * FROM employees WHERE salary > 50000
    ) WHERE department = 'Sales'
) WHERE is_active = TRUE; -- Hard to read, maintain, or debug!
```

### The Clean Solution: CTEs (`WITH`)
```sql
WITH high_earners AS (
    SELECT employee_id, first_name, last_name, department, salary
    FROM employees
    WHERE salary > 50000
),
active_sales AS (
    SELECT *
    FROM high_earners
    WHERE department = 'Sales' AND is_active = TRUE
)
SELECT * FROM active_sales;
```

---

## Video 6.2: The Anatomy of Window Functions

### The `OVER()` Clause
Calculates metrics across a "window" of rows while keeping every row intact:

```sql
SELECT 
    first_name, 
    department, 
    salary,
    AVG(salary) OVER(PARTITION BY department) AS dept_avg_salary,
    salary - AVG(salary) OVER(PARTITION BY department) AS diff_from_avg
FROM employees;
```

* **`PARTITION BY`**: Divides rows into analytical calculation windows (like `GROUP BY`, but without collapsing rows!).
* **`ORDER BY` inside `OVER()`**: Orders rows within each window.

---

## Ranking Functions: ROW_NUMBER, RANK, DENSE_RANK

How do you rank items when ties occur?

```sql
SELECT 
    first_name, 
    department, 
    salary,
    ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK()       OVER(PARTITION BY department ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS dense_rnk
FROM employees;
```

| Salary | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
| :---: | :---: | :---: | :---: |
| $100k | 1 | 1 | 1 |
| $90k | 2 | 2 | 2 |
| $90k (Tie) | 3 | 2 | 2 |
| $80k | 4 | **4** (Skips 3!) | **3** (No gaps!) |

---

## Video 6.3: Running Balances & The Deduplication Pattern

### Running Totals & Cumulative Sums
```sql
SELECT 
    order_id,
    order_date,
    order_amount,
    SUM(order_amount) OVER(ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
FROM orders;
```

### The Industry Standard Deduplication Pattern
Keep only the latest order per customer:

```sql
WITH ranked_orders AS (
    SELECT 
        order_id, customer_id, order_date, total_amount,
        ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn
    FROM orders
)
SELECT * 
FROM ranked_orders 
WHERE rn = 1; -- The latest record only!
```

---

## Unit 6 Summary

1. Use **CTEs (`WITH`)** to make complex queries modular, readable, and testable in steps.
2. **Window functions (`OVER`)** calculate analytical metrics without collapsing rows.
3. Use **`PARTITION BY`** to compute group metrics alongside granular row attributes.
4. Distinguish between **`ROW_NUMBER`** (strictly sequential), **`RANK`** (skips on ties), and **`DENSE_RANK`** (no gaps).
5. Master the **`ROW_NUMBER() = 1` pattern** to deduplicate records in data engineering pipelines.
