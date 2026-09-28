/*
================================================================================
CMAP 1815: SQL & Relational Databases
COMPREHENSIVE LAB SOLUTIONS & EXECUTION WALKTHROUGH
Annotated Guide with Expected Results, Row Counts, & Output Previews
================================================================================

HOW TO USE THIS FILE FOR SELF-TESTING:
1. Ensure the lab schema is loaded. If testing on a fresh database:
   psql -U postgres -d cmap1815 -f sql/setup_chap1.sql
   (Or in DBeaver/VS Code SQLTools: run the setup_chap1.sql script once).
2. Execute each query individually (Ctrl+Enter in DBeaver or SQLTools).
3. Compare the returned table, column headers, row counts, and data types
   against the "EXPECTED OUTPUT" block annotated above each query.

TABLE OF CONTENTS:
- SECTION 1: UNIT 1 LAB — SYSTEM CATALOGS & EXPLORATION (Challenges 1 - 4)
- SECTION 2: UNIT 1 LAB — PRECISION PROJECTION & SORTING (Challenges 5 - 8)
- SECTION 3: UNIT 1 LAB — EXPRESSIONS, ALIASES & MATH (Challenges 9 - 12)
- SECTION 4: UNIT 2 LAB PREVIEW — FILTERING, NULLS & PAGINATION (Challenges 13 - 22)
================================================================================
*/


/*
================================================================================
SECTION 1: ENVIRONMENT & SYSTEM CATALOGS
Focus: Discovering metadata programmatically via ANSI information_schema & engine functions
================================================================================
*/

-- -----------------------------------------------------------------------------
-- Challenge 1: Server Version
-- Concept: Querying internal PostgreSQL engine release and build metadata.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : version (text)
  Row Count : 1 row
  Sample Preview:
  +----------------------------------------------------------------------------+
  | version                                                                    |
  +----------------------------------------------------------------------------+
  | PostgreSQL 16.x (Ubuntu 16.x-...) on x86_64-pc-linux-gnu, compiled by ...  |
  +----------------------------------------------------------------------------+
  Note: Verifies that the container is running PostgreSQL 16+.
*/
SELECT version();


-- -----------------------------------------------------------------------------
-- Challenge 2: Current Session Metadata
-- Concept: Inspecting active session authentication and connected database.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : current_user (name), current_database (name)
  Row Count : 1 row
  Sample Preview:
  +--------------+------------------+
  | current_user | current_database |
  +--------------+------------------+
  | postgres     | cmap1815         |
  +--------------+------------------+
  Note: Depending on whether you connected via docker-compose (cmap1815) or setup.sh
        (classroom/mydb), current_database will reflect your active database name.
*/
SELECT current_user, current_database();


-- -----------------------------------------------------------------------------
-- Challenge 3: Public Table Discovery
-- Concept: Inspecting ANSI information_schema.tables to list user tables.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : table_name (sql_identifier)
  Row Count : 5 rows
  Sort Order: Alphabetical ASC
  Complete Results:
  +-------------+
  | table_name  |
  +-------------+
  | employees   |
  | locations   |
  | order_lines |
  | orders      |
  | products    |
  +-------------+
  Note: Filters out system tables/views by requiring table_type = 'BASE TABLE'
        and table_schema = 'public'.
*/
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name ASC;


-- -----------------------------------------------------------------------------
-- Challenge 4: Column Inspector for the Employees Table
-- Concept: Inspecting schema structure, data types, and nullability constraints.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : column_name, data_type, is_nullable
  Row Count : 10 rows
  Sort Order: Ordinal position (table definition order)
  Complete Results:
  +-------------+-------------------+-------------+
  | column_name | data_type         | is_nullable |
  +-------------+-------------------+-------------+
  | employee_id | integer           | NO          |
  | first_name  | character varying | NO          |
  | last_name   | character varying | NO          |
  | department  | character varying | YES         |
  | title       | character varying | YES         |
  | hire_date   | date              | YES         |
  | salary      | numeric           | YES         |
  | bonus       | numeric           | YES         |
  | location_id | integer           | YES         |
  | is_active   | boolean           | YES         |
  +-------------+-------------------+-------------+
*/
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'employees'
ORDER BY ordinal_position ASC;



