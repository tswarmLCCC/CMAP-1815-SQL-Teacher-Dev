# Unit 3 Assessment: Relational Interconnectivity (Joins) Quiz

**Total Questions:** 15  
**Points Possible:** 30 (2 points per question)  
**Time Limit:** 30 Minutes  
**Format:** Multiple Choice & Code Analysis  
**Aligned Learning Outcomes:** CLO 2, Competency 2.1–2.2

---

## Part 1: Conceptual Foundations & Relational Keys (Questions 1–5)

### Question 1
What is the primary architectural purpose of a **Foreign Key** in a relational database?
* A) To automatically encrypt sensitive customer data.
* B) To enforce referential integrity by establishing a link between a column in one table and the Primary Key of another table.
* C) To speed up string concatenation operations.
* D) To prevent users from running `SELECT` queries without permission.

---

### Question 2
What occurs when two tables are joined in an **`INNER JOIN`**?
* A) All rows from both tables are merged into one large table, regardless of matching values.
* B) Only rows where the specified join condition evaluates to `TRUE` in both tables are included in the result set.
* C) The first table's rows are displayed, and the second table's rows are deleted.
* D) Rows with `NULL` values in the join columns are duplicated.

---

### Question 3
What is a **Cartesian Product** (CROSS JOIN) in SQL?
* A) A query that joins two tables by combining every row from the first table with every row from the second table.
* B) A join that only returns rows that have duplicate primary keys.
* C) An automatic database backup operation.
* D) A query that converts tabular data into an Entity-Relationship Diagram.

---

### Question 4
Why is a **`LEFT JOIN`** preferred over an `INNER JOIN` when querying customer activity reports?
* A) Because `LEFT JOIN` executes 10 times faster than `INNER JOIN`.
* B) Because `LEFT JOIN` preserves all customers in the output, even those who have never placed an order, preventing data loss in reporting.
* C) Because `INNER JOIN` does not support table aliases.
* D) Because `LEFT JOIN` automatically fixes syntax errors in the `WHERE` clause.

---

### Question 5
In SQL anomaly detection, what is the purpose of the **Anti-Join** pattern (`LEFT JOIN ... WHERE right_table.key IS NULL`)?
* A) To delete all records from the database.
* B) To find rows in the left table that have NO corresponding matching rows in the right table (e.g. unsold inventory, inactive users).
* C) To sort query results in reverse alphabetical order.
* D) To merge two databases located on different physical servers.

---

## Part 2: Syntax Debugging & Join Traps (Questions 6–10)

### Question 6
An intern runs the following query and receives the error: `ERROR: column reference "department" is ambiguous`. What caused this error?
```sql
SELECT first_name, department, city
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```
* A) The keyword `INNER` is optional and should be removed.
* B) Both the `employees` table and `departments` table contain a column named `department`, so the query must specify `e.department` or `d.department`.
* C) Single quotes are missing around `department`.
* D) The `ON` clause must use the `WHERE` keyword instead.

---

### Question 7
Which of the following queries correctly joins three tables using ANSI standard syntax?
* A)
```sql
SELECT o.order_id, c.name, p.product_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;
```
* B)
```sql
SELECT o.order_id, c.name, p.product_name
FROM orders o, customers c, products p
ON o.customer_id = c.customer_id;
```
* C)
```sql
SELECT o.order_id, c.name, p.product_name
FROM orders o
JOIN customers c AND products p;
```
* D)
```sql
SELECT o.order_id, c.name, p.product_name
FROM orders o
WHERE customers c ON o.customer_id = c.customer_id;
```

---

### Question 8
What is the effect of placing a filter condition in the `WHERE` clause instead of the `ON` clause during a `LEFT JOIN`?
```sql
-- Query A
SELECT p.product_name, ol.quantity
FROM products p
LEFT JOIN order_lines ol ON p.product_id = ol.product_id AND ol.quantity > 5;

-- Query B
SELECT p.product_name, ol.quantity
FROM products p
LEFT JOIN order_lines ol ON p.product_id = ol.product_id
WHERE ol.quantity > 5;
```
* A) Both queries produce identical output in all scenarios.
* B) Query B accidentally converts the `LEFT JOIN` into an `INNER JOIN` because `WHERE ol.quantity > 5` discards all the `NULL` rows produced for unmatched products.
* C) Query A produces a syntax error.
* D) Query B runs slower because `WHERE` cannot be used with joins.

---

### Question 9
Which keyword can be used to replace a `RIGHT JOIN` simply by inverting the order of tables in the `FROM` clause?
* A) `CROSS JOIN`
* B) `FULL OUTER JOIN`
* C) `LEFT JOIN`
* D) `SELF JOIN`

