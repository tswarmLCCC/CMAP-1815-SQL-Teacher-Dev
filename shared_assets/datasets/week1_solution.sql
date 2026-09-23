/*
====================================================================
Module 1 & 2 Lab: Data Retrieval and Filtering Fundamentals
====================================================================

Objective: 
Write standard SELECT queries to retrieve, format, and filter data 
using conditions, aliases, mathematical operations, and pattern matching.

Instructions: 
Execute the queries below in DBeaver against the provided schema. 
Submit the final SQL syntax for each challenge.
*/

/*
--------------------------------------------------------------------
Part 1: Basic Retrieval & Formatting (Week 1)
--------------------------------------------------------------------
*/

-- 1. Retrieve all data from the products table.
SELECT * 
FROM products;

-- 2. List just the product names, categories, and retail prices for all items in the catalog.
SELECT product_name, category, retail_price 
FROM products;

-- 3. Generate an employee directory listing the first name, last name, and department.
SELECT first_name, last_name, department 
FROM employees;

-- 4. Combine the employee's first and last name into a single column named "Full Name", 
-- and list their title as "Position".
SELECT first_name || ' ' || last_name AS "Full Name", title AS "Position" 
FROM employees;

-- 5. Calculate the gross profit margin for each product. Display the product name, 
-- cost to produce, retail price, and a calculated column named Profit_Per_Unit.
SELECT product_name, cost_to_produce, retail_price, (retail_price - cost_to_produce) AS Profit_Per_Unit 
FROM products;

-- 6. Calculate the total potential inventory value for each product. Display the product name 
-- and multiply the retail price by the stock quantity. Alias the result as Total_Value.
SELECT product_name, (retail_price * stock_quantity) AS Total_Value 
FROM products;

-- 7. List all unique departments where employees currently work. Ensure there are no duplicate rows.
SELECT DISTINCT department 
FROM employees;

-- 8. Display the city and state from the locations table, formatted as a single column 
-- named "Location" (e.g., "Cheyenne, WY").
SELECT city || ', ' || state AS "Location" 
FROM locations;

-- 9. Display all employee names and their base salary. Calculate a projected 5% raise 
-- for everyone and alias it as Projected_Salary.
SELECT first_name, last_name, salary, (salary * 1.05) AS Projected_Salary 
FROM employees;

-- 10. Retrieve the order dates, shipping methods, and statuses from the orders table.
SELECT order_date, shipping_method, status 
FROM orders;


/*
--------------------------------------------------------------------
Part 2: Filtering and Sorting Data (Week 2)
--------------------------------------------------------------------
*/

-- 11. Find all products that cost strictly more than $100.
SELECT product_name, retail_price 
FROM products 
WHERE retail_price > 100.00;

-- 12. Locate all employees who work in either the 'Security' or 'Operations' departments.
SELECT first_name, last_name, department 
FROM employees 
WHERE department = 'Security' OR department = 'Operations';

-- 13. Find all products in the 'Home Automation' category that currently have a stock quantity greater than 0.
SELECT product_name, stock_quantity 
FROM products 
WHERE category = 'Home Automation' AND stock_quantity > 0;

-- 14. Identify all employees who have not been assigned a bonus. (Hint: Look for missing data).
SELECT first_name, last_name, bonus 
FROM employees 
WHERE bonus IS NULL;

-- 15. List all products that contain the word 'Bluetooth' anywhere in their description.
SELECT product_name, description 
FROM products 
WHERE description LIKE '%Bluetooth%';

-- 16. Find all software products (category 'Software') that have *not* been discontinued.
SELECT product_name, category, discontinued_date 
FROM products 
WHERE category = 'Software' AND discontinued_date IS NULL;

-- 17. Retrieve all employees hired between January 1, 2018, and December 31, 2021.
SELECT first_name, last_name, hire_date 
FROM employees 
WHERE hire_date BETWEEN '2018-01-01' AND '2021-12-31';

-- 18. Use the IN operator to list all products in the 'Audio', 'Gaming', or 'Electronics' categories.
SELECT product_name, category 
FROM products 
WHERE category IN ('Audio', 'Gaming', 'Electronics');

-- 19. Generate a list of all active employees, sorted by their salary from highest to lowest.
SELECT first_name, last_name, salary 
FROM employees 
WHERE is_active = TRUE 
ORDER BY salary DESC;

-- 20. Find the top 5 most expensive products currently in stock. 
-- Sort the results descending by price, and use a limit clause to restrict the output.
SELECT product_name, retail_price, stock_quantity 
FROM products 
WHERE stock_quantity > 0 
ORDER BY retail_price DESC 
LIMIT 5;