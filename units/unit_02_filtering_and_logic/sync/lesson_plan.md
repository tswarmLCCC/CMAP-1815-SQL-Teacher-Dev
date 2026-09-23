# Unit 2: Synchronous Active Learning Lesson Plan (150 Minutes)

## Delivery Framework
This lesson plan can be delivered as **two 75-minute class sessions** or as **one continuous 150-minute lab session**.

---

## Session 1 (75 Mins): Numerical & Text Filtering with Comparison Operators & Wildcards

### Objective
Students master row-level filtering using comparison operators, `IN` sets, and wildcard pattern matching (`LIKE` / `ILIKE`), while avoiding the "Alias in WHERE" error.

### Timeline & Pacing
* **00:00 – 00:15 (Warmup & Conceptual Check)**:
  - Quick-fire poll: Display a query using a column alias in the `WHERE` clause on the screen. Ask students why it fails and have them explain the `FROM` $\rightarrow$ `WHERE` $\rightarrow$ `SELECT` execution pipeline.
* **00:15 – 00:35 (Interactive Live Coding: The Scalpel)**:
  - Open `units/unit_02_filtering_and_logic/sync/inclass_challenges.sql`.
  - Walk through:
    1. Single vs. multi-condition numerical filters (`>=`, `<=`, `BETWEEN`).
    2. Exact text vs. categorical sets with `IN ('Research', 'Security')`.
    3. Wildcard pattern matching with `%` and `_`.
    4. Demonstrating the case-insensitive superpower `ILIKE`.
* **00:35 – 00:60 (Paired Coding Challenges: Challenges 1 & 2)**:
  - Students pair up to solve Challenge 1 (Targeted Inventory Search) and Challenge 2 (HR Tenure Roster).
  - Circulate to ensure students are enclosing text/dates in single quotes `'...'` and using uppercase keywords.
* **00:60 – 00:75 (Review & Debrief)**:
  - Student live-share: Ask a student pair to explain how they matched SKUs or names using wildcards.

---

## Session 2 (75 Mins): Complex Boolean Logic, Three-Valued Logic & Pagination

### Objective
Equip students to solve multi-conditional business queries with Boolean operators (`AND`, `OR`, `NOT`), correctly handle `NULL` traps using `IS NULL`, and paginate result sets using `LIMIT` and `OFFSET`.

### Timeline & Pacing
* **00:00 – 00:15 (The Hook: Breaking SQL with = NULL)**:
  - Live demo on projector: Run `SELECT * FROM employees WHERE bonus = NULL;`.
  - Show the empty result set. Ask: *"Why did zero rows return when we know employees have no bonus?"*
  - Introduce Three-Valued Logic (`UNKNOWN`) and demonstrate the fix: `IS NULL`.
* **00:15 – 00:35 (The Parentheses Clinic: AND vs. OR Precedence)**:
  - Show how omitting parentheses causes unexpected records to leak into the result set.
  - Demonstrate:
    ```sql
    WHERE (department = 'Security' OR department = 'Sales') AND salary >= 70000;
    ```
  - Introduce `LIMIT 5 OFFSET 5` for search pagination.
* **00:35 – 00:65 (Paired Coding Challenges: Challenges 3, 4 & 5)**:
  - Students work in pairs on Challenge 3 (The Bonus Audit), Challenge 4 (High-Earner Department Filter), and Challenge 5 (Product Catalog Pagination).
* **00:65 – 00:75 (Debrief & Exit Ticket)**:
  - Exit Ticket: *"In one sentence, explain why bonus = NULL fails in SQL."*
  - Announce Unit 2 Lab & Quiz due dates.
