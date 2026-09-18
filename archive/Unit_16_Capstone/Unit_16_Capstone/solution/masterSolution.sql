-- ====================================================================
-- COSC 2409: Week 16 Capstone Instructor Solution Script
-- Target Database: PostgreSQL (mydb)
-- ====================================================================

-- Clean workspace and tear down existing objects in topological dependency order
DROP VIEW IF EXISTS v_supply_chain_intelligence CASCADE;
DROP TABLE IF EXISTS OrderItems CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Customers CASCADE;
DROP TABLE IF EXISTS Locations CASCADE;

-- ====================================================================
-- STEP 1: ARCHITECTURE & DDL (3NF Schema)
-- ====================================================================

-- Parent geography dimension
CREATE TABLE Locations (
    LocationID SERIAL PRIMARY KEY,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100),
    Country VARCHAR(100) NOT NULL,
    UNIQUE (City, State, Country)
);

-- Customer profile dimension linked to locations
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY, -- Utilizing the structured ID provided by DataCo
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100), -- Made nullable to accommodate missing last names in raw DataCo dataset
    LocationID INT REFERENCES Locations(LocationID)
);

-- Catalog of unique items offered
CREATE TABLE Products (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    CategoryName VARCHAR(100),
    UNIQUE (ProductName, CategoryName)
);

-- Core Order transactions containing order-level data
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT REFERENCES Customers(CustomerID),
    OrderDate DATE NOT NULL,
    ShippingMode VARCHAR(100) NOT NULL,
    PaymentType VARCHAR(50),
    ScheduledDays INT,
    ActualDays INT,
    LateDeliveryRisk INT CHECK (LateDeliveryRisk IN (0, 1))
);

-- Order details containing individual item-level listings (Resolves OrderID key collision)
CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY,
    OrderID INT REFERENCES Orders(OrderID) ON DELETE CASCADE,
    ProductID INT REFERENCES Products(ProductID),
    OrderItemTotal DECIMAL(10,2) NOT NULL,
    Quantity INT NOT NULL
);

-- ====================================================================
-- STEP 2: DATA MIGRATION (DML)
-- ====================================================================

-- 1. Populate Locations
INSERT INTO Locations (City, State, Country)
SELECT DISTINCT customer_city, customer_state, customer_country
FROM raw_staging
WHERE customer_city IS NOT NULL 
  AND customer_country IS NOT NULL;

-- 2. Populate Customers
INSERT INTO Customers (CustomerID, FirstName, LastName, LocationID)
SELECT DISTINCT r.customer_id, r.customer_fname, r.customer_lname, l.LocationID
FROM raw_staging r
JOIN Locations l ON r.customer_city = l.City 
                 AND COALESCE(r.customer_state, '') = COALESCE(l.State, '') 
                 AND r.customer_country = l.Country
WHERE r.customer_id IS NOT NULL;

-- 3. Populate Products
INSERT INTO Products (ProductName, CategoryName)
SELECT DISTINCT product_name, category_name
FROM raw_staging
WHERE product_name IS NOT NULL;

-- 4. Populate Orders (Using DISTINCT ON to safely isolate singular OrderID instances)
INSERT INTO Orders (OrderID, CustomerID, OrderDate, ShippingMode, PaymentType, ScheduledDays, ActualDays, LateDeliveryRisk)
SELECT DISTINCT ON (r.order_id)
    r.order_id, 
    r.customer_id, 
    CAST(r.order_date_dateorders AS DATE), 
    r.shipping_mode, 
    r.type, 
    r.days_for_shipment_scheduled, 
    r.days_for_shipping_real, 
    r.late_delivery_risk
FROM raw_staging r
WHERE r.order_id IS NOT NULL
ORDER BY r.order_id;

-- 5. Populate OrderItems (Individual line items linking orders and products)
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, OrderItemTotal, Quantity)
SELECT DISTINCT 
    r.order_item_id, 
    r.order_id, 
    p.ProductID, 
    r.order_item_total, 
    r.order_item_quantity
FROM raw_staging r
JOIN Products p ON r.product_name = p.ProductName 
                AND COALESCE(r.category_name, '') = COALESCE(p.CategoryName, '')
WHERE r.order_item_id IS NOT NULL;

-- ====================================================================
-- STEP 3: OPTIMIZATION (B-Tree Indexes)
-- ====================================================================
CREATE INDEX idx_orders_customer ON Orders(CustomerID);
CREATE INDEX idx_orders_date ON Orders(OrderDate);
CREATE INDEX idx_order_items_order ON OrderItems(OrderID);
CREATE INDEX idx_order_items_product ON OrderItems(ProductID);

-- ====================================================================
-- STEP 4: ADVANCED ANALYTICS (CTEs, CASE, Window Functions)
-- ====================================================================
CREATE OR REPLACE VIEW v_supply_chain_intelligence AS 
WITH CustomerMetrics AS (
    SELECT 
        o.OrderID,
        c.CustomerID,
        l.Country AS DestinationCountry,
        p.CategoryName,
        oi.OrderItemTotal AS OrderTotal,
        o.ShippingMode,
        o.LateDeliveryRisk,
        o.ActualDays,
        o.ScheduledDays,
        -- Running spending total partitioned by customer over sequence of time
        SUM(oi.OrderItemTotal) OVER(PARTITION BY o.CustomerID ORDER BY o.OrderDate, o.OrderID) AS RunningCustomerSpend,
        -- Rank high delay risk order profiles for targeted customer resolution
        RANK() OVER(PARTITION BY o.CustomerID ORDER BY (o.ActualDays - o.ScheduledDays) DESC) as DelaySeverityRank
    FROM Orders o
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    JOIN Customers c ON o.CustomerID = c.CustomerID
    JOIN Locations l ON c.LocationID = l.LocationID
    JOIN Products p ON oi.ProductID = p.ProductID
)
SELECT 
    OrderID,
    CustomerID,
    DestinationCountry,
    CategoryName,
    OrderTotal,
    ShippingMode,
    LateDeliveryRisk,
    RunningCustomerSpend,
    -- Label categorical state based on analytic ranking boundaries
    CASE 
        WHEN LateDeliveryRisk = 1 THEN 'High Risk'
        WHEN DelaySeverityRank <= 3 AND ActualDays > ScheduledDays THEN 'Chronic Delay Issue'
        ELSE 'On Track'
    END AS Fulfillment_Status
FROM CustomerMetrics;

-- ====================================================================
-- STEP 5: AI INTEGRATION (MindsDB Concept Script)
-- ====================================================================

-- 1. Register Predictor utilizing normalized features
-- CREATE PREDICTOR delivery_delay_predictor
-- FROM DataCoDB (
--     SELECT DestinationCountry, CategoryName, OrderTotal, ShippingMode, LateDeliveryRisk 
--     FROM v_supply_chain_intelligence
-- )
-- PREDICT LateDeliveryRisk;

-- 2. Query against analytical view using MindsDB model interfaces
-- SELECT 
--     LateDeliveryRisk AS Predicted_Risk_Level,
--     LateDeliveryRisk_confidence AS Confidence_Score
-- FROM mindsdb.delivery_delay_predictor
-- WHERE DestinationCountry = 'EE. UU.'
--   AND CategoryName = 'Smart watch'
--   AND ShippingMode = 'Second Class'
--   AND OrderTotal = 299.98
--   AND LateDeliveryRisk_confidence > 0.80;