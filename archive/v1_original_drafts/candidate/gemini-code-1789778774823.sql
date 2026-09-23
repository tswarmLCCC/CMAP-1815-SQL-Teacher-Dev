/*
====================================================================
Module 7: Schema Design and Data Integrity
====================================================================
File: week_7_schema_ddl_lab.sql
Focus: DDL, CREATE TABLE, ALTER TABLE, constraints, and Views.
====================================================================
*/

/* --- INSTRUCTOR DEMONSTRATION --- */

-- Demo 1: DDL with Constraints
CREATE TABLE product_reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date DATE DEFAULT CURRENT_DATE
);

-- Demo 2: Creating a View to encapsulate complex logic
CREATE VIEW vw_active_employee_directory AS
SELECT e.first_name, e.last_name, e.title, e.department, l.city, l.state
FROM employees e
INNER JOIN locations l ON e.location_id = l.location_id
WHERE e.is_active = TRUE;

/* --- STUDENT ASSESSMENT --- */

-- 1. Write the DDL to create a new table named 'equipment_checkouts'.
-- It needs an ID (Primary Key), an employee_id (Foreign Key), a checkout_date, and a return_date.
CREATE TABLE equipment_checkouts (
    checkout_id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(employee_id),
    checkout_date DATE NOT NULL,
    return_date DATE,
    CHECK (return_date >= checkout_date)
);

-- 2. Use ALTER TABLE to add a new string column called 'emergency_contact' to the employees table.
ALTER TABLE employees 
ADD COLUMN emergency_contact VARCHAR(100);

-- 3. Create a View named 'vw_inventory_alerts' that selects product_name, sku, and stock_quantity 
-- but ONLY for products where the stock quantity is below 10.
CREATE VIEW vw_inventory_alerts AS
SELECT product_name, sku, stock_quantity
FROM products
WHERE stock_quantity < 10;