# Unit 2 Student Lab Guide: Targeted Retrieval & Logic Audits

## Lab Objective
In this lab, you will write targeted SQL queries using:
1. Numerical comparisons (`>`, `<`, `>=`, `<=`, `<>`, `BETWEEN`).
2. Categorical filtering with `IN` and `NOT IN`.
3. Pattern matching using wildcards (`LIKE`, `ILIKE`, `%`, `_`).
4. Multi-condition Boolean logic with defensive parentheses (`AND`, `OR`, `NOT`).
5. Missing data audits using `IS NULL` and `IS NOT NULL`.
6. Result set limiting and pagination with `ORDER BY ... LIMIT ... OFFSET`.

---

## Submission Instructions
1. In your personal GitHub Codespace, create a file named `lab2_yourname.sql`.
2. Ensure all SQL keywords are in **UPPERCASE**, clauses are on new lines, and strings are wrapped in single quotes `'...'`.
3. Test every query against your PostgreSQL database to verify error-free execution.
4. Commit and push your code to your repository.

---

## Lab Challenges

### Part 1: Numerical Boundaries & Inclusive Ranges (25 Points)
1. **Premium Inventory:** Write a query against `products` retrieving the `product_name`, `retail_price`, and `stock_quantity` for all items priced at or above `$100.00`. Sort from highest to lowest price.
2. **Mid-Tier Catalog:** Find all products whose `retail_price` is between `$30.00` and `$80.00` (inclusive). Display `product_name`, `category`, and `retail_price`. Sort by price ascending.
3. **Critical Stock Alert:** Management needs an urgent reorder list. Find all products where `stock_quantity` is strictly less than `25` units. Display `product_name`, `stock_quantity`, and `category`, sorted with the lowest inventory at the top.

---

### Part 2: Categorical Sets & Pattern Matching (25 Points)
4. **Key Departments Roster:** Retrieve the `first_name`, `last_name`, `department`, and `salary` for all employees who work in `Research`, `Security`, or `Engineering`. Sort by `department` alphabetically, then by `salary` descending.
5. **Non-Technical Staff:** Find all employees who do **NOT** work in `Security`, `Engineering`, or `Research`. Project their `full_name` (first and last concatenated) and their `department`.
6. **SKU Prefix Audit:** Find all products whose `sku` starts with the prefix `'ELEC'` using the `LIKE` operator. Display `sku`, `product_name`, and `retail_price`.
7. **Description Keyword Search:** Find all products where the `description` contains the word `'heavy'` (case-insensitive, matching 'Heavy', 'heavy', etc.) using `ILIKE`. Display `product_name` and `description`.

---

### Part 3: Boolean Gates & Parentheses Discipline (25 Points)
8. **Senior High-Earners:** Find all employees who earn a salary of `$80,000` or more **AND** were hired prior to January 1, 2018. Display `first_name`, `last_name`, `salary`, and `hire_date`.
9. **The Branch Security/Sales Filter:** Human Resources wants a list of staff in either `Security` **OR** `Sales` who also earn at least `$60,000`.  
   *(CRITICAL: You must use parentheses to ensure that the salary filter applies to BOTH departments!)* Display `last_name`, `department`, and `salary`.
10. **Active Operations Exception:** Find all employees who work in `Operations` **AND** whose `is_active` status is `TRUE`, but whose salary is strictly less than `$60,000`.

---

### Part 4: The Mystery of NULL & Web Pagination (25 Points)
11. **The Missing Bonus Report:** Retrieve all employees whose `bonus` is currently missing (`IS NULL`). Display `first_name`, `last_name`, `department`, `salary`, and `bonus`. Order by salary descending.
12. **Catalog Web Pagination (Page 2):** Simulate pagination on an e-commerce website. Retrieve **Page 2** of the product catalog where each page displays **5 products**, ordered by `retail_price` descending.  
    *(Hint: Use `LIMIT` and `OFFSET` to skip the first 5 records and return the next 5).*
