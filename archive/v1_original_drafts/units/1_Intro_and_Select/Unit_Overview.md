# Unit 1: Selection & Fundamentals

## Asking Questions of Data: The SELECT Statement

### 1. Unit Overview & Objectives

Welcome to your first step in mastering SQL. In this unit, we move from being passive consumers of data—people who simply look at reports—to active investigators who generate them. You will learn the foundational skill of database management: retrieving specific information using the SELECT statement.

This unit is designed to bridge the gap between "having data" and "having answers." It isn't just about memorizing code; it's about learning a new way to interact with structured information. By the end of this unit, you will be able to write precision queries to explore any database table and organize the results into clean, professional reports.

**Learning Objectives:**

* **Conceptualize** the relational database model and articulate why structured data management is superior to flat-file spreadsheets for performance, integrity, and scalability.
* **Construct** syntactically correct SQL queries using the foundational pillars: SELECT, FROM, and ORDER BY.
* **Apply** the mathematical concept of Projection (&pi;) to isolate specific columns from tables.
* **Construct** calculated expressions and column aliases using arithmetic operators (`+`, `-`, `*`, `/`), string concatenation (`||`), and the `AS` keyword.
* **Audit** data integrity and summarize categories using the DISTINCT keyword (with an understanding of query planner performance overhead).
* **Execute** queries within your live PostgreSQL 16 database environment in GitHub Codespaces.

---

### 2. The Narrative of Data: Why We Need SQL

Imagine you are managing an omnichannel retail business with 50,000 customer orders, thousands of products, and hundreds of employees across multiple facilities. If all of this information were stored in a single, massive spreadsheet, finding a list of active warehouse staff or identifying our highest-margin products would be a logistical nightmare. You would have to scroll through tens of thousands of rows, manually ignoring irrelevant data just to find the columns you need. Spreadsheets often freeze, crash, or introduce accidental data desynchronization when sorting large files.

**Relational Databases** solve this by breaking data into normalized tables that "relate" to one another: `employees`, `products`, `locations`, `orders`, and `order_lines`. This structure prevents duplicate data entry and ensures high performance regardless of size. **SQL (Structured Query Language)** is the universal language used to interact with these tables. Instead of manually scrolling, you send a precise instruction—a query—and the PostgreSQL database engine retrieves the exact dataset in milliseconds.

---

### 3. The Core Concept: The "Flashlight" Metaphor

To understand how the SELECT statement works, imagine a massive, pitch-black warehouse (the database) filled with rows of tall filing cabinets (the tables). Each cabinet has dozens of drawers, and each drawer contains one specific attribute of information (the columns).

#### Projection: Your Logical Flashlight

When you walk into this warehouse with a flashlight, you don't turn on floodlights to illuminate everything at once—that would be overwhelming and wasteful. You only illuminate the specific facts needed for your current task. In relational algebra, this precision is called **Projection (&pi;)**.

* **The Flashlight (SELECT):** When you write `SELECT first_name`, you shine a focused beam of light on one specific column across every row in the cabinet. Everything else in the table remains in the dark. If you shine the light on `first_name`, `last_name`, and `salary`, you see those three attributes side-by-side. This is the act of projecting a subset of columns.
* **The Cabinet (FROM):** You must tell the database engine which cabinet to open. Writing `FROM employees` tells the database exactly where to point your flashlight so you don't waste time searching the wrong part of the warehouse.

#### The Result Set: The Temporary View

When you execute a SELECT statement, you are **not** changing the data stored in the database. You are simply creating a temporary in-memory "view" or **result set** displayed on your screen. The actual data in the table remains untouched, ready for the next query.

---

### 4. Implementation: Mastering the SELECT Statement

The SELECT statement is the most frequently used command in SQL. It is a **declarative** command: you describe the *result* you want, and the database engine determines the optimal execution plan to retrieve it.

#### A. Basic Syntax and Grammar: The SQL Sentence

A standard SQL query is composed of structured clauses:

1. **SELECT [Columns]:** Identifies the specific attributes you want to project (the "What").
2. **FROM [Table]:** Identifies the source table where the data lives (the "Where").
3. **ORDER BY [Columns]:** (Optional) Tells the database how to sort the result set (the "How it looks").

