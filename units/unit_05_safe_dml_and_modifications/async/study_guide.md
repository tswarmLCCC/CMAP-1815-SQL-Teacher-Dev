# Unit 5 Asynchronous Study Guide: Safe DML, Transactions & Staging Tables

**Estimated Preparation Time:** 150 Minutes  
**Prerequisites:** Units 1–4 (Relational Schema, Selection, JOINs, Aggregations)  
**Target Competencies:** Data Manipulation Language (DML), ACID Transactions, Pre-Validation Protocols, Temporary Tables

---

## 1. Overview & Learning Objectives
Welcome to Unit 5! You are transitioning from reading relational data (`SELECT`) to mutating data stored permanently on disk (`INSERT`, `UPDATE`, `DELETE`). Because careless modification can corrupt or destroy production data, Unit 5 focuses heavily on **defensive database engineering**: pre-execution validation queries, ACID transaction control, upserts, and temporary staging workflows.

By the end of this study guide, you will be able to:
1. Write explicit, resilient `INSERT INTO` statements and multi-row batch inserts.
2. Execute atomic upserts using PostgreSQL's `ON CONFLICT DO UPDATE` syntax.
3. Apply the **3-Step Pre-Execution Protocol** to guarantee safe `UPDATE` and `DELETE` queries.
4. Capture before-and-after values in real time using the `RETURNING` clause.
5. Manage transaction boundaries (`BEGIN`, `COMMIT`, `ROLLBACK`) to enforce ACID consistency.
6. Isolate and scrub messy incoming data using `CREATE TEMPORARY TABLE`.

---

## 2. Required Video Curriculum (FreeCodeCamp Master Course)
Watch the following chapters from the official FreeCodeCamp PostgreSQL Master Class. These timestamps reflect the authoritative video description chapters:

