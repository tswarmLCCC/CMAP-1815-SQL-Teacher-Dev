# Unit 2: Asynchronous Guided Study Guide (150 Minutes)

## Welcome to Unit 2 Asynchronous Preparation!
In Unit 1, you learned how to project columns using `SELECT`. This week, you master **The Scalpel**: using the `WHERE` clause to surgically extract exact rows, match patterns, evaluate complex Boolean logic, handle missing (`NULL`) data, and paginate query outputs.

---

## Time Budget Breakdown

| Phase | Activity | Estimated Time | Focus / Deliverable |
| :---: | :--- | :---: | :--- |
| **Step 1** | Watch Unit 2 Micro-Lectures (Videos 2.1, 2.2, 2.3) | **30 mins** | Comparison operators, wildcards, and Three-Valued Logic |
| **Step 2** | Curated PostgreSQL Documentation & Readings | **45 mins** | Syntax deep-dive: `WHERE`, `LIKE`, `IN`, `BETWEEN`, `IS NULL`, `LIMIT` |
| **Step 3** | Logic Gate Truth Table Drills | **30 mins** | Evaluating Boolean precedence and three-valued logic ($NULL$) |
| **Step 4** | Focus Questions for In-Class Discussion | **30 mins** | Real-world applications: Security log analysis and data validation |
| **Step 5** | Formative Self-Check Drills | **15 mins** | 5-question pre-class knowledge check |
| **Step 6** | Learning with AI: Interactive Practice Drill | **20 mins** | Persona-based prompt engineering & discussion post |
| **Total** | | **150 mins** | |

---

## Step 1: Micro-Lecture Video Series (30 Mins)
Watch the three micro-lectures recorded for this unit:
1. **Video 2.1: The WHERE Clause & Comparison Operators (~7 min)**
   * *Focus Question:* Why does writing `WHERE sale_price < 50` fail if `sale_price` was defined as an alias in the `SELECT` clause?
2. **Video 2.2: Pattern Matching & Lists: LIKE & IN (~7 min)**
   * *Focus Question:* What is the difference between `%` and `_` wildcards? When should you choose `ILIKE` over `LIKE`?
3. **Video 2.3: Boolean Gates & Three-Valued Logic with NULLs (~8 min)**
   * *Focus Question:* Why does `WHERE bonus = NULL` always return zero rows in SQL? How do parentheses protect against the operator precedence of `AND` over `OR`?

