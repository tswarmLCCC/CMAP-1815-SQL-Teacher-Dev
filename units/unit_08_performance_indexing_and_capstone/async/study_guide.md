# Unit 8 Asynchronous Study Guide: Performance Tuning, Indexing & Capstone

**Estimated Preparation Time:** 150 Minutes  
**Prerequisites:** Units 1–7 (Complete foundational and advanced relational curriculum)  
**Target Competencies:** Query Profiling (`EXPLAIN ANALYZE`), B-Tree Indexing, Index Overhead ("Write Penalty"), Audit Logging, Capstone Synthesis

---

## 1. Overview & Learning Objectives
Welcome to Unit 8! In this final unit of CMAP 1815, you transition from querying and schema design to query performance optimization and enterprise capstone execution. You will master the PostgreSQL cost-based query planner, evaluate `EXPLAIN` execution plans, implement B-Tree and composite indexing strategies, manage index write penalties, and integrate every discipline learned this semester into a comprehensive Capstone Project.

By the end of this study guide, you will be able to:
1. Profile queries using `EXPLAIN` and `EXPLAIN ANALYZE` to interpret execution nodes, costs, and timings.
2. Distinguish between Sequential Scans (`Seq Scan`), Index Scans (`Index Scan`), and Bitmap Index Scans.
3. Understand the internal architecture of B-Tree indexes and evaluate search complexity ($O(\log N)$).
4. Analyze the **Write Penalty**: how excessive indexing degrades `INSERT`, `UPDATE`, and `DELETE` performance.
5. Create single-column, composite, and partial indexes tailored to real-world query workloads.
6. Design an enterprise audit trail schema to track regulatory state modifications.
7. Defend architectural and optimization decisions in the comprehensive Course Capstone.

---

## 2. Required Video Curriculum (FreeCodeCamp Master Course)
Watch the following chapters from the official FreeCodeCamp PostgreSQL Master Class. These timestamps reflect the authoritative video description chapters:

* 🎥 **Exporting Query Results to CSV:** [3:47:27](https://www.youtube.com/watch?v=qw--VYLpxG4&t=13647s) – Extracting datasets for external reporting.
* 🎥 **Indexing & EXPLAIN Walkthrough:** Review the video demonstrations in the [PostgreSQL Tutorial Indexes Guide](https://www.postgresqltutorial.com/postgresql-indexes/) and [PostgreSQL EXPLAIN Guide](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-explain/).

---

## 3. Required Reading & Tutorials (PostgreSQLTutorial.com)
Complete the following modules on PostgreSQLTutorial.com:

1. [PostgreSQL EXPLAIN Guide](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-explain/)  
   *Focus on:* Understanding `Seq Scan`, `Cost`, `Actual Time`, and loops.
2. [PostgreSQL Indexes Overview](https://www.postgresqltutorial.com/postgresql-indexes/)  
   *Focus on:* When to create an index and how indexes speed up searches.
3. [PostgreSQL CREATE INDEX](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-index/)  
   *Focus on:* B-Tree index creation syntax and best practices.
4. [PostgreSQL Composite Index](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-composite-index/)  
   *Focus on:* Leading column rules and multi-column query filtering.
5. [Official PostgreSQL Documentation: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)  
   *Focus on:* Interpreting execution trees and buffer cache hits.

---

## 4. Key Architectural Mental Models

### A. The Cost-Based Query Planner
PostgreSQL evaluates multiple execution pathways before executing a query.
```
  SQL Query String
         |
    [ Parser ]  --> Checks SQL syntax
         |
    [ Rewriter ] --> Applies Views and rule transformations
         |
    [ Planner / Optimizer ] --> Evaluates costs of Seq Scan vs. Index Scan
         |
    [ Executor ] --> Executes the lowest-cost plan on disk pages
```

### B. The Index Trade-off: Read Speed vs. Write Penalty
* **Read Advantage:** Reduces disk page reads from $O(N)$ to $O(\log N)$.
* **Write Penalty:** Every index on a table must be re-balanced whenever an `INSERT`, `UPDATE`, or `DELETE` occurs.
* **Golden Rule:** Never index blindly. Index columns that appear frequently in `WHERE`, `JOIN ON`, and `ORDER BY` clauses with high selectivity.

---

## 5. Summary Reference Cards

| Command / Option | Purpose | Example |
| :--- | :--- | :--- |
| `EXPLAIN query` | Displays estimated query plan without running | `EXPLAIN SELECT * FROM emp;` |
| `EXPLAIN ANALYZE query` | Runs query and shows real execution timings | `EXPLAIN ANALYZE SELECT * FROM emp;` |
| `CREATE INDEX` | Builds a B-Tree index on a column | `CREATE INDEX idx_emp_dept ON emp(dept);` |
| Composite Index | Builds index on multiple columns | `CREATE INDEX idx_name ON emp(dept, salary);` |
| Partial Index | Indexes only rows matching a condition | `CREATE INDEX idx_act ON emp(sal) WHERE active;` |
| `DROP INDEX` | Removes an index to restore write performance | `DROP INDEX idx_emp_dept;` |

---

## 6. Pre-Class Checklist
Before attending the final synchronous classroom session:
- [ ] Read the PostgreSQLTutorial guides on `EXPLAIN` and Indexes.
- [ ] Complete the **5 Formative Self-Check Drills** in `self_check_drills.md`.
- [ ] Review your previous assignments (Units 1–7) in preparation for Capstone defense.


---

---

## Step 6: Learn with AI — Interactive Practice & Prompt Craft (100% Free Tools)

### Role & Persona: The Senior Performance DBA & Capstone Defense Panel
* **Pedagogical Technique:** Execution Plan Profiling & Technical Architecture Defense
* **Core Goal:** Subject your capstone project architecture, indexing decisions, and query execution plans (EXPLAIN ANALYZE) to a rigorous technical defense panel.
* **Recommended Free Tools:** ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot *(Zero subscription or paid API key required)*

#### Copy-and-Paste AI Prompt Template
```text
Act as a demanding Database Administrator (DBA) and Technical Review Board conducting my final Capstone Defense for CMAP 1815.
I have built a complete PostgreSQL database system with a normalized schema, DDL constraints, ETL transaction pipeline, analytical window queries, and B-Tree indexes.
Conduct a 10-minute technical defense simulation:
1. Ask me to provide one of my heaviest analytical queries and explain what EXPLAIN ANALYZE reveals about it (Seq Scan vs. Index Scan, Cost, Execution Time).
2. Challenge me to defend my B-Tree indexing strategy: Explain composite index column order (Leftmost Prefix rule) and the Write Penalty on INSERT/UPDATE.
3. Grill me with edge cases: What happens if table statistics are outdated (ANALYZE)? When would the query planner intentionally ignore an index?
Ask one probing question at a time. Evaluate my answers rigorously like a real technical interview!
```

#### Step-by-Step Interactive Drill
1. Paste the prompt into your free AI tool.
2. Provide one of your heavy Unit 8 lab queries or capstone queries.
3. Defend your index choices, composite column ordering, and EXPLAIN ANALYZE interpretations against the DBA panel.
4. Complete 4 to 5 turns of technical defense.

#### Asynchronous Participation Deliverable
> **Canvas Discussion Prompt:**
> Post to the Unit 8 Capstone Discussion: (1) The toughest technical question the DBA panel asked you, (2) Your defense explaining index column ordering or execution plans, and (3) Your key takeaway on how B-Tree indexes affect read performance vs. write throughput.
