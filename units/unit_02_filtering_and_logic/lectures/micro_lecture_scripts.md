# Unit 2: Micro-Lecture Video Scripts

This document contains recording scripts for **three bite-sized, topical micro-lectures** for Unit 2. Each video runs **6 to 9 minutes**, focusing on a single conceptual pillar with clear visual cues and teleprompter-ready narration.

---

## Video 2.1: The WHERE Clause & Comparison Operators
* **Duration:** ~7 minutes
* **Target Audience:** SQL learners moving from projection to row-level filtering
* **Accompanying SQL File:** `part1_where_and_comparisons.sql`
* **On-Screen Assets:** Slide showing "Projection vs. Selection" filter gate, terminal with `psql`.

### Teleprompter & Delivery Script

**[0:00 - 1:30] The Hook: Moving from Flashlight to Scalpel**
> "In Unit 1, we learned Projection—how to use `SELECT` like a flashlight to illuminate specific columns. But our flashlight still illuminated every single row in the filing cabinet.
> 
> If a company has 10 million customer records, you don't want to scroll through 10 million rows just to find customers located in Wyoming.
> 
> Today, we pick up **The Scalpel**. The command in SQL that performs row-level filtering—or 'Selection'—is the **`WHERE`** clause. The `WHERE` clause acts as a strict security gatekeeper: only rows that satisfy your exact logical test are allowed into the final result set."

**[1:31 - 3:45] The Syntax & Standard Comparison Operators**
> "Let's look at the basic anatomy:
> ```sql
> SELECT product_name, retail_price
> FROM products
> WHERE retail_price >= 100.00;
> ```
> Notice where `WHERE` sits: immediately after `FROM`, and before `ORDER BY`.
> 
> PostgreSQL gives us standard mathematical comparison operators:
> * `=` : Equals (Notice: in SQL, we use a single equals sign, not `==` like Python or Java).
> * `<>` or `!=` : Not equal to.
> * `>`, `<`, `>=`, `<=` : Numerical and date comparisons.
> 
> You can also filter dates:
> ```sql
> SELECT first_name, hire_date
> FROM employees
> WHERE hire_date >= '2020-01-01';
> ```
> In SQL, always wrap dates and string text in **single quotation marks** (`'...'`)."

**[3:46 - 5:30] The BETWEEN Operator: Inclusive Boundaries**
> "What if management asks for products priced between $25 and $75?
> You could write `WHERE retail_price >= 25 AND retail_price <= 75`.
> But SQL gives us a cleaner, more readable shorthand:
> ```sql
> SELECT product_name, retail_price
> FROM products
> WHERE retail_price BETWEEN 25.00 AND 75.00;
> ```
> **Crucial Rule:** `BETWEEN` is strictly **inclusive**. It includes both the low value (25.00) and the high value (75.00). If you need exclusive boundaries, use standard `<` and `>` operators."

