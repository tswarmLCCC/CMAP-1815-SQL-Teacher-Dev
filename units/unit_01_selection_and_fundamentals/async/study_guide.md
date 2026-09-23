# Unit 1: Asynchronous Guided Study Guide (150 Minutes)

## Welcome to Unit 1 Asynchronous Preparation!
In our hybrid model, **150 minutes** of each week are dedicated to guided self-study **before** attending our synchronous in-class sessions. Completing these readings, video modules, and self-checks ensures you come to class ready for hands-on active coding rather than passive listening.

---

## Time Budget Breakdown

| Phase | Activity | Estimated Time | Focus / Deliverable |
| :---: | :--- | :---: | :--- |
| **Step 1** | Watch Unit 1 Micro-Lectures (Videos 1.1, 1.2, 1.3) | **30 mins** | Foundational concepts & demo notes |
| **Step 2** | Curated PostgreSQL Tutorials & Reference | **45 mins** | Core syntax, rules, and variations |
| **Step 3** | Environment Onboarding: GitHub Codespaces Launch | **30 mins** | First login and database ping |
| **Step 4** | Conceptual Deep-Dive & Focus Questions | **30 mins** | Narrative reflection & RAG grounding |
| **Step 5** | Formative Self-Check Drills | **15 mins** | 5-question pre-class knowledge check |
| **Step 6** | Learn with AI: Interactive Practice Drill | **20 mins** | Persona-based prompt engineering & discussion post |
| **Total** | | **150 mins** | |

---

## Step 1: Micro-Lecture Video Series (30 Mins)
Watch the three micro-lectures recorded for this unit:
1. **Video 1.1: Relational Foundations & Why AI Needs Databases (~7 min)**
   * *Focus Question:* Why do spreadsheets fail when data scales past thousands of rows? How does structured data prevent AI hallucinations?
2. **Video 1.2: Anatomy of SELECT & The Projection Flashlight (~8 min)**
   * *Focus Question:* What is the mathematical concept of "Projection"? What is the execution order difference between how you write SQL and how PostgreSQL processes it?
3. **Video 1.3: Expressions, Aliases, DISTINCT & ORDER BY (~8 min)**
   * *Focus Question:* When you calculate `salary * 1.05`, does it alter the underlying database table? Why is `AS` essential for reporting?

