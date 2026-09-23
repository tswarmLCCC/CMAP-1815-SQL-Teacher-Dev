# Unit 6: Formative Self-Check Drills & Solutions

Test your mastery of Common Table Expressions, window functions, and deduplication patterns. Test your code in `psql` before checking the solution below.

---

## Drill 1: Basic Common Table Expression (WITH)
**Prompt:** Write a query using a CTE named `dept_summary` that calculates the employee count and average salary per department. Then, in the main query, select all departments where the average salary is greater than $70,000, sorted by average salary descending.

### Solution
```sql
WITH dept_summary AS (
    SELECT 
        department,
        COUNT(*) AS headcount,
        ROUND(AVG(salary), 2) AS avg_sal
    FROM employees
    GROUP BY department
)
SELECT department, headcount, avg_sal
FROM dept_summary
WHERE avg_sal > 70000.00
ORDER BY avg_sal DESC;
```

---

## Drill 2: Partitioned Average & Variance
**Prompt:** Write a query against `employees` displaying `first_name`, `department`, `salary`, the department's average salary (`dept_avg`), and the difference between the employee's salary and their department average (`diff_from_avg`), using `OVER(PARTITION BY department)`. Round all monetary amounts to 2 decimal places.

### Solution
```sql
SELECT 
    first_name,
    department,
    salary,
    ROUND(AVG(salary) OVER(PARTITION BY department), 2) AS dept_avg,
    ROUND(salary - AVG(salary) OVER(PARTITION BY department), 2) AS diff_from_avg
FROM employees
ORDER BY department, salary DESC;
```

---

## Drill 3: Ranking with DENSE_RANK
**Prompt:** Write a query ranking products within each category based on `retail_price` descending using `DENSE_RANK()`. Output `category`, `product_name`, `retail_price`, and `price_rank`.

### Solution
```sql
SELECT 
    category,
    product_name,
    retail_price,
    DENSE_RANK() OVER(PARTITION BY category ORDER BY retail_price DESC) AS price_rank
FROM products
ORDER BY category, price_rank;
```

---

## Drill 4: Cumulative Running Total
**Prompt:** Write a query against the `orders` table that calculates a running cumulative revenue total ordered by `order_date` and `order_id`. Display `order_id`, `order_date`, `total_amount`, and `cumulative_revenue`.

### Solution
```sql
SELECT 
    order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER(ORDER BY order_date, order_id) AS cumulative_revenue
FROM orders
ORDER BY order_date, order_id;
```

---

## Drill 5: Golden Record Deduplication Pattern
**Prompt:** Using a CTE and `ROW_NUMBER()`, write a query that returns only the single highest-priced product for each category from the `products` table. If two products share the same highest price, use `product_id DESC` as a tie-breaker.

### Solution
```sql
WITH ranked_products AS (
    SELECT 
        product_id,
        product_name,
        category,
        retail_price,
        ROW_NUMBER() OVER(
            PARTITION BY category 
            ORDER BY retail_price DESC, product_id DESC
        ) AS rn
    FROM products
)
SELECT product_id, product_name, category, retail_price
FROM ranked_products
WHERE rn = 1
ORDER BY category;
```
