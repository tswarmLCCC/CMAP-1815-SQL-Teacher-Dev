Instructor Capstone Master Guide

This document is the master teaching file for evaluation, grading, and testing of the COSC 2409 Capstone project. It outlines the architectural design, grading metrics, and common traps to check when grading student submissions.

1. The Design Challenge: OrderID PK Violations

When working with the raw DataCoSupplyChainDataset.csv, students will run into a major database schema issue. If they try to build a basic 4-table schema (Locations, Customers, Products, Orders) where Orders has OrderID as its primary key and directly contains ProductID, their code will fail:

ERROR: duplicate key value violates unique constraint "orders_pkey"


Why this happens:

Orders can contain multiple line items (different products inside the same purchase transaction). If an order has multiple products, order_id will repeat across different rows inside raw_staging.

The Solution:

Students must normalize their schema to 3rd Normal Form (3NF) by splitting orders into two separate tables:

Orders: An order-level table storing unique OrderID entries along with general metrics (dates, payment types, and shipping routes).

OrderItems: An item-level details table storing individual line items, linking the order table with Products.

2. In-Depth Grading Rubric (100-Point Scale)

A. DDL & Schema Architecture (30 Points)

3NF Normalization (15 Points): Did the student successfully split the flat file into normalized parent-child relations without duplicate customer profiles or primary key conflicts?

Integrity Constraints (10 Points): Are foreign keys correctly configured with appropriate reference logic? Are primary keys, unique checks, and default values (like NOT NULL) correctly implemented?

Optimal Data Types (5 Points): Did they use correct spatial and financial representations (e.g., DECIMAL(10,2) rather than float/real datatypes for money)?

B. DML Data Migrations (20 Points)

Topological Ingestion Order (10 Points): Does the script run cleanly from top to bottom? For example, the script must insert records into Locations before Customers, and Products before OrderItems.

Handling Nulls and Duplicates (10 Points): Did they use structural filters (SELECT DISTINCT, handling null values, using COALESCE on nullable state entries) to prevent constraint violations?

C. Performance Optimization (15 Points)

Index Selection (10 Points): Did they create B-Tree indexes on foreign keys (CustomerID, ProductID) and high-traffic query filters (OrderDate)?

Avoid Excess Indexing (5 Points): Did they avoid over-indexing (e.g., adding indexes to low-cardinality flags like LateDeliveryRisk or ShippingMode), which slows down insert operations?

D. Advanced Analytics View (20 Points)

Window Functions (10 Points): Is the running total calculation (SUM() OVER) partitioned and ordered correctly? Is the rank calculation logical?

Business Transformation Rules (10 Points): Does the CASE statement accurately convert the numerical outputs into useful category metrics for the executive team?

E. AI Grounding & Documentation (15 Points)

Data Dictionary Detail (10 Points): Did the student document all columns, datatypes, constraints, and business logic?

AI Confidence Checking (5 Points): Did the student include a filter to ignore predictions with confidence scores below 80%?

3. Quick-Reference Grading Script

Run these tests inside PostgreSQL to quickly verify the structural correctness of a student's submission:

-- 1. Check Row Count matches expectations (180,519 raw rows)
-- If normalization is correct, the unique counts should match exactly:
SELECT count(*) FROM Locations;  -- Expected: ~3,573 rows
SELECT count(*) FROM Customers;  -- Expected: ~20,652 rows
SELECT count(*) FROM Products;   -- Expected: ~120 rows
SELECT count(*) FROM Orders;     -- Expected: ~65,752 unique orders
SELECT count(*) FROM OrderItems; -- Expected: ~180,519 line items

-- 2. Verify relational integrity structure
SELECT c.FirstName, c.LastName, l.City, l.Country 
FROM Customers c 
JOIN Locations l ON c.LocationID = l.LocationID 
LIMIT 5;

-- 3. Run a test join across the analytical view
SELECT * FROM v_supply_chain_intelligence LIMIT 5;


4. Student Interview Questions (Understanding Checks)

Use these targeted questions during project defenses to evaluate if a student understands their database design:

"Why did you need to create both an Orders and an OrderItems table?"

Correct Answer: "In the staging data, OrderID is repeated whenever a customer ordered multiple products. If we made OrderID our primary key on a table containing ProductID, we would get primary key violations. We had to split them into parent and child tables to preserve 3NF and prevent duplicate order information."

"Why should we avoid using DOUBLE PRECISION or FLOAT data types for transactional values like OrderTotal?"

Correct Answer: "Floating-point numbers use binary approximations, which can introduce rounding errors during math operations. We use DECIMAL(10,2) or NUMERIC because they store exact base-10 values, ensuring precision for currency calculation."

"How does a window function like SUM(OrderTotal) OVER (PARTITION BY CustomerID ORDER BY OrderDate) differ from a standard GROUP BY query?"

Correct Answer: "GROUP BY aggregates our rows and reduces the overall output count. A window function performs calculations across a set of table rows while keeping all individual rows intact."