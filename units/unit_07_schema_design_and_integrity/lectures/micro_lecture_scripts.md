# Unit 7: Micro-Lecture Video Scripts

This document contains recording scripts for **three bite-sized, topical micro-lectures** for Unit 7. Each video runs **6 to 9 minutes**, focusing on relational normalization (1NF–3NF), DDL constraints, and architectural abstraction via Views.

---

## Video 7.1: The Three Normal Forms (1NF to 3NF)
* **Duration:** ~8 minutes
* **Target Audience:** SQL developers moving from data querying to database schema modeling
* **Accompanying SQL File:** `part1_normalization_and_1nf_to_3nf.sql`
* **On-Screen Assets:** Visual spreadsheet with repeating comma-separated groups decomposing step-by-step into 1NF, 2NF, and 3NF relational tables.

### Teleprompter & Delivery Script

**[0:00 - 1:45] The Hook: The Spreadsheet Nightmare**
> "Every bad database starts life as a spreadsheet.
> 
> Imagine a company tracking orders in an Excel sheet:
> In row 1, we have Customer Name: 'Alice', Customer Phone: '555-0100', and in the Items column: 'Mouse, Keyboard, Monitor'.
> 
> What happens if Alice changes her phone number? You have to update 50 separate rows. If you miss one, Alice has two different phone numbers in your system. That is an **Update Anomaly**.
> What happens if Alice deletes her only order? Her entire contact information vanishes from the database! That is a **Deletion Anomaly**.
> 
> To eliminate these anomalies, relational theory gives us **Database Normalization**."

**[1:46 - 4:10] 1NF and 2NF: Atomicity & Composite Keys**
> "Let's climb the normalization ladder:
> 
> **First Normal Form (1NF): Atomic Values.**
> 1NF states that every cell must hold a single, indivisible scalar value.
> Storing `'Mouse, Keyboard, Monitor'` in a single cell violates 1NF! You cannot join or index individual items. To reach 1NF, every item gets its own distinct row.
> 
> **Second Normal Form (2NF): No Partial Dependencies.**
> 2NF applies when a table has a composite primary key (a primary key made of multiple columns, like `order_id` and `product_id`).
> In 2NF, every non-key column must depend on the **entire** composite key, not just part of it.
> For instance, if `product_name` is stored in the `order_items` table, it depends only on `product_id`, not `order_id`! To reach 2NF, we extract products into their own table."

**[4:11 - 6:30] Third Normal Form (3NF): The Key, The Whole Key, and Nothing But the Key**
> "Now, the gold standard of enterprise schema design: **Third Normal Form (3NF)**.
> 3NF states: The table must be in 2NF, and have **no transitive dependencies**.
> 
> What is a transitive dependency?
> Suppose in an `employees` table, we store:
> `employee_id`, `name`, `department_id`, and `department_head_name`.
> Notice that `department_head_name` depends on `department_id`, which in turn depends on `employee_id`.
> That is a transitive dependency!
> If the department head changes, you have to update 500 employee records!
> To reach 3NF, we move departments to a separate `departments` table.
> 
> As the famous database oath goes: *'Every non-key attribute must provide a fact about the key, the whole key, and nothing but the key, so help me Codd!'*"

**[6:31 - 8:00] Summary & Transition**
> "By normalizing to 3NF, you eliminate redundancy and guarantee data consistency.
> In Video 7.2, we will write the Data Definition Language commands to turn these blueprints into real PostgreSQL tables with ironclad constraints."

---

## Video 7.2: DDL Syntax & Ironclad Integrity Constraints
* **Duration:** ~8 minutes
* **Target Audience:** Developers building production tables using DDL and constraint rules
* **Accompanying SQL File:** `part2_ddl_and_constraints.sql`
* **On-Screen Assets:** Schema blueprint diagram; error demonstration when violating a `CHECK` or `FOREIGN KEY` constraint in `psql`.

### Teleprompter & Delivery Script

**[0:00 - 1:40] Constraints: Defense at the Storage Layer**
> "Many software engineers make a fatal mistake: they assume the frontend web app will validate all data.
> But what happens when someone writes an automated script, or an analyst runs a direct bulk load, or a bug bypasses the frontend validation?
> 
> If the database doesn't stop invalid data, bad data **will** corrupt your tables.
> The database is the final line of defense. Today, we enforce data integrity using **DDL Constraints**."

