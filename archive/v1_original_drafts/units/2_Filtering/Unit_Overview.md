# **Unit 2: Targeted Retrieval, Pattern Matching & Boolean Logic**

## **Precision Retrieval: Slicing Data with The Scalpel**

### **1. Unit Overview & Objectives**

In Unit 1, you learned how to project columns and explore data structures using the foundational `SELECT` statement—essentially "shining a flashlight" across entire database tables. In professional relational database engineering, however, identifying *what* attributes you want to view is only half the battle. Real-world databases contain millions or billions of rows; extracting the entire table is slow, wasteful, and often dangerous in production microservices.

In this unit, you master **The Scalpel**: the SQL `WHERE` clause. You will learn how the database engine evaluates conditional expressions, explore ANSI Three-Valued Logic (3VL), navigate the subtle traps of `NULL` values, construct sophisticated pattern matching with wildcards and regular expressions, evaluate operator precedence, paginate large result sets, and transform raw numbers using on-the-fly arithmetic calculations.

**Unit Learning Objectives:**

* **Master** the `WHERE` clause to filter datasets based on specific, multi-layered criteria.
* **Analyze** the operational implications of Three-Valued Logic (TRUE, FALSE, UNKNOWN) and understand how `NULL` values propagate through relational filters.
* **Construct** robust search patterns using `LIKE`, `ILIKE`, `IN`, `BETWEEN`, and POSIX regular expressions (`~`, `~*`).
* **Enforce** Boolean operator precedence using explicit grouping parentheses to prevent logic leakage between `AND` and `OR` gates.
* **Implement** pagination controls using deterministic `ORDER BY ... LIMIT ... OFFSET` patterns.
* **Standardize** report headers and calculated columns using expressions and the `AS` aliasing keyword.

---

### **2. The Problem Statement: Precision vs. Noise**

A modern enterprise database is a digital ocean. Consider an e-commerce platform with 500,000 customers or a government agency managing census records. Executing a simple `SELECT` statement (even when specifying three or four columns) produces hundreds of megabytes of raw text. No human analyst or downstream microservice can process that volume of data efficiently.

#### **The Need for Surgical Retrieval**
In high-frequency operational systems, queries frequently target an individual entity:
* A customer support representative searches for an order by tracking number.
* A university registrar retrieves a student profile by student ID number.
* A security engineer audits server access logs for a specific malicious IP address.

Without surgical row filtering, the database would be forced to perform a Full Table Scan (evaluating and transmitting every single row across the network), choking bandwidth and causing severe client lag. The `WHERE` clause empowers the database engine to discard 499,999 non-matching rows and return the exact record required in milliseconds.

#### **Constructing Focused Decision Spaces**
Beyond single-row lookups, analytical queries require isolating targeted segments of data before performing downstream aggregations or management decisions:
* "What is the average transaction value for premium loyalty members in the Mountain West region during Q3?"
* "Which pharmaceutical batches have an expiration date within the next 30 days and a current stock quantity below safety thresholds?"

The `WHERE` clause defines this **Decision Space**. Slicing away irrelevant data is the mandatory prerequisite before calculating sums, averages, or pivots. Filtering out operational noise ensures that the metrics presented to stakeholders are accurate, targeted, and actionable.

---

### **3. Theoretical Framework: The Logic of Retrieval**

To write reliable SQL, you must understand that the `WHERE` clause is an internal **Decision Engine**. The PostgreSQL query executor inspects rows and evaluates an expression against each one, deciding whether the row satisfies the criteria to move forward into the output pipeline.

#### **A. Predicates and Comparison Operators**

At the heart of every `WHERE` clause is the **Predicate**. In relational database theory, a predicate is a conditional statement that evaluates to a Boolean truth value. In PostgreSQL, predicates evaluate to one of three possible values: **TRUE**, **FALSE**, or **UNKNOWN**.

The fundamental comparison operators available in PostgreSQL include:

