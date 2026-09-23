# Unit 7: Instructor Lecture Notes & Pedagogical Guide

## Module Overview & Objectives
Unit 7 transitions students into relational software architecture. Students learn to recognize data anomalies (insertion, update, deletion anomalies) in denormalized flat files and decompose them into Boyce-Codd / Third Normal Form (3NF) structures. They implement these designs using PostgreSQL Data Definition Language (DDL), enforce enterprise business rules with declarative constraints (`PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE`, `NOT NULL`), and provide secure reporting abstractions using `CREATE VIEW`.

### Aligned Course Learning Outcomes
* **CLO 5:** Design normalized relational schemas (1NF through 3NF), write DDL scripts, declare integrity constraints, and create views for data abstraction and security.
* **CLO 1 & 3:** Enforce relational integrity and translate enterprise domain models into performant database structures.

---

## 1. Pedagogical Roadmap & Common Student Traps

### A. The Three Normal Forms (Teaching Intuition)
* **1NF (Atomicity):** No multivalued columns (e.g. no comma-separated skills or phone numbers) and no repeating groups.
* **2NF (No Partial Dependencies):** Only relevant when tables have composite primary keys. Every non-key column must depend on the *entire* primary key, not a sub-part.
* **3NF (No Transitive Dependencies):** Non-key columns cannot depend on other non-key columns.
* **Mnemonic:** *"The Key, the Whole Key, and Nothing But the Key, so help me Codd."*
  * The Key = 1NF (identifiable entity)
  * The Whole Key = 2NF (no partial dependencies)
  * Nothing But the Key = 3NF (no transitive dependencies)

### B. Foreign Key Referential Actions
* **The Concept:** What happens to child records when a parent record is deleted or updated?
  * `ON DELETE RESTRICT` (or `NO ACTION`): Throws an error; deletion blocked. Safest default for financial/core entities.
  * `ON DELETE CASCADE`: Deletes child rows automatically. Dangerous if applied broadly, but useful for pure line-item associations (e.g. `order_lines` when `orders` is deleted).
  * `ON DELETE SET NULL`: Preserves child record while unlinking foreign key (requires nullable foreign key).

### C. Constraint Best Practices
* **Naming Constraints Explicitly:** Always urge students to name constraints (`CONSTRAINT fk_orders_customer ...`, `CONSTRAINT chk_positive_salary ...`) rather than letting PostgreSQL generate anonymous names like `orders_customer_id_fkey`. Explicit names make debugging error logs trivial.

### D. Views: Virtual Tables
* **The Concept:** Views do not store physical copies of data (unlike Materialized Views); they store query execution plans.
* **Security & Encapsulation:** Explain how views provide row-level and column-level security (e.g. masking SSNs or restricting a branch manager to their own region's rows).

---

## 2. In-Class Live Coding & Demonstration Script

### Demo 1: Normalization Workshop (`part1_normalization_and_1nf_to_3nf.sql`)
1. Present a single denormalized table `legacy_clinic_records`.
2. Identify anomalies: updating a doctor's office requires touching 1,000 patient visit rows.
3. Decompose step-by-step into `patients`, `doctors`, and `appointments`.

### Demo 2: DDL Scripting & Constraint Traps (`part2_ddl_and_constraints.sql`)
1. Write a clean `CREATE TABLE` script with `SERIAL PRIMARY KEY`, `CHECK`, and `FOREIGN KEY`.
2. Deliberately attempt an invalid insert (violating `CHECK` or `UNIQUE`) to show PostgreSQL catching the error.
3. Deliberately attempt to delete a referenced parent row to trigger `ON DELETE RESTRICT`.

### Demo 3: View Creation & Data Masking (`part3_views_and_abstractions.sql`)
1. Create a joined view aggregating customer metrics.
2. Query the view like a regular table, showing that joins are abstracted away.
3. Create a restricted security view omitting confidential compensation columns.

---

## 3. Formative Check Questions (Think-Pair-Share)
1. *If a table's primary key consists of a single column (e.g. `product_id`), can it ever violate Second Normal Form (2NF)?*
   * Answer: No! A partial dependency requires a composite (multi-column) key. A table in 1NF with a single-column primary key is automatically in 2NF.
2. *Does dropping a database View delete the data in the underlying tables?*
   * Answer: No. A view is merely a stored query definition; dropping it leaves the underlying table rows intact.
