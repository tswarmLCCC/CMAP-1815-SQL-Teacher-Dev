# Unit 2: Asynchronous Self-Check Drills

Test your understanding of filtering, pattern matching, and Boolean logic before attending class.

---

### Drill 1: The = NULL Trap
You run the following query against your `employees` table:

```sql
SELECT first_name, last_name, bonus
FROM employees
WHERE bonus = NULL;
```

What will PostgreSQL return?

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **0 rows (Empty Result Set).**  
**Reason:** In relational database theory and SQL standard, `NULL` represents an **unknown value**. Because an unknown value cannot be compared for equality, `bonus = NULL` evaluates to **`UNKNOWN`**, not `TRUE`. A `WHERE` clause only returns rows where the condition resolves strictly to `TRUE`.  
**Correct Query:**
```sql
SELECT first_name, last_name, bonus
FROM employees
WHERE bonus IS NULL;
```
</details>

---

### Drill 2: Operator Precedence (AND vs. OR)
Look at this query:

```sql
SELECT first_name, department, salary
FROM employees
WHERE department = 'Security' OR department = 'Sales' AND salary > 80000;
```

Which of the following employees will be returned?
* Employee 1: Department = 'Security', Salary = $30,000
* Employee 2: Department = 'Sales', Salary = $75,000
* Employee 3: Department = 'Sales', Salary = $90,000

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **Employee 1 and Employee 3 are returned. Employee 2 is excluded.**  
**Reason:** In SQL, **`AND` takes precedence over `OR`**. The database interprets the query as:
`WHERE department = 'Security' OR (department = 'Sales' AND salary > 80000)`.
* Employee 1 matches `department = 'Security'`, so the `OR` branch is satisfied regardless of their salary!
* Employee 2 has salary $75,000, failing the second branch.
* Employee 3 has salary $90,000 in Sales, satisfying the second branch.  
**To require $80,000+ for BOTH departments, use parentheses:**
`WHERE (department = 'Security' OR department = 'Sales') AND salary > 80000;`
</details>

---

### Drill 3: Deciphering Wildcards (% vs. _)
Which query will find any employee whose `first_name` has exactly 4 letters and starts with 'J'?

```sql
-- Query A
SELECT * FROM employees WHERE first_name LIKE 'J%';

-- Query B
SELECT * FROM employees WHERE first_name LIKE 'J___';

-- Query C
SELECT * FROM employees WHERE first_name LIKE 'J____';

-- Query D
SELECT * FROM employees WHERE first_name ILIKE 'J*';
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **Query B: `LIKE 'J___'` (Capital J followed by exactly three underscores).**  
**Reason:**
* The underscore `_` represents **exactly one character**.
* A 4-letter name starting with 'J' has 'J' + 3 additional characters (`J___`).
* `J%` matches any length (Jon, John, Jonathan).
* `*` is not a standard SQL wildcard (it is used in regex or filesystem globs, not SQL `LIKE`).
</details>

---

### Drill 4: Range Inclusivity with BETWEEN
If a product has a `retail_price` of exactly `50.00`, will it be included in this query?

```sql
SELECT product_name, retail_price
FROM products
WHERE retail_price BETWEEN 50.00 AND 100.00;
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **Yes.**  
**Reason:** The `BETWEEN` operator in SQL is strictly **inclusive** of both boundary values ($50.00 \le \text{price} \le 100.00$). Both 50.00 and 100.00 will match.
</details>

---

### Drill 5: Why Aliases Fail in WHERE
Why does the following query fail with an error?

```sql
SELECT product_name, retail_price * stock_quantity AS inventory_value
FROM products
WHERE inventory_value > 5000.00;
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **PostgreSQL throws `ERROR: column "inventory_value" does not exist`.**  
**Reason:** The internal logical order of query processing is:
1. `FROM`
2. `WHERE`
3. `SELECT`  
Because the `WHERE` filter executes **before** the `SELECT` clause, the column alias `inventory_value` has not been defined yet when the filter runs! You must write:
`WHERE retail_price * stock_quantity > 5000.00;`
</details>