| Operator | Comparison Type | Definition | Example Syntax |
| :---: | :--- | :--- | :--- |
| `=` | **Equal to** | Evaluates to TRUE if both operands are identical in value and type. | `WHERE department = 'Sales'` |
| `<>` or `!=` | **Not equal to** | Evaluates to TRUE if the values on both sides are different. | `WHERE status <> 'Retired'` |
| `>` | **Greater than** | Evaluates to TRUE if the left operand is strictly larger than the right. | `WHERE age > 21` |
| `<` | **Less than** | Evaluates to TRUE if the left operand is strictly smaller than the right. | `WHERE retail_price < 10.00` |
| `>=` | **Greater than or equal** | Evaluates to TRUE if the left operand is larger than or equal to the right. | `WHERE gpa >= 3.5` |
| `<=` | **Less than or equal** | Evaluates to TRUE if the left operand is smaller than or equal to the right. | `WHERE stock_quantity <= 10` |

*Note: Special comparison predicates such as `BETWEEN`, `IN`, and `IS NULL` are syntactic shorthands. For instance, `age BETWEEN 18 AND 25` is logically equivalent to `(age >= 18 AND age <= 25)`.*

#### **B. Boolean Logic Gates & Operator Precedence**

Real-world filtering criteria rarely consist of a single comparison. We combine multiple predicates using Boolean logic gates: `AND`, `OR`, and `NOT`.

* **The `AND` Gate (Conjunction):** Both conditions must evaluate to TRUE for the row to qualify.
  ```sql
  SELECT product_name, retail_price, stock_quantity
  FROM products
  WHERE retail_price > 50.00 AND stock_quantity > 0;
  ```
* **The `OR` Gate (Disjunction):** If either condition (or both) evaluates to TRUE, the row qualifies.
  ```sql
  SELECT first_name, last_name, state
  FROM customers
  WHERE state = 'WY' OR state = 'CO';
  ```
* **The `NOT` Gate (Negation):** Inverts the truth value of a predicate (TRUE becomes FALSE; FALSE becomes TRUE; UNKNOWN remains UNKNOWN).
  ```sql
  SELECT employee_id, first_name, department
  FROM employees
  WHERE NOT (department = 'Human Resources');
  ```

##### **The Operator Precedence Trap: AND Before OR**
One of the most dangerous bugs in enterprise SQL occurs when mixing `AND` and `OR` without explicit grouping. In standard SQL operator precedence:
$$\mathbf{NOT} \succ \mathbf{AND} \succ \mathbf{OR}$$

The database evaluates all `AND` conditions **before** it evaluates `OR` conditions. Consider the following query intended to find active employees in either Cheyenne or Laramie:

```sql
-- DANGEROUS LOGIC BUG:
SELECT first_name, last_name, city, is_active
FROM employees
WHERE city = 'Cheyenne' OR city = 'Laramie' AND is_active = TRUE;
```

Because `AND` binds more tightly than `OR`, the database interprets this query as:
$$\text{city = 'Cheyenne'} \quad\mathbf{OR}\quad (\text{city = 'Laramie'} \;\mathbf{AND}\; \text{is\_active = TRUE})$$

As a result, **every single employee living in Cheyenne will be returned**, even if they were terminated five years ago (`is_active = FALSE`)! To enforce correct business logic, you must wrap disjunctions in parentheses:

```sql
-- CORRECT SECURE IMPLEMENTATION:
SELECT first_name, last_name, city, is_active
FROM employees
WHERE (city = 'Cheyenne' OR city = 'Laramie') 
  AND is_active = TRUE;
```

#### **C. The Logical Execution Lifecycle: How the Database "Thinks"**

A common point of confusion for beginners is the difference between the **written order** of a query and its **logical execution lifecycle**. You write queries starting with `SELECT`, but the database executes clauses in an entirely different sequence:

1. **`FROM` & `JOIN`:** The database engine identifies and opens the physical tables, constructing the base row-source dataset and performing Cartesian or join alignments.
2. **`WHERE`:** The engine iterates through the row stream and applies filter predicates. Non-qualifying rows are discarded immediately.
3. **`GROUP BY`:** Qualifying rows are partitioned into distinct aggregation buckets.
4. **`HAVING`:** Aggregated buckets are evaluated against summary predicates.
5. **`SELECT`:** The remaining rows are projected into columns, mathematical expressions are computed, and column aliases are assigned.
6. **`DISTINCT`:** Duplicate rows in the projected output are eliminated.
7. **`ORDER BY`:** The final result set is sorted according to specified columns or aliases.
8. **`LIMIT` / `OFFSET`:** The sorted result stream is trimmed to the requested window size.