/*
================================================================================
SECTION 2: PRECISION PROJECTION & DATA EXPLORATION
Focus: Named column projections, de-duplication with DISTINCT, and multi-tier sorting
================================================================================
*/

-- -----------------------------------------------------------------------------
-- Challenge 5: Staff Directory
-- Concept: Strict column projection (avoiding SELECT *) and sorting by last name.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : first_name, last_name, title
  Row Count : 28 rows
  Sort Order: last_name ASC (A -> Z)
  Sample Preview (First 5 and Last 2 rows):
  +------------+------------+-------------------------+
  | first_name | last_name  | title                   |
  +------------+------------+-------------------------+
  | Astarion   | Ancunin    | Acquisitions            |
  | Claire     | Beauchamp  | Medical Lead            |
  | John       | Bradford   | Operations Officer      |
  | Waldo      | Butters    | Medical Examiner        |
  | Casper     | Cat        | Pest Control Lead       |
  | ...        | ...        | ...                     |
  | Yennefer   | Vengerberg | Consultant              |
  | Shadowheart| Viconia    | Customer Success        |
  +------------+------------+-------------------------+
*/
SELECT first_name, last_name, title
FROM employees
ORDER BY last_name ASC;


-- -----------------------------------------------------------------------------
-- Challenge 6: Executive Compensation Roster
-- Concept: Numerical sorting in descending order (highest earners at the top).
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : first_name, last_name, salary
  Row Count : 28 rows
  Sort Order: salary DESC ($150,000.00 down to $20,000.00)
  Sample Preview (Top 5 and Bottom 2 rows):
  +------------+------------+-----------+
  | first_name | last_name  | salary    |
  +------------+------------+-----------+
  | Nathan     | MacKinnon  | 150000.00 |
  | Cale       | Makar      | 145000.00 |
  | Yennefer   | Vengerberg | 140000.00 |
  | Gale       | Dekarios   | 135000.00 |
  | Raymond    | Shen       | 130000.00 |
  | ...        | ...        | ...       |
  | Cheddar    | Cat        |  22000.00 |
  | Bonitto    | Pyrenees   |  20000.00 |
  +------------+------------+-----------+
*/
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC;


-- -----------------------------------------------------------------------------
-- Challenge 7: Unique Departments
-- Concept: De-duplicating recurring categorical data using DISTINCT.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : department
  Row Count : 8 rows
  Sort Order: department ASC
  Complete Results:
  +-------------+
  | department  |
  +-------------+
  | Engineering |
  | Management  |
  | Medical     |
  | Operations  |
  | Research    |
  | Sales       |
  | Security    |
  | Support     |
  +-------------+
  Teaching Note: Emphasize that DISTINCT collapses the 28 raw employee rows
  down to the 8 unique operating departments.
*/
SELECT DISTINCT department
FROM employees
ORDER BY department ASC;


-- -----------------------------------------------------------------------------
-- Challenge 8: Department-Title Roster
-- Concept: Multi-column DISTINCT with two-tier hierarchical sorting.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : department, title
  Row Count : 28 rows (each role within a department is currently distinct)
  Sort Order: department ASC, then title ASC
  Sample Preview:
  +-------------+---------------------------+
  | department  | title                     |
  +-------------+---------------------------+
  | Engineering | Chief Engineer            |
  | Engineering | Defense Architect         |
  | Engineering | Lead Mechanic             |
  | Management  | Operations Officer        |
  | Management  | Regional Manager          |
  | Medical     | First Assist Practitioner |
  | Operations  | Heavy Equipment Operator  |
  | Operations  | Night Watch Supervisor    |
  | Operations  | Pest Control Associate    |
  | Operations  | Pest Control Lead         |
  | Research    | AI Architect              |
  | Research    | Consultant                |
  | ...         | ...                       |
  | Security    | Trainee                   |
  | Support     | Customer Success          |
  +-------------+---------------------------+
*/
SELECT DISTINCT department, title
FROM employees
ORDER BY department ASC, title ASC;



/*
================================================================================
SECTION 3: EXPRESSIONS, ALIASES & MATHEMATICAL PROJECTIONS
Focus: String concatenation (||), column aliasing (AS), arithmetic expressions,
       and NULL propagation mechanics.
================================================================================
*/

