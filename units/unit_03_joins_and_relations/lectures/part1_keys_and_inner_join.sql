/*
====================================================================
CMAP 1815 - Unit 3: Lecture Walkthrough Part 1
Topic: Relational Keys & The First INNER JOIN
Video Duration: ~7 minutes
====================================================================
*/

-- 1. Inspecting the Foreign Key Bridge
-- Notice that employees has location_id (FK), and locations has location_id (PK)
SELECT employee_id, first_name, last_name, location_id 
FROM employees;

SELECT location_id, city, state 
FROM locations;

-- 2. The Basic INNER JOIN: Connecting Staff to Facilities
SELECT 
    e.first_name, 
    e.last_name, 
    e.department,
    l.city, 
    l.state,
    l.facility_type
FROM employees e
INNER JOIN locations l 
    ON e.location_id = l.location_id
ORDER BY l.state ASC, e.last_name ASC;

-- 3. [DEMO TRAP: The Ambiguous Column Error]
-- Uncomment the query below to show students the parser error:
-- SELECT location_id, first_name, city
-- FROM employees e
-- INNER JOIN locations l ON e.location_id = l.location_id;
-- ERROR: column reference "location_id" is ambiguous

-- The Fix: Disambiguate by declaring table alias:
SELECT 
    e.location_id, 
    e.first_name, 
    l.city
FROM employees e
INNER JOIN locations l 
    ON e.location_id = l.location_id;

-- 4. Filtering a Joined Result Set
-- Find employees assigned specifically to facilities in Colorado (CO)
SELECT 
    e.first_name, 
    e.last_name, 
    e.title,
    l.city, 
    l.state
FROM employees e
INNER JOIN locations l 
    ON e.location_id = l.location_id
WHERE l.state = 'CO'
ORDER BY e.last_name ASC;
