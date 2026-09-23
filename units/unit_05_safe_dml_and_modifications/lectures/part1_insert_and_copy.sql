-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 5: Safe DML, Transaction Integrity & Temporary Tables
-- Script 1: The Anatomy of INSERT, Bulk Loading & Upserts
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Explicit Column Lists vs. Positional Inserts
-- Always specify column names explicitly to protect against schema changes.
-- ----------------------------------------------------------------------------

-- 1.1 Single-row insert with explicit column declarations
INSERT INTO products (
    product_name, 
    category, 
    retail_price, 
    wholesale_cost, 
    stock_quantity, 
    is_discontinued
) VALUES (
    'Wireless Noise-Cancelling Headphones', 
    'Technology', 
    149.99, 
    75.00, 
    45, 
    FALSE
);

-- Verify insertion using SELECT
SELECT * 
FROM products 
WHERE product_name = 'Wireless Noise-Cancelling Headphones';

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Multi-Row Batch Loading
-- Loading multiple rows in a single high-efficiency statement.
-- ----------------------------------------------------------------------------

INSERT INTO products (
    product_name, 
    category, 
    retail_price, 
    wholesale_cost, 
    stock_quantity
) VALUES 
    ('USB-C Fast Charging Hub', 'Technology', 39.99, 18.00, 150),
    ('Adjustable Monitor Arm', 'Office Supplies', 69.99, 32.50, 80),
    ('Desk Cable Organizer Clips', 'Office Supplies', 12.99, 3.50, 300);

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Bulk Population from Queries (INSERT INTO ... SELECT)
-- Streaming transformed records directly from one table into another.
-- ----------------------------------------------------------------------------

-- Create a quick sandbox table for demonstration
CREATE TABLE IF NOT EXISTS product_archive (
    archive_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    retail_price NUMERIC(10,2),
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bulk load discontinued items into the archive
INSERT INTO product_archive (product_name, category, retail_price)
SELECT product_name, category, retail_price
FROM products
WHERE is_discontinued = TRUE;

-- Inspect the archived results
SELECT * FROM product_archive;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 4: Handling Duplicate Key Collisions (Upsert)
-- ON CONFLICT DO NOTHING vs. ON CONFLICT DO UPDATE
-- ----------------------------------------------------------------------------

-- 4.1 Safe ignore: Do nothing if the primary key already exists
INSERT INTO products (product_id, product_name, category, retail_price, stock_quantity)
VALUES (1, 'Duplicate Test Item', 'Office Supplies', 19.99, 10)
ON CONFLICT (product_id) DO NOTHING;

-- 4.2 Upsert: Update existing product price and stock on conflict
-- Notice the EXCLUDED pseudo-table representing incoming candidate values!
INSERT INTO products (product_id, product_name, category, retail_price, stock_quantity)
VALUES (1, 'Executive Ballpoint Pen (Restocked)', 'Office Supplies', 24.99, 250)
ON CONFLICT (product_id) 
DO UPDATE SET 
    product_name = EXCLUDED.product_name,
    retail_price = EXCLUDED.retail_price,
    stock_quantity = EXCLUDED.stock_quantity;

-- Inspect updated record
SELECT product_id, product_name, retail_price, stock_quantity
FROM products
WHERE product_id = 1;
