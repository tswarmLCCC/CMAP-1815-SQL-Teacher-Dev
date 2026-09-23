# Unit 3: Synchronous Active Learning Lesson Plan (150 Minutes)

## Delivery Framework
This lesson plan can be delivered as **two 75-minute class sessions** or as **one continuous 150-minute lab session**.

---

## Session 1 (75 Mins): Relational Foundations, Keys & INNER JOINs

### Objective
Students understand how Primary Keys and Foreign Keys bridge normalized tables, master writing two-table and three-table `INNER JOIN` queries with table aliases, and avoid the ambiguous column error.

### Timeline & Pacing
* **00:00 – 00:15 (Warmup & Conceptual Check)**:
  - Display the course ERD on the projector.
  - Ask students: *"Find the path from an individual product to the employee who sold it."* Have a student trace the foreign key relationships (`products` $\rightarrow$ `order_lines` $\rightarrow$ `orders` $\rightarrow$ `employees`).
* **00:15 – 00:35 (Interactive Live Coding: The Two-Table Bridge)**:
  - Open `units/unit_03_joins_and_relations/sync/inclass_challenges.sql`.
  - Live demo:
    1. Joining `employees` and `locations`.
    2. Demonstrate the ambiguous column error by omitting a table prefix on `location_id`.
    3. Demonstrate chaining a third table (`orders`).
* **00:35 – 00:60 (Paired Coding Challenges: Challenges 1 & 2)**:
  - Students pair up (Driver/Navigator) to solve Challenge 1 (Staff Location Directory) and Challenge 2 (Order Line Revenue Itemization).
  - Instructor and TA circulate to ensure students are aliasing tables cleanly and prefixing projected columns.
* **00:60 – 00:75 (Review & Debrief)**:
  - Have a student pair share their multi-table join and explain how the join conditions connect.

---

## Session 2 (75 Mins): Outer Joins & Anomaly Detection (The Anti-Join)

### Objective
Equip students to identify data loss in `INNER JOIN` queries, master `LEFT JOIN` semantics, and execute the **Anti-Join** pattern to detect orphaned or inactive business entities.

### Timeline & Pacing
* **00:00 – 00:15 (The Hook: The Vanishing Inventory Mystery)**:
  - Live demo on projector: Run an `INNER JOIN` between `products` and `order_lines`.
  - Count the distinct products returned.
  - Compare that count to `SELECT count(*) FROM products;`.
  - Ask: *"Where did the other products go?"*
  - Reveal that `INNER JOIN` completely discards unsold items.
* **00:15 – 00:35 (The Anti-Join Clinic)**:
  - Switch query to `LEFT JOIN`. Show rows where `order_line_id` is populated with `NULL`.
  - Add `WHERE ol.order_line_id IS NULL`.
  - Demonstrate how this uncovers dead inventory in seconds.
* **00:35 – 00:65 (Paired Coding Challenges: Challenges 3, 4 & 5)**:
  - Students work in pairs on Challenge 3 (Dead Inventory Audit), Challenge 4 (Unstaffed Facilities Audit), and Challenge 5 (Superstore Multi-Table Integration).
* **00:65 – 00:75 (Debrief & Exit Ticket)**:
  - Exit Ticket: *"In your own words, explain the difference between what an INNER JOIN returns vs. what an Anti-Join returns."*
  - Announce Unit 3 Lab & Quiz due dates.
