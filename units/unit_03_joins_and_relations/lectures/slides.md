---
marp: true
theme: default
paginate: true
header: "CMAP 1815: Introduction to Modern SQL"
footer: "Unit 3: Relational Interconnectivity (Joins)"
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
## Unit 3: Relational Interconnectivity (Joins)

**Instructor:** Department of Computer Applications  
**Environment:** PostgreSQL 16 & GitHub Codespaces  
**Focus:** Primary & Foreign Keys, INNER JOIN, Multi-Table Integration, Outer Joins & The Missing Data Audit

---

## The Relational Problem: Why Separate Tables?

In a poorly designed spreadsheet, customer names, addresses, product specs, and order quantities are repeated on every line:

```
[ Spreadsheet: Massive Redundancy & Update Anomaly Risk ]
Order 101 | John Smith | Cheyenne WY | Widget A | $50
Order 102 | John Smith | Cheyene WY  | Widget B | $80  <-- Typo!
Order 103 | John Smith | Cheyenne WY | Widget A | $50
```

* If John moves, you must update 50 rows.
* If a clerk mistypes "Cheyene", reports break.

<div class="highlight">
<b>The Relational Solution:</b> Store John once in a <code>customers</code> table. Store orders in an <code>orders</code> table. Connect them using a <b>Key</b>!
</div>

---

## Primary Keys vs. Foreign Keys: The Bridge

```
   [ locations ]                             [ employees ]
+-------------------+                    +-------------------------+
| location_id (PK)  | <================= | location_id (FK)        |
| city              |     The Bridge     | employee_id (PK)        |
| state             |                    | first_name, last_name   |
+-------------------+                    +-------------------------+
```

* **Primary Key (PK):** A column that uniquely identifies every single row in *its own* table (`locations.location_id`). Must be unique and never `NULL`.
* **Foreign Key (FK):** A column in a table that references the Primary Key of *another* table (`employees.location_id`).

---

## Video 3.1 & 3.2: The INNER JOIN

An **`INNER JOIN`** returns rows only when there is a match in **both** tables.

```sql
SELECT 
    e.first_name, 
    e.last_name, 
    l.city, 
    l.state
FROM employees e
INNER JOIN locations l 
    ON e.location_id = l.location_id;
```

* **Table Aliasing (`e`, `l`):** Essential for readable, unambiguous code.
* **The `ON` Clause:** Declares the equality bridge (`e.location_id = l.location_id`).

---

## The Fatal Trap: The Cartesian Product (CROSS JOIN)

What happens if you forget the `ON` clause or use comma-style joins improperly?

```sql
-- ❌ DISASTER: No ON clause!
SELECT * 
FROM employees, locations;
```

* If `employees` has **1,000 rows** and `locations` has **1,000 rows**, the database multiplies them:
  $$1,000 \times 1,000 = 1,000,000 \text{ rows!}$$
* In enterprise databases with millions of rows, a missing join predicate can crash the database server.
* **Always use explicit ANSI SQL `JOIN ... ON` syntax!**

---

## Multi-Table Joins: Connecting 3 or More Tables

Think of multi-table joins as following a chain of bridges:

$$\text{orders} \xrightarrow[\text{order\_id}]{\text{Bridge 1}} \text{order\_lines} \xrightarrow[\text{product\_id}]{\text{Bridge 2}} \text{products}$$

```sql
SELECT 
    o.order_id,
    o.order_date,
    p.product_name,
    ol.quantity,
    ol.unit_price
FROM orders o
INNER JOIN order_lines ol 
    ON o.order_id = ol.order_id
INNER JOIN products p 
    ON ol.product_id = p.product_id;
```

---

## Video 3.3: Outer Joins (LEFT, RIGHT, FULL)

What if you want to see **all** customers—even those who have **never placed an order**?  
An `INNER JOIN` silently discards customers without orders!

```
       [ LEFT JOIN Visual ]
   +---------------+---------------+
   | Table A (Left)| Table B(Right)|
   | Keep 100% of  | Match where   |
   | these rows!   | possible      |
   +---------------+---------------+
   (Unmatched columns from B fill with NULL)
```

```sql
SELECT c.customer_name, o.order_id
FROM customers c
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id;
```

---

## Anomaly Detection: The "Anti-Join" Pattern

How do data engineers find broken relationships, inactive users, or unsold inventory?

```sql
SELECT p.product_name, p.sku
FROM products p
LEFT JOIN order_lines ol 
    ON p.product_id = ol.product_id
WHERE ol.order_line_id IS NULL;
```

<div class="highlight">
<b>The Anti-Join:</b> When you <code>LEFT JOIN</code> to a child table and filter for where the child's primary key <code>IS NULL</code>, you instantly isolate records that have <b>never had an activity</b>!
</div>

* Great for: Finding products that never sold, students not enrolled, or customers who churned.

---

## Join Family Summary Reference

| Join Type | What it Returns | Common Use Case |
| :--- | :--- | :--- |
| **`INNER JOIN`** | Only matching records from both tables | Standard transactions where both entities must exist |
| **`LEFT JOIN`** | All rows from Left table, plus matched Right rows | Showing complete catalogs or directories regardless of activity |
| **`RIGHT JOIN`** | All rows from Right table (rarely used; rewrite as LEFT) | Mirror of LEFT JOIN |
| **`FULL OUTER JOIN`** | All rows from both tables, filling NULLs where unmatched | Master data reconciliation between two disparate systems |
| **`ANTI-JOIN`** | Left rows where Right is `NULL` | **Anomaly detection**: orphan records, unsold inventory |
