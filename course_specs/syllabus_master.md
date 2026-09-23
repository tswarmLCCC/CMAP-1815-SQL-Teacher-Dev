# CMAP 1815: Master Syllabus & 8-Week Hybrid Schedule

## Course Structure: The 300-Minute Hybrid Model
Each week is budgeted for **300 minutes of total structured instructional engagement**, precisely divided into:
- **150 Minutes of Asynchronous Guided Learning**:
  - Bite-sized video micro-lectures (5–10 mins each).
  - Targeted PostgreSQL readings & FreeCodeCamp video chapters (see [Master External Resources Guide](file:///c:/dev/CMAP_1815_Autogen/course_specs/external_resources_guide.md)).
  - Formative self-check knowledge checks before class.
- **150 Minutes of Synchronous Active Learning & Practical Lab**:
  - Either **two 75-minute sessions** (e.g., Tuesday/Thursday) or **one 150-minute block**.
  - Instructor live-coding demonstrations and concept reinforcement.
  - Paired coding lab exercises and debriefing.
- *(Independent homework/capstone study occurs outside these 300 instructional contact minutes).*

---

## 8-Week Master Schedule

### Week 1: Selection, Relational Foundations & AI Data Grounding
* **Theme**: The Relational Model, Projection ("The Flashlight"), and Environment Setup.
* **Difficulty Rating**: 1–2 / 5
* **Async Guided Study (150 min)**:
  - Micro-Video 1.1: The Relational Metaphor & RAG Data Grounding (8 min).
  - Micro-Video 1.2: The Anatomy of SELECT, FROM & Semicolon Rules (7 min).
  - Micro-Video 1.3: Column Projection, Aliases & Mathematical Expressions (8 min).
  - Micro-Video 1.4: Removing Duplicates (DISTINCT) & Sorting (ORDER BY) (7 min).
  - Readings: Neon PostgreSQL Tutorial, SELECT, ORDER BY, DISTINCT.
  - Self-Check: 5-question pre-class check.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Codespaces setup, `psql` shell, schema exploration via `information_schema`.
  - Session 2 (75 min): Live coding SELECT queries, column aliases, math operations, and ORDER BY drills.
  - Lab Activity: Data Exploration & System Catalogs Lab (`week1_orientation.sql`).
* **Deliverable**: Lab 1 SQL Script + Unit 1 Quiz.

### Week 2: Targeted Retrieval, Pattern Matching & Three-Valued Logic
* **Theme**: Precision Filtering ("The Scalpel") and Boolean Logic Gates.
* **Difficulty Rating**: 2–3 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: WHERE clause mechanics; Pattern matching (`LIKE`, wildcards `%`, `_`); Three-Valued Logic (`IS NULL` vs `= NULL`); LIMIT & FETCH.
  - Readings: Neon WHERE, LIKE, IN, BETWEEN, IS NULL, LIMIT.
  - Self-Check: Evaluating truth tables with NULLs.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Complex WHERE conditions, operator precedence (AND before OR).
  - Session 2 (75 min): Targeted data extraction and wildcards in practice.
  - Lab Activity: The Census & Server Log Audit Lab.
* **Deliverable**: Lab 2 SQL Script + Unit 2 Quiz.

### Week 3: Relational Interconnectivity (Joins)
* **Theme**: Entity Relationships, Primary/Foreign Key Bridges, and Anomaly Detection.
* **Difficulty Rating**: 3–4 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: ERD Navigation; INNER JOIN mechanics; Outer Joins (LEFT, RIGHT, FULL); The Anti-Join pattern (`LEFT JOIN ... WHERE key IS NULL`).
  - Readings: Neon Joins, INNER JOIN, LEFT JOIN, Table Aliases.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): 2-table and 3-table INNER JOINs; table aliasing best practices.
  - Session 2 (75 min): Outer joins and identifying missing customer/product relationships.
  - Lab Activity: 4-Table Superstore Integration & Missing Records Audit.
* **Deliverable**: Lab 3 SQL Script + Unit 3 Quiz.

### Week 4: Summarization, Aggregations & Pivoting
* **Theme**: Transforming Granular Rows into Executive Summaries.
* **Difficulty Rating**: 3–5 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Aggregate Functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`); The `GROUP BY` boundary; `WHERE` vs `HAVING`; Set Operations (`UNION`); Introduction to Conditional Aggregation (`CASE` inside `SUM`).
  - Readings: Neon GROUP BY, HAVING, Aggregate Functions, UNION.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Aggregation patterns and common `GROUP BY` compilation errors.
  - Session 2 (75 min): Set operations and conditional aggregation matrix pivoting.
  - Lab Activity: Executive Business Reporting & Pivoting Lab (Midterm Checkpoint).
* **Deliverable**: Lab 4 SQL Script + Unit 4 Quiz.

### Week 5: Safe Data Manipulation (DML) & Temporary Tables
* **Theme**: Safe Data Engineering and Validation Protocols.
* **Difficulty Rating**: 3–4 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Anatomy of INSERT (VALUES vs SELECT); The Dangerous UPDATE & DELETE; The Golden Rule: Pre-Execution SELECTs; Staging with Temporary Tables (`TEMP TABLE`).
  - Readings: Neon INSERT, UPDATE, DELETE, RETURNING.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Transaction blocks (`BEGIN`, `COMMIT`, `ROLLBACK`) and safe DML execution.
  - Session 2 (75 min): Staging tables and multi-step data transformation workflows.
  - Lab Activity: Data Cleanup & Safe Modification Protocol Lab.
* **Deliverable**: Lab 5 SQL Script + Unit 5 Quiz.

### Week 6: Query Modularity, CTEs & Window Functions
* **Theme**: Modern Analytical SQL: Readable CTEs and Partitioned Windows.
* **Difficulty Rating**: 4–5 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Subqueries vs CTEs (`WITH`); The OVER() clause & `PARTITION BY`; Ranking functions (`ROW_NUMBER`, `RANK`); Running totals and moving averages.
  - Readings: Neon CTE, Window Functions.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Refactoring messy subqueries into sequential CTE pipelines.
  - Session 2 (75 min): Window functions for cumulative metrics and deduplication.
  - Lab Activity: Advanced Analytics & Deduplication Lab.
* **Deliverable**: Lab 6 SQL Script + Unit 6 Quiz.

### Week 7: Schema Design, DDL & Data Integrity
* **Theme**: Architectural Blueprints, Normalization (1NF–3NF), and Constraint Enforcement.
* **Difficulty Rating**: 3–4 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: Normalization from spreadsheet chaos to 3NF; DDL (`CREATE TABLE`, `ALTER TABLE`); Enforcing integrity (PK, FK, CHECK, UNIQUE, NOT NULL); Views (`CREATE VIEW`).
  - Readings: Neon CREATE TABLE, Data Types, Constraints, Views.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Normalization workshop; identifying functional dependencies.
  - Session 2 (75 min): Writing rock-solid DDL scripts and declaring foreign keys.
  - Lab Activity: "The Denormalized Nightmare" DDL & Views Lab.
* **Deliverable**: Lab 7 DDL Script + Unit 7 Quiz.

### Week 8: Query Performance, Indexing & Capstone Defense
* **Theme**: Query Optimization, B-Tree Indexes, Audit Trails & Comprehensive Capstone.
* **Difficulty Rating**: 2–5 / 5
* **Async Guided Study (150 min)**:
  - Micro-Videos: How Indexes Work (B-Trees); The Write Penalty (Index overhead on DML); Reading `EXPLAIN` query trees; Audit trails and change tracking.
  - Readings: Neon Indexes, EXPLAIN.
* **Sync Active Lab (150 min)**:
  - Session 1 (75 min): Query performance profiling and index tuning clinic.
  - Session 2 (75 min): Capstone Architecture Review & Defense Presentations.
  - Lab Activity: Comprehensive Capstone Project Execution.
* **Deliverable**: Capstone Project Submission + Unit 8 Quiz.
