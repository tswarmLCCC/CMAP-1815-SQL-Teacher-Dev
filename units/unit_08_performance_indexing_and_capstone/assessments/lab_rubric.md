# Unit 8 & Capstone Defense Rubric: Comprehensive Engineering & Tuning

**Total Points:** 100  
**Submission Format:** Single verified SQL script (`capstone_submission.sql`) executed against PostgreSQL 16 + Architecture Defense Documentation.

---

## Grading Criteria Breakdown

| Dimension | Points Possible | Exemplary (100%) | Proficient (80%) | Developing (60%) | Unsatisfactory (0%) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Dimension 1: 3NF Schema & Integrity Constraints** | 20 | Flawless 3NF design; clean PK/FK relationships with referential actions; strict `CHECK`, `UNIQUE`, and `NOT NULL` rules. | 3NF achieved with minor constraint gap (e.g. anonymous constraint name). | Missing foreign key or partial dependency remaining. | Unnormalized flat table submitted. |
| **Dimension 2: Safe Staging & Data Ingestion (DML)** | 20 | Ingests raw data via `TEMP TABLE`; performs robust cleaning; executes multi-row insert with `RETURNING` inside an atomic transaction. | Staging table used, but missing transaction wrapper or `RETURNING` verification. | Ingestion attempted directly on production tables. | Failed execution or omitted. |
| **Dimension 3: Modular Analytics (CTEs & Windows)** | 20 | Implements chained CTEs; calculates non-collapsing metrics with `OVER(PARTITION BY)`; uses window ranking (`DENSE_RANK`/`ROW_NUMBER`) and running totals. | Analytics work, but relies on subqueries or minor window frame issue. | Collapsed data with `GROUP BY` where window was required. | Incomplete analytics or syntax errors. |
| **Dimension 4: Profiling & Index Engineering** | 20 | Profiles baseline query with `EXPLAIN ANALYZE`; engineers targeted B-Tree or composite index; re-profiles and documents latency reduction; discusses write penalty. | Index created and profiled, but missing before/after metrics comparison. | Ineffective index created (wrong column order). | Profiling or indexing omitted. |
| **Dimension 5: Audit Logging & Architecture Defense** | 20 | Creates dedicated audit table; captures state mutations with user/timestamp; writes coherent, professional architecture summary in script headers. | Audit table created, but missing payload detail or defense documentation brief. | Minimal audit logging; weak rationale. | Omitted. |

---

## Deduction Penalties
* **-10 Points:** Lowercase keywords (SQL Style Guide violation).
* **-10 Points:** Fatal syntax errors terminating script execution in `psql`.
* **-5 Points:** Unformatted output (missing column aliases).
