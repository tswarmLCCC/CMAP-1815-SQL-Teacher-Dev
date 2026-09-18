# CMAP-1815: Introduction to Modern SQL

# Master Course Document

---

## Part 1: Course Outcome Summary

### Course Information

**Description**

Gain a comprehensive introduction to Structured Query Language (SQL) combining traditional relational foundations with modern analytical techniques. Students will learn data retrieval, complex joins, subqueries, and advanced concepts including Common Table Expressions (CTEs), Window Functions, and data pivoting. The course emphasizes practical application, including schema design, safe data manipulation (DML), strict query validation protocols, and basic performance tuning.

**Total Credits:** 3 (Assumed based on 300 minutes/week)

**Course Format:** Blended/Flipped Hybrid (150 mins Direct Instruction / 150 mins Practical Lab per week)

**Course Duration:** 8 Weeks

### Course Competencies

#### 1. Construct Basic Data Retrieval and Filtering Queries (Weeks 1 & 2)

**Assessment Strategies**

1.1. Data Exploration Lab (Week 1)

1.2. Targeted Retrieval Lab (Week 2)

1.3. Midterm Exam

**Criteria**

*You will know you are successful when you:*

1.1. successfully authenticate and connect to a PostgreSQL database using a client tool like DBeaver.

1.2. navigate the database schema to identify tables, columns, and data types using the graphical interface.

1.3. correctly extract specific columns and rows from a single table.

1.4. apply appropriate formatting and mathematical operations within the SELECT clause.

1.5. utilize column aliases for output clarity.

1.6. restrict data output using single and multiple conditions (WHERE, AND, OR).

1.7. employ comparison operators, lists (IN), and pattern matching (LIKE) effectively.

1.8. identify and handle NULL values correctly.

1.9. sort results in ascending and descending order based on multiple criteria.

**Learning Objectives**

1.a. Describe the architecture of a database environment (Client tools vs. Server).

1.b. Navigate the DBeaver Object Explorer to discover database schemas and table structures.

1.c. Explain the purpose and syntax of the SELECT, FROM, WHERE, and ORDER BY clauses.

1.d. Differentiate between selecting all columns (\*) and specific columns.

1.e. Demonstrate the use of arithmetic operators and string concatenation.

1.f. Explain how boolean logic (AND/OR) evaluates multiple conditions.

1.g. Describe the challenges and specific syntax required when querying for NULL values.

#### 2. Integrate and Summarize Data from Multiple Sources (Weeks 3 & 4)

**Assessment Strategies**

2.1. Data Integration Lab (Week 3)

2.2. Business Reporting Lab (Week 4)

2.3. Midterm Exam

**Criteria**

*You will know you are successful when you:*

2.1. correctly join three or more tables to answer complex business questions.

2.2. select the appropriate join type (INNER, LEFT, RIGHT) based on data requirements and anomaly detection.

2.3. summarize large datasets using aggregate functions (COUNT, SUM, AVG, MIN, MAX).

2.4. group data effectively and filter grouped results using the HAVING clause.

2.5. combine disparate datasets using set operations (UNION, UNION ALL, INTERSECT, EXCEPT).

2.6. implement conditional aggregation (CASE within SUM/COUNT) to pivot row data into columns.

**Learning Objectives**

2.a. Trace relationships across an Entity Relationship Diagram (ERD).

2.b. Explain the mathematical difference between INNER and OUTER joins.

2.c. Differentiate between row-level filtering (WHERE) and group-level filtering (HAVING).

2.d. Differentiate between scalar functions and aggregate functions.

2.e. Explain the rules for column alignment when using UNION operators.

2.f. Describe the concept of pivoting data and its business use cases.

#### 3. Safely Manipulate Data and Validate Actions (Week 5)

*(Directly addresses Waukesha Competencies 2 & 3)*

**Assessment Strategies**

3.1. Data Cleanup Lab (Week 5)

3.2. Final Project (Week 8)

**Criteria**

*You will know you are successful when you:*

3.1. write INSERT statements using both VALUES and SELECT clauses.

