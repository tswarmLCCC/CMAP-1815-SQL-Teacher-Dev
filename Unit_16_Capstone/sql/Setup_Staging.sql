-- Run this in PostgreSQL BEFORE running the \copy command.
-- This creates a flat staging table matching the DataCo_Trimmed.csv structure.

DROP TABLE IF EXISTS raw_staging;

CREATE TABLE raw_staging (
    Type VARCHAR(50),
    Days_for_shipping_real INT,
    Days_for_shipment_scheduled INT,
    Late_delivery_risk INT,
    Customer_Id INT,
    Customer_Fname VARCHAR(100),
    Customer_Lname VARCHAR(100),
    Customer_City VARCHAR(100),
    Customer_State VARCHAR(100),
    Customer_Country VARCHAR(100),
    Order_Id INT,
    Order_Date VARCHAR(50),
    Order_Item_Total DECIMAL(10,2),
    Product_Name VARCHAR(255),
    Category_Name VARCHAR(100),
    Shipping_Mode VARCHAR(100)
);