# Unit 1 Assessment: Selection & Relational Foundations Quiz

**Total Questions:** 15  
**Points Possible:** 30 (2 points per question)  
**Time Limit:** 30 Minutes  
**Format:** Multiple Choice & Code Analysis  
**Aligned Learning Outcomes:** CLO 1, Competency 1.1–1.9

---

## Part 1: Conceptual Foundations & Architecture (Questions 1–5)

### Question 1
In database theory, what is the technical term for using the `SELECT` clause to specify a subset of columns from a table?
* A) Selection
* B) Restriction
* C) Projection
* D) Partitioning
---

### Question 2
Why are relational database management systems (RDBMS) preferred over flat spreadsheets (like Excel) for grounding modern AI systems and enterprise applications?
* A) Databases enforce structured schemas, relational integrity, and concurrent multi-user access without risk of accidental cell desynchronization.
* B) Spreadsheets cannot store text data, whereas databases can.
* C) Spreadsheets do not support mathematical operations like multiplication and division.
* D) Databases automatically delete duplicate records without requiring queries.
---

### Question 3
In what sequence does the PostgreSQL database engine logically process the following query clauses?
```sql
SELECT first_name, salary 
FROM employees 
ORDER BY salary DESC;
```
* A) `SELECT` → `FROM` → `ORDER BY`
* B) `FROM` → `ORDER BY` → `SELECT`
* C) `ORDER BY` → `FROM` → `SELECT`
* D) `FROM` → `SELECT` → `ORDER BY`
---

### Question 4
What is the primary role of the `psql` command-line tool or VS Code SQLTools in relation to PostgreSQL?
* A) It stores the database tables on your local hard drive.
* B) It acts as a database client that sends SQL query strings to the database server and renders the returned result set.
* C) It compiles SQL queries into binary executable machine code.
* D) It automatically corrects any syntax errors before execution.
---

### Question 5
When an analyst executes the query `SELECT salary * 1.10 FROM employees;`, what happens to the underlying data stored in the `employees` table?
* A) The underlying table remains completely unchanged; the calculation is performed on the fly in memory and displayed in the temporary result set.
* B) The salaries stored in the table are permanently increased by 10%.
* C) The table is copied into a temporary backup table.
* D) The query produces an error because mathematical calculations cannot be performed inside a `SELECT` statement.
---

## Part 2: Syntax Debugging & Code Rules (Questions 6–10)

### Question 6
An intern attempts to run the following query and receives an error message: `ERROR: syntax error at or near "FROM"`. What is the cause of this error?
```sql
SELECT 
    product_name, 
    retail_price, 
    stock_quantity,
FROM products;
```
* A) The column names must be enclosed in single quotation marks.
* B) The table name `products` must be uppercase.
* C) The query is missing an `ORDER BY` clause.
* D) There is a trailing comma after `stock_quantity` before the `FROM` keyword.
---

### Question 7
Which of the following SQL statements correctly assigns the alias `annual_pay` to a calculated salary expression in PostgreSQL?
* A) `SELECT salary * 12 = annual_pay FROM employees;`
* B) `SELECT salary * 12 -> annual_pay FROM employees;`
* C) `SELECT salary * 12 AS annual_pay FROM employees;`
* D) `SELECT annual_pay(salary * 12) FROM employees;`
---

### Question 8
Which character is used in PostgreSQL to concatenate two strings together (e.g., combining a first name and a last name)?
* A) `+`
* B) `||`
* C) `&`
* D) `CONCAT_SYMBOL`
---

### Question 9
Why is the query `SELECT * FROM large_table;` generally considered an anti-pattern in production application environments?
* A) It causes the database server to shut down immediately.
* B) Relational databases do not support the asterisk wildcard operator.
* C) It permanently deletes all unprojected columns from the table.
* D) It incurs unnecessary network and memory overhead, exposes sensitive data, and makes downstream applications fragile to future schema changes.
---

### Question 10
What occurs if you execute a query in the `psql` command-line interface without typing a semicolon (`;`) at the end?
* A) The terminal displays a continuation prompt (e.g. `mydb-#`), waiting for you to complete the statement with a semicolon.
* B) The terminal terminates and closes your connection.
* C) The query automatically runs with default parameters.
* D) PostgreSQL automatically rolls back the entire database.
---

