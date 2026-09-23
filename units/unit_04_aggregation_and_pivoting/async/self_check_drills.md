# Unit 4: Formative Self-Check Drills & Solutions

Test your comprehension of Unit 4 concepts before entering class. Try writing each query in `psql` before checking the solution below.

---

## Drill 1: Aggregate NULL Behavior
**Prompt:** Write a query against the `employees` table that outputs:
1. `total_staff`: Total physical rows in the table.
2. `staff_with_locations`: Count of employees assigned to a physical `location_id`.
3. `staff_missing_locations`: Total rows minus the count of employees with locations.

### Solution
```sql
SELECT 
    COUNT(*) AS total_staff,
    COUNT(location_id) AS staff_with_locations,
    COUNT(*) - COUNT(location_id) AS staff_missing_locations
FROM employees;
```
*Takeaway:* `COUNT(*)` counts rows, while `COUNT(column)` ignores `NULL`s.

---

## Drill 2: Multi-Column GROUP BY
**Prompt:** Write a query against the `products` table showing the `category`, `is_discontinued`, total product count (`product_count`), and average retail price rounded to 2 decimal places (`avg_price`), sorted alphabetically by category and then by discontinued status.

### Solution
```sql
SELECT 
    category,
    is_discontinued,
    COUNT(*) AS product_count,
    ROUND(AVG(retail_price), 2) AS avg_price
FROM products
GROUP BY category, is_discontinued
ORDER BY category, is_discontinued;
```
*Takeaway:* Whenever multiple non-aggregate columns appear in `SELECT`, all of them must appear in `GROUP BY`.

---

## Drill 3: Combining WHERE and HAVING
**Prompt:** Find all departments that have at least 2 active employees (`is_active = TRUE`) whose departmental average active salary is greater than $60,000. Display `department`, `active_count`, and `avg_active_salary` rounded to 2 decimal places.

### Solution
```sql
SELECT 
    department,
    COUNT(*) AS active_count,
    ROUND(AVG(salary), 2) AS avg_active_salary
FROM employees
WHERE is_active = TRUE
GROUP BY department
HAVING COUNT(*) >= 2 AND AVG(salary) > 60000
ORDER BY avg_active_salary DESC;
```
*Takeaway:* `WHERE` filters out inactive employees before grouping; `HAVING` filters the resulting department buckets based on aggregate criteria.

---

## Drill 4: UNION ALL vs. UNION
**Prompt:** Write a single query that returns a unified list of all unique city names from both the `locations` table and the `superstore` table. Then explain how the result would differ if `UNION ALL` were used instead of `UNION`.

### Solution
```sql
SELECT city FROM locations
UNION
SELECT city FROM superstore
ORDER BY city;
```
*Explanation:* `UNION` sorts the combined dataset and eliminates duplicate city names. `UNION ALL` would simply concatenate the lists together, preserving all duplicates and executing significantly faster.

---

## Drill 5: Conditional Aggregation (Pivoting)
**Prompt:** Using the `superstore` table, write a query that outputs each `region` alongside three separate calculated columns:
1. `furniture_orders`: Count of orders where `category = 'Furniture'`.
2. `office_orders`: Count of orders where `category = 'Office Supplies'`.
3. `tech_orders`: Count of orders where `category = 'Technology'`.

### Solution
```sql
SELECT 
    COALESCE(region, 'Unknown') AS region,
    COUNT(CASE WHEN category = 'Furniture' THEN 1 END) AS furniture_orders,
    COUNT(CASE WHEN category = 'Office Supplies' THEN 1 END) AS office_orders,
    COUNT(CASE WHEN category = 'Technology' THEN 1 END) AS tech_orders
FROM superstore
GROUP BY region
ORDER BY region;
```
*Takeaway:* When `category` doesn't match the condition, `CASE` returns `NULL`, which `COUNT` discards, effectively pivoting rows into column counts!
