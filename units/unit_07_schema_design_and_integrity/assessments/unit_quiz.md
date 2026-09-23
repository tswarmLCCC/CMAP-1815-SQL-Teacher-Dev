# Unit 7 Assessment: Schema Design, DDL & Data Integrity Quiz

**Total Questions:** 15  
**Points Possible:** 30 (2 points per question)  
**Time Limit:** 30 Minutes  
**Format:** Multiple Choice & Code Analysis  
**Aligned Learning Outcomes:** CLO 5, Competencies 5.1–5.4

---

## Part 1: Conceptual Foundations & Normalization (Questions 1–5)

### Question 1
In relational database design, what requirement must be satisfied for a table to be in **First Normal Form (1NF)**?
* A) The table must have at least three foreign key relationships.
* B) Every column must contain only atomic (indivisible) scalar values, and there must be no repeating groups or multivalued attributes.
* C) Every table must have an auto-incrementing integer primary key named `id`.
* D) All text columns must be stored as `VARCHAR(255)`.

---

### Question 2
What is a **Partial Functional Dependency**, and which Normal Form explicitly prohibits it?
* A) A non-key attribute depends on another non-key attribute; prohibited by 1NF.
* B) A non-key attribute depends on only a portion of a composite primary key; prohibited by 2NF.
* C) A foreign key references a non-existent table; prohibited by 3NF.
* D) A table has more than 10 columns; prohibited by Boyce-Codd Normal Form.

---

### Question 3
What is a **Transitive Dependency**, and which Normal Form explicitly eliminates it?
* A) An attribute depends on the primary key via another non-key attribute ($X \rightarrow Y \rightarrow Z$); eliminated by 3NF.
* B) An attribute depends on multiple parent tables simultaneously; eliminated by 1NF.
* C) A table contains both uppercase and lowercase column names; eliminated by 2NF.
* D) A foreign key uses `ON DELETE CASCADE`; eliminated by 4NF.

---

### Question 4
What is the core difference between `ON DELETE RESTRICT` and `ON DELETE CASCADE` in a foreign key constraint?
* A) `RESTRICT` prevents deletion of a parent record if child records exist; `CASCADE` automatically deletes all associated child records when the parent record is deleted.
* B) `CASCADE` archives child records to a backup file; `RESTRICT` permanently deletes them.
* C) `RESTRICT` allows child records to have negative values; `CASCADE` sets them to zero.
* D) There is no difference; they are interchangeable keywords in PostgreSQL.

---

### Question 5
What is a SQL **View**?
* A) A physical table stored on an external SSD drive to optimize read operations.
* B) A saved query definition stored in the database catalog that presents virtual rows and columns dynamically upon execution.
* C) A temporary table that is deleted as soon as a transaction commits.
* D) A graphical user interface dashboard in pgAdmin.

---

## Part 2: DDL Syntax & Constraint Engineering (Questions 6–10)

### Question 6
Look at the following DDL statement:
```sql
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    salary NUMERIC(10,2) CHECK (salary >= 30000.00)
);
```
What happens if an application executes `INSERT INTO staff (email, salary) VALUES ('dev@work.com', 25000.00);`?
* A) The row is inserted, but `salary` is automatically rounded up to $30,000.00.
* B) The insert fails with an error indicating that the row violates the `CHECK` constraint.
* C) The row is inserted into a temporary error table.
* D) The salary is inserted as `NULL`.

---

### Question 7
Which constraint type automatically enforces both `UNIQUE` and `NOT NULL` in relational databases?
* A) `FOREIGN KEY`
* B) `PRIMARY KEY`
* C) `CHECK`
* D) `DEFAULT`

---

### Question 8
Why should foreign key constraints generally be explicitly named (e.g. `CONSTRAINT fk_orders_customer FOREIGN KEY ...`) rather than declared anonymously?
* A) PostgreSQL runs named constraints 50% faster than anonymous constraints.
* B) Named constraints produce clear, readable error messages in application logs when referential integrity violations occur.
* C) Anonymous constraints are automatically dropped during server restarts.
* D) PostgreSQL does not support anonymous constraints.

---

### Question 9
Examine the following table definition:
```sql
CREATE TABLE inventory (
    sku VARCHAR(20) PRIMARY KEY,
    stock INT NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 10
);
```
If a user executes `INSERT INTO inventory (sku) VALUES ('SKU-99');`, what values will `stock` and `reorder_level` receive?
* A) `NULL` and `NULL`
* B) `0` and `10`
* C) An error will occur because `stock` and `reorder_level` were omitted.
* D) `0` and `0`

---

### Question 10
Look at this statement:
```sql
DROP TABLE customers CASCADE;
```
What does the `CASCADE` keyword accomplish here?
* A) It deletes the table and automatically drops all dependent database objects, including foreign keys and views referencing this table.
* B) It creates a backup copy of `customers` before deleting it.
* C) It empties the table's rows while keeping the table definition intact.
* D) It rolls back the drop operation if any other user is currently connected.

