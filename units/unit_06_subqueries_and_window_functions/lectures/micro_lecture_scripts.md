# Unit 6: Micro-Lecture Video Scripts

This document contains recording scripts for **three bite-sized, topical micro-lectures** for Unit 6. Each video runs **6 to 9 minutes**, focusing on query modularity, Common Table Expressions (CTEs), and Window Functions.

---

## Video 6.1: Subqueries vs. Common Table Expressions (CTEs)
* **Duration:** ~7 minutes
* **Target Audience:** SQL learners transitioning from messy nested subqueries to clean, modular pipelines
* **Accompanying SQL File:** `part1_subqueries_and_ctes.sql`
* **On-Screen Assets:** Visual comparison of inside-out nested subqueries vs. top-down CTE pipelines; `psql` demonstration.

### Teleprompter & Delivery Script

**[0:00 - 1:30] The Hook: Escaping the "Subquery Inception"**
> "Have you ever tried reading a query written by a coworker that has four levels of nested subqueries inside the `FROM` clause?
> 
> You have to scroll to line 45, read backwards to line 30, wrap your head around what table is being generated, and then scroll back out to line 10. We call this **Subquery Inception**. It is fragile, hard to maintain, and a nightmare to debug.
> 
> In modern professional SQL, we replace nested subqueries with **Common Table Expressions**, or **CTEs** using the **`WITH`** keyword."

**[1:31 - 4:00] The Syntax of WITH**
> "A Common Table Expression is essentially a temporary, named result set that exists only for the duration of your query.
> Think of it like defining a local variable in Python or JavaScript:
> ```sql
> WITH departmental_averages AS (
>     SELECT department, AVG(salary) AS avg_sal
>     FROM employees
>     GROUP BY department
> )
> SELECT e.first_name, e.salary, d.avg_sal
> FROM employees e
> JOIN departmental_averages d ON e.department = d.department
> WHERE e.salary > d.avg_sal;
> ```
> Notice how clean and readable that is!
> 1. In line 1, we define `departmental_averages`.
> 2. In line 7, our main query reads like simple English: join employees to departmental averages and find staff earning above average."

**[4:01 - 6:15] Chaining Multiple CTEs**
> "You aren't limited to a single CTE. You can chain as many as you need, separated by commas:
> ```sql
> WITH raw_orders AS (
>     SELECT * FROM orders WHERE order_date >= '2023-01-01'
> ),
> customer_order_totals AS (
>     SELECT customer_id, COUNT(*) AS total_orders, SUM(total_amount) AS total_spend
>     FROM raw_orders
>     GROUP BY customer_id
> ),
> vip_customers AS (
>     SELECT * FROM customer_order_totals WHERE total_spend > 5000.00
> )
> SELECT * FROM vip_customers ORDER BY total_spend DESC;
> ```
> Each CTE can reference any CTE defined before it! This transforms your SQL from a convoluted puzzle into an organized, step-by-step data pipeline."

**[6:16 - 7:30] Summary & Transition**
> "To recap:
> * Prefer CTEs (`WITH`) over deeply nested subqueries.
> * CTEs read from top to bottom, making your logic self-documenting and easy to unit test.
> In Video 6.2, we introduce the most powerful analytical tool in SQL: Window Functions."

---

## Video 6.2: The Anatomy of Window Functions & Ranking
* **Duration:** ~8 minutes
* **Target Audience:** Developers needing analytical calculations without losing row-level granularity
* **Accompanying SQL File:** `part2_window_functions_and_ranking.sql`
* **On-Screen Assets:** Animation showing rows passing through an analytical calculation window while retaining all original columns; `ROW_NUMBER` vs `RANK` vs `DENSE_RANK` comparison graphic.

### Teleprompter & Delivery Script

**[0:00 - 1:40] The Fundamental Dilemma: Detail vs. Summary**
> "In Unit 4, we learned that `GROUP BY` collapses rows. If you have 50 employees across 5 departments, `GROUP BY department` outputs exactly 5 rows.
> 
> But what if you want to display the employee's name, their individual salary, AND their department's average salary on the exact same row?
> 
> With `GROUP BY`, that was impossible without joining the table back to itself.
> Today, we unlock the superpower that changed SQL forever: **Window Functions**."

**[1:41 - 4:10] The OVER() Clause & PARTITION BY**
> "A window function performs a calculation across a set of rows, but does **not** collapse the rows!
> Look at this query:
> ```sql
> SELECT 
>     first_name,
>     department,
>     salary,
>     AVG(salary) OVER(PARTITION BY department) AS dept_avg_salary
> FROM employees;
> ```
> Notice what happens:
> * Every single employee row remains on your screen!
> * The `OVER(PARTITION BY department)` clause tells PostgreSQL: *'Group rows by department in memory, calculate the average salary for each department, and stamp that departmental average onto every employee's row.'*
> 
> We can now easily compute variance:
> `salary - AVG(salary) OVER(PARTITION BY department) AS salary_diff_from_dept_avg`."

