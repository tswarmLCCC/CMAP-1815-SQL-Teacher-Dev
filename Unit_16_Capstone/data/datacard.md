# **Dataset Card: DataCo Smart Supply Chain**

This dataset card documents the provenance, architecture, structure, and real-world execution anomalies of the DataCo Smart Supply Chain dataset. Use this as a reference guide for curriculum mapping, student support, and ETL platform setup.

## **1\. Dataset Overview**

* **Title:** DataCo Smart Supply Chain for Big Data Analysis  
* **Author/Curator:** Shashwat (Kaggle Community Curator)  
* **Original Creator:** DataCo Global Logistics  
* **Repository Source:** [Kaggle Dataset Link](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)  
* **License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International ([CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))  
* **Primary Task Focus:** Relational Database Normalization (3NF), Advanced SQL Analytics, and Binary Delay Classification (Predictive modeling)

### **Key Metrics**

* **Total Rows:** 180,519  
* **Total Columns (Raw):** 53  
* **Size on Disk:** \~15.2 MB (Zipped) / \~44.8 MB (Raw CSV)  
* **Temporal Span:** January 2015 – January 2018

## **2\. Dataset Provenance & Context**

The dataset represents structured operational activity from **DataCo Global**, a supply chain, sales, and logistics enterprise. It tracks individual transaction records across diverse global corridors.

The dataset includes:

* **Spatial Geography:** Coordinates and addresses for customer accounts and physical fulfillment shipping ports (spanning North America, South America, Europe, Asia, and Africa).  
* **Financial Accounting:** Production costs, pricing, transaction discounts, product margins, and total product sales.  
* **Logistics & Timeline Metrics:** Target scheduling parameters vs. real-world transit measurements, shipping modes, payment types, and binary risk tracking indicators.

## **3\. Structural Properties**

### **Key Technical Anomalies (For ETL Engineers)**

1. **Character Encoding (LATIN1 / ISO-8859-1):**  
   * **The Issue:** The dataset was generated in a Spanish-language locale. It contains regional accent characters (such as á, ó, and ñ in locations like *San Sebastián* or names like *Andrés*).  
   * **The Fix:** If imported as standard UTF-8, the PostgreSQL engine crashes. The parser must read the source stream using explicit LATIN1 encoding.  
2. **Customer LastName NULL Values:**  
   * **The Issue:** A portion of the customer database contains empty strings or complete NULL data points for the Customer Lname column.  
   * **The Fix:** The normalized target table Customers must define LastName as nullable (VARCHAR(100) NULL instead of NOT NULL), or use a string fallback like COALESCE(customer\_lname, '').  
3. **Multi-Item Order Key Collisions:**  
   * **The Issue:** Order Id represents a transaction container. Because orders can contain multiple product line items, the same Order Id appears on multiple rows in the flat file.  
   * **The Fix:** Setting OrderID as a Primary Key on a single database table containing product dimensions triggers a constraint violation. The data must be normalized into parent Orders and child OrderItems tables to preserve 3NF.

## **4\. Column Schema Mapping**

Below is the dictionary of columns utilized in our staging and final normalized configurations.

| CSV Column Name | Staging SQL Field | Target Datatype | Description & Context |
| :---- | :---- | :---- | :---- |
| Type | type | VARCHAR(50) | Transaction payment method (DEBIT, TRANSFER, CASH, PAYMENT). |
| Days for shipping (real) | days\_for\_shipping\_real | INTEGER | Actual days taken to deliver the goods. |
| Days for shipment (scheduled) | days\_for\_shipment\_scheduled | INTEGER | Planned or scheduled delivery days requested. |
| Late\_delivery\_risk | late\_delivery\_risk | INTEGER | Binary risk flag. (1 \= Delivery was late, 0 \= On Time). |
| Customer Id | customer\_id | INTEGER | Unique identity number of the purchasing customer. |
| Customer Fname | customer\_fname | VARCHAR(100) | Customer's given first name. |
| Customer Lname | customer\_lname | VARCHAR(100) | Customer's family last name (Can contain NULLs). |
| Customer City | customer\_city | VARCHAR(100) | City where the customer lives. |
| Customer State | customer\_state | VARCHAR(100) | State where the customer lives (Can contain NULLs). |
| Customer Country | customer\_country | VARCHAR(100) | Country where the customer lives. |
| Order Id | order\_id | INTEGER | Dynamic key indicating the parent transaction. |
| Order Date | order\_date\_dateorders | DATE (parsed) | Exact date/time the purchase was finalized. |
| Order Item Total | order\_item\_total | DECIMAL(10,2) | Net total paid for the line item after discounts. |
| Product Name | product\_name | VARCHAR(255) | Plain text description of the product. |
| Category Name | category\_name | VARCHAR(100) | Department category class (e.g., Sporting Goods). |
| Shipping Mode | shipping\_mode | VARCHAR(100) | Shipment class (e.g., Standard Class, First Class). |

## **5\. Educational Objectives**

This dataset serves as an ideal framework for students studying database management and data pipelines:

* **Relational Normalization:** Moving away from flat tables to resolve 1NF, 2NF, and 3NF issues.  
* **Performance Tuning:** Proving how index choices change query execution plans under heavy data loads.  
* **Real-World Integrity Handling:** Confronting common data issues like text encoding and nullable fields.  
* **AI Feature Engineering:** Building clean view schemas for machine learning predictions.