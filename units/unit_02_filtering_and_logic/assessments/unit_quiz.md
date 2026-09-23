# Unit 2 Assessment: Targeted Retrieval, Pattern Matching & Three-Valued Logic Quiz

**Total Questions:** 15  
**Points Possible:** 30 (2 points per question)  
**Time Limit:** 30 Minutes  
**Format:** Multiple Choice & Code Analysis  
**Aligned Learning Outcomes:** CLO 1, Competency 1.6–1.9

---

## Part 1: Conceptual Foundations & Logic Gates (Questions 1–5)

### Question 1
In relational database terminology, what is the fundamental difference between **Projection** and **Selection**?
* A) Projection filters rows; Selection chooses columns.
* B) Projection chooses columns (`SELECT`); Selection restricts rows (`WHERE`).
* C) Projection modifies data on disk; Selection displays data on screen.
* D) Projection works only on numbers; Selection works only on text.

---

### Question 2
Why does the comparison `WHERE bonus = NULL` fail to return records where the bonus column contains missing data?
* A) Because `bonus` is a reserved keyword in PostgreSQL.
* B) Because `NULL` represents an unknown value, and comparing any value to an unknown produces `UNKNOWN`, which fails the `WHERE` filter.
* C) Because `= NULL` only works if the table is sorted in ascending order.
* D) Because PostgreSQL automatically converts all `NULL` values to zero.

---

### Question 3
Under SQL's Three-Valued Logic, what does the Boolean expression `FALSE AND UNKNOWN` evaluate to?
* A) `TRUE`
* B) `FALSE`
* C) `UNKNOWN`
* D) `NULL`

---

### Question 4
Why is `AND` evaluated before `OR` when multiple conditions are chained together without parentheses?
* A) Because SQL standard operator precedence assigns higher priority to conjunction (`AND`) over disjunction (`OR`).
* B) Because `AND` appears earlier in the alphabet than `OR`.
* C) Because PostgreSQL executes clauses from right to left.
* D) This is false; `OR` always executes before `AND`.

---

### Question 5
Why does a query attempting to filter by a column alias in the `WHERE` clause (e.g. `WHERE sale_price < 50`) result in an error in PostgreSQL?
* A) Column aliases cannot contain lowercase letters.
* B) The `WHERE` clause is logically evaluated before the `SELECT` clause where the alias is defined.
* C) The `WHERE` clause only allows column aliases if they are enclosed in square brackets.
* D) Aliases are only permitted in the `ORDER BY` clause.

---

## Part 2: Syntax Debugging & Traps (Questions 6–10)

### Question 6
An analyst writes the following query to find all employees whose last name begins with 'S'. The query returns an error:
```sql
SELECT first_name, last_name
FROM employees
WHERE last_name = "S%";
```
What is the error?
* A) In SQL, string literals and wildcards must be enclosed in single quotes `'S%'`, not double quotes `"S%"`.
* B) The wildcard symbol should be `*` instead of `%`.
* C) The table name `employees` must be in uppercase.
* D) The `SELECT` clause must contain all columns when using `LIKE`.

---

### Question 7
Which query correctly finds all products priced between $20.00 and $60.00, including both $20.00 and $60.00?
* A) `SELECT * FROM products WHERE retail_price IN (20.00, 60.00);`
* B) `SELECT * FROM products WHERE retail_price BETWEEN 20.00 AND 60.00;`
* C) `SELECT * FROM products WHERE retail_price = 20.00 TO 60.00;`
* D) `SELECT * FROM products WHERE retail_price > 20.00 AND retail_price < 60.00;`

---

### Question 8
Which wildcard character in SQL `LIKE` pattern matching represents **exactly one single character**?
* A) `%`
* B) `?`
* C) `_` (Underscore)
* D) `*`

---

### Question 9
What is the difference between `LIKE` and `ILIKE` in PostgreSQL?
* A) `LIKE` matches numbers; `ILIKE` matches strings.
* B) `LIKE` is case-sensitive; `ILIKE` is case-insensitive.
* C) `LIKE` only searches from the start of a string; `ILIKE` searches from the end.
* D) `ILIKE` is deprecated and should not be used in modern SQL.

---

### Question 10
Which query will retrieve the third "page" of an employee list when each page displays 10 records, ordered by salary descending?
* A) `SELECT * FROM employees ORDER BY salary DESC LIMIT 10 OFFSET 20;`
* B) `SELECT * FROM employees ORDER BY salary DESC LIMIT 20 OFFSET 10;`
* C) `SELECT * FROM employees ORDER BY salary DESC PAGE 3 SIZE 10;`
* D) `SELECT * FROM employees ORDER BY salary DESC LIMIT 30;`

---

## Part 3: Result Set & Output Prediction (Questions 11–15)

### Question 11
Consider an `employees` table with the following data:

| first_name | department | salary |
| :--- | :--- | :---: |
| Jon | Operations | 52000 |
| Karlach | Operations | 62000 |
| Jamie | Management | 110000 |
| Lestat | Sales | 75000 |

How many rows will the following query return?
```sql
SELECT first_name
FROM employees
WHERE department = 'Operations' AND salary > 60000;
```
* A) 0
* B) 1
* C) 2
* D) 4

---

### Question 12
Referring to the same table above, how many rows will this query return?
```sql
SELECT first_name
FROM employees
WHERE department = 'Operations' OR salary > 70000;
```
* A) 1
* B) 2
* C) 3
* D) 4

---

### Question 13
Consider the following list of product names:
1. `Heavy Duty Steel Bracket`
2. `Light Duty Bracket`
3. `Heavy Cable Tie`
4. `bracket screw set`

How many records will be returned by this query in PostgreSQL?
```sql
SELECT product_name
FROM products
WHERE product_name ILIKE '%bracket%';
```
* A) 1
* B) 2
* C) 3
* D) 4

---

### Question 14
Consider the following 4 records in an inventory table:

| product_name | discontinued_date |
| :--- | :--- |
| Widget A | 2023-01-15 |
| Widget B | NULL |
| Widget C | NULL |
| Widget D | 2024-06-01 |

How many rows will the following query return?
```sql
SELECT product_name
FROM products
WHERE discontinued_date IS NOT NULL;
```
* A) 0
* B) 2
* C) 4
* D) NULL

---

### Question 15
Look at the following query:
```sql
SELECT first_name, department, salary
FROM employees
WHERE department = 'Research' OR department = 'Security' AND salary > 80000;
```
If an employee named Waldo works in `Research` with a salary of `$45,000`, will Waldo appear in the result set?
* A) Yes, because Waldo satisfies the `department = 'Research'` condition, and `OR` requires only one branch to be true.
* B) No, because his salary is not greater than $80,000.
* C) No, because `AND` forces all conditions across the entire query to be true.
* D) It will result in a syntax error because parentheses were omitted.

---

# Answer Key & Pedagogical Rationales

| Q# | Correct Answer | Rationale / Explanation |
| :---: | :---: | :--- |
| **1** | **B** | **Projection** (`SELECT`) chooses vertical columns; **Selection** (`WHERE`) restricts horizontal rows. |
| **2** | **B** | In SQL's Three-Valued Logic, comparing an unknown value using `=` produces `UNKNOWN`. Rows only pass a `WHERE` filter when the test evaluates to `TRUE`. `IS NULL` must be used instead. |
| **3** | **B** | Under short-circuit boolean logic, `FALSE AND <anything>` is conclusively `FALSE`, because both operands must be true for `AND` to succeed. |
| **4** | **A** | Conjunction (`AND`) has higher algebraic operator precedence than disjunction (`OR`), mirroring mathematical multiplication over addition. |
| **5** | **B** | Logical execution order: `FROM` $\rightarrow$ `WHERE` $\rightarrow$ `SELECT`. The alias is assigned during the `SELECT` phase and is unknown during `WHERE`. |
| **6** | **A** | In SQL standard and PostgreSQL, double quotes `"..."` denote database object identifiers (tables/columns). String literals must use single quotes `'...'`. |
| **7** | **B** | `BETWEEN` provides inclusive range filtering ($A \le x \le B$). Option D is exclusive ($>$ and $<$). |
| **8** | **C** | The underscore `_` matches exactly one character. The percent sign `%` matches zero or more characters. |
| **9** | **B** | `ILIKE` is PostgreSQL's case-insensitive pattern matching operator. `LIKE` is strictly case-sensitive. |
| **10** | **A** | Page 1: `OFFSET 0` (rows 1–10). Page 2: `OFFSET 10` (rows 11–20). Page 3: `LIMIT 10 OFFSET 20` (rows 21–30). |
| **11** | **B** | Only Karlach satisfies both conditions (Operations and salary $62,000 > 60,000). Jon fails the salary check. |
| **12** | **C** | Jon and Karlach match `department = 'Operations'` (2 rows). Jamie ($110k) and Lestat ($75k) match `salary > 70000` (2 rows). Total unique matching rows = 3 (Karlach matches both, Jon matches dept, Jamie & Lestat match salary). |
| **13** | **D** | `ILIKE '%bracket%'` is case-insensitive and matches any text containing "bracket" anywhere in the string. All 4 items contain "Bracket" or "bracket". |
| **14** | **B** | `IS NOT NULL` filters for rows where a date is recorded (Widgets A and D). Widgets B and C are excluded. |
| **15** | **A** | Because `AND` binds first to `department = 'Security' AND salary > 80000`, the query treats `department = 'Research'` as a standalone `OR` branch. Waldo matches `Research`, so his row is included regardless of salary! |
