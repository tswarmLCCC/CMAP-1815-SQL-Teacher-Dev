---
marp: true
theme: default
paginate: true
header: "CMAP 1815: Introduction to Modern SQL"
footer: "Unit 1: Selection & Relational Foundations"
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
## Unit 1: Selection & Relational Foundations

**Instructor:** Department of Computer Applications  
**Environment:** PostgreSQL 16 & GitHub Codespaces  
**Focus:** The Relational Model, Projection ("The Flashlight"), & Basic Queries

---

## The Big Picture: Spreadsheets vs. Databases

| Excel / Flat Files | Relational Databases (PostgreSQL) |
| :--- | :--- |
| Single, massive table with duplicate data | Normalized tables with defined relationships |
| High risk of accidental cell desynchronization | Enforced data integrity (Types, Keys, Constraints) |
| Hard row limit (1,048,576 rows) | Handles millions/billions of records seamlessly |
| AI "hallucinates" on messy docs | **Factual Grounding Anchor** for enterprise AI / RAG |

<div class="highlight">
<b>The AI Connection:</b> Modern AI models cannot guess real-time facts. They must be grounded in verified, structured relational databases.
</div>

---

## Mental Model: The Warehouse & Filing Cabinet

* **The Warehouse:** The entire **Database** (`mydb`).
* **The Filing Cabinet:** A specific **Table** (`employees`, `products`).
* **The Vertical Drawers:** The **Columns / Attributes** (`first_name`, `salary`).
* **The Paper Folders:** The individual **Rows / Records** (One person or product).

```
+-------------------------------------------------------+
| Database: mydb                                        |
|   +-------------------+       +--------------------+  |
|   | Table: employees  |       | Table: locations   |  |
|   | [id, name, dept]  | <---> | [id, city, state]  |  |
|   +-------------------+       +--------------------+  |
+-------------------------------------------------------+
```

---

## Client vs. Server: Where Does SQL Live?

1. **The Server (PostgreSQL 16):**
   * Runs in the cloud (inside your GitHub Codespace container).
   * Manages storage, validates security, executes query math.
2. **The Client (`psql` CLI / VS Code SQLTools):**
   * Runs in your browser interface.
   * Sends SQL query text over the wire $\rightarrow$ displays tabular results.

```
[ You in VS Code ] --- (Sends SQL Query) ---> [ PostgreSQL Server ]
[ (Client Tool)  ] <--- (Returns Result) --- [ (Database Engine) ]
```

---

## Video 1.2: Anatomy of a Query

```sql
SELECT first_name, last_name, salary
FROM employees;
```

* **`SELECT` (What):** Identifies the specific columns you want to view.
* **`FROM` (Where):** Identifies the target table cabinet.
* **The Semicolon (`;`):** The period at the end of the sentence.

<div class="highlight">
<b>The Projection Flashlight:</b> You don't turn on overhead floodlights. You shine a focused beam on only the columns you need.
</div>

---

## The "Sledgehammer" vs. The "Scalpel"

```sql
-- The Sledgehammer (Anti-pattern in production)
SELECT * FROM employees;

-- The Scalpel (Industry Best Practice)
SELECT first_name, last_name, title 
FROM employees;
```

**Why avoid `SELECT *`?**
* **Bandwidth:** Transmitting 80 columns when you need 3 wastes bandwidth.
* **Security:** Prevents accidental leakage of PII (SSNs, salaries, passwords).
* **Reliability:** Downstream code doesn't break when columns are added or reordered.

---

## Order of Execution: How Postgres Actually Reads

```
How You Write It:              How Postgres Executes It:
1. SELECT                      1. FROM      (Finds the table)
2. FROM                        2. SELECT    (Pulls the columns)
3. ORDER BY                    3. ORDER BY  (Sorts the results)
```

> **Remember:** The database cannot pick columns (`SELECT`) until it first opens the cabinet (`FROM`).

---

## Video 1.3: Expressions & Virtual Columns

SQL is a powerful mathematical calculator:

```sql
SELECT 
    first_name, 
    salary, 
    salary * 1.05 AS projected_salary
FROM employees;
```

* `salary * 1.05` is computed on the fly in memory.
* **Crucial Rule:** `SELECT` statements **never** alter data on disk!
* **`AS projected_salary`:** Provides a clean, professional header alias.

---

## String Concatenation & DISTINCT

### Combining Text with `||`
```sql
SELECT first_name || ' ' || last_name AS full_name
FROM employees;
```

### De-duplicating Results with `DISTINCT`
```sql
-- Scans the column and removes duplicate entries
SELECT DISTINCT department 
FROM employees;
```
*Evaluates the unique combination of all projected columns.*

---

## Sorting Your Output: `ORDER BY`

Relational tables are **unordered bags of rows** by default. To guarantee order:

```sql
SELECT department, last_name, salary
FROM employees
ORDER BY department ASC, salary DESC;
```

* **`ASC` (Ascending):** Smallest to largest, A to Z (Default).
* **`DESC` (Descending):** Largest to smallest, Z to A.
* **Multi-Sort:** Evaluates left to right (Primary sort $\rightarrow$ Tie-breaker).

---

## Unit 1 Summary & Next Steps

1. **Foundations:** Databases enforce structure and ground modern AI systems.
2. **Grammar:** `SELECT` projects columns, `FROM` selects tables, `;` terminates.
3. **Enhancements:** Use `AS` for aliases, `||` for strings, `DISTINCT` for unique sets, and `ORDER BY` for sorting.

**Up Next:** Transition to your Codespace and open `week1_orientation.sql`!
