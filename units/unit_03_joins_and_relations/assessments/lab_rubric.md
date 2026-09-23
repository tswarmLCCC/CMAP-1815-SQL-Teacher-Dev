# Unit 3: Lab Evaluation Rubric (100 Points)

## Overview
This rubric is used to evaluate student submissions for the **Unit 3 Practical Lab: Multi-Table Relational Integration & Anomaly Audits**.

---

## Detailed Scoring Criteria

| Criteria | Exemplary (Full Points) | Competent (Partial Points) | Developing (Needs Revision) | Points |
| :--- | :--- | :--- | :--- | :---: |
| **1. Join Mechanics & Key Alignment** | Correct keys used in `ON` clauses across all 2-table, 3-table, and 4-table joins. Primary Key $\leftrightarrow$ Foreign Key relationships correctly matched. | 1 minor key mismatch or redundant join included. | Key alignment incorrect; joined on incompatible attributes; Cartesian products generated. | **40** |
| **2. Outer Join & Anti-Join Execution** | Proper use of `LEFT JOIN` to prevent data loss. Anti-Join pattern correctly constructed using `WHERE right_key IS NULL`. | `LEFT JOIN` syntax correct, but filter placement in `WHERE` accidentally converts it to an inner join. | Failed to detect missing records; attempted `= NULL`. | **25** |
| **3. Disambiguation & Table Aliasing** | Short, professional table aliases used (`e`, `l`, `o`, `ol`, `p`). Every projected column explicitly prefixed with its alias. Zero ambiguous column errors. | Missing table prefixes on columns that share names across tables, or generic unreadable aliases (`t1`, `t2`). | Frequent ambiguous column reference errors; missing aliases. | **15** |
| **4. Calculation & Projection Precision** | Multi-table calculations (e.g. `quantity * unit_price`) properly aliased. Named columns used exclusively (zero unrequested `SELECT *`). | Calculations correct but missing aliases (`?column?` in output). | Calculations incorrect or unaliased `SELECT *` used. | **10** |
| **5. Formatting & SQL Style Standards** | Keywords strictly **UPPERCASE**, each `JOIN` and `ON` begins on a new line, clean indentation, semicolons present. | Minor casing inconsistencies or cramped multi-join formatting. | Unformatted single-line queries; missing semicolons; unreadable code. | **10** |
| **Total** | | | | **100** |
