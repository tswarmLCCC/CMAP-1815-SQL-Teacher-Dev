# CMAP 1815: Course Learning Outcomes & Competency Alignment

## Course Overview
**Course Title:** Introduction to Modern SQL  
**Course Number:** CMAP 1815  
**Credits:** 3 Semester Credits  
**Delivery Format:** 8-Week Accelerated Hybrid (150 minutes Synchronous Instruction + 150 minutes Asynchronous Guided Study per week)  
**Target Environment:** PostgreSQL 16 on GitHub Codespaces (CLI `psql` & VS Code SQLTools)

---

## Pedagogical Philosophy: The AI Practitioner Model
Modern database education must transcend mechanical syntax memorization. CMAP 1815 trains students as **AI Practitioners**—engineers and analysts who build, maintain, and query the structured data foundations required for reliable enterprise operations and AI systems:
- **Fact-Grounding vs. Hallucination**: Students learn why modern generative AI and Retrieval-Augmented Generation (RAG) require factual, normalized database anchors.
- **Human-in-the-Loop Validation**: Rigorous data modification protocols (pre-execution SELECTs, transaction checkpoints) ensuring safe operations in automated environments.
- **Modern Analytical SQL**: Moving beyond basic single-table queries into Window Functions, Common Table Expressions (CTEs), and query optimization.

---

## Master Course Learning Outcomes (CLOs)
Upon successful completion of this course, students will be able to:

1. **CLO 1 (Query Construction & Filtering)**: Formulate syntactically accurate SQL queries to extract, filter, format, and sort data from single and relational tables using ANSI/PostgreSQL standards. *(Bloom's: Applying)*
2. **CLO 2 (Multi-Table Integration & Summarization)**: Synthesize business metrics across normalized relational tables using diverse join techniques (INNER, LEFT, RIGHT, FULL) and aggregation logic (`GROUP BY`, `HAVING`, conditional `CASE` aggregations). *(Bloom's: Analyzing)*
3. **CLO 3 (Safe Data Manipulation & Validation)**: Execute Data Manipulation Language (`INSERT`, `UPDATE`, `DELETE`) operations adhering to strict pre- and post-execution verification protocols and staging strategies using temporary tables. *(Bloom's: Evaluating / Applying)*
4. **CLO 4 (Advanced Analytical Structuring)**: Decompose complex analytical requirements into modular, readable Common Table Expressions (CTEs) and perform partitioned calculations using SQL Window Functions. *(Bloom's: Creating / Analyzing)*
5. **CLO 5 (Relational Design & Integrity)**: Design and normalize relational database schemas up to Third Normal Form (3NF), declaring optimal data types and enforcing declarative integrity constraints (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`, `NOT NULL`). *(Bloom's: Creating)*
6. **CLO 6 (Performance Optimization & Auditing)**: Evaluate query execution plans (`EXPLAIN ANALYZE`), diagnose indexing bottlenecks, and articulate architectural strategies for data change tracking and auditing. *(Bloom's: Evaluating)*

---

## State & Institutional Competency Alignment Matrix

| Unit | Institutional Competency | Bloom's Level | Difficulty (1–5) | Key Assessment Target |
| :---: | :--- | :---: | :---: | :--- |
| **Unit 1** | Construct basic data retrieval statements and navigate database catalogs. | Applying | **1–2** | System Catalog Orientation & SELECT Exploration Lab |
| **Unit 2** | Restrict output using multi-condition boolean logic, lists, and pattern matching. | Analyzing | **2–3** | Targeted Retrieval & Census/Log Audit Lab |
| **Unit 3** | Integrate data from multiple normalized tables and identify anomalies via joins. | Analyzing | **3–4** | Multi-Table Superstore Integration & Missing Record Audit |
| **Unit 4** | Summarize tabular data, apply group filters, and pivot data conditionally. | Evaluating | **3–5** | Executive Business Reporting & Pivoting Lab (Midterm Checkpoint) |
| **Unit 5** | Safely manipulate data using DML statements and execute strict verification protocols. | Applying / Evaluating | **3–4** | Data Cleanup & Staged DML Modification Lab |
| **Unit 6** | Refactor complex subqueries into modular CTEs and execute windowed calculations. | Creating | **4–5** | Advanced Analytics & Deduplication Lab |
| **Unit 7** | Design 3NF normalized schemas and implement DDL constraints and views. | Creating | **3–4** | "Denormalized Nightmare" Normalization & DDL Lab |
| **Unit 8** | Evaluate query performance via execution plans, indexes, and audit strategies. | Evaluating | **2–5** | Comprehensive Capstone Architecture Defense |
