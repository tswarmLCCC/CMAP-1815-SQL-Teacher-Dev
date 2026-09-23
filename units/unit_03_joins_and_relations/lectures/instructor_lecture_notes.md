# Unit 3: Instructor Lecture Walkthrough Notes

## Purpose of this Document
These notes provide the instructor with the exact talking points, on-screen demo cues, pacing guidelines, and student pitfalls to highlight when delivering or recording the Unit 3 micro-lectures and leading in-class discussions.

---

## Micro-Lecture 3.1: Relational Theory & Primary/Foreign Keys
* **Estimated Recording Time:** 7 minutes
* **Key Demonstration SQL:** `units/unit_03_joins_and_relations/lectures/part1_keys_and_inner_join.sql`

### Preparation & Screen Setup
- Open GitHub Codespaces in browser with terminal connected to `psql $DATABASE_URL`.
- Have the ERD from `course_specs/database_schema_spec.md` visible on a slide or side tab.

### Key Talking Points & Teaching Tips
1. **The Normalization Motivation:** Contrast storing raw text in 500 rows vs. storing an ID integer once. Explain update anomalies and insertion anomalies.
2. **Key Distinctions:**
   - **Primary Key:** Must be unique and NOT NULL (`locations.location_id`).
   - **Foreign Key:** Points to a Primary Key (`employees.location_id`). Can be NULL if an employee is unassigned.
3. **Table Aliasing Discipline:** Always use short, meaningful aliases (`e`, `l`, `p`, `o`, `ol`). Do not use confusing generic aliases like `t1`, `t2`.

---

## Micro-Lecture 3.2: Multi-Table Joins & The Cartesian Disaster
* **Estimated Recording Time:** 8 minutes
* **Key Demonstration SQL:** `units/unit_03_joins_and_relations/lectures/part2_multi_table_joins.sql`

### Intentional Traps to Demonstrate On Camera
1. **The Ambiguous Column Crash:**
   - Write: `SELECT location_id, first_name, city FROM employees e JOIN locations l ON e.location_id = l.location_id;`.
   - Run it. Show PostgreSQL's error: `ERROR: column reference "location_id" is ambiguous`.
   - Explain: *"Both tables have a column called location_id! PostgreSQL cannot guess which one you want. You must write e.location_id or l.location_id."*
2. **The Accidental Cartesian Product:**
   - Explain how old SQL (SQL-89) allowed `FROM table1, table2`.
   - Show how forgetting a WHERE clause multiplies row counts exponentially. Emphasize why modern ANSI SQL `JOIN ... ON` prevents this fatal mistake.

---

## Micro-Lecture 3.3: Outer Joins & The Missing Data Audit (Anti-Joins)
* **Estimated Recording Time:** 8 minutes
* **Key Demonstration SQL:** `units/unit_03_joins_and_relations/lectures/part3_outer_joins_and_antijoins.sql`

### Teaching the Anti-Join (The "Aha!" Moment)
1. **Venn Diagram vs. Relational Reality:** Clarify that Venn diagrams can be misleading because SQL joins match rows, not sets.
2. **Step-by-Step Anti-Join Reveal:**
   - Step 1: Run an `INNER JOIN` between `products` and `order_lines`. Count rows.
   - Step 2: Change to `LEFT JOIN`. Show how unsold products now appear with `NULL` under `order_id`.
   - Step 3: Add `WHERE ol.order_line_id IS NULL`.
   - Highlight the result: *"Look at that! We have instantly extracted the exact list of dead inventory without writing a subquery!"*
3. **LEFT vs. RIGHT Join:** Advise students to stick to `LEFT JOIN` exclusively. Any `RIGHT JOIN` can be rewritten as a `LEFT JOIN` simply by swapping the table order in the `FROM` clause. Consistent left-to-right reading makes code vastly easier to review.
