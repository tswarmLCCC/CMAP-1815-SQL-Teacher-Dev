# Unit 7 Asynchronous Study Guide: Schema Design, DDL & Integrity

**Estimated Preparation Time:** 150 Minutes  
**Prerequisites:** Units 1–6 (Foundations, Selection, Joins, Aggregation, Safe DML, CTEs)  
**Target Competencies:** Relational Normalization (1NF–3NF), DDL Scripting, Integrity Constraints (`PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE`), Views

---

## 1. Overview & Learning Objectives
Welcome to Unit 7! In this unit, you transition from querying databases to designing and engineering relational database schemas. You will learn the theoretical principles of normalization to eliminate data redundancy and anomalies, implement table structures using PostgreSQL Data Definition Language (DDL), enforce enterprise business rules using declarative constraints, and create Views for data security and simplified reporting.

By the end of this study guide, you will be able to:
1. Identify insertion, update, and deletion anomalies in flat, unnormalized files.
2. Decompose denormalized data step-by-step into First (1NF), Second (2NF), and Third Normal Form (3NF).
3. Write clean, production-ready DDL scripts (`CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`).
4. Enforce referential integrity using Foreign Keys and configure referential actions (`RESTRICT`, `CASCADE`, `SET NULL`).
5. Enforce domain integrity using `CHECK`, `UNIQUE`, `NOT NULL`, and `DEFAULT` constraints.
6. Create virtual tables using `CREATE OR REPLACE VIEW` for security masking and reporting encapsulation.

---

## 2. Required Video Curriculum (FreeCodeCamp Master Course)
Watch the following chapters from the official FreeCodeCamp PostgreSQL Master Class. These timestamps reflect the authoritative video description chapters:

* 🎥 **How To Create Tables:** [0:41:37](https://www.youtube.com/watch?v=qw--VYLpxG4&t=2497s) – DDL basics, data types, and table structures.
* 🎥 **Creating Tables with Constraints:** [0:49:12](https://www.youtube.com/watch?v=qw--VYLpxG4&t=2952s) – Declaring constraints at table creation.
* 🎥 **Adding Primary Keys:** [2:36:26](https://www.youtube.com/watch?v=qw--VYLpxG4&t=9386s) – Primary key constraints and identity enforcement.
* 🎥 **Unique Constraints:** [2:40:55](https://www.youtube.com/watch?v=qw--VYLpxG4&t=9655s) – Preventing duplicate emails and business identifiers.
* 🎥 **Check Constraints:** [2:49:15](https://www.youtube.com/watch?v=qw--VYLpxG4&t=10155s) – Restricting value ranges and allowed categorical states.
* 🎥 **Serial & Sequences:** [3:50:42](https://www.youtube.com/watch?v=qw--VYLpxG4&t=13842s) – Auto-incrementing primary key generators.

---

## 3. Required Reading & Tutorials (PostgreSQLTutorial.com)
Complete the following modules on PostgreSQLTutorial.com:

1. [PostgreSQL CREATE TABLE](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-table/)  
   *Focus on:* Column data types and table creation syntax.
2. [PostgreSQL Primary Key](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-primary-key/)  
   *Focus on:* Uniqueness and automatic `NOT NULL` enforcement.
3. [PostgreSQL Foreign Key](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-foreign-key/)  
   *Focus on:* Referential actions: `ON DELETE RESTRICT` vs. `ON DELETE CASCADE`.
4. [PostgreSQL CHECK Constraint](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-check-constraint/)  
   *Focus on:* Enforcing numerical limits and enum-style categorical checks.
5. [PostgreSQL CREATE VIEW](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-views/)  
   *Focus on:* Encapsulating multi-table joins into virtual tables.

---

## 4. Key Architectural Mental Models

### A. The Three Normal Forms
```
Unnormalized Flat File: Contains multivalued lists and repeated data groups.
           |
       [ 1NF ] --> Atomic values only. No comma-separated lists. Every cell is indivisible.
           |
       [ 2NF ] --> In 1NF + No partial dependencies on composite primary keys.
           |
       [ 3NF ] --> In 2NF + No transitive dependencies (Non-key columns cannot depend on non-key columns).
```
**The Relational Mnemonic:** *"Every non-key attribute must depend on the Key, the Whole Key, and Nothing But the Key, so help me Codd!"*

### B. Foreign Key Referential Actions
* **`ON DELETE RESTRICT` (Default):** Rejects deletion of a parent row if child rows exist. Prevents orphaned records.
* **`ON DELETE CASCADE`:** Automatically deletes all dependent child rows when a parent row is deleted.
* **`ON DELETE SET NULL`:** Unlinks child rows by setting their foreign key column to `NULL`.

---

## 5. Summary Reference Cards

| Constraint / Clause | Purpose | Example |
| :--- | :--- | :--- |
| `PRIMARY KEY` | Unique identifier; enforces NOT NULL | `id SERIAL PRIMARY KEY` |
| `FOREIGN KEY` | Enforces referential integrity to parent | `REFERENCES customers(id) ON DELETE RESTRICT` |
| `CHECK (condition)` | Validates business rules at storage layer | `CHECK (salary >= 0.00)` |
| `UNIQUE` | Guarantees column values are distinct | `email VARCHAR(255) UNIQUE` |
| `DEFAULT` | Auto-supplies value if omitted | `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP` |
| `CREATE VIEW` | Virtual table encapsulating a query | `CREATE VIEW v_active_users AS SELECT ...;` |

---

## 6. Pre-Class Checklist
Before attending the synchronous classroom session:
- [ ] Watch the 6 video chapters on DDL, constraints, and sequences.
- [ ] Read the 5 PostgreSQLTutorial.com guides.
- [ ] Complete the **5 Formative Self-Check Drills** in `self_check_drills.md`.
- [ ] Review the difference between 2NF (partial dependency) and 3NF (transitive dependency).