### Supplemental Video Deep-Dive
Watch these exact chapter segments from **[FreeCodeCamp: Learn PostgreSQL Tutorial](https://www.youtube.com/watch?v=qw--VYLpxG4)**:
* [0:03:16 – What is a Database](https://www.youtube.com/watch?v=qw--VYLpxG4&t=196s)
* [0:05:17 – What is SQL And Relational Database](https://www.youtube.com/watch?v=qw--VYLpxG4&t=317s)
* [0:09:10 – What is PostgreSQL AKA Postgres](https://www.youtube.com/watch?v=qw--VYLpxG4&t=550s)
* [0:33:35 – How to Connect to Databases](https://www.youtube.com/watch?v=qw--VYLpxG4&t=2015s)
* [1:12:28 – Select From](https://www.youtube.com/watch?v=qw--VYLpxG4&t=4348s)
* [1:15:18 – Order By](https://www.youtube.com/watch?v=qw--VYLpxG4&t=4518s)
* [1:19:53 – Distinct](https://www.youtube.com/watch?v=qw--VYLpxG4&t=4793s)
* [2:01:55 – Basics of Arithmetic Operators](https://www.youtube.com/watch?v=qw--VYLpxG4&t=7315s)
* [2:09:43 – Column Alias](https://www.youtube.com/watch?v=qw--VYLpxG4&t=7783s)

---

## Step 2: Curated PostgreSQL Documentation & Readings (45 Mins)
Read through the following tutorials from the verified **[PostgreSQL Tutorial Guide](https://www.postgresqltutorial.com/)** and official docs:
* [PostgreSQL Getting Started & SELECT](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-select/) (12 mins) — Basic query structure and projecting specific columns.
* [Column Aliases (`AS`)](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-alias/) (8 mins) — Renaming column headers and calculated expressions.
* [The ORDER BY Clause](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-order-by/) (10 mins) — Sorting rules, ASC vs. DESC, and NULL positioning.
* [The DISTINCT Clause](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select-distinct/) (8 mins) — De-duplicating rows and evaluating multi-column unique sets.
* [Official PostgreSQL Documentation: The SELECT Statement](https://www.postgresql.org/docs/current/sql-select.html) (7 mins) — Syntax reference and standards.

---

## Step 3: Environment Setup & Codespaces Launch (30 Mins)
1. Navigate to our course repository: `github.com/tswarmLCCC/CMAP-1815-SQL-Teacher-Dev`.
2. Click the green **Code** button $\rightarrow$ select **Codespaces** $\rightarrow$ **Create codespace on main**.
3. Wait ~2 minutes for the automated setup container to spin up.
4. When the terminal displays `>>> Done!`, test your connection by typing:
   ```bash
   psql $DATABASE_URL
   ```
5. Run your first query:
   ```sql
   SELECT version();
   ```
6. Type `\q` to exit the `psql` shell.

---

## Step 4: Focus Questions for Synchronous Class Discussion (30 Mins)
Reflect on these questions before class. You will be asked to discuss these in pairs during Period 1:
1. *The Flashlight Metaphor:* Explain how `SELECT first_name, last_name FROM employees;` mimics walking into a dark warehouse with a flashlight. What represents the warehouse? What represents the filing cabinet?
2. *Order of Operations:* Why does PostgreSQL execute `FROM` before `SELECT`?
3. *The Sledgehammer Risk:* Name three distinct operational risks associated with using `SELECT *` in production software.

---

## Step 5: Formative Self-Check (15 Mins)
Complete the 5 self-check questions in `units/unit_01_selection_and_fundamentals/async/self_check_drills.md` to confirm your understanding before attending class.


---

---

## Step 6: Learn with AI — Interactive Practice & Prompt Craft (100% Free Tools)

### Role & Persona: The Socratic Database Sensei (Professor Codd)
* **Pedagogical Technique:** Socratic Inversion & Execution Order Probing
* **Core Goal:** Master relational query foundations by having the AI challenge your assumptions on how the database engine parses SQL versus how humans write it, focusing on projection, row deduplication, and production safety.
* **Recommended Free Tools:** ChatGPT Free (GPT-4o-mini), Claude Free, Google Gemini Free, Microsoft Copilot *(Zero subscription or paid API key required)*

#### Copy-and-Paste AI Prompt Template
```text
Act as a strict, Socratic SQL professor named Professor Codd. I am a student learning SQL SELECT statements and relational database fundamentals in PostgreSQL 16. Do NOT give me direct answers or write the SQL for me. Instead, ask me one challenging question at a time to test my understanding of:
1. Why PostgreSQL evaluates FROM before SELECT during query execution.
2. The fundamental difference between physical row storage and relational projection.
3. Why 'SELECT *' is considered a dangerous anti-pattern in production microservices and reporting pipelines.
Start by asking me your first question about query execution order. Wait for my response before evaluating my reasoning and asking the next question.
```

#### Step-by-Step Interactive Drill
1. Open any free AI chat tool (ChatGPT Free, Claude Free, Gemini Free, or MS Copilot).
2. Paste the prompt above.
3. Answer Professor Codd's questions one at a time for at least 3 to 4 turns.
4. If you get stuck, reply: 'Give me a real-world analogy to help me reason through this, but don't give me the answer yet!'

#### Asynchronous Participation Deliverable
> **Canvas Discussion Prompt:**
> In the Canvas Asynchronous Discussion for Unit 1, share: (1) The toughest question Professor Codd asked you, (2) The key insight you discovered about execution order or projection, and (3) One question you still have for our in-class session.