-- -----------------------------------------------------------------------------
-- Challenge 9: Polished Full Name with String Concatenation
-- Concept: Combining text columns with literal spaces using || and snake_case alias.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : full_name (text), department (varchar)
  Row Count : 28 rows
  Sort Order: department ASC, full_name ASC
  Sample Preview:
  +---------------------+-------------+
  | full_name           | department  |
  +---------------------+-------------+
  | Cale Makar          | Engineering |
  | Lily Shen           | Engineering |
  | Raymond Shen        | Engineering |
  | Jamie Fraser        | Management  |
  | John Bradford       | Management  |
  | Shala Swarm         | Medical     |
  | Casper Cat          | Operations  |
  | Cheddar Cat         | Operations  |
  | Jon Snow            | Operations  |
  | Karlach Cliffgate   | Operations  |
  | ...                 | ...         |
  | Shadowheart Viconia | Support     |
  +---------------------+-------------+
*/
SELECT 
    first_name || ' ' || last_name AS full_name,
    department
FROM employees
ORDER BY department ASC, full_name ASC;


-- -----------------------------------------------------------------------------
-- Challenge 10: Bonus Simulation & The Behavior of NULL
-- Concept: Arithmetic expressions and observation of NULL propagation.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : last_name, base_salary, annual_bonus, total_compensation
  Row Count : 28 rows
  Key Teaching Observation:
  Look closely at rows with NULL bonuses (e.g., Murphy, Beauchamp, Dekarios, Bradford).
  Their total_compensation evaluates to NULL, NOT base_salary!
  Why? In SQL, NULL represents "unknown". (Any Number + NULL = NULL).
  In Unit 2, students learn to defend against this using COALESCE(bonus, 0).

  Sample Preview:
  +------------+-------------+--------------+--------------------+
  | last_name  | base_salary | annual_bonus | total_compensation |
  +------------+-------------+--------------+--------------------+
  | Dresden    |    65000.00 |      1500.00 |           66500.00 |
  | Murphy     |    95000.00 |         NULL |               NULL | <-- Notice NULL!
  | Butters    |    82000.00 |      2000.00 |           84000.00 |
  | Snow       |    52000.00 |       500.00 |           52500.00 |
  | Stark      |    68000.00 |      3000.00 |           71000.00 |
  | Beauchamp  |   115000.00 |         NULL |               NULL | <-- Notice NULL!
  | ...        |         ... |          ... |                ... |
  | MacKinnon  |   150000.00 |     25000.00 |          175000.00 |
  | Makar      |   145000.00 |     20000.00 |          165000.00 |
  +------------+-------------+--------------+--------------------+
*/
SELECT 
    last_name,
    salary AS base_salary,
    bonus AS annual_bonus,
    salary + bonus AS total_compensation
FROM employees;


-- -----------------------------------------------------------------------------
-- Challenge 11: Retail Product Margins
-- Concept: Subtraction in SELECT expressions, aliasing, and sorting on expressions.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : product_name, retail_price, cost_to_produce, estimated_unit_profit
  Row Count : 30 rows
  Sort Order: estimated_unit_profit DESC
  Sample Preview (Top 5 and Bottom 2 rows):
  +--------------------------------------+--------------+-----------------+-----------------------+
  | product_name                         | retail_price | cost_to_produce | estimated_unit_profit |
  +--------------------------------------+--------------+-----------------+-----------------------+
  | DaVinci Resolve Studio License Key   |       295.00 |            0.00 |                295.00 |
  | Onkyo TX-NR6050 7.2 Channel Receiver |       499.00 |          250.00 |                249.00 |
  | Dreame L10 Pro Robot Vacuum          |       389.99 |          200.00 |                189.99 |
  | Klipsch Reference 10" Subwoofer      |       349.00 |          160.00 |                189.00 |
  | Saris Fluid2 Indoor Bike Trainer     |       299.99 |          150.00 |                149.99 |
  | ...                                  |          ... |             ... |                   ... |
  | Prime Rib Rub 16oz                   |        12.99 |            4.00 |                  8.99 |
  | Lalvin EC-1118 Yeast 10-pack         |         9.50 |            3.00 |                  6.50 |
  +--------------------------------------+--------------+-----------------+-----------------------+
*/
SELECT 
    product_name,
    retail_price,
    cost_to_produce,
    retail_price - cost_to_produce AS estimated_unit_profit
FROM products
ORDER BY estimated_unit_profit DESC;


