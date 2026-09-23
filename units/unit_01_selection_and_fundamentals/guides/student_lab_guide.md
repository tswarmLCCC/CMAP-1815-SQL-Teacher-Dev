# Unit 1 Student Lab Guide: Data Exploration & Orientation

## Lab Objective
In this lab, you will:
1. Connect to your live PostgreSQL 16 server in **GitHub Codespaces**.
2. Query system catalogs to inspect server version, current user, and database structure.
3. Write clean, formatted `SELECT` statements with column projection, aliases, math expressions, string concatenation, `DISTINCT`, and multi-column `ORDER BY`.

---

## Submission Instructions
1. Open your personal GitHub Codespace.
2. In the terminal or editor, write your solutions in a file named `lab1_yourname.sql`.
3. Test every query to ensure it executes without syntax errors!
4. Check that all keywords are in **UPPERCASE** and clauses are on new lines.
5. Commit and push your changes to your repository.

---

## Lab Challenges

### Part 1: Environment & System Catalogs (20 Points)
1. **Server Version:** Write a query to display the exact version of PostgreSQL running on your server.
2. **Current Session:** Write a query to display your current active database user and the database name you are connected to.
3. **Table Discovery:** Query the `information_schema.tables` catalog to list all base table names in the `public` schema, sorted alphabetically by table name.
4. **Column Inspector:** Query `information_schema.columns` to find all column names and data types for the `employees` table, sorted by `ordinal_position`.

---

### Part 2: Precision Projection & Data Exploration (40 Points)
5. **Staff Directory:** From the `employees` table, retrieve the `first_name`, `last_name`, and `title`. Sort alphabetically by `last_name`.
6. **Executive Compensation Roster:** Retrieve the `first_name`, `last_name`, and `salary` of all employees. Sort from highest paid to lowest paid.
7. **Unique Departments:** Write a query that returns a list of all distinct departments in the company, sorted alphabetically from A to Z.
8. **Department-Title Roster:** Find all unique combinations of `department` and `title` across the company. Order by department first, then by title.

---

### Part 3: Expressions, Aliases & Mathematical Projections (40 Points)
9. **Polished Full Name:** Write a query against `employees` that combines `first_name` and `last_name` into a single column aliased as `full_name` using string concatenation (`||`), along with their `department`. Sort by `department` ascending, then by `full_name` ascending.
10. **Bonus Simulation:** Many employees receive an annual bonus. Write a query against `employees` displaying:
    - `last_name`
    - `salary` (aliased as `base_salary`)
    - `bonus` (aliased as `annual_bonus`)
    - A calculated column adding `salary + bonus` aliased as `total_compensation`.  
    *(Note: For employees with no bonus, what happens? Observe this result for our Unit 2 discussion!)*
11. **Retail Product Margins:** From the `products` table, retrieve:
    - `product_name`
    - `retail_price`
    - `cost_to_produce`
    - A calculated column `retail_price - cost_to_produce` aliased as `estimated_unit_profit`.  
    Sort the results so the most profitable products appear first.
12. **Inventory Value Analysis:** From `products`, project:
    - `product_name`
    - `stock_quantity`
    - `retail_price`
    - A calculated column `stock_quantity * retail_price` aliased as `total_inventory_value`.  
    Sort from the highest inventory value to lowest.
