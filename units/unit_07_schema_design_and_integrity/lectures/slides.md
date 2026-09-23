---
marp: true
theme: default
paginate: true
header: "CMAP 1815: Introduction to Modern SQL"
footer: "Unit 7: Schema Design, DDL & Data Integrity"
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
  .danger {
    background-color: #fff5f5;
    border-left: 5px solid #e53e3e;
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
## Unit 7: Schema Design, DDL & Data Integrity

**Instructor:** Department of Computer Applications  
**Environment:** PostgreSQL 16 & GitHub Codespaces  
**Focus:** Normalization (1NF–3NF), DDL (`CREATE TABLE`), Constraints (PK, FK, CHECK, UNIQUE), and Data Abstraction via Views

---

## From Data Consumer to Database Architect

Up to now, you queried schemas designed by others.  
Today, you become the **Database Architect**.

<div class="highlight">
<b>The Law of Relational Schema Design:</b> Good queries cannot fix a broken schema. If your tables are poorly normalized, you will suffer insertion anomalies, update nightmares, and data corruption.
</div>

Our mission: Build robust, normalized database structures that guarantee **Data Integrity at the Storage Layer**.

---

## Video 7.1: The Three Normal Forms (1NF to 3NF)

```
Denormalized Spreadsheet Chaos:
[ OrderID | CustomerName | CustomerPhone | ItemsPurchased         | TotalPrice ]
[ 101     | Alice Smith  | 555-0199      | Mouse, Keyboard, Cable | $150.00    ]

1NF (First Normal Form): Atomic Values
* Every column must hold a single, indivisible scalar value.
* No repeating groups, no comma-separated lists!

2NF (Second Normal Form): Full Functional Dependency
* Must be in 1NF + No partial dependencies on composite primary keys.
* Every non-key column must depend on the WHOLE primary key.

3NF (Third Normal Form): No Transitive Dependencies
* Must be in 2NF + No transitive dependencies.
* "Every non-key attribute must depend on the Key, the Whole Key, and Nothing But the Key!"
```

---

## Video 7.2: DDL & Declaring Data Integrity Constraints

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    total_amount NUMERIC(10,2) NOT NULL,
    
    -- Foreign Key Constraint with Referential Action:
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
        ON DELETE RESTRICT,
        
    -- Business Check Constraint:
    CONSTRAINT chk_positive_total
        CHECK (total_amount >= 0.00),
        
    CONSTRAINT chk_valid_status
        CHECK (status IN ('Pending', 'Processing', 'Shipped', 'Cancelled'))
);
```

---

## Foreign Key Referential Actions

What happens when someone deletes a record from the parent table?

* **`ON DELETE RESTRICT` (Default/Safest):** Rejects the deletion if child records exist.
* **`ON DELETE CASCADE`:** Automatically deletes all related child records! (Use with caution!).
* **`ON DELETE SET NULL`:** Keeps the child records, but sets their foreign key column to `NULL`.

<div class="danger">
<b>Warning:</b> <code>ON DELETE CASCADE</code> can wipe out entire tables of financial history if applied recklessly to master customer or account records.
</div>

---

## Video 7.3: Views & Architectural Abstraction

### What is a SQL View?
A stored query that acts like a virtual table:

```sql
CREATE OR REPLACE VIEW v_active_customer_summary AS
SELECT 
    c.customer_id,
    c.full_name,
    c.email,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0.00) AS lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.full_name, c.email;
```

### Why Use Views?
1. **Security & Column Masking:** Hide sensitive columns (passwords, SSNs) from reporting users.
2. **Simplicity:** Eliminate repetitive multi-table joins for analysts.
3. **API Stability:** Decouple underlying table schemas from client applications.

---

## Unit 7 Summary Checklist

1. **Normalize to 3NF:** Atomic values, no partial dependencies, no transitive dependencies.
2. Choose appropriate data types (`VARCHAR`, `INT`, `NUMERIC(10,2)`, `TIMESTAMP`).
3. Enforce business rules at the schema level using **`CHECK`**, **`UNIQUE`**, and **`NOT NULL`**.
4. Define **Foreign Keys** explicitly to prevent orphaned records.
5. Create **Views** to abstract complex joins and secure sensitive data.