##### **Why Column Aliases Fail in the WHERE Clause**
Notice where `WHERE` sits in relation to `SELECT`: `WHERE` executes in Step 2, while column aliases created with `AS` are not generated until Step 5!

```sql
-- COMPILATION ERROR: column "estimated_profit" does not exist
SELECT product_name, retail_price - cost_to_produce AS estimated_profit
FROM products
WHERE estimated_profit > 20.00;
```

Because the alias `estimated_profit` does not yet exist when Step 2 executes, the query fails with a compilation error. To filter on this calculation, you must repeat the expression in the `WHERE` clause:

```sql
-- CORRECT: The calculation is evaluated directly during Step 2
SELECT product_name, retail_price - cost_to_produce AS estimated_profit
FROM products
WHERE (retail_price - cost_to_produce) > 20.00;
```
*(Note: Because `ORDER BY` executes in Step 7, you CAN safely use column aliases in your `ORDER BY` clause!)*

#### **D. Three-Valued Logic & The Mystery of NULL**

Most programming languages use binary Boolean logic (True or False). Relational databases, however, operate on **ANSI Three-Valued Logic (3VL)** consisting of three distinct states:
* **TRUE** (1)
* **FALSE** (0)
* **UNKNOWN** (Null logic state)

##### **What is NULL?**
In relational database theory, `NULL` is **not a value**. It is not zero (`0`), it is not an empty string (`''`), and it is not a blank space. `NULL` is a marker signifying **missing, unrecorded, or inapplicable information**.

Because `NULL` represents the unknown, any comparison against `NULL` produces `UNKNOWN`:
* Is an unknown age greater than 21? We cannot know: **UNKNOWN**.
* Is an unknown salary equal to $50,000? We cannot know: **UNKNOWN**.
* Is one unknown value equal to another unknown value (`NULL = NULL`)? In SQL, the answer is **UNKNOWN**, not TRUE!

##### **The Truth Table for Three-Valued Logic**

| Operand A | Operator | Operand B | Resulting Evaluation |
| :---: | :---: | :---: | :---: |
| `TRUE` | `AND` | `UNKNOWN` | **UNKNOWN** |
| `FALSE` | `AND` | `UNKNOWN` | **FALSE** |
| `TRUE` | `OR` | `UNKNOWN` | **TRUE** |
| `FALSE` | `OR` | `UNKNOWN` | **UNKNOWN** |
| `UNKNOWN` | `AND` | `UNKNOWN` | **UNKNOWN** |
| `UNKNOWN` | `OR` | `UNKNOWN` | **UNKNOWN** |
| `NOT` | | `UNKNOWN` | **UNKNOWN** |

##### **The Golden Filtering Rule: Only TRUE Rows Pass**
In SQL, the `WHERE` clause filters rows according to a strict threshold: **a row is included in the output IF AND ONLY IF the final predicate evaluates to TRUE**.
* If a predicate evaluates to `FALSE` &rarr; the row is discarded.
* If a predicate evaluates to `UNKNOWN` &rarr; the row is discarded!

##### **The Fatal "= NULL" Trap**
Because developers intuitively expect equality checks to work, beginners frequently write:

```sql
-- WRONG: ALWAYS RETURNS ZERO ROWS
SELECT first_name, last_name, commission_pct
FROM employees
WHERE commission_pct = NULL;
```

For every employee with a missing commission, `NULL = NULL` evaluates to `UNKNOWN`. Because `UNKNOWN` is not `TRUE`, the database discards every single row! To test for missing data, SQL provides dedicated predicates:

```sql
-- CORRECT SYNTAX:
SELECT first_name, last_name, commission_pct
FROM employees
WHERE commission_pct IS NULL;

-- TO FIND COMPLETED RECORDS:
SELECT first_name, last_name, commission_pct
FROM employees
WHERE commission_pct IS NOT NULL;
```

