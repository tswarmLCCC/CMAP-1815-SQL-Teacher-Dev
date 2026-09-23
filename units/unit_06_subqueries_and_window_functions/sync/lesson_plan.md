# Unit 6: Synchronous Active Learning Lesson Plan (150 Minutes)

## Delivery Framework
This lesson plan can be delivered as **two 75-minute class sessions** or as **one continuous 150-minute lab session**.

---

## Session 1 (75 Mins): Subquery Refactoring, Modular CTEs & Multi-Step Pipelines

### Objective
Students learn to eliminate messy nested subqueries by refactoring them into clean, top-down Common Table Expressions (`WITH`), chaining multiple CTEs into a cohesive analytical pipeline.

### Timeline & Pacing
* **00:00 – 00:15 (The Subquery Inception Hook)**:
  - Display a 40-line nested subquery on projector. Ask students to find where the date filter is applied.
  - Show how difficult it is to read inside-out SQL.
  - Introduce Common Table Expressions (`WITH`).
* **00:15 – 00:35 (Interactive Live Coding: CTE Pipelines)**:
  - Open `units/unit_06_subqueries_and_window_functions/sync/inclass_challenges.sql`.
  - Walk through:
    1. Single CTE vs. inline subquery.
    2. Chaining multiple CTEs with comma-separated syntax.
    3. How to test and debug individual CTEs by selecting directly from intermediate blocks.
* **00:35 – 00:60 (Paired Coding Challenges: Challenges 1 & 2)**:
  - Students pair up to solve Challenge 1 (Refactoring Nested Subqueries) and Challenge 2 (Multi-Tier Customer Spend Pipeline).
  - Circulate to verify that students are naming CTEs descriptively.
* **00:60 – 00:75 (Review & Debrief)**:
  - Student live-share: Have a student pair walk through how their chained CTE steps pass data cleanly from one stage to the next.

---

## Session 2 (75 Mins): Window Functions, Ranking Semantics & Deduplication

### Objective
Equip students to calculate partitioned group metrics without row collapse using `OVER(PARTITION BY)`, analyze tie-breaking behaviors across ranking functions, compute cumulative balances, and execute deduplication filters.

### Timeline & Pacing
* **00:00 – 00:15 (The "Non-Collapsing" Hook)**:
  - Run `SELECT department, AVG(salary) FROM employees GROUP BY department;` (5 rows).
  - Ask: *"How do I keep all 50 employee names and show their department's average on every single row?"*
  - Introduce `AVG(salary) OVER(PARTITION BY department)`.
* **00:15 – 00:35 (Live Coding: Ranking, Cumulative Balances & Deduplication)**:
  - Compare `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` side-by-side with ties.
  - Demonstrate running totals using `SUM(sales) OVER(ORDER BY order_date)`.
  - Introduce the `ROW_NUMBER() = 1` deduplication pattern wrapped in a CTE.
* **00:35 – 00:65 (Paired Coding Challenges: Challenges 3, 4 & 5)**:
  - Students work in pairs on Challenge 3 (Department Salary Variance), Challenge 4 (Top-N Performer Filter), and Challenge 5 (The Golden Order Deduplication).
* **00:65 – 00:75 (Debrief & Exit Ticket)**:
  - Exit Ticket: *"Why must we wrap a window function in a CTE or subquery if we want to filter on its value?"*
  - Assign Unit 6 Lab and Quiz.