* 🎥 **Insert Into & Examples:** [0:55:55](https://www.youtube.com/watch?v=qw--VYLpxG4&t=3355s) – Basic syntax, explicit column lists, inserting records.
* 🎥 **How to Delete Records:** [2:54:45](https://www.youtube.com/watch?v=qw--VYLpxG4&t=10485s) – Safe deletion and using the `WHERE` clause.
* 🎥 **How to Update Records:** [3:01:36](https://www.youtube.com/watch?v=qw--VYLpxG4&t=10896s) – Modifying existing columns safely.
* 🎥 **On Conflict & Upserts:** [3:05:55](https://www.youtube.com/watch?v=qw--VYLpxG4&t=11155s) – Handling duplicate key collisions with `DO NOTHING` and `DO UPDATE`.

---

## 3. Required Reading & Tutorials (PostgreSQLTutorial.com)
Complete the following modules on PostgreSQLTutorial.com:

1. [PostgreSQL INSERT Tutorial](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-insert/)  
   *Focus on:* Explicit column mapping and inserting multiple rows in a single statement.
2. [PostgreSQL UPDATE Guide](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-update/)  
   *Focus on:* Using expressions in `SET` and returning updated values with `RETURNING`.
3. [PostgreSQL DELETE Guide](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-delete/)  
   *Focus on:* Filtering targets with `WHERE` and soft deletes vs. hard deletes.
4. [PostgreSQL Transactions Tutorial](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-transaction/)  
   *Focus on:* ACID properties, `BEGIN`, `COMMIT`, and `ROLLBACK`.
5. [PostgreSQL Temporary Tables](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-temporary-table/)  
   *Focus on:* Session-scoped staging tables and why they disappear upon disconnect.

---

## 4. Key Architectural Mental Models

### A. The 3-Step Pre-Execution Protocol
Never run an `UPDATE` or `DELETE` directly. Always follow this protocol:
```
Step 1: Write a SELECT statement with your exact intended WHERE clause.
        Verify that the returned rows and row count match expectations.
Step 2: Wrap your modification in a transaction:
        BEGIN;
        UPDATE ... (or DELETE ...) RETURNING *;
Step 3: If the returned rows look correct: COMMIT;
        If anything went wrong: ROLLBACK;
```

### B. ACID Properties of Transactions
* **Atomicity:** All changes in the block succeed, or none do.
* **Consistency:** The database never violates primary keys, foreign keys, or check constraints.
* **Isolation:** Uncommitted changes are invisible to other concurrent user sessions.
* **Durability:** Once `COMMIT` returns success, the changes survive power outages and crashes.

---

## 5. Summary Reference Cards

| Command / Clause | Purpose | Example |
| :--- | :--- | :--- |
| `INSERT INTO` | Adds new rows with explicit column lists | `INSERT INTO products (name, price) VALUES ('Pen', 1.99);` |
| `ON CONFLICT` | Handles key collisions (Upsert) | `ON CONFLICT (id) DO UPDATE SET price = EXCLUDED.price;` |
| `UPDATE` | Modifies existing column values in place | `UPDATE employees SET salary = salary * 1.05 WHERE id = 10;` |
| `DELETE` | Purges matching rows permanently | `DELETE FROM products WHERE stock_quantity = 0;` |
| `RETURNING` | Returns modified rows immediately | `DELETE FROM products WHERE id = 5 RETURNING *;` |
| `BEGIN` / `ROLLBACK` | Starts transaction / aborts all changes | `BEGIN; UPDATE ...; ROLLBACK;` |
| `TEMP TABLE` | Scratchpad table isolated to session | `CREATE TEMPORARY TABLE stage_data (...);` |

---

## 6. Pre-Class Checklist
Before attending the synchronous classroom session:
- [ ] Watch all 4 video chapters (0:55:55, 2:54:45, 3:01:36, 3:05:55).
- [ ] Read the 5 PostgreSQLTutorial.com guides.
- [ ] Complete the **5 Formative Self-Check Drills** in `self_check_drills.md`.
- [ ] Ensure you understand how `EXCLUDED` works in `ON CONFLICT`.


---

---

## Step 6: Learn with AI — Interactive Practice & Prompt Craft (100% Free Tools)

### Role & Persona: The Database Disaster Recovery Lead (Reliability SRE)
* **Pedagogical Technique:** Chaos Engineering & Transaction Rollback Drills
* **Core Goal:** Practice safe data modification, transaction control (BEGIN, COMMIT, ROLLBACK), and ETL staging tables by having the AI inject simulated production crashes and data corruption threats.
* **Recommended Free Tools:** ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot *(Zero subscription or paid API key required)*

#### Copy-and-Paste AI Prompt Template
```text
Act as a Database Reliability Engineer (SRE). We are running critical data maintenance and ETL pipeline updates on a live production PostgreSQL 16 database.
I will write DML scripts (INSERT, UPDATE, DELETE) using temporary staging tables, explicit transactions (BEGIN, COMMIT, ROLLBACK), and RETURNING clauses.
Your role:
1. Act as the safety reviewer: Red-team every query I write. If I write an UPDATE or DELETE without a verified WHERE clause, or without running inside a transaction, reject it with a catastrophic failure scenario.
2. Introduce unexpected runtime anomalies (e.g., 'Constraint violation on row 452!', 'Network timeout during bulk insert!').
3. Force me to demonstrate how my transaction script rolls back cleanly leaving zero orphaned records.
Start by presenting me with our first maintenance mission: Purging inactive users while archiving their billing records into an audit staging table.
```

#### Step-by-Step Interactive Drill
1. Paste the prompt and inspect the maintenance mission.
2. Wrap your DML in a defensive transaction block (BEGIN; ... ROLLBACK;) with RETURNING verification.
3. Respond to the AI's simulated runtime failure by demonstrating a clean rollback.
4. Refactor the script to use a staging table before committing.

#### Asynchronous Participation Deliverable
> **Canvas Discussion Prompt:**
> Post to the Unit 5 Discussion: (1) The disaster scenario simulated by the AI, (2) The safe transaction script you engineered, and (3) The safety difference between modifying live tables directly vs. staging transformations in a temporary table.
