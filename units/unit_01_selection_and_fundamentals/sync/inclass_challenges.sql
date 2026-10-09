/*
====================================================================
CMAP 1815 - Unit 1: Lecture Walkthrough & Coding Clinic
Follow-Along Practice: Gradual Release ("Try First, Then Watch")
====================================================================

Pedagogical Purpose:
These coding clinic challenges follow the "Gradual Release of Responsibility"
model. Before watching the instructor video walkthrough, attempt each query
below in your Codespace sandbox. Then watch the recording to compare your
syntax, observe execution plans, and examine common beginner pitfalls!

Instructions:
1. Ensure your PostgreSQL connection is active in Codespaces.
2. Draft your query below each challenge block.
3. Test execution with Ctrl+Enter (or in psql).
4. SQL keywords should be UPPERCASE (SELECT, FROM, ORDER BY, AS).
====================================================================
*/

-- ==================================================================
-- CHALLENGE 1: The Clean Contact List
-- ==================================================================
-- Write a query against the 'employees' table that retrieves:
--   1. The employee's first name and last name merged together as 'full_name'
--   2. Their department
--   3. Their job title
-- Format the query so that it sorts alphabetically by department (A to Z),
-- and within each department, sorts by last name (A to Z).

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 2: Product Catalog & Profit Margin Preview
-- ==================================================================
-- Management wants to review the pricing of all products.
-- Write a query against the 'products' table that retrieves:
--   1. The product name
--   2. The category
--   3. The cost to produce
--   4. The retail price
--   5. A calculated column called 'unit_profit' (retail_price minus cost_to_produce)
-- Sort the result set so that the most profitable products appear at the top.

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 3: Geographic Footprint Audit
-- ==================================================================
-- Write a query against the 'locations' table to find all unique states
-- where our company operates facilities.
-- Ensure the output column is labeled 'operational_state' and is 
-- sorted in alphabetical order.

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 4: Salary Budget Simulation
-- ==================================================================
-- The leadership team is modeling an 8% cost-of-living adjustment (COLA).
-- Write a query against the 'employees' table that displays:
--   1. Last name
--   2. Current salary (aliased as 'current_base')
--   3. Simulated salary with an 8% increase (aliased as 'proposed_salary')
--   4. The exact dollar increase (aliased as 'dollar_adjustment')
-- Sort from the largest proposed salary to the lowest.

-- [YOUR QUERY HERE]




-- ==================================================================
-- CHALLENGE 5: Multi-Column DISTINCT Exploration
-- ==================================================================
-- Write a query to discover all distinct combinations of 'department' 
-- and 'title' currently active across the company.
-- Order the results by department, then by title.

-- [YOUR QUERY HERE]