-- -----------------------------------------------------------------------------
-- Challenge 12: Total Inventory Value Analysis
-- Concept: Multiplication across quantity and price columns, aliasing, and descending sort.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : product_name, stock_quantity, retail_price, total_inventory_value
  Row Count : 30 rows
  Sort Order: total_inventory_value DESC
  Sample Preview (Top 5 and Bottom 3 rows):
  +--------------------------------------+----------------+--------------+-----------------------+
  | product_name                         | stock_quantity | retail_price | total_inventory_value |
  +--------------------------------------+----------------+--------------+-----------------------+
  | Baldur's Gate 3 PC Key               |            999 |        59.99 |              59930.01 |
  | No Man's Sky PC Key                  |            999 |        59.99 |              59930.01 |
  | Satisfactory 1.0 Release Key         |            999 |        39.99 |              39950.01 |
  | DaVinci Resolve Studio License Key   |             99 |       295.00 |              29205.00 |
  | Hades PC Key                         |            999 |        24.99 |              24965.01 |
  | ...                                  |            ... |          ... |                   ... |
  | Satisfactory Early Access Key        |              0 |        29.99 |                  0.00 |
  | Digital Meat Thermometer Bluetooth   |              0 |        39.99 |                  0.00 |
  | Raspberry Pi 5 8GB                   |              0 |        80.00 |                  0.00 |
  +--------------------------------------+----------------+--------------+-----------------------+
  Note: Digital licenses with 999 keys dominate the valuation, while out-of-stock items (qty = 0)
        correctly drop to the bottom with $0.00 value.
*/
SELECT 
    product_name,
    stock_quantity,
    retail_price,
    stock_quantity * retail_price AS total_inventory_value
FROM products
ORDER BY total_inventory_value DESC;



/*
================================================================================
SECTION 4: EXTENDED PRACTICE & UNIT 2 FILTERING PREVIEW
Focus: Targeted filtering with WHERE, compound boolean logic (AND/OR), pattern
       matching (LIKE/ILIKE), NULL testing, and pagination (LIMIT/OFFSET).
================================================================================
*/

-- -----------------------------------------------------------------------------
-- Challenge 13: High-Value Products Filter
-- Concept: Simple numerical comparison strictly greater than ($100.00).
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : product_name, retail_price
  Row Count : 7 rows
  Results Preview:
  - Saris Fluid2 Indoor Bike Trainer ($299.99)
  - Steam Deck OLED 512GB ($549.00)
  - Dreame L10 Pro Robot Vacuum ($389.99)
  - Klipsch Reference 10" Subwoofer ($349.00)
  - Onkyo TX-NR6050 7.2 Channel Receiver ($499.00)
  - DaVinci Resolve Studio License Key ($295.00)
  - Vintage Oak End Table ($125.00)
*/
SELECT product_name, retail_price 
FROM products 
WHERE retail_price > 100.00;


-- -----------------------------------------------------------------------------
-- Challenge 14: Department Compound Filter (OR)
-- Concept: Categorical OR filtering across multiple department matches.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : first_name, last_name, department
  Row Count : 11 rows (7 Security + 4 Operations)
*/
SELECT first_name, last_name, department 
FROM employees 
WHERE department = 'Security' OR department = 'Operations';


-- -----------------------------------------------------------------------------
-- Challenge 15: In-Stock Home Automation Filter (AND)
-- Concept: Narrowing result sets using dual-condition conjunction.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : product_name, stock_quantity
  Row Count : 3 rows
  Results:
  +------------------------------------------+----------------+
  | product_name                             | stock_quantity |
  +------------------------------------------+----------------+
  | Zooz 800 Series Z-Wave Plus Smart Switch |             60 |
  | TP-Link Tapo 2K Pan/Tilt Security Camera |            115 |
  | Dreame L10 Pro Robot Vacuum              |             12 |
  +------------------------------------------+----------------+
*/
SELECT product_name, stock_quantity 
FROM products 
WHERE category = 'Home Automation' AND stock_quantity > 0;


-- -----------------------------------------------------------------------------
-- Challenge 16: Audit of Missing Bonuses (IS NULL)
-- Concept: Identifying unknown/unassigned values using the IS NULL operator.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : first_name, last_name, bonus
  Row Count : 9 rows
  Results: Murphy, Beauchamp, Dekarios, Bradford, Raymond Shen, Geralt Riv,
           Shala Swarm, Casper Cat, Cheddar Cat (all have bonus = NULL).
  Common Mistake: WHERE bonus = NULL will return 0 rows! SQL requires IS NULL.