**[5:31 - 7:30] The Order of Execution Trap!**
> "Here is the number one syntax mistake students make in Unit 2:
> Suppose you create a column alias:
> ```sql
> SELECT product_name, retail_price * 0.90 AS sale_price
> FROM products
> WHERE sale_price < 50.00; -- ❌ THIS WILL FAIL!
> ```
> If you run this, PostgreSQL throws an error: `ERROR: column "sale_price" does not exist`.
> 
> Why? Remember the internal order of execution:
> 1. `FROM`
> 2. `WHERE` (The filter runs HERE!)
> 3. `SELECT` (The alias `sale_price` isn't created until here!)
> 
> Because `WHERE` runs *before* `SELECT`, it has no idea what `sale_price` means! You must repeat the expression in the `WHERE` clause:
> `WHERE retail_price * 0.90 < 50.00`.
> 
> In Video 2.2, we'll learn how to search within lists and match messy text patterns."

---

## Video 2.2: Pattern Matching & Lists: LIKE & IN
* **Duration:** ~7 minutes
* **Target Audience:** Beginners handling text searches and categorical filters
* **Accompanying SQL File:** `part2_pattern_matching_and_in.sql`
* **On-Screen Assets:** Editor showing string searches, wildcard visual animations (`%` vs `_`).

### Teleprompter & Delivery Script

**[0:00 - 2:00] The IN Operator: Filtering Against Sets**
> "Welcome back. Let's say human resources asks for a roster of employees in three specific departments: 'Security', 'Research', and 'Sales'.
> 
> Without `IN`, you'd have to write:
> `WHERE department = 'Security' OR department = 'Research' OR department = 'Sales'`.
> That's tedious and error-prone.
> 
> Instead, SQL gives us the elegant **`IN`** operator:
> ```sql
> SELECT first_name, last_name, department
> FROM employees
> WHERE department IN ('Security', 'Research', 'Sales');
> ```
> You pass a comma-separated list inside parentheses. If an employee's department matches *any* item in that set, the row passes through the gate.
> 
> And if you want everyone *except* those three departments? Just negate it:
> `WHERE department NOT IN ('Security', 'Research', 'Sales');`."

**[2:01 - 5:15] Pattern Matching with LIKE & ILIKE**
> "What happens when you don't know the exact text? For instance, searching for a customer whose last name starts with 'Mac', or finding product SKUs that start with 'ELEC'?
> 
> An exact equals sign `=` fails because `'MacDonald'` is not equal to `'Mac'`.
> 
> To solve this, we use the **`LIKE`** operator with **wildcards**:
> 
> 1. **The Percent Symbol (`%`):** Matches **zero, one, or multiple characters**.
>    * `'ELEC%'` matches anything starting with 'ELEC' (`ELEC-01`, `ELECTRONICS`).
>    * `'%cat%'` matches any string containing 'cat' anywhere inside (`concatenate`, `bobcat`, `catalog`).
>    * `'%ing'` matches anything ending in 'ing' (`Engineering`, `Marketing`).
> 
> 2. **The Underscore (`_`):** Matches **exactly one character**.
>    * `'T_m'` matches `'Tom'`, `'Tim'`, and `'Tam'`, but NOT `'Team'`.
> 
> 3. **The PostgreSQL Superpower: `ILIKE`**
> In standard SQL, `LIKE` is case-sensitive: `'cat'` won't match `'Catalog'`. But PostgreSQL provides `ILIKE` (the 'I' stands for Insensitive):
> ```sql
> SELECT product_name FROM products WHERE product_name ILIKE '%widget%';
> ```
> This matches 'Widget', 'WIDGET', or 'widget' effortlessly."

**[5:16 - 7:00] Summary & Transition to Logic Gates**
> "Pattern matching with `LIKE` and set filtering with `IN` are the daily bread and butter of data analysts and software engineers.
> 
> But what happens when you have to evaluate two or three conditions at once—and what happens when data is missing? That brings us to Video 2.3: Boolean Gates and the Mystery of `NULL`."

---

## Video 2.3: Boolean Gates & Three-Valued Logic with NULLs
* **Duration:** ~8 minutes
* **Target Audience:** Students tackling boolean evaluation and SQL's unique NULL behavior
* **Accompanying SQL File:** `part3_boolean_logic_and_nulls.sql`
* **On-Screen Assets:** Truth table graphics, terminal demonstration of the `= NULL` disaster.

### Teleprompter & Delivery Script

**[0:00 - 2:30] Boolean Gates: AND, OR, and The Parentheses Rule**
> "Welcome to Video 2.3. When you have multiple criteria, you combine them with boolean operators:
> * **`AND`**: Both conditions must be true.
> * **`OR`**: At least one condition must be true.
> * **`NOT`**: Inverts the condition.
> 
> But beware the **Operator Precedence Trap**:
> In mathematics, multiplication happens before addition. In SQL, **`AND` always executes before `OR`**!
> 
> Look at this query:
> ```sql
> SELECT first_name, department, salary
> FROM employees
> WHERE department = 'Security' OR department = 'Sales' AND salary >= 70000;
> ```
> A human reads this as: *'Give me everyone in Security or Sales making at least 70k.'*
> But SQL reads it as: *'Give me anyone making 70k in Sales... OR literally anyone in Security, even if they make 20k!'*
> 
> **The Golden Rule:** Always protect your `OR` statements with **parentheses**:
> `WHERE (department = 'Security' OR department = 'Sales') AND salary >= 70000;`."

**[2:31 - 5:45] The Mystery of NULL & The = NULL Trap**
> "Now, let's confront the single most misunderstood concept in all of relational databases: **`NULL`**.
> 
> In SQL, `NULL` does NOT mean zero. It does NOT mean an empty string `""`.
> `NULL` means: **Unknown, Missing, or Not Recorded.**
> 
> Because `NULL` represents an unknown state, SQL uses **Three-Valued Logic**: an expression can be `TRUE`, `FALSE`, or `UNKNOWN`.
> 
> Here is the fatal trap:
> ```sql
> SELECT * FROM employees WHERE bonus = NULL; -- ❌ NEVER DO THIS!
> ```
> If you run this query, PostgreSQL returns **zero rows**. Even if you have 10 employees with no bonus, none of them show up!
> 
> Why? Because you are asking: *'Is this unknown value equal to that unknown value?'* And SQL answers: *'I don't know! It's UNKNOWN.'* And in a `WHERE` clause, only `TRUE` gets through the gate.
> 
> To test for missing data, you must use the special keywords:
> ```sql
> SELECT first_name, bonus FROM employees WHERE bonus IS NULL;
> SELECT first_name, bonus FROM employees WHERE bonus IS NOT NULL;
> ```
> Memorize this: **Never use `=` with `NULL`. Always use `IS NULL` or `IS NOT NULL`.**"

**[5:46 - 8:00] Pagination: LIMIT & OFFSET**
> "Finally, let's talk about result limits:
> ```sql
> SELECT product_name, retail_price
> FROM products
> ORDER BY retail_price DESC
> LIMIT 5;
> ```
> `LIMIT 5` gives you only the top 5 records.
> 
> If you add `OFFSET 5`:
> `LIMIT 5 OFFSET 5;`
> PostgreSQL skips the first 5 records and gives you records 6 through 10. That is exactly how modern web applications paginate through search results!
> 
> You now have the complete filtering toolkit: comparison operators, `IN`, `LIKE`, Boolean logic with parentheses, `IS NULL`, and `LIMIT`. Open up your Codespace and let's put it to work in the lab!"
