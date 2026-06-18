# **Enterprise ETL: Loading and Manipulating Data in PostgreSQL**

In modern data engineering, the paradigm has largely shifted from traditional **ETL** (Extract, Transform, Load) to **ELT** (Extract, Load, Transform). Instead of transforming raw data in an external processing engine before loading it, we dump raw data directly into the database first.

This guide covers how to ingest raw data, manipulate it inside PostgreSQL, and safely migrate it between tables using staging tables, temporary tables, CTEs, and Python.

## **1\. The Strategy: Staging vs. Target Tables**

When dealing with messy, unnormalized data sources, you should never attempt to load raw data directly into your clean, production-ready tables. Doing so will violate constraints, fail due to data type mismatches, and lock up your production database.

### **The Land-then-Transform Pipeline**

1. **Staging Table (raw\_staging):** A temporary landing strip. It has no constraints, no foreign keys, and permissive data types (often everything is a VARCHAR or simple numeric type).  
2. **Transformation Phase:** SQL queries clean, cast, deduplicate, and split the data.  
3. **Target Tables (3NF Schema):** The clean, production-grade destination tables with strict primary keys, foreign keys, and indexes.

## **2\. Ingesting Data (The "Load" Phase)**

There are two primary ways to load flat files (like CSVs) into PostgreSQL: via the PostgreSQL command-line terminal (\\copy) or using a programmatic script (Python).

### **Method A: Command-Line Ingestion via \\copy**

The \\copy command is a client-side instruction. It reads a file on your local machine and streams it directly to the database port. This avoids permissions issues common with the server-side COPY command.

PGPASSWORD=postgres psql \-U postgres \-h db \-d mydb \-c "\\copy raw\_staging FROM 'Unit\_16\_Capstone/data/DataCoSupplyChainDataset.csv' WITH CSV HEADER ENCODING 'LATIN1';"

### **Technical Breakdown of the Command-Line Ingestion**

This single-line terminal command combines shell environment variables, PostgreSQL client execution flags, and internal database SQL engine arguments. Here is exactly what every individual segment does:

* **PGPASSWORD=postgres** This is an environment variable set inline at the very beginning of the terminal command. By default, psql prompts you to type a password interactively. This stops automated scripts from running. Setting PGPASSWORD tells the shell to temporarily expose this password to the executing psql client, allowing the connection to complete instantly without human interaction.  
* **psql** This initiates the PostgreSQL Command Line Interface (CLI) client. It is the executable application used to talk to the PostgreSQL server engine.  
* **\-U postgres** The \-U flag stands for **User**. Here, we specify that we want to log in as the administrative user postgres.  
* **\-h db** The \-h flag stands for **Host**. In your Codespaces environment, the database is running inside a separate network container named db. This flag redirects the network socket away from standard localhost to the container host name db.  
* **\-d mydb** The \-d flag stands for **Database**. This instructs the client to bypass the system's default admin database and open a direct channel into the specific database named mydb.  
* **\-c** The \-c flag stands for **Command**. It tells the psql client: *"Do not open an interactive SQL terminal session. Instead, run the single string query that follows inside quotes, execute it, and exit immediately."*  
* **\\copy (Backslash Copy vs. Standard COPY)** This is the most critical distinction in database security and context.  
  * **Standard SQL COPY** is run inside the server engine. The database server itself searches its *local system path* for the CSV file. If the file is on your computer and the server is on a remote host (like our container setup), the server will throw a "File Not Found" error. Furthermore, standard COPY requires administrative superuser filesystem access, which is a major security risk.  
  * **The meta-command \\copy** is executed by the *client* (VS Code / terminal). It opens the local file on your workspace, reads it line by line into memory, and streams it across the open port to the database server using PostgreSQL's native copy protocol. This bypasses permission blocks and server filesystem limitations.  
