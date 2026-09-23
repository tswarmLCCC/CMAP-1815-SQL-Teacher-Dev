# Unit 3: Asynchronous Self-Check Drills

Test your understanding of relational keys, multi-table joins, and outer joins before attending class.

---

### Drill 1: Identifying Keys
Look at the following schema definition:

```sql
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    dept_id INT REFERENCES departments(dept_id)
);
```

Which column is the **Primary Key** of `staff`, and which column is the **Foreign Key**?

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:**
* **Primary Key of `staff`:** `staff_id` (Uniquely identifies each employee).
* **Foreign Key of `staff`:** `dept_id` (References the primary key of the `departments` table).
</details>

---

### Drill 2: Diagnosing the Ambiguous Column Error
You run this query:

```sql
SELECT order_id, order_date, quantity
FROM orders o
INNER JOIN order_lines ol ON o.order_id = ol.order_id;
```

PostgreSQL throws: `ERROR: column reference "order_id" is ambiguous`. Why did this happen, and how do you fix it?

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **Both tables contain a column named `order_id`.**  
**Reason:** Because both the parent table (`orders`) and child table (`order_lines`) share the identical column name `order_id`, PostgreSQL does not know which table's column you want in the projection list.  
**Fix:** Prefix the column with the table alias:
```sql
SELECT o.order_id, o.order_date, ol.quantity
FROM orders o
INNER JOIN order_lines ol ON o.order_id = ol.order_id;
```
</details>

---

### Drill 3: Predicting INNER vs. LEFT JOIN Outputs
Suppose you have two tables:

**`customers` (3 rows):**
* ID 1: Alice
* ID 2: Bob
* ID 3: Charlie

**`orders` (2 rows):**
* Order 101: Customer 1 (Alice)
* Order 102: Customer 1 (Alice)
*(Notice: Bob and Charlie have never placed an order!)*

How many rows will this **`INNER JOIN`** return?
```sql
SELECT c.name, o.order_id
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;
```

And how many rows will this **`LEFT JOIN`** return?
```sql
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:**
* **`INNER JOIN`:** Returns **2 rows** (Alice with Order 101, Alice with Order 102). Bob and Charlie are completely excluded because they have no matching orders.
* **`LEFT JOIN`:** Returns **4 rows**:
  1. Alice | Order 101
  2. Alice | Order 102
  3. Bob | NULL
  4. Charlie | NULL  
A `LEFT JOIN` preserves all rows from the left table (`customers`), filling in `NULL` for missing right-table columns.
</details>

---

### Drill 4: The Cartesian Product Nightmare
If Table A contains **50 rows** and Table B contains **20 rows**, how many rows will be returned if an engineer runs:

```sql
SELECT * FROM table_a, table_b;
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **1,000 rows** ($50 \times 20 = 1000$).  
**Reason:** Because there is no `ON` or `WHERE` join condition, the database performs a **Cartesian Product (CROSS JOIN)**, pairing every single row in Table A with every single row in Table B.
</details>

---

### Drill 5: Constructing an Anti-Join
Referring back to Drill 3, which query will return ONLY the customers who have **never placed an order**?

```sql
-- Query A
SELECT c.name FROM customers c 
INNER JOIN orders o ON c.id = o.customer_id
WHERE o.order_id IS NULL;

-- Query B
SELECT c.name FROM customers c 
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.order_id IS NULL;

-- Query C
SELECT c.name FROM customers c 
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.order_id = NULL;
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **Query B.**  
**Reason:**
* Query A fails because an `INNER JOIN` discards customers without orders before the `WHERE` clause ever evaluates.
* Query C fails because `= NULL` evaluates to `UNKNOWN` in SQL.
* **Query B** correctly keeps all customers via `LEFT JOIN`, generates `NULL` for customers without orders, and then filters with `IS NULL` to isolate Bob and Charlie!
</details>
