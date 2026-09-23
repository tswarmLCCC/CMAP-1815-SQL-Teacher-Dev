# Unit 5: Synchronous Active Learning Lesson Plan (150 Minutes)

## Delivery Framework
This lesson plan can be delivered as **two 75-minute class sessions** or as **one continuous 150-minute lab session**.

---

## Session 1 (75 Mins): Safe Mutation Protocols, Upserts & The RETURNING Clause

### Objective
Students master the 3-Step Pre-Execution Protocol for `UPDATE` and `DELETE`, write atomic upserts with `ON CONFLICT`, and use `RETURNING` for immediate operational feedback.

### Timeline & Pacing
* **00:00 – 00:15 (The Runaway Update Hook)**:
  - Open terminal on projector. Type `UPDATE employees SET salary = 100000;`.
  - Show the 50 affected rows. Ask: *"What just happened, and how do we prevent this from destroying our careers?"*
  - Introduce the 3-Step Pre-Execution Protocol (SELECT first $\rightarrow$ check row count $\rightarrow$ execute modification).
* **00:15 – 00:35 (Interactive Live Coding: Safe DML & RETURNING)**:
  - Open `units/unit_05_safe_dml_and_modifications/sync/inclass_challenges.sql`.
  - Walk through:
    1. Multi-row `INSERT` with explicit column lists.
    2. Atomic upserts using `ON CONFLICT (product_id) DO UPDATE SET ...` and explain `EXCLUDED`.
    3. Running `UPDATE` and `DELETE` with `RETURNING` to inspect mutated rows in real-time.
* **00:35 – 00:60 (Paired Coding Challenges: Challenges 1 & 2)**:
  - Students pair up to solve Challenge 1 (Catalog Expansion & Upsert) and Challenge 2 (Targeted Compensation Adjustment).
  - Circulate to verify that students are running validation queries before modifying data.
* **00:60 – 00:75 (Review & Debrief)**:
  - Student live-share: Have a pair demonstrate their upsert and explain how `EXCLUDED` worked.

---

## Session 2 (75 Mins): ACID Transactions, Staging Tables & ETL Cleanup Pipelines

### Objective
Equip students to use ACID transactions (`BEGIN`, `COMMIT`, `ROLLBACK`) as safety nets, create private `TEMP TABLE`s, and implement multi-step data cleaning pipelines.

### Timeline & Pacing
* **00:00 – 00:15 (The ATM & Power Outage Hook)**:
  - Diagram the $500 bank transfer on the whiteboard. Explain how partial failure results in money vanishing.
  - Introduce ACID properties, focusing on Atomicity and the `ROLLBACK` command.
* **00:15 – 00:35 (Live Coding: Transactions & Temp Staging)**:
  - Live demo: Run a `DELETE` inside `BEGIN;`, verify table is empty, then run `ROLLBACK;` to restore everything.
  - Create a `TEMPORARY TABLE stage_inventory`, insert dirty text data with currency signs and commas, clean it using SQL functions, and promote clean rows.
* **00:35 – 00:65 (Paired Coding Challenges: Challenges 3, 4 & 5)**:
  - Students work in pairs on Challenge 3 (Transaction Rollback Clinic), Challenge 4 (Vendor Feed Staging & Scrubbing), and Challenge 5 (Production Promotion).
* **00:65 – 00:75 (Debrief & Exit Ticket)**:
  - Exit Ticket: *"Why is a temporary table safer for data ingestion than a production table?"*
  - Assign Unit 5 Lab and Quiz.