**The Golden Rules of SQL Syntax:**

* **The Semicolon (;):** Every SQL command must end with a semicolon. It is the period at the end of your SQL sentence. Without it, PostgreSQL will wait indefinitely for you to finish your thought.
* **Commas (,):** When projecting multiple columns, separate them with commas (e.g., `SELECT first_name, last_name, salary`). **Crucial Rule:** Never put a trailing comma after the last column before the `FROM` keyword. If you do, PostgreSQL expects another column and throws a syntax error.
* **Whitespace and Keyword Casing:** SQL is whitespace-insensitive and case-insensitive. However, professional standard practice requires writing SQL keywords in **ALL CAPS** (`SELECT`, `FROM`, `ORDER BY`, `AS`) and beginning each clause on a **new line** for readability.

#### B. Selecting Data: The Scalpel Approach

* **The Wildcard (`*`):** If you want to see every column in a table during initial exploration, use:
  ```sql
  SELECT * FROM employees;
  ```
  The asterisk acts as a "show all" button. While useful for exploratory work, avoid using `SELECT *` in production applications because it retrieves unnecessary data and wastes network bandwidth.
* **Specific Column Projection:** Act like a precise data surgeon by explicitly naming your columns:
  ```sql
  SELECT first_name, last_name, title
  FROM employees;
  ```
  This returns a clean, focused result set without horizontal clutter.

#### C. Removing Redundancy with DISTINCT

Often, column values repeat across rows. For example, selecting the `department` column from `employees` will return duplicate entries for every employee in each department:

```sql
-- Returns duplicate rows for departments:
SELECT department FROM employees;

-- Returns only unique department categories:
SELECT DISTINCT department FROM employees;
```

When multiple columns follow `DISTINCT`, PostgreSQL evaluates the **unique combination** of all projected columns:

```sql
SELECT DISTINCT department, title 
FROM employees
ORDER BY department ASC, title ASC;
```

> **Performance Caveat on DISTINCT:** When you execute a query with `DISTINCT`, PostgreSQL must scan every candidate row and perform a de-duplication pass using an in-memory hash table or on-disk sort. On tables containing millions of rows, `DISTINCT` can introduce significant CPU and I/O latency. Use `DISTINCT` intentionally when auditing data or generating category lists, but avoid using it casually to mask duplicate rows caused by improper join conditions.

#### D. Calculated Expressions & Column Aliasing (AS)

SQL is not limited to retrieving static column values; you can also use it as a powerful calculation engine. You can create virtual columns using scalar arithmetic operators (`+`, `-`, `*`, `/`) and string concatenation (`||`).

* **Mathematical Expressions:** Calculate profit margins directly from numeric columns in `products`:
  ```sql
  SELECT 
      product_name, 
      retail_price, 
      cost_to_produce,
      retail_price - cost_to_produce AS estimated_unit_profit
  FROM products
  ORDER BY estimated_unit_profit DESC;
  ```
* **Inventory Asset Valuation:** Calculate total dollar value held in inventory:
  ```sql
  SELECT 
      product_name,
      stock_quantity,
      retail_price,
      stock_quantity * retail_price AS total_inventory_value
  FROM products
  ORDER BY total_inventory_value DESC;
  ```
* **String Concatenation (`||`):** Merge text columns together:
  ```sql
  SELECT 
      first_name || ' ' || last_name AS full_name,
      department,
      title
  FROM employees;
  ```
* **The AS Keyword for Column Aliasing:** When you calculate an expression without an alias, PostgreSQL labels the column header as `?column?`. Always use the `AS` keyword with a descriptive, lowercase `snake_case` identifier (such as `AS estimated_unit_profit`) to produce clean, professional report headers.

#### E. Organizing Results with ORDER BY

By default, relational database engines return rows in non-deterministic order. To organize data for human consumption or reporting, you must supply an `ORDER BY` clause:

* **ASC (Ascending):** The default order (A to Z, lowest number to highest number).
  ```sql
  SELECT first_name, last_name, salary
  FROM employees
  ORDER BY salary ASC;
  ```
