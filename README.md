# CMAP 1815: Introduction to Modern SQL

Welcome to the curriculum repository for **CMAP 1815: Introduction to Modern SQL**. This course is designed as an accelerated **8-week hybrid course** combining **150 minutes of synchronous active learning/labs** with **150 minutes of structured asynchronous guided study** per week.

---

## Quick Start with GitHub Codespaces

Everything runs directly in your browser—no local database installation required!

1. Click **Code** (green button) $\rightarrow$ **Codespaces** $\rightarrow$ **Create codespace on main**.
2. Wait ~2 minutes for the automated PostgreSQL 16 container to build.
3. Open a terminal and connect:
   ```bash
   psql $DATABASE_URL
   ```
4. Run sample queries or use the VS Code SQLTools extension.

---

## Curriculum Structure

```
.
├── .devcontainer/             # Automated PostgreSQL 16 container configuration
├── .vscode/                   # Pre-configured SQLTools database connections
├── course_specs/              # Master Course Governance
│   ├── course_learning_outcomes.md       # CLOs 1–6, Bloom's & AI Practitioner mapping
│   ├── syllabus_master.md                # 8-week hybrid schedule & time budgeting
│   ├── database_schema_spec.md           # Mermaid ERD, table DDL & Data Dictionaries
│   ├── grading_and_assessment_policy.md  # 40% Labs, 20% Quizzes, 30% Capstone
│   ├── external_resources_guide.md       # Verified PostgreSQL tutorials & FreeCodeCamp timestamps
│   └── canvas_api_browser_sync_guide.md  # Browser DevTools session sync guide
│
├── units/                     # 8 Modular Units
│   ├── unit_01_selection_and_fundamentals/
│   ├── unit_02_filtering_and_logic/
│   ├── unit_03_joins_and_relations/
│   ├── unit_04_aggregation_and_pivoting/
│   ├── unit_05_safe_dml_and_temp_tables/
│   ├── unit_06_ctes_and_window_functions/
│   ├── unit_07_schema_design_and_ddl/
│   └── unit_08_indexing_and_capstone/
│
├── shared_assets/             # Core Datasets & Seed Scripts
│   └── datasets/              # setup_chap1.sql, superstore.csv
│
└── archive/                   # Consolidated Legacy Materials
    └── v1_original_drafts/    # Original brainstorms and early unit drafts (also tagged in Git)
```

---

## 8-Week Course Roadmap

| Week | Unit Theme | Key Concepts | Lab & Assessment |
| :---: | :--- | :--- | :--- |
| **1** | **Selection & Fundamentals** | Relational Model, Projection ("The Flashlight"), SELECT, FROM, ORDER BY, DISTINCT, Aliases | System Catalog Exploration & SELECT Lab |
| **2** | **Targeted Retrieval & Logic** | Filtering ("The Scalpel"), WHERE, Comparison Operators, BETWEEN, IN, LIKE/ILIKE, IS NULL, LIMIT | Targeted Inventory & Tenure Audit Lab |
| **3** | **Relational Joins** | Primary/Foreign Keys, INNER JOIN, Multi-Table Joins, LEFT JOIN, Anti-Join Anomaly Detection | 4-Table Superstore Integration & Dead Inventory Audit |
| **4** | **Summarization & Pivoting** | Aggregate Functions (COUNT, SUM, AVG), GROUP BY, HAVING, Set Operations (UNION), CASE Pivoting | Executive Business Reporting & Pivoting Lab |
| **5** | **Safe DML & Temp Tables** | INSERT, UPDATE, DELETE, Pre-Execution SELECTs, Transaction Boundaries, Local Temp Tables | Safe Data Cleanup & Archiving Lab |
| **6** | **CTEs & Window Functions** | Subqueries vs. WITH CTEs, Window Partitions (OVER, PARTITION BY), Ranking (ROW_NUMBER), Moving Averages | Advanced Analytics & Deduplication Lab |
| **7** | **Schema Design & DDL** | Normalization (1NF to 3NF), CREATE TABLE, Constraints (PK, FK, CHECK, UNIQUE, NOT NULL), Views | "The Denormalized Nightmare" DDL Lab |
| **8** | **Indexing & Capstone** | B-Tree Indexes, EXPLAIN ANALYZE, Read vs. Write Trade-offs, Audit Trails, Capstone Defense | Comprehensive Capstone Defense Project |
