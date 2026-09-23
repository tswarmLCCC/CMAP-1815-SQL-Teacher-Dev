# Unit 1: Asynchronous Self-Check Drills

Test your knowledge before attending this week's synchronous class session. Try answering these questions on paper or in your terminal before looking at the provided explanations!

---

### Drill 1: Identifying Syntax Errors
Look at the following query. Will it execute successfully in PostgreSQL? If not, what is wrong?

```sql
SELECT 
    first_name, 
    last_name, 
    department,
FROM employees;
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** ❌ **Syntax Error.**  
**Reason:** There is a **trailing comma** after `department`. In SQL, a comma signals that another projected column or expression will follow. Because the next keyword is `FROM`, PostgreSQL's parser encounters an unexpected token and throws:
`ERROR: syntax error at or near "FROM"`.  
**Correct Query:**
```sql
SELECT 
    first_name, 
    last_name, 
    department
FROM employees;
```
</details>

---

### Drill 2: Physical Table vs. Result Set
You run the following SQL query in `psql`:

```sql
SELECT 
    product_name, 
    retail_price * 0.90 AS discounted_price
FROM products;
```

Did this query modify the prices of the products stored in the database?

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **No.**  
**Reason:** The `SELECT` statement is strictly a **read-only retrieval operation**. It calculates the 10% discount on the fly and presents it in a temporary in-memory "result set" displayed on your screen. The actual `retail_price` column in the `products` table on the disk remains completely unchanged. Only Data Manipulation Language (DML) statements like `UPDATE` alter data on disk.
</details>

---

### Drill 3: Logical Order of Execution
In what order does PostgreSQL logically process the following query clauses?

```sql
SELECT department, title 
FROM employees 
ORDER BY department ASC;
```

1. `ORDER BY` $\rightarrow$ `FROM` $\rightarrow$ `SELECT`
2. `SELECT` $\rightarrow$ `FROM` $\rightarrow$ `ORDER BY`
3. `FROM` $\rightarrow$ `SELECT` $\rightarrow$ `ORDER BY`
4. `FROM` $\rightarrow$ `ORDER BY` $\rightarrow$ `SELECT`

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **Option 3: `FROM` $\rightarrow$ `SELECT` $\rightarrow$ `ORDER BY`.**  
**Reason:**  
1. **`FROM`**: The engine must first locate and open the source table (`employees`).
2. **`SELECT`**: The engine extracts and projects the requested columns (`department`, `title`).
3. **`ORDER BY`**: Finally, the projected result set is sorted before being transmitted to the client.
</details>

---

### Drill 4: De-duplicating Multi-Column Projections
Consider an `employees` table with 5 rows:

| first_name | department |
| :--- | :--- |
| Harry | Security |
| Karrin | Security |
| Waldo | Research |
| Jon | Operations |
| Arya | Security |

How many rows will the following query return?

```sql
SELECT DISTINCT department FROM employees;
```

And how many rows will this query return?

```sql
SELECT DISTINCT first_name, department FROM employees;
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:**
* **First Query (`department`):** Returns **3 rows** (`Security`, `Research`, `Operations`). It collapses all three 'Security' entries into one.
* **Second Query (`first_name, department`):** Returns **5 rows**.  
**Reason:** When multiple columns follow `DISTINCT`, PostgreSQL evaluates the **unique combination** of all projected columns across each row. Since each of the five rows has a unique `first_name`, none of the pairs are duplicates!
</details>

---

### Drill 5: Column Aliasing with Reserved Words or Spaces
Which of the following queries correctly aliases a column with a phrase containing a space?

```sql
-- Query A
SELECT salary * 1.10 AS new salary FROM employees;

-- Query B
SELECT salary * 1.10 AS 'new_salary' FROM employees;

-- Query C
SELECT salary * 1.10 AS "new salary" FROM employees;

-- Query D
SELECT salary * 1.10 AS [new salary] FROM employees;
```

<details>
<summary><b>Click to View Solution & Explanation</b></summary>

**Result:** **Query C: `AS "new salary"`.**  
**Reason:** In standard SQL and PostgreSQL:
* **Double quotes (`"..."`)** are used for identifier names (columns or tables) that contain spaces or special characters.
* **Single quotes (`'...'`)** are strictly for literal string text (e.g. `'Security'`).
* **Square brackets (`[...]`)** are Microsoft SQL Server syntax and will fail in PostgreSQL.
*(Pro Tip: While double quotes work, standard industry best practice is to avoid spaces altogether by using snake_case: `AS new_salary`)*.
</details>