---

### Question 10
When joining a table to itself (a **Self-Join**, such as matching employees to their managers within the same `employees` table), what is strictly required?
* A) The table must be copied into a temporary table first.
* B) Two distinct table aliases must be assigned to distinguish the two roles of the same table.
* C) The primary key must be deleted.
* D) The query must be executed twice.

---

## Part 3: Result Set & Output Prediction (Questions 11–15)

### Question 11
Consider two tables:

**`departments`:**
| dept_id | dept_name |
| :---: | :--- |
| 10 | IT |
| 20 | HR |
| 30 | Finance |

**`employees`:**
| emp_name | dept_id |
| :--- | :---: |
| Alice | 10 |
| Bob | 10 |
| Charlie | 20 |
| David | NULL |

How many rows will be returned by this query?
```sql
SELECT e.emp_name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```
* A) 4
* B) 3
* C) 2
* D) 1

---

### Question 12
Referring to the same tables in Question 11, how many rows will be returned by this query?
```sql
SELECT e.emp_name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;
```
* A) 4
* B) 3
* C) 2
* D) 1

---

### Question 13
Referring again to the tables in Question 11, how many rows will be returned by this query?
```sql
SELECT d.dept_name, e.emp_name
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
WHERE e.emp_name IS NULL;
```
* A) 0
* B) 1 (Finance)
* C) 2
* D) 3

---

### Question 14
Table A has 4 rows. Table B has 5 rows. An engineer executes:
```sql
SELECT * FROM table_a, table_b;
```
How many total rows are in the resulting output?
* A) 9
* B) 20
* C) 4
* D) 5

---

### Question 15
Look at this query:
```sql
SELECT p.product_name, ol.order_id
FROM products p
LEFT JOIN order_lines ol ON p.product_id = ol.product_id
ORDER BY ol.order_id ASC NULLS FIRST;
```
What will appear at the very top of the query output?
* A) The products with the highest order numbers.
* B) The products that have never been ordered (where `order_id` is `NULL`).
* C) An error message stating that `NULLS FIRST` is invalid syntax.
* D) The product with `product_id = 1`.

---

# Answer Key & Pedagogical Rationales

| Q# | Correct Answer | Rationale / Explanation |
| :---: | :---: | :--- |
| **1** | **B** | Foreign Keys enforce referential integrity, ensuring child table records accurately reference existing parent table Primary Keys. |
| **2** | **B** | An `INNER JOIN` evaluates the `ON` condition and includes only rows where matching values exist in both tables. |
| **3** | **A** | A Cartesian product (CROSS JOIN) pairs every row of Table A with every row of Table B ($M \times N$ rows). |
| **4** | **B** | `LEFT JOIN` preserves all left-table master records (e.g. all customers), even if they have zero activity in the child table, preventing silent record loss. |
| **5** | **B** | The Anti-Join pattern uses `LEFT JOIN ... WHERE right.pk IS NULL` to isolate orphaned or inactive records. |
| **6** | **B** | When the same column name appears in multiple joined tables, PostgreSQL requires an explicit table alias prefix (`e.department` vs. `d.department`) to disambiguate. |
| **7** | **A** | Multi-table joins are chained sequentially using ANSI standard `JOIN ... ON ... JOIN ... ON ...`. |
| **8** | **B** | Filtering a right-table column in the `WHERE` clause discards `NULL` rows generated by the `LEFT JOIN`, effectively turning it into an `INNER JOIN`. Filters on the right table should be placed in the `ON` clause to preserve the outer join. |
| **9** | **C** | `TableA RIGHT JOIN TableB` is logically identical to `TableB LEFT JOIN TableA`. Industry standard prefers rewriting all right joins as left joins for consistent left-to-right code readability. |
| **10** | **B** | Self-joins require two unique table aliases (e.g. `employees emp JOIN employees mgr ON emp.manager_id = mgr.employee_id`) to allow the engine to treat the same table as two separate entities. |
| **11** | **B** | Alice (10), Bob (10), and Charlie (20) match. David has `dept_id = NULL` and Finance has no staff, so only 3 rows match. |
| **12** | **A** | `LEFT JOIN` preserves all 4 employees: Alice, Bob, Charlie, and David (with `dept_name = NULL`). |
| **13** | **B** | This Anti-Join finds departments with zero employees. Only Finance (dept 30) has no staff assigned (1 row). |
| **14** | **B** | A comma join with no `WHERE` condition produces a Cartesian product ($4 \times 5 = 20$ rows). |
| **15** | **B** | `ORDER BY ... NULLS FIRST` places all `NULL` values at the beginning of the result set, surfacing unsold products first. |
