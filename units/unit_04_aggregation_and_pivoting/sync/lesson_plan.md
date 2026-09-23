# Unit 4: Synchronous Active Learning Lesson Plan (150 Minutes)

## Delivery Framework
This lesson plan can be delivered as **two 75-minute class sessions** or as **one continuous 150-minute lab session**.

---

## Session 1 (75 Mins): Aggregate Foundations, The Golden Rule & GROUP BY Semantics

### Objective
Students understand the "Funnel" mental model, master the Big Five aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`), and internalize the Golden Rule of `GROUP BY` to eliminate grouping syntax errors.

### Timeline & Pacing
* **00:00 – 00:15 (Warmup & The "Funnel" Hook)**:
  - Display a 5,000-row transactional table on screen. Ask: *"If the CEO asks for total company revenue, how many rows do you hand them?"*
  - Introduce the Funnel concept: collapsing thousands of rows into actionable summary metrics.
* **00:15 – 00:35 (Interactive Live Coding: The Big Five)**:
  - Open `units/unit_04_aggregation_and_pivoting/sync/inclass_challenges.sql`.
  - Walk through:
    1. `COUNT(*)` vs. `COUNT(column)` with missing data.
    2. How `AVG()` ignores `NULL`s in its denominator.
    3. Multi-column grouping: `GROUP BY department, job_title`.
    4. Deliberately trigger the `must appear in the GROUP BY clause` error; guide students to articulate why a 2D relational grid forbids mixing 50 individual values with 5 grouped summary metrics.
* **00:35 – 00:60 (Paired Coding Challenges: Challenges 1 & 2)**:
  - Students pair up to solve Challenge 1 (Departmental Salary Audit) and Challenge 2 (Inventory Valuation by Category).
  - Circulate to check that every unaggregated column in `SELECT` is included in `GROUP BY`.
* **00:60 – 00:75 (Review & Debrief)**:
  - Student live-share: Have a student pair explain how `ROUND(AVG(salary), 2)` was formatted and grouped.

---

## Session 2 (75 Mins): WHERE vs. HAVING, Set Operations & Matrix Pivoting

### Objective
Equip students to distinguish between row filters (`WHERE`) and aggregate group filters (`HAVING`), stack datasets with Set Operations, and pivot vertical rows into horizontal reporting columns using conditional aggregation.

### Timeline & Pacing
* **00:00 – 00:15 (The Execution Pipeline Hook: Aggregates in WHERE)**:
  - Live demo: Run `SELECT department, AVG(salary) FROM employees WHERE AVG(salary) > 70000 GROUP BY department;`.
  - Ask: *"Why did PostgreSQL throw an error?"* Walk through the query execution pipeline (`FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `SELECT`).
  - Demonstrate the fix with `HAVING`.
* **00:15 – 00:35 (Live Coding: Set Operations & Conditional Pivoting)**:
  - Demonstrate `UNION` vs. `UNION ALL` and explain the performance advantage of `UNION ALL`.
  - Demonstrate pivoting: transforming vertical categories into horizontal columns using `COUNT(CASE WHEN ... THEN 1 END)` and `SUM(CASE WHEN ... THEN amount ELSE 0 END)`.
  - Contrast with PostgreSQL's modern `FILTER (WHERE ...)` clause.
* **00:35 – 00:65 (Paired Coding Challenges: Challenges 3, 4 & 5)**:
  - Students work in pairs on Challenge 3 (High-Performing Departments Filter), Challenge 4 (Set Operation Reconciliation), and Challenge 5 (The Executive Regional Matrix).
* **00:65 – 00:75 (Debrief & Exit Ticket)**:
  - Exit Ticket: *"What is the architectural difference between WHERE and HAVING?"*
  - Assign Unit 4 Lab and Quiz.