### Supplemental Video Deep-Dive
Watch these exact chapter segments from **[FreeCodeCamp: Learn PostgreSQL Tutorial](https://www.youtube.com/watch?v=qw--VYLpxG4)**:
* [1:21:59 – Where Clause and AND](https://www.youtube.com/watch?v=qw--VYLpxG4&t=4919s)
* [1:25:29 – Comparison Operators](https://www.youtube.com/watch?v=qw--VYLpxG4&t=5129s)
* [1:29:35 – Limit, Offset & Fetch](https://www.youtube.com/watch?v=qw--VYLpxG4&t=5375s)
* [1:32:43 – IN Operator](https://www.youtube.com/watch?v=qw--VYLpxG4&t=5563s)
* [1:35:43 – Between Operator](https://www.youtube.com/watch?v=qw--VYLpxG4&t=5743s)
* [1:37:45 – Like And iLike](https://www.youtube.com/watch?v=qw--VYLpxG4&t=5865s)
* [2:12:32 – Coalesce (Handling Missing NULL Values)](https://www.youtube.com/watch?v=qw--VYLpxG4&t=7952s)
* [2:16:15 – NULLIF](https://www.youtube.com/watch?v=qw--VYLpxG4&t=8175s)

---

## Step 2: Curated PostgreSQL Documentation & Readings (45 Mins)
Review the following essential sections of the verified **[PostgreSQL Tutorial Guide](https://www.postgresqltutorial.com/)** and official docs:
* [The WHERE Clause](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-where/) (10 mins) — Filtering rows with equality, comparison, and logic.
* [The IN Operator](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-in/) (8 mins) — Evaluating membership in discrete lists.
* [The BETWEEN Operator](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-between/) (7 mins) — Inclusive numerical and date ranges.
* [The LIKE & ILIKE Operators](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-like/) (10 mins) — Pattern matching with wildcards (`%`, `_`).
* [The IS NULL Operator](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-is-null/) (8 mins) — Understanding Three-Valued Logic and missing values.
* [The LIMIT & OFFSET Clauses](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-limit/) (8 mins) — Pagination and subset control.
* [Official PostgreSQL Documentation: The WHERE Clause](https://www.postgresql.org/docs/current/queries-where.html) (6 mins) — Standard syntax specification.

---

## Step 3: Logic Gate & Truth Table Exercises (30 Mins)
Work through these logical truth table challenges on paper:
1. In SQL, if Expression A is `FALSE` and Expression B is `UNKNOWN` (because of a `NULL` column), what does `A AND B` evaluate to?
2. What does `A OR B` evaluate to?
3. What does `NOT (UNKNOWN)` evaluate to?
4. Why does a SQL query only return a row when the final `WHERE` condition resolves strictly to `TRUE`?

---

## Step 4: Discussion Focus Questions (30 Mins)
Reflect on these real-world scenarios for our in-class paired discussion:
* **Scenario A (Security Log Audit):** You are auditing a web server access log table with 2 million entries. You need to identify suspicious brute-force attempts from IP addresses starting with `192.168.` that targeted the endpoint `/admin/login` between 2:00 AM and 4:00 AM. What combination of `LIKE`, `BETWEEN`, and `AND` would you structure?
* **Scenario B (The Missing Commission Bug):** A sales dashboard query calculates `salary + bonus` for sales reps. Several top salespeople are missing from the leaderboard entirely because their bonus is currently recorded as `NULL`. Why does arithmetic involving `NULL` produce `NULL`, and how will `IS NOT NULL` or `COALESCE` solve this?

---

## Step 5: Formative Self-Check (15 Mins)
Complete the 5 self-check questions in `units/unit_02_filtering_and_logic/async/self_check_drills.md` to verify your readiness before class.


---

## Step 6: Learning with AI — Interactive Practice & Prompt Craft (100% Free Tools)

### Role & Persona: The Pedantic QA Lead / Compiler
* **Pedagogical Technique:** Three-Valued Logic Red-Teaming & Edge-Case Traps
* **Core Goal:** Stress-test your Boolean filtering logic against ANSI Three-Valued Logic (TRUE, FALSE, UNKNOWN), NULL propagation traps, and operator precedence.
* **Recommended Free Tools:** ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot *(Zero subscription or paid API key required)*

#### Copy-and-Paste AI Prompt Template
```text
Act as a pedantic Senior Database QA Engineer. I am writing PostgreSQL queries using WHERE, AND, OR, NOT, BETWEEN, LIKE, and IS NULL.
Present me with 3 realistic SQL query snippets that contain subtle logic bugs related to:
1. ANSI Three-Valued Logic (TRUE, FALSE, UNKNOWN) and NULL propagation (e.g., '= NULL' or 'NOT IN (subquery with NULL)').
2. Operator precedence between AND and OR without proper parentheses.
3. Inclusive vs. exclusive boundaries in BETWEEN with timestamps.
Present the first buggy query snippet and ask me to identify the exact data trap and how to fix it. Do NOT reveal the fix until I attempt an answer.
```

#### Step-by-Step Interactive Drill
1. Paste the prompt into your free AI tool.
2. Analyze the QA Engineer's first puzzle. Explain why the query fails on edge-case data.
3. Write the corrected SQL clause and submit it to the AI for verification.
4. Work through all 3 puzzles.

#### Asynchronous Participation Deliverable
> **Canvas Discussion Prompt:**
> In the Unit 2 Discussion, share: (1) One of the three-valued logic traps the AI gave you, (2) Why standard Boolean intuition (True/False) breaks down when NULL is involved, and (3) The corrected WHERE clause.