**[4:11 - 6:40] Ranking: ROW_NUMBER vs. RANK vs. DENSE_RANK**
> "Often in business, you need to rank entities: *'Who are our top 3 salespeople in each region?'*
> SQL gives us three ranking functions, and you must know the difference:
> 
> 1. **`ROW_NUMBER()`**: Assigns a strictly sequential integer: 1, 2, 3, 4. Even if two people earn the exact same salary, one gets 2 and the other gets 3. Never produces ties.
> 2. **`RANK()`**: Assigns the same rank to ties, but **skips** numbers afterwards. If two people tie for rank 2, the next person is ranked 4!
> 3. **`DENSE_RANK()`**: Assigns the same rank to ties, but **does not skip** numbers. If two people tie for rank 2, the next person is ranked 3!
> 
> ```sql
> SELECT 
>     first_name, department, salary,
>     DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS dept_rank
> FROM employees;
> ```"

**[6:41 - 8:00] Summary & Next Steps**
> "Window functions give you the power of aggregation without the row destruction of `GROUP BY`.
> In Video 6.3, we'll use window functions to calculate running cumulative balances and explore the industry-standard record deduplication pattern."

---

## Video 6.3: Running Balances & The Deduplication Pattern
* **Duration:** ~8 minutes
* **Target Audience:** Data engineers and analysts implementing financial tracking and golden-record deduplication
* **Accompanying SQL File:** `part3_running_totals_and_deduplication.sql`
* **On-Screen Assets:** Visual running total accumulator chart; deduplication filter pipeline diagram.

### Teleprompter & Delivery Script

**[0:00 - 1:45] Cumulative Metrics & Moving Averages**
> "In financial auditing and revenue reporting, point-in-time metrics aren't enough. Leadership wants to see **momentum**:
> *'What is our cumulative revenue day by day throughout the quarter?'*
> 
> In traditional programming, you'd write a `for` loop with an accumulator variable.
> In modern SQL, you use an ordered window:
> ```sql
> SELECT 
>     order_date,
>     order_amount,
>     SUM(order_amount) OVER(ORDER BY order_date) AS running_total_revenue
> FROM daily_orders;
> ```
> By adding `ORDER BY order_date` inside `OVER()`, PostgreSQL automatically accumulates every row from the beginning of time up to the current row!"

**[1:46 - 4:30] Window Frames: ROWS BETWEEN**
> "By default, when you provide `ORDER BY` inside `OVER()`, PostgreSQL evaluates the frame from `UNBOUNDED PRECEDING` to `CURRENT ROW`.
> 
> What if you want a **3-day rolling moving average**?
> You specify the frame explicitly:
> ```sql
> SELECT 
>     order_date,
>     order_amount,
>     ROUND(AVG(order_amount) OVER(
>         ORDER BY order_date 
>         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
>     ), 2) AS rolling_3day_avg
> FROM daily_orders;
> ```
> The database calculates the average using only the current row and the two preceding rows. This is the cornerstone of algorithmic trend analysis."

**[4:31 - 6:50] The Industry Deduplication Pattern**
> "Now, let's learn the single most famous SQL interview pattern in data engineering: **Deduplication**.
> 
> Suppose a bug in your payment gateway inserted duplicate orders, or you want to find the single latest order for each customer:
> ```sql
> WITH ranked_orders AS (
>     SELECT 
>         order_id,
>         customer_id,
>         order_date,
>         order_amount,
>         ROW_NUMBER() OVER(
>             PARTITION BY customer_id 
>             ORDER BY order_date DESC, order_id DESC
>         ) AS row_num
>     FROM orders
> )
> SELECT *
> FROM ranked_orders
> WHERE row_num = 1;
> ```
> Let's analyze how this works:
> 1. `PARTITION BY customer_id` creates a private bucket for each customer.
> 2. `ORDER BY order_date DESC` places their most recent order at rank 1.
> 3. The outer query filters `WHERE row_num = 1`.
> All older or duplicate records are filtered out instantly, leaving only the pristine, latest record for every customer!"

**[6:51 - 8:00] Wrap-Up & Lab Preview**
> "You have now mastered:
> * CTEs for structured, readable SQL.
> * Window functions with `PARTITION BY` and `ORDER BY`.
> * Ranking functions and tie-breakers.
> * Cumulative metrics and moving averages.
> * And the bulletproof `ROW_NUMBER() = 1` deduplication pattern.
> 
> In this week's lab, you'll build an executive financial ledger and clean up a real-world messy dataset using these techniques. Let's get started!"
