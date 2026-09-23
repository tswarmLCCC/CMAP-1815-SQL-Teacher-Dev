# Unit 7 Lab Rubric: Normalized Schema Design & Constraint Architecture

**Total Points:** 100  
**Submission Format:** Single verified DDL SQL script (`lab7_submission.sql`) executed against PostgreSQL 16.

---

## Grading Criteria Breakdown

| Dimension | Points Possible | Exemplary (100%) | Proficient (80%) | Developing (60%) | Unsatisfactory (0%) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Task 1: Relational Decomposition (3NF)** | 25 | Correctly decomposes flat dataset into 3NF entities; resolves many-to-many relationships via junction table; no transitive dependencies. | 3NF structure mostly achieved; minor redundant column retained. | Partial dependency remains (violates 2NF) or composite key flawed. | Unnormalized flat table submitted. |
| **Task 2: Primary & Foreign Key Integrity** | 25 | Correctly declares `PRIMARY KEY` on every entity; establishes `FOREIGN KEY` constraints with appropriate referential action (`RESTRICT`/`CASCADE`). | Keys declared, but referential actions omitted or anonymous constraint names used. | Foreign keys missing data type alignment or invalid references. | Missing primary or foreign keys. |
| **Task 3: Domain Check & Unique Constraints** | 20 | Explicitly names and configures `CHECK` constraints (positive numbers, status enums) and `UNIQUE` constraints (emails/SKUs). | Constraints function, but anonymous names used or minor condition gap. | Incomplete validation logic or syntax errors. | Constraints omitted. |
| **Task 4: Constraint Stress Testing** | 15 | Provides documented test statements attempting to insert invalid data, proving PostgreSQL rejects the violations. | Tests present, but missing comment explanations of expected errors. | Incomplete test coverage. | Tests omitted. |
| **Task 5: Security & Analytical View Creation** | 15 | Creates `CREATE OR REPLACE VIEW` that encapsulates joins and hides sensitive data; queries view cleanly. | View functions, but omits column alias or formatting polish. | View logic incomplete or fails to query. | View omitted. |

---

## Deduction Penalties
* **-10 Points:** Lowercase keywords (SQL Style Guide violation).
* **-10 Points:** Syntax errors preventing script execution in `psql`.
* **-5 Points:** Anonymous constraints without explicit naming conventions.
