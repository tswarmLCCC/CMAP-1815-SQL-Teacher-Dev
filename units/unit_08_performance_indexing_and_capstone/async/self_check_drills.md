# Unit 8: Formative Self-Check Drills & Solutions

Test your comprehension of query performance profiling, execution plans, and indexing strategies. Test your code in `psql` before reviewing the solutions below.

---

## Drill 1: Profiling with EXPLAIN ANALYZE
**Prompt:** Write a query that runs `EXPLAIN ANALYZE` on a search for all employees in the `'Research'` department earning more than $75,000. Identify the scan type (`Seq Scan` or `Index Scan`) in the output.

### Solution
```sql
EXPLAIN ANALYZE
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE department = 'Research' AND salary > 75000.00;
```
*Takeaway:* Look at the first node of the plan. If no index exists on `department`, PostgreSQL will perform a `Seq Scan on employees`.

---

## Drill 2: Creating a Targeted B-Tree Index
**Prompt:** Write a DDL statement creating a standard B-Tree index named `idx_employees_department` on the `department` column of `employees`. Then re-run Drill 1 to observe any plan change.

### Solution
```sql
CREATE INDEX idx_employees_department ON employees(department);
```
*Takeaway:* On small tables (<100 rows), PostgreSQL may still prefer `Seq Scan` because reading one memory page is faster than an index traversal! On large tables, it will switch to `Index Scan` or `Bitmap Index Scan`.

---

## Drill 3: Composite Indexing & Column Order
**Prompt:** A workload frequently queries:
`SELECT * FROM products WHERE category = 'Office Supplies' AND retail_price < 25.00;`
Create a composite index named `idx_products_cat_price` optimized for this exact query.

### Solution
```sql
CREATE INDEX idx_products_cat_price ON products(category, retail_price);
```
*Explanation:* Placing `category` first (equality filter) and `retail_price` second (range filter) follows the leading-column best practice for multi-column indexes.

---

## Drill 4: Partial Indexing
**Prompt:** Management frequently queries orders with status `'Pending'` to prioritize dispatch. Because only 2% of orders are `'Pending'`, writing a full index would waste disk space. Create a Partial Index named `idx_orders_pending` that indexes only `'Pending'` orders.

### Solution
```sql
CREATE INDEX idx_orders_pending 
ON orders(order_date) 
WHERE order_status = 'Pending';
```
*Takeaway:* Partial indexes drastically reduce index file size and write penalty overhead by excluding inactive or irrelevant rows.

---

## Drill 5: Identifying the Write Penalty
**Prompt:** In 1–2 sentences, explain why adding 10 indexes to a high-volume transactional `orders` table that receives 500 inserts per second can degrade system throughput.

### Solution
*Answer:* Every single `INSERT` must synchronously update all 10 B-Tree index files on disk in addition to writing the row to the table heap. This causes massive write amplification, disk I/O contention, and transaction lock delays.
