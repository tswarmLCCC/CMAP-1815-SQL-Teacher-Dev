---
marp: true
theme: default
paginate: true
header: "CMAP 1815: Introduction to Modern SQL"
footer: "Unit 2: Targeted Retrieval, Pattern Matching & Three-Valued Logic"
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
## Unit 2: Targeted Retrieval, Pattern Matching & Three-Valued Logic

**Instructor:** Department of Computer Applications  
**Environment:** PostgreSQL 16 & GitHub Codespaces  
**Focus:** The WHERE Clause ("The Scalpel"), Boolean Gates, Pattern Matching & The Mystery of NULL

---

## The Mental Model: Projection vs. Selection

* In **Unit 1**, we learned **Projection** (`SELECT`):
  * Choosing which vertical **columns** to illuminate.
* In **Unit 2**, we master **Selection / Restriction** (`WHERE`):
  * Choosing which horizontal **rows** are allowed through the gate.

```
       [ ALL 100,000 ROWS IN TABLE ]
                     |
       +-------------v-------------+
       |   WHERE Condition Filter   |  <--- "The Gatekeeper"
       +-------------+-------------+
                     |
         [ 42 MATCHING ROWS ONLY ]
                     |
          [ SELECT Projects Columns ]
```

---

## Video 2.1: The WHERE Clause & Comparison Operators

```sql
SELECT product_name, retail_price
FROM products
WHERE retail_price >= 100.00;
```

### Standard Comparison Operators
| Operator | Meaning | Example |
| :---: | :--- | :--- |
| `=` | Exactly equal to | `WHERE department = 'Security'` |
| `<>`, `!=` | Not equal to | `WHERE is_active != FALSE` |
| `>`, `<` | Greater than / Less than | `WHERE salary > 75000` |
| `>=`, `<=` | Greater/Less than or equal | `WHERE stock_quantity <= 10` |
| `BETWEEN` | Inclusive range ($A \le x \le B$) | `WHERE retail_price BETWEEN 20 AND 50` |

---

## Order of Execution Update!

Where does `WHERE` fit into PostgreSQL's internal processing order?

```
Written Order:                  Internal Execution Order:
1. SELECT                       1. FROM     (Finds table)
2. FROM                         2. WHERE    (Filters rows FIRST!)
3. WHERE                        3. SELECT   (Projects columns)
4. ORDER BY                     4. ORDER BY (Sorts filtered output)
```

<div class="highlight">
<b>Crucial Takeaway:</b> Because <code>WHERE</code> executes before <code>SELECT</code>, you <b>CANNOT</b> use a column alias created in <code>SELECT</code> inside your <code>WHERE</code> clause!
</div>

---

## Video 2.2: Pattern Matching & Lists

### 1. The `IN` Operator: Multiple Match Targets
```sql
-- Instead of: department = 'Sales' OR department = 'Research' OR ...
SELECT first_name, department
FROM employees
WHERE department IN ('Sales', 'Research', 'Security');
```

### 2. Pattern Matching with `LIKE` and `ILIKE`
* `%` (Percent): Matches **zero or more** characters.
* `_` (Underscore): Matches **exactly one** character.
* `ILIKE`: PostgreSQL-specific **case-insensitive** pattern matching.

```sql
SELECT product_name, sku FROM products WHERE sku LIKE 'ELEC-%';
SELECT last_name FROM employees WHERE last_name ILIKE 'd%';
```

---

## Video 2.3: Boolean Gates & Operator Precedence

Combining multiple conditions using `AND`, `OR`, and `NOT`:

```sql
SELECT first_name, department, salary
FROM employees
WHERE (department = 'Security' OR department = 'Sales')
  AND salary >= 65000;
```

<div class="highlight">
<b>The Parentheses Rule:</b> In SQL, <code>AND</code> always takes precedence over <code>OR</code> (just like multiplication before addition). <b>Always wrap your OR statements in parentheses</b> to avoid catastrophic logical leaks!
</div>

---

## The Mystery of NULL & Three-Valued Logic

In relational theory, `NULL` does **NOT** mean zero, empty string, or blank space.  
`NULL` means: **Unknown, Missing, or Not Applicable.**

### The Trap: Why `= NULL` Always Fails!
```sql
-- ❌ WRONG: Returns ZERO rows every single time!
SELECT * FROM employees WHERE bonus = NULL;

--  CORRECT: Evaluates missing state
SELECT * FROM employees WHERE bonus IS NULL;
SELECT * FROM employees WHERE bonus IS NOT NULL;
```

> **SQL Law:** You cannot use `=` with `NULL`. Nothing can be "equal" to an unknown value—not even another `NULL`!

---

## Three-Valued Logic Truth Table

SQL uses **True**, **False**, and **Unknown**:

| Expression | Evaluates To |
| :--- | :---: |
| `TRUE AND UNKNOWN` | **UNKNOWN** |
| `FALSE AND UNKNOWN` | **FALSE** |
| `TRUE OR UNKNOWN` | **TRUE** |
| `FALSE OR UNKNOWN` | **UNKNOWN** |
| `NOT UNKNOWN` | **UNKNOWN** |

*Rows are ONLY returned if the final WHERE condition evaluates to **TRUE**.*

---

## Limiting Your Result Sets: `LIMIT` & `OFFSET`

When working with massive enterprise datasets, never pull everything:

```sql
SELECT product_name, retail_price
FROM products
ORDER BY retail_price DESC
LIMIT 5 OFFSET 0;   -- Page 1: Top 5 most expensive products
```

* **`LIMIT n`:** Restricts the output to at most $n$ rows.
* **`OFFSET k`:** Skips the first $k$ rows (essential for building web pagination).
* **Golden Rule:** Always pair `LIMIT` with an explicit `ORDER BY` clause; otherwise, your results are non-deterministic!

---

## Unit 2 Summary

1. **`WHERE`** filters rows *before* `SELECT` projects columns.
2. Use **`IN`** for discrete sets and **`BETWEEN`** for inclusive ranges.
3. Use **`LIKE` / `ILIKE`** for wildcards (`%` multi, `_` single).
4. Guard Boolean logic with **parentheses** when combining `AND` and `OR`.
5. Check for missing data with **`IS NULL`** and **`IS NOT NULL`**, never `= NULL`.
6. Control pagination using **`ORDER BY ... LIMIT ... OFFSET`**.
