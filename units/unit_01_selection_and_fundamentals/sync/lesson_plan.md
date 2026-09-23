# Unit 1: Synchronous Active Learning Lesson Plan (150 Minutes)

## Delivery Framework
This lesson plan can be delivered as **two 75-minute class sessions** (e.g., Tuesday/Thursday) or as **one continuous 150-minute lab session**.

---

## Session 1 (75 Mins): Environment Onboarding & System Catalog Exploration

### Objective
Ensure 100% of students are successfully connected to PostgreSQL 16 via GitHub Codespaces, understand the client-server distinction, and can navigate database metadata programmatically.

### Timeline & Pacing
* **00:00 – 00:15 (Warmup & Setup Triage)**:
  - Students open laptops and launch their GitHub Codespaces.
  - Triage any connection or authentication errors immediately.
  - Verify terminal command: `psql $DATABASE_URL`.
* **00:15 – 00:35 (Interactive Concept Debrief)**:
  - Think-Pair-Share: Ask students to turn to their neighbor and explain the **"Flashlight Metaphor"** (Warehouse $\rightarrow$ Table $\rightarrow$ Column $\rightarrow$ Row).
  - Call on two student pairs to share their definitions.
  - Instructor live-demo: The Trailing Comma trap and the Missing Semicolon trap in `psql`.
* **00:35 – 00:60 (Guided Activity: Investigating the Information Schema)**:
  - Have students open `week1_orientation.sql` in their Codespaces editor.
  - Work through Queries 1–5 together (checking PostgreSQL version, current database, timezone).
  - Challenge students to write Query 6: Finding all table names in the `public` schema.
* **00:60 – 00:75 (Debrief & Exit Ticket)**:
  - Review: Why do we use `information_schema.tables` instead of relying only on a GUI? *(Answer: Code is automatable; GUIs require manual clicks)*.
  - Exit Ticket: Run `SELECT count(*) FROM information_schema.columns WHERE table_name = 'employees';` and record the result.

---

## Session 2 (75 Mins): Live-Coding SELECT, Expressions, Aliases & Sorting

### Objective
Transition students from system orientation to writing clean, production-grade `SELECT` queries with column projection, math expressions, string concatenation, de-duplication, and multi-column sorting.

### Timeline & Pacing
* **00:00 – 00:10 (Review & Logic Check)**:
  - Quick quiz poll on the board: *"What order does the database execute FROM, SELECT, and ORDER BY?"*
* **00:10 – 00:35 (Instructor Live Demonstration & Student Shadow Coding)**:
  - Open `units/unit_01_selection_and_fundamentals/sync/inclass_challenges.sql`.
  - Walk through:
    1. Single-column vs. multi-column projection.
    2. Adding a computed column (calculating employee annual compensation including bonus).
    3. String concatenation with `||` and column aliasing with `AS`.
    4. Multi-level `ORDER BY` (Department ASC, Salary DESC).
* **00:35 – 00:65 (Paired Active Learning Lab)**:
  - Pair up students into Driver/Navigator roles.
  - Students work on Challenges 1 through 5 in `inclass_challenges.sql`.
  - Instructor and TA circulate to check syntax formatting (UPPERCASE keywords, no trailing commas).
* **00:65 – 00:75 (Solutions Review & Wrap-up)**:
  - Have volunteer students share their queries on the main display.
  - Highlight alternative valid approaches.
  - Remind students of the Unit 1 Lab submission and Quiz deadline.