* **DESC (Descending):** Reverses the sort order (Z to A, highest number to lowest number). Ideal for finding top earners or highest-priced products.
  ```sql
  SELECT product_name, retail_price
  FROM products
  ORDER BY retail_price DESC;
  ```
* **Multi-Column Sorting:** Sort by primary category, then by a secondary tie-breaker:
  ```sql
  SELECT department, last_name, first_name, salary
  FROM employees
  ORDER BY department ASC, salary DESC;
  ```
  This groups employees alphabetically by department, and within each department, ranks them from highest salary to lowest.

---

### 5. Student Exercises: Live Practice

Connect to your live PostgreSQL 16 environment in GitHub Codespaces and execute these practice queries:

* **Console vs. GUI Navigation:** In the integrated terminal, launch `psql` to run command-line queries. In the **SQLTools GUI** (cylinder icon in the VS Code sidebar), expand **CMAP 1815 Local PostgreSQL &rarr; public &rarr; Tables** to browse table schemas and preview records in an interactive grid.

1. **Table Discovery:** In `psql`, execute `\dt` to list all base tables (`employees`, `locations`, `orders`, `order_lines`, `products`). In SQLTools, expand the `Tables` folder to inspect the same entities visually.
2. **Staff Directory:** Write a query that projects `first_name`, `last_name`, and `title` from the `employees` table, sorted alphabetically by `last_name`. Remember your terminating semicolon!
3. **Department Audit:** Write a query using `SELECT DISTINCT department` from `employees` to find all unique departments in the company, ordered alphabetically from A to Z.
4. **Product Profit Margins:** Retrieve `product_name`, `retail_price`, `cost_to_produce`, and a calculated column `retail_price - cost_to_produce` aliased as `estimated_unit_profit` from the `products` table. Sort descending by profit.
5. **Multi-Column Sort:** Retrieve `department`, `last_name`, and `salary` from `employees`. Sort alphabetically by `department ASC`, then by `salary DESC`.

---

### 6. Frequently Asked Questions & Common Pitfalls

* **Q: Why does my query seem frozen after I press Enter?**  
  **A: The "Invisible" Semicolon:** The most common stumbling block for beginners is forgetting the semicolon. In PostgreSQL, pressing Enter simply creates a new line in your command buffer (the prompt changes to `cmap1815-#`). The database engine is waiting for you to finish your command. Type `;` and press Enter to execute.
* **Q: Why do we write SELECT first if PostgreSQL executes FROM first?**  
  **A: Declarative vs. Logical Execution:** SQL is declarative: you state the desired output columns in `SELECT`, but the engine must first open the table in `FROM` before it can extract and project those attributes.
* **Q: How do I read PostgreSQL error messages without panic?**  
  **A: Follow the Caret (`^`) Pointer:** PostgreSQL error messages are precise and helpful. If you forget a comma or misspell a keyword, PostgreSQL prints an error message with a caret pointing directly to the character where parsing failed.
* **Q: Do calculated expressions permanently modify data in the table?**  
  **A: No, expressions are temporary in-memory projections:** Calculating `retail_price - cost_to_produce` produces a dynamic calculated column in your result set. The underlying values in the table on disk remain unaltered.
* **Q: Why should I avoid `SELECT *` in production queries?**  
  **A: Explicit projection protects performance:** `SELECT *` retrieves every column, including large text fields or sensitive data, increasing network payload size and preventing the query optimizer from using index-only scans. Always name your columns explicitly.

---

### Appendix: GitHub Codespaces Reference

For this course, we use **GitHub Codespaces** to provide a pre-configured, cloud-hosted Linux workstation running PostgreSQL 16:

* **Launching:** Open your personal student repository on GitHub, click **Code &rarr; Codespaces &rarr; Create codespace on main** (or resume your existing container).
* **Connecting via Terminal:** Open the integrated terminal (`Ctrl + ` `) and type `psql` (or `psql -U postgres -d cmap1815`).
* **Active Prompt:** When the prompt displays `cmap1815=#`, you are connected and ready to execute queries! Type `\q` to exit back to the Linux terminal prompt.
