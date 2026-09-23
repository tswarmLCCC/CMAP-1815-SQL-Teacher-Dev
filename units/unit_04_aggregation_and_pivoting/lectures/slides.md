---
marp: true
theme: default
paginate: true
header: "CMAP 1815: Introduction to Modern SQL"
footer: "Unit 4: Summarization, Aggregation & Pivoting"
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
## Unit 4: Summarization, Aggregations & Pivoting

**Instructor:** Department of Computer Applications  
**Environment:** PostgreSQL 16 & GitHub Codespaces  
**Focus:** Aggregate Functions, GROUP BY, HAVING, Set Operations & Conditional Pivoting

---

## The Mental Model: The "Funnel"

Up to now, every query returned **one row per record** on disk.  
In Unit 4, we use the **Funnel**: collapsing thousands or millions of granular rows into **executive metric summaries**.

```
    [ 10,000 Granular Sales Line Items ]
                   |
         +---------v---------+
         |     GROUP BY      |  <--- Categorical Buckets (e.g. by Region)
         |   category / dept |
         +---------+---------+
                   |
      [ SUM, AVG, COUNT, MIN, MAX ]
                   |
    [ 4 High-Level Summary Rows Only ]
```

---

## Video 4.1: The Core Aggregate Functions

* **`COUNT(*)`**: Counts total rows (including NULLs).
* **`COUNT(column)`**: Counts populated rows only (**ignores NULLs!**).
* **`SUM(column)`**: Adds numerical values.
* **`AVG(column)`**: Computes mathematical mean.
* **`MIN(column)` / `MAX(column)`**: Finds extremes across numbers, dates, or strings.

```sql
SELECT 
    COUNT(*) AS total_employees,
    AVG(salary) AS average_salary,
    MAX(salary) AS highest_salary,
    MIN(hire_date) AS oldest_hire_date
FROM employees;
```

---

## The Golden Rule of `GROUP BY`

When you mix individual columns and aggregate functions:

```sql
SELECT department, AVG(salary) AS avg_sal
FROM employees
GROUP BY department;
```

<div class="highlight">
<b>The SQL Law of Aggregation:</b> Any non-aggregated column in your <code>SELECT</code> clause <b>MUST</b> appear in your <code>GROUP BY</code> clause! Otherwise, PostgreSQL throws an immediate error: <code>column must appear in the GROUP BY clause or be used in an aggregate function</code>.
</div>

---

## Video 4.2: Row Filtering vs. Group Filtering

```
How You Write It:              Internal Execution Order:
1. SELECT                      1. FROM
2. FROM                        2. WHERE     (Filters individual rows BEFORE grouping)
3. WHERE                       3. GROUP BY  (Collapses rows into buckets)
4. GROUP BY                    4. HAVING    (Filters summarized buckets AFTER grouping!)
5. HAVING                      5. SELECT
6. ORDER BY                    6. ORDER BY
```

```sql
SELECT department, COUNT(*) AS staff_count
FROM employees
WHERE is_active = TRUE         -- Row filter (Active staff only)
GROUP BY department
HAVING COUNT(*) >= 3           -- Group filter (Depts with at least 3 active staff)
ORDER BY staff_count DESC;
```

---

## Set Operations: Combining Separate Query Results

Stacking result sets vertically:

* **`UNION`**: Combines rows from two queries and **removes duplicates**.
* **`UNION ALL`**: Combines rows and **keeps all duplicates** (faster!).
* **`INTERSECT`**: Returns only rows that appear in **both** queries.
* **`EXCEPT`**: Returns rows from Query 1 that do **not** appear in Query 2.

<div class="highlight">
<b>Alignment Rules:</b> Both queries must project the exact same number of columns, and corresponding columns must have compatible data types!
</div>

---

## Video 4.3: Conditional Aggregation & Data Pivoting

How do you transform vertical row categories into horizontal columns?

```sql
SELECT 
    l.city,
    COUNT(CASE WHEN e.department = 'Security' THEN 1 END) AS security_staff,
    COUNT(CASE WHEN e.department = 'Research' THEN 1 END) AS research_staff,
    COUNT(CASE WHEN e.department = 'Sales' THEN 1 END) AS sales_staff
FROM locations l
LEFT JOIN employees e ON l.location_id = e.location_id
GROUP BY l.city;
```

* **`CASE WHEN` inside `COUNT` or `SUM`** evaluates on the fly.
* Turns relational normalized rows into a spreadsheet-style executive matrix!

---

## Unit 4 Summary

1. **Aggregates** (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) collapse rows into metrics.
2. Every unaggregated projected column **must be listed in `GROUP BY`**.
3. **`WHERE`** filters rows *before* grouping; **`HAVING`** filters aggregated buckets *after* grouping.
4. **`UNION ALL`** stacks compatible datasets vertically.
5. Use **`CASE` inside aggregates** to pivot category rows into horizontal reporting columns.