*/
SELECT first_name, last_name, bonus 
FROM employees 
WHERE bonus IS NULL;


-- -----------------------------------------------------------------------------
-- Challenge 17: Pattern Matching on Product Descriptions
-- Concept: Wildcard matching with LIKE '%pattern%'.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : product_name, description
  Row Count : 1 row
  Result:
  - Magene Bluetooth Speed & Cadence Sensor
*/
SELECT product_name, description 
FROM products 
WHERE description LIKE '%Bluetooth%';


-- -----------------------------------------------------------------------------
-- Challenge 18: Active Catalog Software Audit (IS NULL Negation)
-- Concept: Filtering on categorical match and testing for absence of retirement date.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : product_name, category, discontinued_date
  Row Count : 5 rows
  Results: Baldur's Gate 3, Satisfactory 1.0, No Man's Sky, Hades, DaVinci Resolve.
  (Excludes Satisfactory Early Access Key which was discontinued in 2024).
*/
SELECT product_name, category, discontinued_date 
FROM products 
WHERE category = 'Software' AND discontinued_date IS NULL;


-- -----------------------------------------------------------------------------
-- Challenge 19: Date Range Boundaries (BETWEEN)
-- Concept: Inclusive date filtering across multiple calendar years.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : first_name, last_name, hire_date
  Row Count : 8 rows
  Results: Jon Snow, Arya Stark, Gale Dekarios, Zagreus, Shala Swarm,
           Lando Pyrenees, Bonitto Pyrenees, Cheddar Cat.
*/
SELECT first_name, last_name, hire_date 
FROM employees 
WHERE hire_date BETWEEN '2018-01-01' AND '2021-12-31';


-- -----------------------------------------------------------------------------
-- Challenge 20: Categorical Membership (IN operator)
-- Concept: Cleaner, idiomatic alternative to chained OR conditions.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : product_name, category
  Row Count : 6 rows
  Results: 8BitDo Controller (Gaming), Steam Deck (Gaming), Raspberry Pi (Electronics),
           Coral TPU (Electronics), Klipsch Subwoofer (Audio), Onkyo Receiver (Audio).
*/
SELECT product_name, category 
FROM products 
WHERE category IN ('Audio', 'Gaming', 'Electronics');


-- -----------------------------------------------------------------------------
-- Challenge 21: Active Employees Ranked by Salary
-- Concept: Combining boolean flag filtering with descending ordering.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : first_name, last_name, salary
  Row Count : 26 rows (excludes 2 inactive employees: Moira Vahlen and Raymond Shen)
  Top Earner: Nathan MacKinnon ($150,000.00)
  Lowest    : Bonitto Pyrenees ($20,000.00)
*/
SELECT first_name, last_name, salary 
FROM employees 
WHERE is_active = TRUE 
ORDER BY salary DESC;


-- -----------------------------------------------------------------------------
-- Challenge 22: Top 5 In-Stock Products (ORDER BY ... LIMIT)
-- Concept: Restricting result set cardinality for leaderboards and e-commerce feeds.
-- -----------------------------------------------------------------------------
/*
EXPECTED OUTPUT:
  Columns   : product_name, retail_price, stock_quantity
  Row Count : Exactly 5 rows
  Sort Order: retail_price DESC
  Complete Results:
  +--------------------------------------+--------------+----------------+
  | product_name                         | retail_price | stock_quantity |
  +--------------------------------------+--------------+----------------+
  | Steam Deck OLED 512GB                |       549.00 |              8 |
  | Onkyo TX-NR6050 7.2 Channel Receiver |       499.00 |              4 |
  | Dreame L10 Pro Robot Vacuum          |       389.99 |             12 |
  | Klipsch Reference 10" Subwoofer      |       349.00 |              8 |
  | Saris Fluid2 Indoor Bike Trainer     |       299.99 |             15 |
  +--------------------------------------+--------------+----------------+
*/
SELECT product_name, retail_price, stock_quantity 
FROM products 
WHERE stock_quantity > 0 
ORDER BY retail_price DESC 
LIMIT 5;

-- End of Lab Solutions Walkthrough