##### **The Propagation of NULL in Arithmetic**
When performing arithmetic, `NULL` is infectious: any mathematical operation involving `NULL` yields `NULL`:
$$5 + \text{NULL} = \text{NULL}$$
$$100 \times \text{NULL} = \text{NULL}$$

If an employee earns a base salary of $60,000 and has a `NULL` bonus, calculating `salary + bonus` produces `NULL` rather than $60,000! To handle missing values gracefully, PostgreSQL provides the `COALESCE` function, which returns the first non-null argument in its list:

```sql
-- Safe calculation: if bonus is NULL, substitute 0
SELECT 
    first_name, 
    last_name, 
    salary, 
    bonus,
    salary + COALESCE(bonus, 0) AS total_compensation
FROM employees;
```

---

### **4. Implementation: The Advanced Filtering Tutorial**

#### **A. Range and Set Membership (BETWEEN & IN)**

##### **1. The IN Operator (Discrete Set Membership)**
When filtering against a list of specific allowable values, writing long chains of `OR` clauses is verbose and prone to error. The `IN` operator checks whether a value matches any member of a specified set:

```sql
-- Verbose, repetitive approach:
SELECT product_name, category
FROM products
WHERE category = 'Electronics' OR category = 'Computers' OR category = 'Audio';

-- Clean, idiomatic SQL using IN:
SELECT product_name, category
FROM products
WHERE category IN ('Electronics', 'Computers', 'Audio');
```

You can negate the set with `NOT IN`:

```sql
SELECT product_name, category
FROM products
WHERE category NOT IN ('Discontinued', 'Seasonal');
```

> **Warning (The NOT IN + NULL Trap):** If the list passed to `NOT IN` contains a `NULL` value (e.g. `category NOT IN ('Discontinued', NULL)`), the entire condition evaluates to `UNKNOWN` for all rows, causing the query to return zero records! Always ensure lists evaluated with `NOT IN` are sanitized against `NULL`s.

##### **2. The BETWEEN Operator (Continuous Ranges)**
The `BETWEEN` operator filters values within an **inclusive** range:
$$\text{val BETWEEN low AND high} \iff \text{val} \ge \text{low} \;\mathbf{AND}\; \text{val} \le \text{high}$$

```sql
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE salary BETWEEN 50000 AND 75000
ORDER BY salary ASC;
```

##### **The Timestamp Boundary Trap with BETWEEN**
While `BETWEEN` works cleanly for integers and standard dates, using it on `timestamp` columns containing hours, minutes, and seconds often introduces subtle data omission bugs:

```sql
-- SUBTLE BUG:
SELECT order_id, order_date, total_amount
FROM orders
WHERE order_date BETWEEN '2026-09-01' AND '2026-09-30';
```

When PostgreSQL casts `'2026-09-30'` to a timestamp, it defaults to midnight: `'2026-09-30 00:00:00'`. Any order placed on September 30th at 10:15 AM or 4:30 PM will be omitted from the results!

In production database environments, always write open-ended half-interval timestamp ranges:

```sql
-- INDUSTRY BEST PRACTICE: Half-Open Interval [Start, End)
SELECT order_id, order_date, total_amount
FROM orders
WHERE order_date >= '2026-09-01' 
  AND order_date < '2026-10-01';
```

#### **B. Pattern Matching: LIKE, ILIKE, and Regular Expressions**

When searching text fields where exact equality (`=`) is too restrictive, SQL provides pattern matching engines.

##### **1. Standard SQL Wildcards: LIKE & ILIKE**
The `LIKE` operator compares a text column against a pattern string using two special wildcard characters:
* `%` (Percent): Matches **zero or more** arbitrary characters.
* `_` (Underscore): Matches **exactly one** character.

| Pattern | Match Description | Example Matches |
| :--- | :--- | :--- |
| `'John%'` | Starts with "John" followed by any characters. | "John", "Johnson", "Johnathan" |
| `'%son'` | Ends with "son" preceded by any characters. | "Wilson", "Johnson", "Nelson" |
| `'%tech%'` | Contains "tech" anywhere in the string. | "Biotech", "Initech Corp", "Technical" |
| `'_a%'` | Has any character in position 1, 'a' in position 2. | "Data", "Sales", "Marketing" |
| `'INV-____'` | "INV-" followed by exactly four characters. | "INV-1001", "INV-9999" |