**[1:41 - 4:15] Declaring Constraints in CREATE TABLE**
> "Let's examine a rock-solid table definition:
> ```sql
> CREATE TABLE customers (
>     customer_id SERIAL PRIMARY KEY,
>     email VARCHAR(255) NOT NULL UNIQUE,
>     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
> );
> ```
> Notice what we declared:
> * `PRIMARY KEY`: Guarantees uniqueness and automatically enforces `NOT NULL`.
> * `NOT NULL`: Prevents missing required fields.
> * `UNIQUE`: Ensures no two customers share the same email address.
> * `DEFAULT`: Automatically supplies values if omitted."

**[4:16 - 6:40] Foreign Keys & Referential Actions**
> "Now let's link tables together with a Foreign Key:
> ```sql
> CREATE TABLE orders (
>     order_id SERIAL PRIMARY KEY,
>     customer_id INT NOT NULL,
>     total_amount NUMERIC(10,2) NOT NULL,
>     CONSTRAINT fk_orders_customer
>         FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
>         ON DELETE RESTRICT,
>     CONSTRAINT chk_positive_total
>         CHECK (total_amount >= 0.00)
> );
> ```
> Look at `CHECK (total_amount >= 0.00)`. If an application tries to insert a negative order amount, PostgreSQL immediately rejects the query with an error!
> 
> And look at `ON DELETE RESTRICT`:
> If a rogue script tries to delete a customer who has existing orders, PostgreSQL refuses to delete the customer, preventing orphaned order records!"

**[6:41 - 8:00] Summary & Next Steps**
> "When you design tables with strict constraints, you make it mathematically impossible for invalid or orphaned data to enter your database.
> In Video 7.3, we'll learn how to present these complex normalized tables to users and apps cleanly using Views."

---

## Video 7.3: Database Views & Architectural Abstraction
* **Duration:** ~7 minutes
* **Target Audience:** Database architects designing security boundaries and simplified data models
* **Accompanying SQL File:** `part3_views_and_abstractions.sql`
* **On-Screen Assets:** Architectural diagram showing underlying tables masked behind virtual view layers.

### Teleprompter & Delivery Script

**[0:00 - 1:30] The Challenge of Normalization**
> "In Video 7.1, we broke apart our messy spreadsheet into four distinct 3NF tables: customers, orders, order_lines, and products.
> 
> From an engineering standpoint, this is pure perfection: zero redundancy, zero anomalies.
> But from the perspective of a business analyst or a frontend developer, querying four joined tables just to see who bought what is tedious and error-prone.
> 
> How do we maintain normalized integrity under the hood while providing simple, user-friendly access to reporting tools?
> The answer is **Database Views**."

**[1:31 - 4:00] What is a View?**
> "A View is essentially a stored SQL query saved inside the database that behaves exactly like a virtual table:
> ```sql
> CREATE OR REPLACE VIEW v_customer_order_summary AS
> SELECT 
>     c.customer_id,
>     c.full_name,
>     c.email,
>     COUNT(o.order_id) AS total_orders,
>     COALESCE(SUM(o.total_amount), 0.00) AS lifetime_spend
> FROM customers c
> LEFT JOIN orders o ON c.customer_id = o.customer_id
> GROUP BY c.customer_id, c.full_name, c.email;
> ```
> Once created, an analyst doesn't need to write complex joins. They simply query:
> `SELECT * FROM v_customer_order_summary WHERE lifetime_spend > 1000;`!
> PostgreSQL runs the underlying view definition on the fly."

**[4:01 - 6:15] Security & Column Masking**
> "Views are also an indispensable security tool.
> Suppose your `employees` table contains confidential data: `ssn`, `birth_date`, `home_address`, and `salary`.
> You need the department managers to see their staff roster, but they must not see SSNs:
> ```sql
> CREATE OR REPLACE VIEW v_manager_staff_roster AS
> SELECT employee_id, first_name, last_name, department, job_title
> FROM employees;
> ```
> You grant managers `SELECT` permissions on `v_manager_staff_roster` while completely blocking access to the underlying `employees` table. The sensitive columns are completely shielded!"

**[6:16 - 7:30] Wrap-Up & Lab Preview**
> "In this week's lab, you will take a heavily denormalized, broken spreadsheet dataset, analyze its dependencies, normalize it into a pristine 3NF schema with primary keys, foreign keys, and check constraints, and build executive reporting views on top. Let's build!"
