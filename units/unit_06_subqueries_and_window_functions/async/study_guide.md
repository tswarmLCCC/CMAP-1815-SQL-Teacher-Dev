# Unit 6 Asynchronous Study Guide: CTEs & Analytical Window Functions

**Estimated Preparation Time:** 150 Minutes  
**Prerequisites:** Units 1–5 (Selection, Joins, Aggregations, Safe DML)  
**Target Competencies:** Common Table Expressions (`WITH`), Window Functions (`OVER`, `PARTITION BY`), Ranking (`ROW_NUMBER`, `DENSE_RANK`), Running Balances, Deduplication

---

## 1. Overview & Learning Objectives
Welcome to Unit 6! In this unit, you transition from standard relational operations to advanced **analytical SQL**. You will master Common Table Expressions (CTEs) to make complex logic modular and readable, and Window Functions to perform calculations across subsets of rows without collapsing the underlying dataset.

By the end of this study guide, you will be able to:
1. Refactor unreadable nested subqueries into modular Common Table Expressions (`WITH`).
2. Chain multiple CTEs together into a sequential data processing pipeline.
3. Use the `OVER()` and `PARTITION BY` clauses to compute group metrics alongside row-level data.
4. Distinguish clearly between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` and explain how each handles ties.
5. Compute cumulative running totals and moving averages using window frame specifications.
6. Apply the industry-standard `ROW_NUMBER() = 1` deduplication pattern to isolate golden records.

---

## 2. Required Video Curriculum (FreeCodeCamp Master Course)
Review the official video segments covering subqueries and analytical partitioning:
* 🎥 **Subqueries & Analytical Expressions:** Refer to [PostgreSQL Tutorial Window Functions Guide](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-window-function/) and [PostgreSQL CTE Guide](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-cte/) for step-by-step video and visual animations.

---

## 3. Required Reading & Tutorials (PostgreSQLTutorial.com)
Complete the following modules on PostgreSQLTutorial.com:

1. [PostgreSQL CTE (Common Table Expression)](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-cte/)  
   *Focus on:* Why CTEs improve readability over nested subqueries.
2. [PostgreSQL Window Function Overview](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-window-function/)  
   *Focus on:* How window functions differ from `GROUP BY` by preserving all individual rows.
3. [PostgreSQL ROW_NUMBER](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-row_number/)  
   *Focus on:* Assigning unique sequential ranks and the `ROW_NUMBER() = 1` deduplication pattern.
4. [PostgreSQL RANK & DENSE_RANK](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-rank/)  
   *Focus on:* Handling ties with and without rank gaps.
5. [Official PostgreSQL Documentation: Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)  
   *Focus on:* Window framing (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).

---

## 4. Key Architectural Mental Models

### A. Aggregation vs. Window Functions
* **`GROUP BY` (Collapsing):** Reduces 100 rows into 4 summary rows. Granular attributes are lost.
* **`OVER(PARTITION BY ...)` (Non-Collapsing):** Calculates group metrics in memory and stamps the summary value onto all 100 original rows!

### B. The 3 Ranking Functions Compared

| Value | `ROW_NUMBER()` | `RANK()` | `DENSE_RANK()` |
| :---: | :---: | :---: | :---: |
| 100 | 1 | 1 | 1 |
| 90 (Tie) | 2 | 2 | 2 |
| 90 (Tie) | 3 | 2 | 2 |
| 80 | 4 | **4** (Gap after tie!) | **3** (No gap!) |

---

## 5. Summary Reference Cards

| Clause / Function | Purpose | Example |
| :--- | :--- | :--- |
| `WITH cte_name AS (...)` | Defines a temporary modular result set | `WITH active_staff AS (SELECT * FROM emp WHERE active)` |
| `OVER()` | Establishes a window calculation | `AVG(salary) OVER()` |
| `PARTITION BY` | Divides window into analytical groups | `AVG(salary) OVER(PARTITION BY department)` |
| `ROW_NUMBER()` | Unique sequential integer per row | `ROW_NUMBER() OVER(ORDER BY date DESC)` |
| `DENSE_RANK()` | Rank without gaps on ties | `DENSE_RANK() OVER(ORDER BY sales DESC)` |
| Cumulative Sum | Running total over ordered rows | `SUM(amt) OVER(ORDER BY date)` |

---

## 6. Pre-Class Checklist
Before attending the synchronous classroom session:
- [ ] Read the PostgreSQLTutorial guides on CTEs, Window Functions, and `ROW_NUMBER`.
- [ ] Complete the **5 Formative Self-Check Drills** in `self_check_drills.md`.
- [ ] Understand why a window function cannot be placed directly inside a `WHERE` clause.


---

---

## Step 6: Learn with AI — Interactive Practice & Prompt Craft (100% Free Tools)

### Role & Persona: The Staff SQL Architect
* **Pedagogical Technique:** Query Refactoring & Window Partitioning Deconstruction
* **Core Goal:** Refactor unreadable, slow nested subqueries into elegant Common Table Expressions (CTEs) and calculate running totals, moving averages, and ranks with analytical window functions.
* **Recommended Free Tools:** ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot *(Zero subscription or paid API key required)*

#### Copy-and-Paste AI Prompt Template
```text
Act as a Principal Database Architect at a high-scale tech company. I am learning modular SQL, Common Table Expressions (WITH clauses), and analytical Window Functions (ROW_NUMBER, RANK, DENSE_RANK, SUM() OVER).
Please provide me with an ugly, 4-level deeply nested subquery that calculates:
- Top 3 highest-earning employees in each department.
- The department's average salary alongside each employee's salary.
- The salary difference between each employee and the highest earner in their department.
Challenge me to:
1. Refactor this unreadable query into clean, modular CTEs (WITH dept_metrics AS (...)).
2. Replace redundant group-by subqueries with appropriate OVER (PARTITION BY ... ORDER BY ...) window frames.
Review my refactored query, evaluate its readability and efficiency, and explain how the database processes the window frame.
```

#### Step-by-Step Interactive Drill
1. Paste the prompt and review the AI's complex nested subquery.
2. Break the query down into modular, sequential CTE steps using WITH.
3. Apply analytical window functions (DENSE_RANK() OVER (...), AVG() OVER (...)).
4. Submit your refactored SQL for architectural code review.

#### Asynchronous Participation Deliverable
> **Canvas Discussion Prompt:**
> In the Unit 6 Discussion, share: (1) The original nested subquery vs. your clean CTE/Window function query, (2) Why PARTITION BY does not collapse rows like GROUP BY, and (3) When you would choose DENSE_RANK() over ROW_NUMBER().