* **raw\_staging** The target table inside PostgreSQL that will receive the streamed data.  
* **FROM 'Unit\_16\_Capstone/data/DataCoSupplyChainDataset.csv'** The relative path to the source file located in your local development workspace directory.  
* **WITH CSV HEADER** This argument tells the parser how to read the file structure:  
  * CSV configures the parser to expect commas as field delimiters and double-quotes for escaping strings containing commas.  
  * HEADER tells PostgreSQL that the first row of the CSV file contains the plain-text column names, and should be discarded rather than imported as a row of data.  
* **ENCODING 'LATIN1'** Character encodings define how binary bytes are mapped to readable text characters.  
  * **UTF-8** is the modern internet standard. However, if a file has special regional characters (such as accents like á in "San Sebastián") and was saved in an older European standard format like **LATIN1** (ISO-8859-1), UTF-8 parser execution will crash immediately with an "invalid byte sequence" error.  
  * Specifying ENCODING 'LATIN1' instructs the parser to read those characters safely using the correct regional translation dictionary.

### **Method B: Programmatic Ingestion via Python**

In a professional production pipeline, you will often schedule Python scripts (using tools like Apache Airflow or Prefect) to run imports.

When loading large datasets with Python, **never** use standard SQL INSERT loops—they are extremely slow. Instead, stream the data using PostgreSQL's bulk copy protocol via psycopg2.

import os  
import psycopg2

import os
import psycopg2