## Part 3: Result Set & Output Prediction (Questions 11–15)

### Question 11
Consider the following table named `locations`:

| location_id | city | state |
| :---: | :--- | :---: |
| 1 | Cheyenne | WY |
| 2 | Laramie | WY |
| 3 | Denver | CO |
| 4 | Topeka | KS |
| 5 | Fort Collins | CO |

How many rows will the following query return?
```sql
SELECT DISTINCT state FROM locations;
```
* A) 5
* B) 3
* C) 4
* D) 2
---

### Question 12
Referring to the same `locations` table above, how many rows will this query return?
```sql
SELECT DISTINCT state, city FROM locations;
```
* A) 3
* B) 2
* C) 5
* D) 1
---

### Question 13
Consider the following `products` table data:

| product_name | retail_price |
| :--- | :---: |
| Alpha Widget | 50.00 |
| Beta Widget | 120.00 |
| Gamma Widget | 15.00 |
| Delta Widget | 85.00 |

If you run:
```sql
SELECT product_name, retail_price
FROM products
ORDER BY retail_price DESC;
```
Which product will appear in the very first row of the output?
* A) Beta Widget
* B) Gamma Widget
* C) Alpha Widget
* D) Delta Widget
---

### Question 14
What is the default sort order if the `ORDER BY` clause is used without specifying `ASC` or `DESC`?
* A) Descending (`DESC`)
* B) Ascending (`ASC`)
* C) Random Order
* D) Order of insertion into the physical disk
---

### Question 15
Consider this multi-column sort:
```sql
SELECT department, last_name, salary
FROM employees
ORDER BY department ASC, salary DESC;
```
How does PostgreSQL order the rows?
* A) It sorts all rows by salary descending first, completely ignoring the department column.
* B) It randomly alternates between sorting by department and sorting by salary.
* C) It groups and sorts rows alphabetically by department (A to Z), and for employees within the same department, sorts their salaries from highest to lowest.
* D) It will return an error because `ORDER BY` only accepts one column.
---

# Answer Key & Pedagogical Rationales

| Q# | Correct Answer | Rationale / Explanation |
| :---: | :---: | :--- |
| **1** | **C** | **Projection** is the relational algebra term for selecting specific columns (attributes). *Selection* (or restriction) refers to filtering rows using `WHERE`. |
| **2** | **A** | Relational databases provide ACID compliance, schema integrity constraints (PK/FK), and concurrency without the human-error risks and row limits inherent in spreadsheets. |
| **3** | **D** | The engine must first locate and open the source table (`FROM`), project the requested columns/expressions (`SELECT`), and finally sort the resulting rows (`ORDER BY`). |
| **4** | **B** | Client software (`psql`, SQLTools, DBeaver) is purely an interface. The PostgreSQL daemon server running in the cloud or background processes the data and returns results. |
| **5** | **A** | `SELECT` statements are strictly read-only. Data on disk is never altered by a projection or calculation. |
| **6** | **D** | A trailing comma after the final column signals to the parser that another expression is expected. Hitting `FROM` instead creates a syntax error. |
| **7** | **C** | The standard keyword `AS` followed by an unquoted or double-quoted identifier is the ANSI/PostgreSQL syntax for column aliases. |
| **8** | **B** | In PostgreSQL and ANSI SQL, string concatenation is performed using the double-pipe operator ` |
| **9** | **D** | `SELECT *` creates bandwidth bottlenecks, risks accidental leakage of confidential columns, and causes client code to fail if columns are reordered or added. |
| **10** | **A** | Semicolons terminate SQL commands. Without one, `psql` prompts `mydb-#` indicating a multi-line continuation prompt. |
| **11** | **B** | The unique states in the table are `WY`, `CO`, and `KS` (3 distinct values). |
| **12** | **C** | `DISTINCT` across multiple columns evaluates the unique *combination* of all projected attributes. Every city-state pair is unique, returning all 5 rows. |
| **13** | **A** | `DESC` orders from highest to lowest. Beta Widget has the highest price ($120.00) and appears first. |
| **14** | **B** | By default, SQL sorts ascending (`ASC`)—lowest numbers first, earliest dates first, alphabetical A to Z. |
| **15** | **C** | Multi-column sorts evaluate sequentially: primary sort by `department ASC`, then tie-breaking secondary sort by `salary DESC`. |