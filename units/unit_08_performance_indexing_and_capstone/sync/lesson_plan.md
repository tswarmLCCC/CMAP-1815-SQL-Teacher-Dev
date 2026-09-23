# Unit 8: Synchronous Active Learning Lesson Plan (150 Minutes)

## Delivery Framework
This lesson plan can be delivered as **two 75-minute class sessions** or as **one continuous 150-minute lab session**.

---

## Session 1 (75 Mins): Query Performance Profiling & Index Engineering Clinic

### Objective
Students learn to read PostgreSQL execution plans using `EXPLAIN ANALYZE`, identify sequential scan bottlenecks, engineer targeted B-Tree and composite indexes, and evaluate the trade-offs of the Write Penalty.

### Timeline & Pacing
* **00:00 – 00:15 (The 45-Second Production Nightmare Hook)**:
  - Demonstrate a query on a large table with and without an index.
  - Show the dramatic contrast in latency (e.g. 1,200 ms vs. 1.4 ms).
  - Introduce `EXPLAIN ANALYZE` and the cost-based optimizer.
* **00:15 – 00:35 (Interactive Live Coding: Indexing Clinic)**:
  - Open `units/unit_08_performance_indexing_and_capstone/sync/inclass_challenges.sql`.
  - Walk through:
    1. Interpreting `Seq Scan`, `Index Scan`, `Bitmap Index Scan`.
    2. Creating single-column vs. composite B-Tree indexes.
    3. The Write Penalty: Demonstrating how indexes slow down batch `INSERT` operations.
    4. Partial indexes for skewed status columns.
* **00:35 – 00:60 (Paired Coding Challenges: Challenges 1 & 2)**:
  - Students pair up to solve Challenge 1 (Plan Profiling Clinic) and Challenge 2 (Targeted Composite Indexing).
  - Circulate to ensure students understand the leading-column rule in composite indexes.
* **00:60 – 00:75 (Review & Debrief)**:
  - Student live-share: Have a pair explain their execution plan before and after index creation.

---

## Session 2 (75 Mins): Capstone Architecture Defense & Final Review

### Objective
Students finalize and defend their comprehensive Course Capstone Architecture, synthesizing all 8 weeks of schema design, constraints, ETL staging, advanced analytics, and performance optimization.

### Timeline & Pacing
* **00:00 – 00:15 (The Capstone Synthesis Review)**:
  - Review the 5 core pillars of the Capstone project: Normalization, Integrity, DML Staging, Analytics (CTEs/Windows), and Performance Profiling.
* **00:15 – 00:50 (Capstone Clinic & Paired Review)**:
  - Students work in pairs to cross-review their Capstone scripts (`lab8_submission.sql`).
  - Peer verification: Run peer scripts in `psql` to verify zero syntax errors and validate schema constraints.
* **00:50 – 00:70 (Capstone Defense Presentations)**:
  - Selected student teams present their normalized schemas, explain their constraint choices, and walk through their `EXPLAIN ANALYZE` optimization gains.
* **00:70 – 00:75 (Course Wrap-up & Celebration)**:
  - Instructor closing remarks: Transitioning from student to professional database engineer.
  - Final Quiz and Capstone submission deadlines.
