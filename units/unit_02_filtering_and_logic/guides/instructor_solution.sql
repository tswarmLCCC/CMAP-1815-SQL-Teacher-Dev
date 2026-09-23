/*
====================================================================
CMAP 1815 - Unit 2: Instructor Solution Key
Lab: Targeted Retrieval & Logic Audits
====================================================================
*/

-- ==================================================================
-- Part 1: Numerical Boundaries & Inclusive Ranges
-- ==================================================================

-- 1. Premium Inventory
SELECT product_name, retail_price, stock_quantity
FROM products
WHERE retail_price >= 100.00
ORDER BY retail_price DESC;

-- 2. Mid-Tier Catalog
SELECT product_name, category, retail_price
FROM products
WHERE retail_price BETWEEN 30.00 AND 80.00
ORDER BY retail_price ASC;

-- 3. Critical Stock Alert
SELECT product_name, stock_quantity, category
FROM products
WHERE stock_quantity < 25
ORDER BY stock_quantity ASC;


-- ==================================================================
-- Part 2: Categorical Sets & Pattern Matching
-- ==================================================================

-- 4. Key Departments Roster
SELECT first_name, last_name, department, salary
FROM employees
WHERE department IN ('Research', 'Security', 'Engineering')
ORDER BY department ASC, salary DESC;

-- 5. Non-Technical Staff
SELECT 
    first_name || ' ' || last_name AS full_name,
    department
FROM employees
WHERE department NOT IN ('Security', 'Engineering', 'Research')
ORDER BY department ASC;

-- 6. SKU Prefix Audit
SELECT sku, product_name, retail_price
FROM products
WHERE sku LIKE 'ELEC%'
ORDER BY sku ASC;

-- 7. Description Keyword Search
SELECT product_name, description
FROM products
WHERE description ILIKE '%heavy%';


-- ==================================================================
-- Part 3: Boolean Gates & Parentheses Discipline
-- ==================================================================

-- 8. Senior High-Earners
SELECT first_name, last_name, salary, hire_date
FROM employees
WHERE salary >= 80000.00
  AND hire_date < '2018-01-01'
ORDER BY salary DESC;

-- 9. The Branch Security/Sales Filter
-- Teaching Note: Emphasize the required parentheses around the OR condition!
SELECT last_name, department, salary
FROM employees
WHERE (department = 'Security' OR department = 'Sales')
  AND salary >= 60000.00
ORDER BY department ASC, salary DESC;

-- 10. Active Operations Exception
SELECT first_name, last_name, department, salary
FROM employees
WHERE department = 'Operations'
  AND is_active = TRUE
  AND salary < 60000.00;


-- ==================================================================
-- Part 4: The Mystery of NULL & Web Pagination
-- ==================================================================

-- 11. The Missing Bonus Report
-- Teaching Note: Emphasize that bonus = NULL will return 0 rows. IS NULL is required!
SELECT first_name, last_name, department, salary, bonus
FROM employees
WHERE bonus IS NULL
ORDER BY salary DESC;

-- 12. Catalog Web Pagination (Page 2)
-- Page 2 skips the first 5 records (OFFSET 5) and displays the next 5 (LIMIT 5)
SELECT product_name, retail_price
FROM products
ORDER BY retail_price DESC
LIMIT 5 OFFSET 5;