```sql
-- Case-sensitive pattern search (Standard SQL):
SELECT customer_name, email
FROM customers
WHERE email LIKE '%@gmail.com';
```

##### **The PostgreSQL ILIKE Superpower**
Standard SQL `LIKE` is strictly case-sensitive: searching for `LIKE '%wyoming%'` will miss `"Wyoming"` or `"WYOMING"`. PostgreSQL introduces the case-insensitive operator `ILIKE`:

```sql
-- Case-insensitive pattern search (Matches 'cheyenne', 'Cheyenne', 'CHEYENNE'):
SELECT city, county, population
FROM wyoming_census
WHERE city ILIKE 'cheyenne';
```

##### **Escaping Literal Wildcards**
If you need to search for a literal percent sign (`%`) or underscore (`_`) in your data (such as finding product codes like `PROMO_50`), use the `ESCAPE` clause:

```sql
-- Search for literal underscore using backslash as escape character:
SELECT product_code, description
FROM products
WHERE product_code LIKE '%!_%' ESCAPE '!';
```

##### **2. Advanced POSIX Regular Expressions**
For complex string matching where simple wildcards are insufficient, PostgreSQL supports full POSIX regular expressions:

* `~` : Case-sensitive regex match.
* `~*` : Case-insensitive regex match.
* `!~` : Does not match case-sensitive regex.
* `!~*` : Does not match case-insensitive regex.

```sql
-- Match phone numbers formatted as (XXX) XXX-XXXX:
SELECT customer_id, phone_number
FROM customers
WHERE phone_number ~ '^\([0-9]{3}\) [0-9]{3}-[0-9]{4}$';

-- Case-insensitive search for names starting with B, ending in s, exactly 5 letters:
SELECT first_name, last_name
FROM wyoming_census
WHERE last_name ~* '^B...s$';
```

> **Performance Warning on Text Patterns:** Queries utilizing leading wildcards (e.g. `LIKE '%smith'`) or unanchored regular expressions cannot utilize standard B-Tree database indexes. The database engine must perform a slow, full table scan to inspect every row. For high-volume production searches, reserve regex for batch data cleaning or configure specialized trigram indexes (`pg_trgm`).

#### **C. Pagination & Result Windowing (LIMIT & OFFSET)**

When rendering search results on the web or building APIs, sending 100,000 records to a client browser will crash the front-end application. We use `LIMIT` and `OFFSET` to paginate data:

* `LIMIT n` : Caps the output stream to a maximum of $n$ rows.
* `OFFSET m` : Skips the first $m$ rows before beginning to return records.

```sql
-- Page 1: Retrieve the first 10 highest-paid employees (Rows 1 to 10)
SELECT employee_id, first_name, last_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 10 OFFSET 0;

-- Page 2: Retrieve the next 10 employees (Rows 11 to 20)
SELECT employee_id, first_name, last_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 10 OFFSET 10;
```

##### **The Deterministic Ordering Requirement**
`LIMIT` and `OFFSET` should **never** be executed without an explicit `ORDER BY` clause! Relational tables are unordered sets. Without `ORDER BY`, the database engine returns rows in arbitrary physical storage order. Consecutive page requests could return duplicate records or omit rows entirely.

---

### **5. Student Exercises: Live Practice in GitHub Codespaces**

Connect to your live PostgreSQL 16 database in GitHub Codespaces using the integrated terminal (`psql`) or the SQLTools extension. Execute the following queries against the `cmap1815` database:

1. **High Earners Audit:** Retrieve all employees with a salary strictly greater than $75,000. Display `first_name`, `last_name`, `department`, and `salary`, sorted by `salary DESC`.
2. **Geographic Multi-City Filter:** Write a query using `IN` to find all customers located in `'Cheyenne'`, `'Laramie'`, or `'Casper'`.
3. **Compound Boolean Logic with Parentheses:** Retrieve all active products (`is_active = TRUE`) that belong to either the `'Apparel'` or `'Footwear'` category, with a `retail_price` under $50.00. (Ensure your parentheses prevent logic leakage!).
4. **Missing Data Inspection:** Query the `customers` table to find all accounts that have a `NULL` phone number (`phone_number IS NULL`).
5. **Case-Insensitive Domain Search:** Using `ILIKE`, find all employees whose email address ends with `@company.org`.
6. **Safe Compensation Calculation:** Display each employee's `first_name`, `salary`, `bonus`, and a calculated column named `total_pay` that sums salary and bonus, using `COALESCE` to convert missing bonuses to 0.
7. **Deterministic Top 5 Pagination:** Retrieve the 5 least expensive products in the catalog (`retail_price ASC`). Ensure you include both `ORDER BY` and `LIMIT`.

---

### **6. Frequently Asked Questions & Common Pitfalls**

* **Q: Why does `WHERE bonus = NULL` never return any rows?**  
  **A: The Three-Valued Logic Principle:** In ANSI SQL, `NULL` represents an unknown state rather than an empty value. Comparing anything to `NULL` using `=` produces `UNKNOWN`. Because the `WHERE` clause only keeps rows that evaluate strictly to `TRUE`, all rows are discarded. You must use `IS NULL` or `IS NOT NULL`.

* **Q: Why do I get `ERROR: column "net_income" does not exist` when I filter on an alias?**  
  **A: The Logical Execution Pipeline:** The `WHERE` clause executes in Step 2 of the query lifecycle to discard non-qualifying rows, while `SELECT` aliases are not evaluated until Step 5. Because the alias does not exist yet when the filter runs, you must repeat the full mathematical expression in the `WHERE` clause (e.g. `WHERE (gross_income - taxes) > 50000`).

* **Q: How does `AND` precedence cause data leaks when combined with `OR`?**  
  **A: Conjunction Binds Tighter Than Disjunction:** Without parentheses, `WHERE A OR B AND C` is evaluated as `A OR (B AND C)`. Any row satisfying condition `A` will pass the filter regardless of condition `C`. Always wrap your `OR` conditions in parentheses: `WHERE (A OR B) AND C`.

* **Q: What is the difference between `LIKE` and `ILIKE` in PostgreSQL?**  
  **A: Case Sensitivity:** `LIKE` is standard SQL and performs strictly case-sensitive pattern matching (`'Apple'` will not match `'apple'`). `ILIKE` is a PostgreSQL extension that performs case-insensitive pattern matching, making it ideal for user-submitted text search queries.

* **Q: Why does `BETWEEN '2026-09-01' AND '2026-09-30'` miss transactions on September 30th?**  
  **A: Implicit Midnight Timestamp Casting:** When a date string without a time component is cast to a timestamp, PostgreSQL defaults to `00:00:00` (midnight). Therefore, any order created after midnight on September 30th falls outside the boundary. Use half-open intervals instead: `WHERE order_date >= '2026-09-01' AND order_date < '2026-10-01'`.

* **Q: Why does `NOT IN` return zero rows when the list contains a NULL?**  
  **A: UNKNOWN Negation Trap:** `x NOT IN (1, 2, NULL)` expands to `x != 1 AND x != 2 AND x != NULL`. Because `x != NULL` evaluates to `UNKNOWN`, the conjunction evaluates to `UNKNOWN` for every single row. To prevent this, ensure subqueries or lists filtered by `NOT IN` exclude `NULL`s.

---

### **Appendix: GitHub Codespaces & Environment Reference**

* **Connecting to PostgreSQL via Terminal:** Open your terminal and run `psql` (or `psql -U postgres -d cmap1815`).
* **Inspecting Table Columns:** Use `\d table_name` (e.g. `\d employees`) to view data types, nullability constraints, and primary keys.
* **Toggling Expanded Display:** For queries with many columns, run `\x` inside `psql` to toggle vertical row display for easy reading.
* **Exiting psql:** Type `\q` and press Enter to return to the Linux shell.
* **Visual Querying in SQLTools:** Click the cylinder icon on the left VS Code activity bar, expand **CMAP 1815 Local PostgreSQL**, and double-click any table to inspect its schema and data visually.
