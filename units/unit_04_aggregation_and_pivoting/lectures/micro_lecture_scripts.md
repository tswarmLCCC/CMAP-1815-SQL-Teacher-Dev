# Unit 4: Micro-Lecture Video Scripts

This document contains recording scripts for **three bite-sized, topical micro-lectures** for Unit 4. Each video runs **6 to 9 minutes**, focusing on a single conceptual pillar with clear visual cues and teleprompter-ready narration.

---

## Video 4.1: The Core Aggregate Functions & The Funnel
* **Duration:** ~7 minutes
* **Target Audience:** SQL learners shifting from row-level retrieval to executive summarization
* **Accompanying SQL File:** `part1_aggregations_and_groupby.sql`
* **On-Screen Assets:** Slide illustrating the "Funnel" diagram collapsing 10,000 granular rows into categorical summary metrics; terminal with `psql`.

### Teleprompter & Delivery Script

**[0:00 - 1:20] The Hook: From Row Detail to Executive Metrics**
> "Up until today, every query you've written has obeyed a simple rule: one row in your table produces one row on your screen. If you have 50 employees, you get 50 rows.
> 
> But business executives rarely want to read 50,000 individual receipt lines. The CEO wants to know: *'What was total revenue this quarter?'* The CFO asks: *'What is our average employee salary by department?'*
> 
> Today, we transition from reading individual trees to surveying the entire forest. We enter the world of **Aggregation** and the **`GROUP BY`** clause. We call this mental model **The Funnel**—taking hundreds or thousands of granular records and collapsing them into single, actionable numbers."

**[1:21 - 3:15] The Big Five Aggregate Functions**
> "PostgreSQL provides five fundamental mathematical aggregate functions:
> * `COUNT(*)` or `COUNT(column)`: Counts records.
> * `SUM(column)`: Adds up numerical values.
> * `AVG(column)`: Computes the arithmetic mean.
> * `MIN(column)`: Finds the minimum value—works on numbers, dates, and strings.
> * `MAX(column)`: Finds the maximum value.
> 
> Let's look at the critical distinction between `COUNT(*)` and `COUNT(column_name)`:
> ```sql
> SELECT 
>     COUNT(*) AS total_rows,
>     COUNT(manager_id) AS staff_with_managers
> FROM employees;
> ```
> In PostgreSQL, `COUNT(*)` counts the number of physical rows, period. But `COUNT(manager_id)` only counts rows where `manager_id` is **NOT NULL**! If two employees are department heads without a manager, `COUNT(*)` returns 50, while `COUNT(manager_id)` returns 48. Always remember: aggregate functions ignore `NULL` values!"

**[3:16 - 5:20] The Golden Rule of GROUP BY**
> "What if we don't want one giant number for the entire company, but rather numbers grouped by category? That is where `GROUP BY` enters:
> ```sql
> SELECT department, COUNT(*) AS staff_count, AVG(salary) AS avg_salary
> FROM employees
> GROUP BY department;
> ```
> Now pay close attention. Here is the single most common error beginners face in all of SQL:
> ```sql
> SELECT department, first_name, AVG(salary)
> FROM employees
> GROUP BY department;
> ```
> If you run this, PostgreSQL immediately stops you cold:
> `ERROR: column 'employees.first_name' must appear in the GROUP BY clause or be used in an aggregate function.`
> 
> Why? Because `first_name` produces 50 different individual values, while `AVG(salary)` grouped by department produces only 5 rows. A relational table is a strict 2D rectangle—it cannot return a 50-row column and a 5-row column side-by-side!
> 
> **The Golden Rule:** Every single unaggregated column in your `SELECT` list must be explicitly listed in your `GROUP BY` clause."

**[5:21 - 7:00] Summary & Transition**
> "To recap:
> 1. Aggregates collapse rows into summary metrics.
> 2. `COUNT(*)` counts all rows; column-specific aggregates ignore `NULL`s.
> 3. Any column in `SELECT` that isn't wrapped in an aggregate function **must** appear in `GROUP BY`.
> 
> In Video 4.2, we will look at how to filter these grouped results using the `HAVING` clause."

---

## Video 4.2: Row Filtering vs. Group Filtering (WHERE vs. HAVING) & Set Operations
* **Duration:** ~8 minutes
* **Target Audience:** SQL developers needing to filter aggregated data and combine query sets
* **Accompanying SQL File:** `part2_having_and_set_operations.sql`
* **On-Screen Assets:** Execution pipeline animation showing `WHERE` before `GROUP BY` and `HAVING` after `GROUP BY`; Venn diagrams for `UNION`, `INTERSECT`, and `EXCEPT`.

### Teleprompter & Delivery Script

**[0:00 - 1:45] The Trap: Filtering Aggregates in WHERE**
> "Welcome back. Let's start with a problem. Management asks: *'Show me all departments where the average salary is greater than $75,000.'*
> 
> Naturally, a beginner writes:
> ```sql
> SELECT department, AVG(salary)
> FROM employees
> WHERE AVG(salary) > 75000
> GROUP BY department;
> ```
> PostgreSQL immediately rejects this: `ERROR: aggregate functions are not allowed in WHERE`.
> 
> Why does this happen? Remember the database's internal order of execution:
> 1. `FROM`
> 2. `WHERE` (filters individual physical rows)
> 3. `GROUP BY` (collapses surviving rows into buckets)
> 4. `HAVING` (filters summary buckets)
> 5. `SELECT`
> 6. `ORDER BY`
> 
> When the database is evaluating `WHERE`, the groups haven't even been formed yet! The average salary doesn't exist yet."