---

## Part 3: Applied Architecture & Schema Scenarios (Questions 11–15)

### Question 11
Consider a university spreadsheet with columns:
`student_id`, `student_name`, `class_code`, `class_name`, `instructor_name`, `instructor_office`.
If `instructor_office` depends directly on `instructor_name` rather than the primary key `(student_id, class_code)`, what type of anomaly occurs if an instructor moves offices?
* A) Insertion Anomaly
* B) Update Anomaly (Modifying the instructor's office requires updating multiple student enrollment rows)
* C) Deletion Anomaly
* D) Network Timeout Anomaly

---

### Question 12
How should a Many-to-Many relationship between `students` and `courses` be modeled in a 3NF relational database?
* A) Store a comma-separated list of course codes in the `students` table.
* B) Add 10 separate columns to `students`: `course_1`, `course_2`, ..., `course_10`.
* C) Create an intermediate associative junction table (e.g. `enrollments`) containing foreign keys to both `students` and `courses`.
* D) Combine students and courses into a single 50-column mega-table.

---

### Question 13
A developer wants to create a View that provides analysts access to customer orders without exposing customer credit card numbers. Which statement represents this design?
* A) Create a view selecting only non-sensitive columns (`customer_id`, `order_id`, `order_date`, `total_amount`) from the underlying tables, and grant analysts permissions on the view.
* B) Encrypt the entire database disk.
* C) Delete the credit card column from the production table.
* D) Add a `CHECK` constraint to the credit card column.

---

### Question 14
What is the effect of dropping a View using `DROP VIEW v_customer_orders;`?
* A) All customer and order rows in the underlying physical tables are permanently deleted.
* B) Only the saved query definition of the view is removed from the catalog; physical table data remains completely untouched.
* C) The underlying tables are converted to unlogged tables.
* D) The view is moved to the recycle bin.

---

### Question 15
Which SQL constraint guarantees that a column only accepts one of four specific values: `'Pending'`, `'Approved'`, `'Shipped'`, or `'Cancelled'`?
* A) `UNIQUE ('Pending', 'Approved', 'Shipped', 'Cancelled')`
* B) `CHECK (status IN ('Pending', 'Approved', 'Shipped', 'Cancelled'))`
* C) `FOREIGN KEY (status) DEFAULT 'Pending'`
* D) `PRIMARY KEY (status)`

---

# Answer Key & Pedagogical Rationales

| Q# | Correct Answer | Rationale / Explanation |
| :---: | :---: | :--- |
| **1** | **B** | First Normal Form requires atomic values: every attribute must contain a single scalar value. Multivalued lists or repeating groups violate 1NF. |
| **2** | **B** | Second Normal Form eliminates partial functional dependencies, where a non-key attribute depends on only part of a composite primary key. |
| **3** | **A** | Third Normal Form eliminates transitive dependencies, where non-key attributes depend on other non-key attributes rather than solely on the primary key. |
| **4** | **A** | `ON DELETE RESTRICT` enforces referential integrity by blocking parent deletion if child rows exist. `ON DELETE CASCADE` propagates deletion downward to child rows. |
| **5** | **B** | A View is a virtual table defined by a stored query. It calculates results on demand without storing redundant physical rows. |
| **6** | **B** | The `CHECK (salary >= 30000.00)` constraint intercepts the insert at the storage layer and immediately rejects the invalid value ($25,000). |
| **7** | **B** | Relational primary keys inherently enforce both uniqueness and non-nullability for entity identification. |
| **8** | **B** | Explicitly naming constraints (`CONSTRAINT fk_name ...`) produces clear error logs in production, pinpointing the exact business rule violated. |
| **9** | **B** | Because explicit defaults were defined in the DDL (`DEFAULT 0` and `DEFAULT 10`), omitting those columns automatically supplies the default values. |
| **10** | **A** | `CASCADE` on `DROP TABLE` automatically drops all foreign keys, views, and dependent triggers referencing the dropped table. |
| **11** | **B** | Because `instructor_office` is repeated across every student enrollment row, updating an office location requires modifying multiple records, creating an Update Anomaly. |
| **12** | **C** | Many-to-Many relationships must be resolved using a junction/associative table with foreign keys referencing each parent entity. |
| **13** | **A** | Views provide column masking: projecting only authorized columns while withholding sensitive attributes (credit cards, SSNs) from unauthorized roles. |
| **14** | **B** | A view is merely a stored query; dropping it deletes only the catalog metadata, leaving all underlying table data intact. |
| **15** | **B** | `CHECK (column IN (...))` provides domain constraint enforcement, restricting column inputs to an approved set of categorical literals. |
