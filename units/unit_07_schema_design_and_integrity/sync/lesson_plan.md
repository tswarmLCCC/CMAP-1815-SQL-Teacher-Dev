# Unit 7: Synchronous Active Learning Lesson Plan (150 Minutes)

## Delivery Framework
This lesson plan can be delivered as **two 75-minute class sessions** or as **one continuous 150-minute lab session**.

---

## Session 1 (75 Mins): Relational Normalization Workshop (1NF through 3NF)

### Objective
Students diagnose insertion, update, and deletion anomalies in flat, unnormalized files and decompose multi-tiered entities into pristine Third Normal Form (3NF) structures.

### Timeline & Pacing
* **00:00 – 00:15 (The Spreadsheet Disaster Hook)**:
  - Project a 15-column denormalized spreadsheet on screen containing repeated customer phone numbers and comma-separated items.
  - Ask: *"If customer Bob changes his phone number, how many rows must we update? What if he cancels his order?"*
  - Define Insertion, Update, and Deletion Anomalies.
* **00:15 – 00:35 (Interactive Live Normalization Clinic)**:
  - Open `units/unit_07_schema_design_and_integrity/sync/inclass_challenges.sql`.
  - Walk through:
    1. Achieving 1NF: Splitting repeating groups and ensuring atomic values.
    2. Achieving 2NF: Identifying composite keys and removing partial dependencies.
    3. Achieving 3NF: Removing transitive dependencies (*"the key, the whole key, and nothing but the key"*).
* **00:35 – 00:60 (Paired Coding Challenges: Challenges 1 & 2)**:
  - Students pair up to solve Challenge 1 (Spreadsheet Decomposition) and Challenge 2 (Entity Relationship Mapping).
  - Circulate to check that students are identifying junction tables for many-to-many relationships.
* **00:60 – 00:75 (Review & Debrief)**:
  - Student live-share: Have a student pair present their 3NF decomposition diagram.

---

## Session 2 (75 Mins): DDL Constraint Engineering & Database Views

### Objective
Equip students to write rock-solid DDL scripts with declarative constraints (`PK`, `FK`, `CHECK`, `UNIQUE`), test constraint rejections, and build secure reporting abstractions using `CREATE VIEW`.

### Timeline & Pacing
* **00:00 – 00:15 (Storage-Layer Defense Hook)**:
  - Demonstrate a bad insert bypassing frontend validation (inserting a negative salary or an invalid status string).
  - Explain why constraint enforcement must live inside the database engine.
* **00:15 – 00:35 (Live Coding: DDL & Constraints)**:
  - Write table DDL with `SERIAL PRIMARY KEY`, `CHECK`, and `FOREIGN KEY`.
  - Demonstrate `ON DELETE RESTRICT` blocking parent row deletion when child rows exist.
  - Create a multi-table joined View with `CREATE OR REPLACE VIEW`.
  - Demonstrate column masking for sensitive employee compensation data.
* **00:35 – 00:65 (Paired Coding Challenges: Challenges 3, 4 & 5)**:
  - Students work in pairs on Challenge 3 (DDL Implementation), Challenge 4 (Constraint Stress Testing), and Challenge 5 (The Executive View).
* **00:65 – 00:75 (Debrief & Exit Ticket)**:
  - Exit Ticket: *"What is the difference between ON DELETE RESTRICT and ON DELETE CASCADE?"*
  - Assign Unit 7 Lab and Quiz.
