# Unit 1: Lab Evaluation Rubric (100 Points)

## Overview
This rubric is used to evaluate student submissions for the **Unit 1 Practical Lab: Data Exploration & Environment Orientation**.

---

## Detailed Scoring Criteria

| Criteria | Exemplary (Full Points) | Competent (Partial Points) | Developing (Needs Revision) | Points |
| :--- | :--- | :--- | :--- | :---: |
| **1. Query Accuracy & Execution** | All required challenge queries execute cleanly without syntax errors and produce the exact requested dataset. | 1–2 minor logic or execution errors (e.g., incorrect sort direction, minor column omission). | Multiple queries fail to execute or return incorrect datasets. | **40** |
| **2. Formatting & SQL Style Standards** | Keywords are strictly **UPPERCASE** (`SELECT`, `FROM`, `ORDER BY`, `AS`). Clauses begin on separate lines. No trailing commas. | Inconsistent keyword casing (mixed upper/lower) or cluttered single-line formatting. | Unformatted code block; difficult to read; missing semicolons. | **20** |
| **3. Precision Projection & Aliasing** | Named columns used exclusively (zero unrequested `SELECT *`). Expressions cleanly aliased with meaningful `snake_case` headers using `AS`. | Missing aliases for computed expressions (`?column?` in output) or unnecessary use of `SELECT *`. | Monolithic `SELECT *` used throughout; no aliases provided. | **20** |
| **4. Sorting & De-duplication Logic** | Correct application of `DISTINCT` and multi-level `ORDER BY` sorting (ascending vs. descending). | Single sort correct, but secondary tie-breaker omitted or inverted. | Incorrect sort ordering; failed to de-duplicate unique values. | **10** |
| **5. Environment & System Catalog Questions** | Accurate answers provided for server metadata inspection (PostgreSQL version, current user, table counts). | Minor omission or misunderstanding of system catalog roles. | Catalog exploration questions unanswered or incorrect. | **10** |
| **Total** | | | | **100** |
