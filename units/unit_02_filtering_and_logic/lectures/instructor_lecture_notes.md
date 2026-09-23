# Unit 2: Instructor Lecture Walkthrough Notes

## Purpose of this Document
These notes provide the instructor with the exact talking points, on-screen demo cues, pacing guidelines, and student pitfalls to highlight when delivering or recording the Unit 2 micro-lectures and leading in-class discussions.

---

## Micro-Lecture 2.1: The WHERE Clause & Comparison Operators
* **Estimated Recording Time:** 7 minutes
* **Key Demonstration SQL:** `units/unit_02_filtering_and_logic/lectures/part1_where_and_comparisons.sql`

### Preparation & Screen Setup
- Open GitHub Codespaces terminal connected to PostgreSQL (`psql $DATABASE_URL`).
- Have a split editor ready showing the `products` table schema.

### Key Talking Points & Live Demos
1. **Selection vs. Projection:** Reinforce the difference: `SELECT` chooses columns; `WHERE` restricts rows.
2. **Single Equals Sign:** Emphasize that SQL uses a single `=` for equality comparison (unlike C++, Java, or Python which use `==`).
3. **Quoting Values:** Strings and dates require single quotes `'...'`. Numerical values must NOT have quotes.
4. **The Order of Execution Trap:** Intentionally write a query trying to use a column alias in the `WHERE` clause. Show students the error: `column "alias" does not exist`. Trace the pipeline on screen (`FROM` $\rightarrow$ `WHERE` $\rightarrow$ `SELECT` $\rightarrow$ `ORDER BY`) to prove *why* the alias isn't available yet.

---

## Micro-Lecture 2.2: Pattern Matching & Lists: LIKE & IN
* **Estimated Recording Time:** 7 minutes
* **Key Demonstration SQL:** `units/unit_02_filtering_and_logic/lectures/part2_pattern_matching_and_in.sql`

### Key Teaching Tips
1. **The Elegance of `IN`:** Contrast a multi-line `OR` query against a clean `WHERE department IN ('Security', 'Sales')`.
2. **Wildcards Visualized:**
   - Draw `%` on the whiteboard or screen: "Zero, one, or any number of characters."
   - Draw `_` on screen: "Exactly one character placeholder."
   - Demo the difference between `LIKE 'D%'` (Dresden, Denver) vs. `LIKE '%d'` (Fraser, Snow).
3. **`ILIKE` in PostgreSQL:** Explain that ANSI SQL specifies `LIKE` as case-sensitive. PostgreSQL provides `ILIKE` as an invaluable real-world extension, preventing missed records caused by inconsistent user input (e.g., `'retail'`, `'Retail'`, `'RETAIL'`).

---

## Micro-Lecture 2.3: Boolean Gates & Three-Valued Logic with NULLs
* **Estimated Recording Time:** 8 minutes
* **Key Demonstration SQL:** `units/unit_02_filtering_and_logic/lectures/part3_boolean_logic_and_nulls.sql`

### Intentional Traps to Break On Camera (High Impact)
1. **The Dangerous Ambiguity of `AND` vs. `OR`:**
   - Run: `SELECT * FROM employees WHERE department = 'Security' OR department = 'Sales' AND salary >= 70000;`.
   - Show how low-earning security staff (e.g. guard dogs at $20,000!) appear in the result set because `AND` bound to `Sales` first.
   - Add parentheses: `WHERE (department = 'Security' OR department = 'Sales') AND salary >= 70000;`.
   - Watch the irrelevant rows vanish! Emphasize: *"Always use parentheses with OR."*
2. **The `= NULL` Trap:**
   - Run: `SELECT * FROM employees WHERE bonus = NULL;`.
   - Point out that it returns **0 rows**.
   - Then run: `SELECT * FROM employees WHERE bonus IS NULL;`.
   - Watch 7 rows suddenly appear! Explain Three-Valued Logic (`UNKNOWN` $\ne$ `TRUE`).
3. **`LIMIT` and `OFFSET`:**
   - Demonstrate `LIMIT 5 OFFSET 0` (Page 1) and `LIMIT 5 OFFSET 5` (Page 2).
   - Emphasize that without `ORDER BY`, `LIMIT` is unpredictable because the database doesn't guarantee row order.