def load_csv_to_postgres(csv_filepath, target_table):
    # Establish connection using environment variables or explicit config
    conn = psycopg2.connect(
        host="db",
        database="mydb",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    
    try:
        print(f"Starting ingestion of {csv_filepath}...")
        
        # 1. Open the CSV file locally
        with open(csv_filepath, 'r', encoding='latin1') as f:
            # 2. Use copy_expert to stream the raw file straight to PostgreSQL
            # This is significantly faster than using pandas or execute_many
            sql_command = f"COPY {target_table} FROM STDIN WITH CSV HEADER;"
            cursor.copy_expert(sql=sql_command, file=f)
            
        conn.commit()
        print("Bulk ingestion completed successfully.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during ingestion: {e}")
        raise e
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load_csv_to_postgres("Unit_16_Capstone/data/DataCoSupplyChainDataset.csv", "raw_staging")


### **Technical Breakdown of the Python Script**

When you execute database actions inside a programming language, you are working with an abstraction layer over standard SQL. Here is exactly what is happening in the code execution cycle above:

* **import psycopg2** psycopg2 is the standard PostgreSQL driver adapter for Python. It acts as the C-level wrapper that converts Python objects and logic into the binary protocol format PostgreSQL understands.  
* **psycopg2.connect(...)** This initiates a TCP/IP connection handshake to the PostgreSQL instance running on host db. This returns a connection object (conn) which represents your active transaction state and communication pipe to the database server.  
* **conn.cursor()** In relational databases, a **Cursor** is an execution context control structure. It acts as your active pointer inside the database. Think of the connection as the phone line, and the cursor as the actual voice message carrying and returning specific SQL execution instructions.  
* **with open(csv\_filepath, 'r', encoding='latin1') as f:**  
  * with is a Python context manager. It guarantees that regardless of whether the file loads perfectly or crashes mid-way, the OS file pointer will be safely closed, preventing memory leaks or file locks on your machine.  
  * 'r' opens the file in read-only mode.  
  * encoding='latin1' tells Python's internal reader how to decode non-standard bytes (like Latin characters with accent marks) before sending them over.  
* **COPY ... FROM STDIN** Standard SQL COPY FROM 'filename' requires the database server to read from its *own* local disk. But when running Python remotely, the database engine cannot see your local Python file.  
  * FROM STDIN (Standard Input) instructs the PostgreSQL engine to wait and prepare to receive a raw stream of data bytes directly over the open network connection port instead of looking for a local file.  
* **cursor.copy\_expert(sql=sql\_command, file=f)** This is the high-performance core of the script.  
  * Standard cursor.execute("INSERT ...") methods force Python to parse rows, construct separate SQL strings, and send them one-by-one, which takes ages for 180,000 rows.  
  * copy\_expert opens a raw, low-level binary pipe that directly streams the open system file pointer f to PostgreSQL's native engine. This operates at memory-bus speeds, completing in seconds.  
* **conn.commit() & conn.rollback()** PostgreSQL is transactional by default.  
  * If copy\_expert runs successfully, conn.commit() writes the changes permanently to the database disk.  
  * If *any* error occurs (such as a parsing error on row 50,000), execution falls to the except block, and conn.rollback() is executed. This completely undoes everything that occurred since the transaction began. It leaves the database in its original clean state rather than saving a corrupted, half-filled table.  
* **cursor.close() & conn.close()** These operations run inside the finally: block, ensuring that regardless of success or failure, your system resources are returned to the OS. Leaving connections open will block future database access, eventually locking out other client processes.

## **3\. Data Wrangling: Moving Data Table-to-Table**

Once your raw data is loaded in raw\_staging, you must normalize it into your target database tables.

### **Basic Extraction (The DML Pattern)**

To populate a basic, unlinked dimension table (like Locations), you must pull unique occurrences of these values from the staging area.

\-- Step 1: Drop the existing table to allow a clean write during testing  
DROP TABLE IF EXISTS Locations CASCADE;

\-- Step 2: Create the target Locations dimension table with structural constraints  
CREATE TABLE Locations (  
    LocationID SERIAL PRIMARY KEY,  
    City VARCHAR(100) NOT NULL,  
    State VARCHAR(100),  
    Country VARCHAR(100) NOT NULL,  
    UNIQUE (City, State, Country)  
);

\-- Step 3: Extract unique geographical records from the staging landing strip  
INSERT INTO Locations (City, State, Country)  
SELECT DISTINCT customer\_city, customer\_state, customer\_country  
FROM raw\_staging  
WHERE customer\_city IS NOT NULL   
  AND customer\_country IS NOT NULL;

### **Technical Breakdown of Basic Extraction**

* **DROP TABLE IF EXISTS Locations CASCADE;** The CASCADE modifier ensures that any dependent objects (such as child tables with Foreign Keys or Views referencing this table) are also dropped or detached safely, avoiding dependency locks.  
* **LocationID SERIAL PRIMARY KEY** The SERIAL type is a autoincrementing integer generator. Behind the scenes, PostgreSQL creates an invisible sequence object. Every time you insert a row without specifying a LocationID, the sequence increments by 1 and assigns that value. The PRIMARY KEY modifier automatically applies a UNIQUE index and a NOT NULL constraint to guarantee identity.  
* **UNIQUE (City, State, Country)** This creates a multi-column composite unique constraint. This prevents us from storing duplicates of "San Juan, PR, Puerto Rico" in our table. If a duplicate is inserted, the database will raise a constraint violation error.  
* **INSERT INTO Locations (City, State, Country)** This defines our write destination. By explicitly listing the target columns inside parentheses, we ensure the query matches our values exactly, even if more columns are added to the table design later.  
* **SELECT DISTINCT customer\_city, customer\_state, customer\_country** Out of 180,000 rows in staging, thousands of transactions will occur in the same city. If we executed a simple SELECT, we would attempt to write thousands of duplicate city entries, which would violate our UNIQUE constraint. DISTINCT executes a fast sorting and deduplication pass in temporary execution memory, returning only unique geographic locations.  
* **WHERE customer\_city IS NOT NULL AND customer\_country IS NOT NULL** This is a data quality safeguard. In relational design, dimension attributes must not contain complete null records, as nulls cannot be accurately joined to other operational transactional tables later.

### **Complex Extraction with Dependencies**

When inserting into a table that requires a foreign key pointing to another table, you must join the staging table to your newly created parent table to grab the generated primary keys.

\-- Step 1: Drop existing table to clean workspace  
DROP TABLE IF EXISTS Customers CASCADE;

\-- Step 2: Create the Customers table with a Foreign Key relationship  
CREATE TABLE Customers (  
    CustomerID INT PRIMARY KEY,  
    FirstName VARCHAR(100) NOT NULL,  
    LastName VARCHAR(100) NOT NULL,  
    LocationID INT REFERENCES Locations(LocationID)  
);

\-- Step 3: Populate Customers by matching staging text to Locations IDs  
INSERT INTO Customers (CustomerID, FirstName, LastName, LocationID)  
SELECT DISTINCT   
    r.customer\_id,   
    r.customer\_fname,   
    r.customer\_lname,   
    l.LocationID  
FROM raw\_staging r  
JOIN Locations l ON r.customer\_city \= l.City   
                 AND COALESCE(r.customer\_state, '') \= COALESCE(l.State, '')   
                 AND r.customer\_country \= l.Country  
WHERE r.customer\_id IS NOT NULL;

### **Technical Breakdown of Complex Extraction**

* **LocationID INT REFERENCES Locations(LocationID)** This is the foundation of relational integrity. The REFERENCES constraint defines a Foreign Key. This tells PostgreSQL that the integer written to LocationID *must* already exist inside the Locations table. If we try to write a customer with a non-existent LocationID, the write will fail.  
* **FROM raw\_staging r** The r acts as an alias. In complex queries, writing the full name of tables repeatedly makes code hard to read. Defining r allows us to refer to staging variables quickly (e.g., r.customer\_id).  
* **JOIN Locations l ON ...** We cannot write the city name directly into the Customers table, as that violates 3NF normalization. Instead, we must retrieve the primary integer key (LocationID) that represents that city. The join acts as a translation bridge:  
  * It looks at a staging row's address fields.  
  * It searches the Locations table for the matching row.  
  * When it finds the match, it pulls the generated l.LocationID and lines it up side-by-side with the customer's name.  
* **COALESCE(r.customer\_state, '') \= COALESCE(l.State, '')** In SQL, a comparison of NULL \= NULL does not return TRUE. It returns NULL, which fails to match. If some records do not have a state listed (e.g., countries outside the US), they will be lost during a join. The COALESCE function converts any null value into an empty string '' dynamically, ensuring null states still join together successfully.

## **4\. In-Memory Manipulation: Temp Tables and CTEs**

Sometimes, transformations are too complex to perform in a single INSERT INTO ... SELECT statement. PostgreSQL provides two powerful in-memory structures to split up your logic: **Temporary Tables** and **Common Table Expressions (CTEs)**.

### **Tool 1: Temporary Tables (CREATE TEMP TABLE)**

Temporary tables exist only for the duration of your current database session. They are automatically dropped when you close your connection. They are excellent for processing intermediate steps in a multi-step ETL script.

\-- Step 1: Create a persistent target table for the final data  
DROP TABLE IF EXISTS HighValueRegistry CASCADE;

CREATE TABLE HighValueRegistry (  
    RegistryID SERIAL PRIMARY KEY,  
    OrderID INT NOT NULL,  
    CustomerID INT NOT NULL,  
    OrderTotal DECIMAL(10,2) NOT NULL,  
    OrderDate DATE NOT NULL  
);

\-- Step 2: Create a temporary working table in session memory  
CREATE TEMP TABLE temp\_high\_value\_orders AS  
SELECT   
    order\_id,   
    customer\_id,   
    order\_item\_total as sales,  
    CAST(order\_date\_dateorders AS DATE) as formatted\_date  
FROM raw\_staging  
WHERE order\_item\_total \> 1000;

\-- Step 3: Generate an index on the temporary table to optimize reads  
CREATE INDEX idx\_temp\_order\_id ON temp\_high\_value\_orders(order\_id);

\-- Step 4: Stream the optimized subset into the final production target table  
INSERT INTO HighValueRegistry (OrderID, CustomerID, OrderTotal, OrderDate)  
SELECT order\_id, customer\_id, sales, formatted\_date   
FROM temp\_high\_value\_orders;

### **Technical Breakdown of Temporary Tables**

* **CREATE TEMP TABLE temp\_high\_value\_orders AS** The TEMP modifier creates this table inside a specialized, private system schema. It is entirely invisible to other concurrent connections. If 50 students run this query at the same time, they will each work in their own isolated memory space.  
  * By default, temporary tables avoid writing data to persistent transaction logs (WAL), saving immense system disk write IO.  
* **CAST(order\_date\_dateorders AS DATE)** Our staging area represents dates as string-based characters. However, strings like '1/31/2018' cannot be sorted or compared as dates. CAST(val AS DATE) instructs the query optimizer to parse the characters, identify the date pattern, and convert the layout into a structured 4-byte DATE value.  
* **CREATE INDEX idx\_temp\_order\_id ON temp\_high\_value\_orders(order\_id);** Inline queries and CTEs cannot be indexed. However, temporary tables behave like physical tables. If your staging script needs to perform a heavy calculation on 180,000 rows and then join that dataset multiple times, writing it to a temp table and creating a B-Tree index on the join key is one of the most effective optimization strategies.  
* **INSERT INTO HighValueRegistry ... SELECT ... FROM temp\_high\_value\_orders;** Once the messy work of sorting and casting is complete inside the indexed temp table, we execute a simple, direct, fast append into our structured production registry.

### **Tool 2: Writable Common Table Expressions (CTEs)**

CTEs (created using the WITH keyword) are temporary result sets that exist only for the execution of a single query. What many developers don't know is that you can perform write operations (INSERT, UPDATE, DELETE) inside CTEs.

This allows you to write "chained" migrations in a single SQL statement:

\-- Step 1: Create target tables for our chained write demo  
DROP TABLE IF EXISTS Inventory CASCADE;  
DROP TABLE IF EXISTS Products CASCADE;

CREATE TABLE Products (  
    ProductID SERIAL PRIMARY KEY,  
    ProductName VARCHAR(255) UNIQUE NOT NULL,  
    CategoryName VARCHAR(100) NOT NULL  
);

CREATE TABLE Inventory (  
    InventoryID SERIAL PRIMARY KEY,  
    ProductID INT REFERENCES Products(ProductID),  
    StockLevel INT NOT NULL,  
    WarehouseCode VARCHAR(50) NOT NULL  
);

\-- Step 2: Execute chained inserts passing dynamic key structures in-memory  
WITH inserted\_product AS (  
    INSERT INTO Products (ProductName, CategoryName)  
    VALUES ('Super Rugged Smart Watch', 'Wearables')  
    ON CONFLICT (ProductName) DO NOTHING  
    RETURNING ProductID  
)  
INSERT INTO Inventory (ProductID, StockLevel, WarehouseCode)  
SELECT ProductID, 100, 'WH-EAST'   
FROM inserted\_product;

### **Technical Breakdown of Writable CTEs**

This single, continuous statement writes to the database, generates dynamic sequence keys, captures those keys, and writes them to a completely different table without storing anything on your physical client machine.

* **WITH inserted\_product AS (...)** This defines the Common Table Expression. It sets up an in-memory virtual view called inserted\_product that only exists for the duration of this single transaction run.  
* **ON CONFLICT (ProductName) DO NOTHING** In standard SQL, if you attempt to write a row that violates a UNIQUE constraint, the engine halts the entire query and rolls back the changes. ON CONFLICT DO NOTHING turns a potential error into a silent pass. If the product name already exists, the database ignores the insert step and safely continues.  
* **RETURNING ProductID** Normally, a SQL INSERT statement only returns the number of rows written. Because ProductID is an auto-generating SERIAL column, the client application has no direct way of knowing what number was assigned to this new product. RETURNING ProductID forces the database engine to return the generated integer as a dynamic, select-style table layout in memory.  
* **INSERT INTO Inventory (ProductID, StockLevel, WarehouseCode) SELECT ProductID, 100, 'WH-EAST' FROM inserted\_product;** This is the primary outer query. It treats the CTE inserted\_product as if it were a physical source table. It reads the returned ProductID, appends the stock metrics, and writes them straight into the dependent child table Inventory.

## **5\. Architectural Comparison**

| Feature | Staging Table | Temporary Table | CTE (WITH block) |
| :---- | :---- | :---- | :---- |
| **Scope/Lifetime** | Permanent database object (persistent until dropped). | Session-based (deleted when connection closes). | Query-based (deleted immediately after query finishes). |
| **Disk Storage** | Written to physical disk. | Stored in memory (spills to disk if extremely large). | Kept completely in-memory. |
| **Indexing** | Fully indexable. | Fully indexable. | Cannot be indexed directly. |
| **Primary Use Case** | Ingesting raw, unconstrained CSV files via bulk copy. | Heavy intermediate calculations, indexing datasets before big joins. | Readability, structural organization of a single script, quick one-off writes. |

## **6\. Enterprise Best Practices for Students**

### **1\. Always Use Transactions**

Wrap your migration scripts in BEGIN; and COMMIT;.

\-- Step 1: Open the transaction block  
BEGIN;

\-- Step 2: Insert into the Parent Geography table  
INSERT INTO Locations (City, State, Country)  
VALUES ('Cheyenne', 'WY', 'United States')  
ON CONFLICT (City, State, Country) DO NOTHING;

\-- Step 3: Insert into the dependent Customer table referencing that parent record  
INSERT INTO Customers (CustomerID, FirstName, LastName, LocationID)  
SELECT 99999, 'John', 'Doe', LocationID  
FROM Locations  
WHERE City \= 'Cheyenne'   
  AND State \= 'WY'   
  AND Country \= 'United States';

\-- Step 4: Write all changes permanently to physical disk  
COMMIT;

* **Why?** A transaction is an "all-or-nothing" execution package. If your insert script contains 50 queries to migrate 180,000 rows, and query 42 crashes due to a data mismatch, a transaction rollback will undo the entire script, leaving the database clean. Without a transaction block, you are left with a half-migrated database, forcing you to manually hunt down where the process stopped.

### **2\. Explicit Type Casting**

Do not rely on the database engine to guess your data types. Always cast staging text data into explicit, native formats.

\-- Complete query demonstrating type transformation during staging reads  
SELECT   
    order\_id,  
    CAST(order\_date\_dateorders AS DATE) AS typed\_order\_date,  
    CAST(order\_item\_total AS DECIMAL(10,2)) AS typed\_sales,  
    CAST(customer\_id AS INTEGER) AS typed\_customer\_id  
FROM raw\_staging  
LIMIT 5;

* **Why?** Raw CSV imports write dates, integers, and decimals as simple strings of text. If you attempt to run mathematical functions or temporal sort queries on string data, your results will be slow and inaccurate. Explicitly casting using CAST(col AS type) guarantees that the downstream engine receives formatted, predictable binary representations.

### **3\. Handle Duplicates First**

Relational systems enforce primary and unique key integrity. You must deduplicate your staging records *before* trying to append them to your production schemas.

\-- Complete example using aggregation to isolate unique records from raw staging duplicates  
INSERT INTO Products (ProductName, CategoryName)  
SELECT DISTINCT product\_name, category\_name  
FROM raw\_staging  
WHERE product\_name IS NOT NULL   
  AND category\_name IS NOT NULL;

* **Why?** The staging table can contain hundreds of rows representing transactions for a single product. If you try to write all of these occurrences directly into your Products table, your query will fail immediately due to primary/unique key constraint checks. Running a deduplication step like SELECT DISTINCT or a grouping analysis cleans your dataset before it hits target constraints.
