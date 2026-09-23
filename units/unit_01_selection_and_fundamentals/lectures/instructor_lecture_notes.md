# Unit 1: Instructor Lecture Walkthrough Notes

## Purpose of this Document
These notes provide the instructor with the exact talking points, on-screen demo cues, pacing guidelines, and student pitfalls to highlight when delivering or recording the Unit 1 micro-lectures and leading in-class discussions.

---

## Micro-Lecture 1.1: Relational Foundations & AI Grounding
* **Estimated Recording Time:** 7 minutes
* **Key Demonstration SQL:** `units/unit_01_selection_and_fundamentals/lectures/part1_relational_foundations.sql`

### Preparation & Screen Setup
- Open GitHub Codespaces in full-screen browser mode.
- Terminal in bottom panel connected via `psql $DATABASE_URL`.
- Slide deck or conceptual diagram tab open showing:
  1. Spreadsheet row limit / corruption risks vs. Relational Table separation.
  2. The "Warehouse & Filing Cabinet" Metaphor diagram.
  3. Client-Server interaction model.

### Key Talking Points & Teaching Tips
1. **Emphasize the "Why":** Students frequently ask *"Why can't I just do this in Excel?"* Point out Excel's 1,048,576 row hard ceiling and how easily a user can desynchronize columns when sorting manually.
2. **The AI Connection:** Frame SQL as the language of factual truth. An LLM trained on web data guesses; a SQL query against PostgreSQL returns verifiable facts. This connects directly to RAG (Retrieval-Augmented Generation).
3. **Client vs. Server:** Emphasize that `psql` and VS Code don't hold the data. The data is managed by PostgreSQL. If you shut down your laptop, the data in the cloud database remains safe and untouched.

---

## Micro-Lecture 1.2: Anatomy of SELECT & Projection
* **Estimated Recording Time:** 8 minutes
* **Key Demonstration SQL:** `units/unit_01_selection_and_fundamentals/lectures/part2_anatomy_of_select.sql`

### Common Traps to Intentionally Demonstrate & Break On Camera
1. **The Missing Semicolon:**
   - Type `SELECT first_name FROM employees` and hit Enter without a semicolon.
   - Show how `psql` gives you a continuation prompt (`mydb-#`).
   - Explain to students: *"The computer isn't frozen; it is politely waiting for you to finish your thought."* Type `;` and hit Enter to complete it.
2. **The Trailing Comma Error:**
   - Type `SELECT first_name, last_name, FROM employees;`.
   - Run it. Show PostgreSQL's error message pointing directly at `FROM`.
   - Explain: *"A comma means 'another column is coming.' If the next word is FROM, the parser panics."*
3. **The Sledgehammer Asterisk (`*`):**
   - Run `SELECT * FROM employees;`.
   - Ask students: *"If this table had 100 columns including SSN, hashed passwords, and home phone numbers, would you want this on a projector screen or sent to a frontend web app?"* Emphasize why explicit column projection is industry best practice.

---

## Micro-Lecture 1.3: Expressions, Aliases & Sorting
* **Estimated Recording Time:** 8 minutes
* **Key Demonstration SQL:** `units/unit_01_selection_and_fundamentals/lectures/part3_projection_and_sorting.sql`

### Key Teaching Strategies
1. **Expressions as Virtual Columns:**
   - Emphasize that `salary * 1.05` does **NOT** update the table. Run `SELECT salary FROM employees;` immediately afterward to prove the underlying values never changed.
2. **Column Aliases with `AS`:**
   - Show what happens without `AS` (`?column?`).
   - Mention standard naming conventions: use `snake_case` for aliases (`projected_salary`, not `Projected Salary`). If you must use spaces, double quotes `"Projected Salary"` are required, but discourage double quotes in beginner classes to avoid syntax confusion.
3. **`DISTINCT` Placement:**
   - Point out that `DISTINCT` applies to the *entire combination of projected columns*, not just the first column.
   - Example: `SELECT DISTINCT department, title FROM employees;` returns unique *pairs*.
4. **`ORDER BY` Mechanics:**
   - Emphasize that SQL tables are unordered bags of rows by default. Without `ORDER BY`, PostgreSQL can return rows in whatever physical disk order it finds easiest.
   - Demonstrate multi-column sort: `ORDER BY department ASC, salary DESC`. Explain: *"Sort the departments first; within each department, rank salaries from highest to lowest."*
