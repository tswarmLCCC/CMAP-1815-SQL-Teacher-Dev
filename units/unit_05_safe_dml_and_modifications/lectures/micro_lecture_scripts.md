# Unit 5: Micro-Lecture Video Scripts

This document contains recording scripts for **three bite-sized, topical micro-lectures** for Unit 5. Each video runs **6 to 9 minutes**, focusing on safe data modification workflows, transaction control, and temporary staging tables.

---

## Video 5.1: Anatomy of INSERT, Multi-Row Loading & Upserts
* **Duration:** ~7 minutes
* **Target Audience:** SQL students shifting from read queries (`SELECT`) to write queries (`INSERT`)
* **Accompanying SQL File:** `part1_insert_and_copy.sql`
* **On-Screen Assets:** Diagrams comparing explicit column lists vs. implicit table defaults; `psql` demonstration of `ON CONFLICT DO UPDATE`.

### Teleprompter & Delivery Script

**[0:00 - 1:30] The Hook: Entering the Write World**
> "Up until now, you've been a tourist in the database—reading books, examining charts, and running `SELECT` queries without leaving a footprint.
> 
> Starting today, you become an architect. You are going to write new rows, modify existing records, and delete outdated information.
> 
> That power comes with immense responsibility. In this video, we begin with the fundamental command for adding data: the **`INSERT`** statement."

**[1:31 - 3:45] The Explicit Column List Rule**
> "Here is how beginners often write an insert:
> `INSERT INTO products VALUES (50, 'Widget', 'Gadgets', 19.99, 10.00, 100, FALSE);`
> 
> In a professional engineering environment, this is strictly forbidden. Why?
> What happens next month when the DBA adds a `created_at` timestamp column to the middle of the table? Your query immediately breaks because the column positions no longer align!
> 
> **Always write an explicit column list:**
> ```sql
> INSERT INTO products (product_name, category, retail_price, stock_quantity)
> VALUES ('Ergonomic Mouse', 'Office Supplies', 49.99, 120);
> ```
> By explicitly declaring the columns, your query is resilient to schema changes. Any columns you omit will automatically receive their default value or `NULL`."

**[3:46 - 5:30] Batch Loading: INSERT INTO ... SELECT**
> "What if you need to load 5,000 records from another table? You don't write 5,000 individual insert statements. You use `INSERT INTO ... SELECT`:
> ```sql
> INSERT INTO products (product_name, category, retail_price)
> SELECT product_name, category, sales / quantity
> FROM superstore
> WHERE quantity > 0;
> ```
> PostgreSQL streams the query results directly into the destination table in a single high-speed operation."

**[5:31 - 7:15] The Upsert: ON CONFLICT**
> "What happens if you insert a product with an ID that already exists? PostgreSQL stops you with a unique constraint violation error.
> 
> But what if you want to update the existing record instead of crashing? We use an **Upsert**:
> ```sql
> INSERT INTO products (product_id, product_name, retail_price)
> VALUES (101, 'Upgraded Keyboard', 99.99)
> ON CONFLICT (product_id) 
> DO UPDATE SET 
>     product_name = EXCLUDED.product_name,
>     retail_price = EXCLUDED.retail_price;
> ```
> Notice the special keyword `EXCLUDED`. That refers to the new values you tried to insert. If a conflict occurs, PostgreSQL updates the existing row with those incoming values seamlessly.
> 
> In Video 5.2, we will look at the most dangerous commands in SQL: `UPDATE` and `DELETE`."

---

## Video 5.2: Safe UPDATE, DELETE & The RETURNING Clause
* **Duration:** ~8 minutes
* **Target Audience:** SQL developers needing defensive protocols to prevent accidental data destruction
* **Accompanying SQL File:** `part2_update_delete_and_returning.sql`
* **On-Screen Assets:** Warning alerts showing runaway updates; terminal demonstrating `RETURNING`.

### Teleprompter & Delivery Script

**[0:00 - 1:45] The Nightmare Scenario**
> "There is an old saying among database administrators: *'There are two types of developers: those who have accidentally updated all rows in a production table, and those who are about to.'*
> 
> Consider this query:
> `UPDATE employees SET salary = 100000;`
> Notice what is missing? There is no `WHERE` clause!
> In SQL, if you omit the `WHERE` clause, PostgreSQL doesn't ask *'Are you sure?'* It assumes you meant what you wrote, and modifies every single row in the entire company!
> 
> Today, we establish the **Golden Rule of Data Modification**."

