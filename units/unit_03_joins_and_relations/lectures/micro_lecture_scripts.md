# Unit 3: Micro-Lecture Video Scripts

This document contains recording scripts for **three bite-sized, topical micro-lectures** for Unit 3. Each video runs **7 to 9 minutes**, focusing on relational architecture, join mechanics, and anomaly detection.

---

## Video 3.1: Relational Theory & The Primary/Foreign Key Bridge
* **Duration:** ~7 minutes
* **Target Audience:** SQL learners connecting separate tables for the first time
* **Accompanying SQL File:** `part1_keys_and_inner_join.sql`
* **On-Screen Assets:** ERD graphic showing `locations` $\leftrightarrow$ `employees`, terminal with `psql`.

### Teleprompter & Delivery Script

**[0:00 - 2:00] The Core Problem: Why Can't Everything Be in One Table?**
> "Welcome to Unit 3. Up to now, every query we've written has pulled data from a single filing cabinet—either `employees` or `products`.
> 
> But real enterprise data is normalized across dozens or hundreds of tables. Why?
> 
> Imagine if every time an employee was hired in our Cheyenne headquarters, we typed 'Cheyenne', 'WY', 'Headquarters', the office manager's name, and the building square footage directly into their employee row.
> 
> What happens if the headquarters moves across town? You have to run an update on 500 individual rows. If you miss three of them, your database is corrupted with conflicting data. In database theory, this is called an **Update Anomaly**.
> 
> To solve this, we store information about the Cheyenne facility *once* in a table called `locations`. And inside `employees`, we store a single integer pointer: `location_id`."

**[2:01 - 4:30] Primary Keys vs. Foreign Keys**
> "Let's establish two definitions that are the bedrock of database engineering:
> 
> 1. **Primary Key (PK):** A column in a table that uniquely identifies each individual record in *that* table. In `locations`, `location_id` is the primary key. Location 1 is Cheyenne. Location 2 is Laramie. No two locations can ever have the same ID, and a primary key can never be `NULL`.
> 
> 2. **Foreign Key (FK):** A column in a table that points directly to the Primary Key of *another* table. In our `employees` table, `location_id` is a foreign key.
> 
> When Harry Dresden has `location_id = 1`, that integer is a literal bridge connecting Harry to the entire row of data for Cheyenne in the `locations` table."

**[4:31 - 7:00] The First INNER JOIN**
> "How do we cross that bridge in SQL? With the **`INNER JOIN`**:
> 
> ```sql
> SELECT 
>     e.first_name, 
>     e.last_name, 
>     l.city, 
>     l.state
> FROM employees e
> INNER JOIN locations l 
>     ON e.location_id = l.location_id;
> ```
> Look at the syntax:
> 1. `FROM employees e`: We assign a 1-letter alias `e` to `employees`.
> 2. `INNER JOIN locations l`: We name the second table and alias it `l`.
> 3. `ON e.location_id = l.location_id`: This is the **Join Condition**. It tells PostgreSQL: *'Line up an employee row with a location row only when their location IDs match!'*
> 
> In Video 3.2, we'll see how to chain three or four tables together in a single query."

---

## Video 3.2: Multi-Table Joins & The Cartesian Product Trap
* **Duration:** ~8 minutes
* **Target Audience:** Intermediate learners querying complex relational networks
* **Accompanying SQL File:** `part2_multi_table_joins.sql`
* **On-Screen Assets:** Diagram showing `orders` $\rightarrow$ `order_lines` $\rightarrow$ `products`.

### Teleprompter & Delivery Script

**[0:00 - 2:00] Chaining Multiple Tables**
> "Welcome back. In production software, answering a single business question often requires joining three, four, or five tables.
> 
> Look at our retail schema:
> * `orders` knows *when* an order happened and *who* placed it.
> * But `orders` doesn't know what items were purchased. That lives in `order_lines`!
> * And `order_lines` has the product ID and quantity, but it doesn't know the human-readable product name. That lives in `products`!
> 
> To see customer orders with product names, we must traverse a chain of two bridges:
> `orders` $\rightarrow$ `order_lines` $\rightarrow$ `products`."