3.2. write multi-conditional UPDATE and DELETE statements.

3.3. **Crucial:** write a SELECT statement *prior* to DML execution to identify target rows.

3.4. **Crucial:** compare row counts and write supporting post-execution queries to validate changes.

3.5. utilize local Temporary Tables (#Table) to stage data during multi-step processes.

**Learning Objectives**

3.a. Differentiate between Data Manipulation Language (DML) statements.

3.b. Explain the syntax and risks associated with each DML statement.

3.c. Explain why strict validation protocols are necessary in production environments.

3.d. Describe the workflow for validating that DML statements performed the correct actions.

3.e. Explain the scope and lifecycle of temporary tables.

#### 4. Apply Advanced Query Structuring and Analytics (Week 6)

**Assessment Strategies**

4.1. Advanced Analytics Lab (Week 6)

4.2. Final Project (Week 8)

**Criteria**

*You will know you are successful when you:*

4.1. refactor complex, nested subqueries into readable Common Table Expressions (CTEs).

4.2. apply Window Functions (OVER, PARTITION BY) to perform calculations across related rows.

4.3. utilize ranking functions (ROW_NUMBER, RANK) to order data within partitions.

4.4. calculate running totals and moving averages without using GROUP BY.

4.5. identify and deduplicate records using analytic functions.

**Learning Objectives**

4.a. Explain the syntax and purpose of the WITH clause (CTEs).

4.b. Describe how CTEs improve query readability and modularity compared to subqueries.

4.c. Differentiate the concept of a "Window" from a traditional GROUP BY aggregation.

4.d. Explain how the PARTITION BY clause isolates calculations within a window.

#### 5. Design Schemas and Enforce Data Integrity (Week 7)

*(Directly addresses Waukesha Competencies 4 & 5)*

**Assessment Strategies**

5.1. Schema Design Lab (Week 7)

5.2. Final Project (Week 8)

**Criteria**

*You will know you are successful when you:*

5.1. normalize flat, chaotic data into Third Normal Form (3NF).

5.2. write Data Definition Language (DDL) scripts (CREATE TABLE) selecting optimal data types.

5.3. write ALTER TABLE statements to enforce relationships and business rules.

5.4. define Primary Keys and Foreign Keys correctly based on ERD requirements.

5.5. implement CHECK, UNIQUE, and NOT NULL constraints to protect data integrity.

5.6. describe the purpose and use cases for programmable database objects like views, stored procedures, and user-defined functions.

**Learning Objectives**

5.a. Describe the normalization process and identify data in Normal Forms 0-3.

5.b. Describe the importance of Primary and Foreign keys in relational theory.

5.c. Explain the dangers of unnormalized tables and lack of constraints.

5.d. Differentiate between Data Definition Language (DDL) and DML.

5.e. Differentiate between tables, views, stored procedures, and user-defined functions.

5.f. Explain the high-level differences between OLTP (transactional) and OLAP (analytical/Data Warehouse) database structures.

#### 6. Understand Database Performance and Auditing (Week 8)

**Assessment Strategies**

6.1. Final Project Architecture Review (Week 8)

**Criteria**

*You will know you are successful when you:*

6.1. explain the basic function of a database index.

6.2. identify scenarios where indexing improves performance and where it degrades performance (during DML).

6.3. describe fundamental methods for tracking data changes over time (audit trails).

**Learning Objectives**

6.a. Differentiate between clustered and non-clustered index concepts.

6.b. Explain how an execution plan can aid in query optimization.

6.c. Describe the business need for data auditing and historical tracking.

---

## Part 2: Detailed Course Syllabus

### Structure Overview

**Format:** Blended/Flipped Hybrid. 4 periods per week (75 minutes each).

*   **Periods 1 & 2:** Direct Instruction / Guided Lab (150 minutes total in-class)

*   **Periods 3 & 4:** Independent Practical Application / Projects (150 minutes total outside class)

*   **Difficulty Rating:** Each lesson and lab activity includes a difficulty rating from **1 (Easiest)** to **5 (Hardest)** to assist with pacing and potential curriculum pruning.

### Week 1: 1_Intro_and_Select

**Focus:** Environment setup, understanding the relational model, and writing basic data retrieval statements.

*   **Period 1 (In-Class): Environment Setup & Database Basics** *(Difficulty: 2/5 - Technical setup can have hiccups)*

    *   What is a database? Client vs. Server architecture.

    *   Introduction to PostgreSQL and DBeaver.

    *   Authentication: Using usernames, passwords, and connection strings.

    *   Navigating the schema: locating databases, schemas, tables, and columns in the UI.

*   **Period 2 (In-Class): The `SELECT` Statement & Basic Formatting** *(Difficulty: 1/5 - Very straightforward syntax)*

    *   The structure of a SQL query (`SELECT`, `FROM`).

    *   Selecting specific columns vs. `SELECT *`.

    *   Basic arithmetic and string concatenation in the `SELECT` clause.

    *   Using column aliases (`AS`).

*   **Periods 3 & 4 (Independent): Data Exploration Lab**

    *   *Mastery Focus:* Navigating the environment and syntax fundamentals.

    *   *150-Minute Activity Breakdown:*

        *   **Environment & Navigation (45 mins):** *(Difficulty: 2/5)* Configure the PostgreSQL connection in DBeaver using provided credentials. Successfully connect and use the Object Explorer to navigate the database tree. Identify the target schema, view table data dictionaries, and document primary keys without writing code.

        *   **Guided Queries (45 mins):** *(Difficulty: 1/5)* Write 15-20 foundational queries. (e.g., "Retrieve a list of all employee names, combining first and last names into a single column named 'FullName'. Calculate a hypothetical 5% bonus for all salaried employees.")

        *   **Exploration Challenge (60 mins):** *(Difficulty: 2/5)* Students are given three broad business questions. They must determine which tables contain the necessary data and write the `SELECT` statements to extract that raw data, formatting the output logically.

### Week 2: 2_Filtering

**Focus:** Restricting data output using row-level criteria.

*   **Period 1 (In-Class): The `WHERE` Clause** *(Difficulty: 2/5)*

    *   Basic filtering (operators: `=`, `<`, `>`, `BETWEEN`).

    *   Filtering with lists (`IN`) and pattern matching (`LIKE`).

*   **Period 2 (In-Class): Advanced Filtering & Sorting** *(Difficulty: 3/5 - Boolean logic is tricky for some)*

    *   Handling `NULL` values (`IS NULL` / `IS NOT NULL`).

    *   Combining conditions with `AND` / `OR`.

    *   Ordering results with `ORDER BY` and limiting results (`LIMIT`/`TOP`).

*   **Periods 3 & 4 (Independent): Targeted Retrieval Lab**

    *   *Mastery Focus:* Precision in data extraction using complex logic.

    *   *150-Minute Activity Breakdown:*

        *   **Logic Drills (45 mins):** *(Difficulty: 3/5)* Practice combining multiple `AND`/`OR` conditions. Identify logic errors in pre-written, failing queries.

        *   **Pattern Matching Scenarios (45 mins):** *(Difficulty: 2/5)* Use `LIKE` and wildcards to find poorly formatted data (e.g., finding phone numbers missing area codes).

        *   **Business Reporting Challenge (60 mins):** *(Difficulty: 3/5)* Produce specific, ordered lists requiring combination of logic. (e.g., "Generate a report of the top 10 most expensive products in the 'Components' category that are currently in stock, ordered by price descending.")

### Week 3: 3_Joins

**Focus:** Bringing data together from multiple normalized tables.

*   **Period 1 (In-Class): Relational Concepts & Inner Joins** *(Difficulty: 3/5 - First major conceptual hurdle)*

    *   Understanding primary and foreign keys.

    *   `INNER JOIN`: Finding matching records across tables.

*   **Period 2 (In-Class): Outer Joins & Complex Joins** *(Difficulty: 4/5)*

    *   `LEFT JOIN` / `RIGHT JOIN`: Handling unmatched records.

    *   Joining more than two tables.

*   **Periods 3 & 4 (Independent): Data Integration Lab**

    *   *Mastery Focus:* Reconstructing normalized data into meaningful flat sets.

    *   *150-Minute Activity Breakdown:*

        *   **ERD Navigation (30 mins):** *(Difficulty: 2/5)* Trace relationships on a provided Entity Relationship Diagram to map the path between distant tables.

        *   **Join Mechanics (60 mins):** *(Difficulty: 4/5)* Write queries that require joining 3, 4, and 5 tables to answer a single question. (e.g., "List the Customer Name, Order Date, Product Name, and Sales Rep Name for all orders placed in Q1.")

        *   **The "Missing Data" Audit (60 mins):** *(Difficulty: 4/5)* Utilize `LEFT JOIN` and `IS NULL` to identify anomalies. (e.g., "Find all products in the catalog that have never been ordered.")

### Week 4: 4_Grouping_Set_Operation_and_Pivoting

**Focus:** Summarizing data and combining separate query results.

*   **Period 1 (In-Class): Aggregation & Grouping** *(Difficulty: 3/5)*

    *   Aggregate functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.

    *   Grouping data with `GROUP BY`.

    *   Filtering grouped data using the `HAVING` clause.

*   **Period 2 (In-Class): Set Operations & Basic Pivoting** *(Difficulty: 5/5 - Conditional aggregation is highly advanced for intro level)*

    *   Set operations: `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`.

    *   Introduction to conditional aggregation (using `CASE` inside aggregates) to pivot data.

*   **Periods 3 & 4 (Independent): Business Reporting Lab**

    *   *Mastery Focus:* Transforming granular data into executive summaries.

    *   *150-Minute Activity Breakdown:*

        *   **Summary Reports (45 mins):** *(Difficulty: 3/5)* Use `GROUP BY` and `HAVING`. (e.g., "Show total sales revenue by region, but only for regions that generated more than \$50,000.")

        *   **Set Operations (45 mins):** *(Difficulty: 2/5)* Use `UNION` to combine distinct datasets.

        *   **The Pivot Challenge (60 mins):** *(Difficulty: 5/5)* Take row-based data and use conditional aggregation to pivot it into column-based data. This requires synthesizing multiple concepts. *(Prime candidate for pruning if pacing is behind)*.

### Week 5: 5_Insert_Update_Delete_Temp_Tables

**Focus:** Modifying data safely and managing intermediate datasets.

*   **Period 1 (In-Class): DML & The Art of Validation** *(Difficulty: 3/5)*

    *   `INSERT INTO ... VALUES` vs. `INSERT INTO ... SELECT`.

    *   `UPDATE` and `DELETE`.

    *   *Crucial Skill:* Writing `SELECT` statements *before* `UPDATE`/`DELETE` to preview changes and validating post-execution.

*   **Period 2 (In-Class): Temporary Tables** *(Difficulty: 3/5)*

    *   Creating and using Local Temp Tables (`#Table`).

    *   When to use temp tables for complex, multi-step data transformations.

*   **Periods 3 & 4 (Independent): Data Cleanup Lab**

    *   *Mastery Focus:* Safe execution of DML and mastering the validation workflow.

    *   *150-Minute Activity Breakdown:*

        *   **Staging Data (30 mins):** *(Difficulty: 2/5)* Create a temporary table and populate it with a subset of data.

        *   **The Safe Update Protocol (60 mins):** *(Difficulty: 4/5)* Perform a complex update. *Requirement:* Submit the `SELECT` query used to identify the target rows, the `UPDATE` statement, and the subsequent `SELECT` query verifying the change.

        *   **Data Archiving (60 mins):** *(Difficulty: 4/5)* Use a multi-step process involving Temp Tables to archive and delete old records, documenting row counts at every step.

### Week 6: 6_Modularity_Window_Functions_and_CTE

**Focus:** Advanced query structuring and modern analytical tools.

*   **Period 1 (In-Class): Subqueries & Common Table Expressions (CTEs)** *(Difficulty: 4/5)*

    *   Brief review of subqueries.

    *   Introduction to the `WITH` clause (CTEs).

    *   Refactoring complex queries into readable, modular CTEs.

*   **Period 2 (In-Class): Window Functions** *(Difficulty: 5/5 - Heavy conceptual abstraction)*

    *   Concept of the "Window" vs. `GROUP BY`.

    *   The `OVER()` clause and `PARTITION BY`.

    *   Ranking functions: `ROW_NUMBER()`, `RANK()`.

*   **Periods 3 & 4 (Independent): Advanced Analytics Lab**

    *   *Mastery Focus:* Solving complex logic problems without messy nested queries.

    *   *150-Minute Activity Breakdown:*

        *   **Refactoring Exercise (45 mins):** *(Difficulty: 4/5)* Take a highly nested query and refactor it into a clean chain of CTEs.

        *   **Ranking & Deduplication (45 mins):** *(Difficulty: 4/5)* Use `ROW_NUMBER()` and `PARTITION BY` to rank items and filter out duplicates.

        *   **Running Totals & Moving Averages (60 mins):** *(Difficulty: 5/5)* Use Window Functions to calculate running totals and 7-day moving averages. *(Can be pruned if class is struggling with basic Window concepts)*.

### Week 7: 7_Schema_Design_Data_Integrity_DataWarehouse_Intro

**Focus:** Understanding database architecture, enforcing rules, and broad data concepts.

*   **Period 1 (In-Class): Design & Integrity** *(Difficulty: 4/5 - Normalization is highly theoretical)*

    *   The goals of Normalization (up to 3NF) and reading ERDs.

    *   Data Definition Language (DDL): `CREATE TABLE`, `ALTER`.

    *   Enforcing integrity: Primary Keys, Foreign Keys, `CHECK`, `UNIQUE`, `NOT NULL`.

*   **Period 2 (In-Class): Custom Database Objects & Intro to Data Warehousing** *(Difficulty: 3/5)*

    *   Overview of other database objects: Views (virtual tables), Stored Procedures, and User-Defined Functions (UDFs).

    *   OLTP vs. OLAP concepts.

    *   High-level overview of Star Schemas.

*   **Periods 3 & 4 (Independent): Schema Design Lab**

    *   *Mastery Focus:* Translating raw requirements into a structured, protected database schema.

    *   *150-Minute Activity Breakdown:*

        *   **The Denormalized Nightmare (45 mins):** *(Difficulty: 4/5)* Normalize a chaotic, flat spreadsheet into 3NF.

        *   **DDL Scripting (60 mins):** *(Difficulty: 3/5 - Easy concepts, syntax-heavy)* Write the `CREATE TABLE` scripts to build the normalized schema.

        *   **Enforcing the Rules (30 mins):** *(Difficulty: 3/5)* Write `ALTER TABLE` statements to add keys and constraints.

        *   **Custom Objects (15 mins):** *(Difficulty: 2/5)* Create a simple View that encapsulates a complex, multi-table query to simplify reporting for end-users.

### Week 8: 8_Performance_Indexing_and_Audit_Trails

**Focus:** Optimizing queries, tracking changes, and final assessment.

*   **Period 1 (In-Class): Performance & Indexing Basics** *(Difficulty: 3/5)*

    *   What is an Index?

    *   How indexes speed up queries (and when they slow down DML).

    *   Reading basic execution plans.

*   **Period 2 (In-Class): Audit Trails & Final Project Kickoff** *(Difficulty: 2/5)*

    *   Concepts of tracking data changes.

    *   Final project requirements and architecture review.

*   **Periods 3 & 4 (Independent): Final Project Execution**

    *   *Mastery Focus:* Comprehensive synthesis of all course competencies.

    *   *150-Minute Activity Breakdown:*

        *   **Project Execution (150 mins):** *(Difficulty: 5/5)* Design a small schema (Week 7), populate it using DML (Week 5), and write a series of complex analytical queries requiring Joins, CTEs, and Window Functions (Weeks 3 & 6) to answer specific business objectives.