**[1:46 - 4:20] The Pre-Validation Protocol**
> "Whenever you write an `UPDATE` or `DELETE`, follow this 3-step discipline:
> 
> **Step 1: Write a `SELECT` query first.**
> If management asks you to delete discontinued products that have zero stock:
> First, run:
> ```sql
> SELECT product_id, product_name, stock_quantity
> FROM products
> WHERE is_discontinued = TRUE AND stock_quantity = 0;
> ```
> Inspect the output. Are those 14 rows exactly what you intend to delete?
> 
> **Step 2: Convert the query to DELETE or UPDATE.**
> Replace `SELECT ...` with `DELETE`:
> ```sql
> DELETE FROM products
> WHERE is_discontinued = TRUE AND stock_quantity = 0;
> ```
> 
> **Step 3: Check the affected row count.**
> If your `SELECT` returned 14 rows, your `DELETE` must report `DELETE 14`. If it reports `DELETE 500`, you know immediately that something went wrong."

**[4:21 - 6:40] The RETURNING Clause**
> "In traditional SQL, when you execute an update or delete, the database only responds with a generic message: `UPDATE 5`.
> You can't see which rows were changed unless you run a second query.
> 
> PostgreSQL solves this with the powerful **`RETURNING`** clause:
> ```sql
> UPDATE employees
> SET salary = salary * 1.08
> WHERE department = 'Research'
> RETURNING employee_id, first_name, last_name, salary AS new_salary;
> ```
> With `RETURNING`, PostgreSQL immediately projects the modified rows back to your terminal, like a `SELECT` statement attached directly to your update!
> 
> You can use `RETURNING` on `INSERT`, `UPDATE`, and `DELETE`."

**[6:41 - 8:00] Summary & Next Steps**
> "Remember:
> 1. Never execute an `UPDATE` or `DELETE` without writing a `SELECT` first.
> 2. Always double-check your `WHERE` filter.
> 3. Use `RETURNING` to get real-time verification of the rows you mutated.
> 
> In Video 5.3, we'll learn how to wrap our modifications in ACID Transactions so you can safely undo your mistakes with a single command: `ROLLBACK`."

---

## Video 5.3: Transactions (ACID) & Temporary Staging Tables
* **Duration:** ~8 minutes
* **Target Audience:** Data engineers building multi-step ETL pipelines and staging workflows
* **Accompanying SQL File:** `part3_transactions_and_temp_tables.sql`
* **On-Screen Assets:** Transaction state diagram showing `BEGIN`, `COMMIT`, `ROLLBACK`; staging pipeline animation.

### Teleprompter & Delivery Script

**[0:00 - 1:40] What is an ACID Transaction?**
> "Imagine you go to an ATM to transfer $500 from your checking account to your savings account.
> The bank runs two SQL statements:
> 1. Deduct $500 from Checking.
> 2. Add $500 to Savings.
> 
> What happens if the power cuts out after statement 1, but before statement 2?
> Your $500 vanishes into thin air!
> 
> To prevent partial updates, databases provide **Transactions**. A transaction guarantees **Atomicity**: either all operations succeed together, or the database rolls back to the exact state it was in before anything started."

**[1:41 - 4:15] BEGIN, COMMIT, and ROLLBACK**
> "Here is how transactions work in PostgreSQL:
> ```sql
> BEGIN; -- Starts the private transaction sandbox
> 
> UPDATE employees 
> SET salary = salary * 1.10 
> WHERE department = 'Security';
> 
> -- Let's check our work:
> SELECT department, AVG(salary) FROM employees WHERE department = 'Security' GROUP BY department;
> ```
> At this moment, your changes are invisible to every other user on the system.
> If the results look correct:
> ```sql
> COMMIT; -- Permanently writes changes to disk
> ```
> But what if you realized you made an error?
> ```sql
> ROLLBACK; -- Completely aborts and undoes every change since BEGIN!
> ```
> `ROLLBACK` is your time machine. When doing manual data cleanup, always start with `BEGIN`."

**[4:16 - 6:30] Temporary Staging Tables (ETL Workflows)**
> "In data engineering, raw data arriving from external APIs or CSV files is almost always dirty: missing keys, invalid phone numbers, text inside price columns.
> 
> You should never dump dirty data directly into your production tables.
> Instead, we create a **Temporary Table**:
> ```sql
> CREATE TEMPORARY TABLE stage_inventory (
>     raw_sku VARCHAR(50),
>     raw_price VARCHAR(50),
>     raw_quantity VARCHAR(50)
> );
> ```
> Why use a temporary table?
> 1. It is completely isolated to your current connection session. Other users cannot see it.
> 2. It does not write to the persistent write-ahead log, so operations are blazing fast.
> 3. When your session ends or you disconnect, PostgreSQL automatically drops the table and frees the memory!"

**[6:31 - 8:00] Summary & Lab Preview**
> "In this week's lab, you will put all these safety mechanisms into practice:
> You will import a messy vendor batch into a temporary staging table, write SQL cleaning rules to scrub anomalies, execute safe multi-row upserts inside transaction blocks, and use `RETURNING` to audit your work. Let's dive in!"