**[1:46 - 4:10] The Solution: The HAVING Clause**
> "To filter summarized buckets after they are calculated, SQL provides the **`HAVING`** clause:
> ```sql
> SELECT department, AVG(salary) AS avg_sal
> FROM employees
> WHERE is_active = TRUE         -- 1. Discard inactive staff rows first
> GROUP BY department            -- 2. Group surviving staff by department
> HAVING AVG(salary) > 75000     -- 3. Discard department groups earning under $75k
> ORDER BY avg_sal DESC;
> ```
> Notice how `WHERE` and `HAVING` work together in harmony:
> * `WHERE` filters rows **before** aggregation.
> * `HAVING` filters metric groups **after** aggregation.
> 
> If a filter condition does not involve an aggregate function, put it in `WHERE`! Doing so filters out unnecessary rows early, saving memory and compute time."

**[4:11 - 6:30] Set Operations: UNION, INTERSECT, and EXCEPT**
> "Now, what if you have two independent queries and you need to combine their results vertically? We use SQL Set Operations:
> * `UNION`: Combines rows from two queries and strips out duplicate rows.
> * `UNION ALL`: Combines rows and preserves all duplicates. It is much faster because PostgreSQL doesn't need to sort the dataset to detect duplicates.
> * `INTERSECT`: Returns only the rows that exist in both Query 1 and Query 2.
> * `EXCEPT`: Returns rows in Query 1 that do not exist in Query 2.
> 
> **The Two Invariant Rules of Set Operations:**
> 1. Both queries must select the exact same number of columns.
> 2. Corresponding columns must share compatible data types (e.g. integer with integer, text with text)."

**[6:31 - 8:00] Summary & Next Steps**
> "Remember:
> * Use `WHERE` for raw row filters.
> * Use `HAVING` for aggregated group filters.
> * Default to `UNION ALL` unless you specifically require duplicate deduplication.
> In Video 4.3, we'll combine conditional logic with aggregations to pivot data from vertical rows into executive cross-tab reports."

---

## Video 4.3: Conditional Aggregation & Data Pivoting
* **Duration:** ~8 minutes
* **Target Audience:** Analysts building dashboard feeds and executive cross-tab matrices
* **Accompanying SQL File:** `part3_case_and_pivoting.sql`
* **On-Screen Assets:** Visual matrix showing normalized transactional rows folding horizontally into columns.

### Teleprompter & Delivery Script

**[0:00 - 1:40] The Business Problem: Long Data vs. Wide Reports**
> "In relational databases, data is stored 'long': normalized rows stacked vertically. You might have 500 sales rows across 4 quarters.
> 
> But when you deliver data to an executive or an analytics dashboard, they want 'wide' data:
> A table with Region down the left, and Q1, Q2, Q3, Q4 as horizontal columns across the top.
> 
> How do we transform vertical categorical values into separate horizontal metric columns using pure SQL? The answer is **Conditional Aggregation**."

**[1:41 - 4:15] The CASE Statement Inside Aggregates**
> "The secret weapon is placing a `CASE WHEN` expression inside an aggregate function like `COUNT` or `SUM`.
> 
> Let's look at an example from our Superstore dataset:
> ```sql
> SELECT 
>     region,
>     COUNT(CASE WHEN category = 'Furniture' THEN 1 END) AS furniture_orders,
>     COUNT(CASE WHEN category = 'Technology' THEN 1 END) AS technology_orders,
>     COUNT(CASE WHEN category = 'Office Supplies' THEN 1 END) AS office_supplies_orders
> FROM superstore
> GROUP BY region;
> ```
> How does this work?
> When a row's category is 'Furniture', `CASE` returns `1`. `COUNT` increments by 1.
> When a row's category is 'Technology', the condition is false. Because there is no `ELSE`, `CASE` returns `NULL`.
> And what did we learn in Video 4.1? `COUNT` completely ignores `NULL`s!
> The result: a pure, clean category counter pivoted into separate columns."

**[4:16 - 6:30] Pivoting Dollar Volumes with SUM**
> "We can do the exact same trick to calculate revenue totals:
> ```sql
> SELECT 
>     region,
>     SUM(CASE WHEN category = 'Furniture' THEN sales ELSE 0 END) AS furniture_sales,
>     SUM(CASE WHEN category = 'Technology' THEN sales ELSE 0 END) AS tech_sales,
>     SUM(sales) AS total_sales
> FROM superstore
> GROUP BY region;
> ```
> In this query, if the row is 'Furniture', we pass the `sales` dollar amount into `SUM`. Otherwise, we pass `0`.
> 
> In PostgreSQL, you can also use the modern `FILTER` clause:
> ```sql
> SELECT 
>     region,
>     SUM(sales) FILTER (WHERE category = 'Furniture') AS furniture_sales,
>     SUM(sales) FILTER (WHERE category = 'Technology') AS tech_sales
> FROM superstore
> GROUP BY region;
> ```
> Both syntaxes achieve identical results, but the `CASE WHEN` approach is ANSI standard and works in every relational database engine on earth."

**[6:31 - 8:00] Wrap-Up & Lab Challenge**
> "You now possess the foundational tools of modern data analysis:
> * You can collapse data into summary metrics with `COUNT`, `SUM`, and `AVG`.
> * You know how to bucket data with `GROUP BY` and filter buckets with `HAVING`.
> * You can vertically stitch datasets with `UNION ALL`.
> * And you can reshape data horizontally using conditional aggregation.
> 
> In this week's lab, you'll put these techniques to work building a comprehensive regional performance audit for executive leadership. Let's get to work!"
