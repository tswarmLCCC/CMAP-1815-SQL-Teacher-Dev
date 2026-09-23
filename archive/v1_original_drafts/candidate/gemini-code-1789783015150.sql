/*
====================================================================
Module 7: Schema Design and Data Integrity
File: week_7_schema_ddl_lab.sql
Focus: DDL, CREATE TABLE, ALTER TABLE, constraints, and Views.
====================================================================
*/

/* 
--------------------------------------------------------------------
Part 1: Instructor Demonstration Queries
Use these during Periods 1 & 2 to explain schema modification.
--------------------------------------------------------------------
*/

-- Demo 1: DDL with Constraints
-- Goal: Create a new table to track product reviews, enforcing rules 
-- on the data right at the table level.
CREATE TABLE product_reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date DATE DEFAULT CURRENT_DATE
);

-- Demo 2: Creating a View
-- Goal: Encapsulate a complex join so business users can query a simple 
-- "virtual table" without needing to know how to write the join themselves.
CREATE VIEW vw_active_employee_directory AS
SELECT 
    e.first_name, 
    e.last_name, 
    e.title, 
    e.department, 
    l.city, 
    l.state
FROM employees e
INNER JOIN locations l ON e.location_id = l.location_id
WHERE e.is_active = TRUE;

-- Show how simple it is to query the new view.
SELECT * FROM vw_active_employee_directory WHERE department = 'Security';


/* 
--------------------------------------------------------------------
Part 2: Student Assessment (Schema Design Lab)
Periods 3 & 4 Independent Practice
--------------------------------------------------------------------
*/

-- 1. Write the DDL (CREATE TABLE) to build a new table named 'equipment_checkouts'.
-- It must include:
--   - A checkout_id that auto-increments as the Primary Key.
--   - An employee_id that acts as a Foreign Key to the employees table.
--   - A checkout_date that cannot be null.
--   - A return_date.
--   - A CHECK constraint ensuring the return_date is greater than or equal to the checkout_date.
CREATE TABLE equipment_checkouts (
    checkout_id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(employee_id),
    checkout_date DATE NOT NULL,
    return_date DATE,
    CHECK (return_date >= checkout_date)
);

-- 2. Modify an Existing Schema: The HR department needs to track emergency contacts.
-- Write an ALTER TABLE statement to add a new column called 'emergency_contact_phone' 
-- to the employees table. Make it a VARCHAR(20).
ALTER TABLE employees 
ADD COLUMN emergency_contact_phone VARCHAR(20);

-- 3. Create a Custom Database Object: Write the DDL to create a View named 'vw_inventory_alerts'.
-- The view should select the product_name, sku, and stock_quantity from the products table, 
-- but ONLY for products where the stock quantity is less than 15.
CREATE VIEW vw_inventory_alerts AS
SELECT 
    product_name, 
    sku, 
    stock_quantity
FROM products
WHERE stock_quantity < 15;

-- 4. Test your View: Write a simple SELECT statement against your new 'vw_inventory_alerts' view.
SELECT * FROM vw_inventory_alerts;