/*
====================================================================
CMAP 1815: Introduction to Modern SQL
Unit 1 Applied SQL Lab: Data Exploration & Orientation
Starter Template File (100 Points Total)
====================================================================
Student Name : [YOUR NAME HERE]
Submission   : lab1_yourlastname.sql
Due Date     : Friday at 11:59 PM (Midnight MT)

Grading Rubric Summary (100 Points):
- Query Accuracy & Execution (40 Pts)
- Formatting & SQL Standards: UPPERCASE keywords, multi-line (20 Pts)
- Precision Projection & Aliasing: AS snake_case (20 Pts)
- Sorting & DISTINCT Logic (10 Pts)
- Environment & System Catalogs (10 Pts)
====================================================================
*/

-- ==================================================================
-- PART 1: ENVIRONMENT & SYSTEM CATALOGS (20 Points)
-- ==================================================================

-- Challenge 1: Server Version
-- Write a query to display the exact version of PostgreSQL running on your server.
-- [YOUR QUERY HERE]




-- Challenge 2: Current Session Metadata
-- Write a query to display your current active database user and the connected database name.
-- [YOUR QUERY HERE]




-- Challenge 3: Public Table Discovery
-- Query information_schema.tables to list all user base table names in the 'public' schema,
-- sorted alphabetically by table name.
-- [YOUR QUERY HERE]




-- Challenge 4: Column Inspector for Employees
-- Query information_schema.columns to display column_name, data_type, and is_nullable
-- for the 'employees' table, sorted by ordinal_position ASC.
-- [YOUR QUERY HERE]




-- ==================================================================
-- PART 2: PRECISION PROJECTION & DATA EXPLORATION (40 Points)
-- ==================================================================

-- Challenge 5: Staff Directory
-- From the 'employees' table, retrieve first_name, last_name, and title.
-- Sort alphabetically by last_name ASC.
-- [YOUR QUERY HERE]




-- Challenge 6: Executive Compensation Roster
-- Retrieve first_name, last_name, and salary for all employees.
-- Sort from highest paid to lowest paid (DESC).
-- [YOUR QUERY HERE]




-- Challenge 7: Unique Departments
-- Write a query that returns a list of all distinct departments in the company,
-- sorted alphabetically from A to Z.
-- [YOUR QUERY HERE]




-- Challenge 8: Department-Title Roster
-- Find all unique combinations of department and title across the company.
-- Order by department ASC, then by title ASC.
-- [YOUR QUERY HERE]




-- ==================================================================
-- PART 3: EXPRESSIONS, ALIASES & MATHEMATICAL PROJECTIONS (40 Points)
-- ==================================================================

-- Challenge 9: Polished Full Name with String Concatenation
-- Query 'employees' combining first_name and last_name into a single column
-- aliased as 'full_name' using string concatenation (||), along with their department.
-- Sort by department ASC, then by full_name ASC.
-- [YOUR QUERY HERE]




-- Challenge 10: Bonus Simulation
-- Query 'employees' displaying:
--   - last_name
--   - salary AS base_salary
--   - bonus AS annual_bonus
--   - salary + bonus AS total_compensation
-- (Observe what happens for employees with no bonus!)
-- [YOUR QUERY HERE]




-- Challenge 11: Retail Product Margins
-- From the 'products' table, retrieve:
--   - product_name
--   - retail_price
--   - cost_to_produce
--   - calculated column (retail_price - cost_to_produce) aliased as estimated_unit_profit
-- Sort so the most profitable products appear first (DESC).
-- [YOUR QUERY HERE]




-- Challenge 12: Total Inventory Value Analysis
-- From the 'products' table, project:
--   - product_name
--   - stock_quantity
--   - retail_price
--   - calculated column (stock_quantity * retail_price) aliased as total_inventory_value
-- Sort from highest inventory value to lowest (DESC).
-- [YOUR QUERY HERE]