**[2:01 - 5:15] Writing the Multi-Table Query**
> "[Demonstrating live in editor]:
> ```sql
> SELECT 
>     o.order_id,
>     o.order_date,
>     p.product_name,
>     ol.quantity,
>     ol.unit_price,
>     ol.quantity * ol.unit_price AS line_total
> FROM orders o
> INNER JOIN order_lines ol 
>     ON o.order_id = ol.order_id
> INNER JOIN products p 
>     ON ol.product_id = p.product_id
> ORDER BY o.order_id ASC;
> ```
> Notice how clean this is:
> Each `INNER JOIN` adds another table to our working set, and each `ON` clause provides the specific key bridge.
> 
> Also notice: every column in the `SELECT` clause is prefixed with its table alias (`o.`, `p.`, `ol.`).
> **Teaching Tip:** If two joined tables both contain a column named `status` or `created_at`, typing `SELECT status` will crash your query with an `ambiguous column reference` error. Always prefix your columns with their table alias!"

**[5:16 - 7:45] The Disaster of the Cartesian Product**
> "What happens if a developer forgets the `ON` clause, or writes an old-style comma join like `FROM orders, order_lines` without a `WHERE` filter?
> 
> You trigger a **Cartesian Product** (or `CROSS JOIN`).
> 
> In a Cartesian product, the database pairs every single row in Table A with every single row in Table B.
> * If Table A has 10,000 rows and Table B has 10,000 rows, your query returns **100,000,000 rows**!
> * The server's memory spikes, disk fills up, and your query can lock the production database.
> 
> Always use explicit ANSI SQL `INNER JOIN ... ON` syntax. It forces you to declare the matching logic every single time."

---

## Video 3.3: Outer Joins & The Missing Data Audit (Anti-Joins)
* **Duration:** ~8 minutes
* **Target Audience:** Analysts detecting business anomalies and orphaned records
* **Accompanying SQL File:** `part3_outer_joins_and_antijoins.sql`
* **On-Screen Assets:** Venn diagram showing matched vs. unmatched rows, `NULL` padding graphic.

### Teleprompter & Delivery Script

**[0:00 - 2:30] The Blind Spot of INNER JOIN**
> "Welcome to Video 3.3. Here is the hidden danger of `INNER JOIN`:
> **It only shows records that successfully match on both sides.**
> 
> Suppose your CEO asks: *'Show me a list of all products in our catalog and their total sales.'*
> If you write an `INNER JOIN` between `products` and `order_lines`, any product that has **never been sold** will vanish from the report completely!
> 
> Why? Because an unsold product has no matching row in `order_lines`.
> 
> If you want to keep **100% of the products**, regardless of whether they have ever appeared in an order, you need a **`LEFT JOIN`** (or Left Outer Join)."

**[2:31 - 5:15] How LEFT JOIN Works**
> "In a `LEFT JOIN`:
> 1. The table on the **LEFT** (the one in the `FROM` clause) is the **Master Table**. Every single row from this table will appear in your result set.
> 2. The table on the **RIGHT** (the one named in `LEFT JOIN`) matches where it can.
> 3. For any left-side row with no match on the right, PostgreSQL automatically fills in the right-side columns with **`NULL`**.
> 
> ```sql
> SELECT 
>     p.product_name,
>     ol.order_id,
>     ol.quantity
> FROM products p
> LEFT JOIN order_lines ol 
>     ON p.product_id = ol.product_id;
> ```
> If 'Heavy Duty Steel Bracket' has never been ordered, its name still shows up, with `NULL` under `order_id` and `quantity`!"

**[5:16 - 8:00] The Anti-Join: Isolating Inactive Data**
> "Now here is a technique used daily by database engineers: **The Anti-Join**.
> 
> What if the inventory manager says: *'I don't want to see all products. I ONLY want to see the products that have NEVER been ordered so we can put them on clearance.'*
> 
> You combine a `LEFT JOIN` with an `IS NULL` filter:
> ```sql
> SELECT 
>     p.product_name, 
>     p.sku, 
>     p.stock_quantity
> FROM products p
> LEFT JOIN order_lines ol 
>     ON p.product_id = ol.product_id
> WHERE ol.order_line_id IS NULL;
> ```
> Think about what this does:
> 1. The `LEFT JOIN` pulls all products and pairs them with sales lines.
> 2. For unsold products, `ol.order_line_id` is filled with `NULL`.
> 3. The `WHERE ol.order_line_id IS NULL` filter discards every product that was sold, leaving **only** the unsold inventory on your screen!
> 
> This is how companies find inactive customers, students who haven't registered, or orphaned database records.
> 
> Let's hop into our Codespace and run these live queries!"
