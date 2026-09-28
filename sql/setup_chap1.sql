-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Master Database Seed & Architecture: setup_chap1.sql
-- Compatible with all 8 Units, In-Class Demos, and SpeedGrader Labs
-- ============================================================================

-- Drop tables in reverse order of foreign key dependencies
DROP TABLE IF EXISTS superstore CASCADE;
DROP TABLE IF EXISTS order_lines CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS locations CASCADE;

-- 1. Create Locations Table
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    facility_type VARCHAR(50)
);

-- 2. Create Employees Table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(50),
    title VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10, 2),
    bonus DECIMAL(10, 2),
    location_id INT REFERENCES locations(location_id),
    is_active BOOLEAN DEFAULT TRUE
);

-- 3. Create Products Table
-- Includes both cost_to_produce & wholesale_cost for backwards/forward compatibility
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(50) DEFAULT ('SKU-' || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0')),
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    cost_to_produce DECIMAL(10, 2),
    wholesale_cost DECIMAL(10, 2),
    retail_price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    description TEXT,
    release_date DATE,
    discontinued_date DATE,
    is_discontinued BOOLEAN DEFAULT FALSE
);

-- 4. Create Orders Table (Header)
-- Includes customer_id and total_amount for Unit 4/6 advanced analytics
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(employee_id),
    customer_id INT DEFAULT 101,
    order_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Completed',
    shipping_method VARCHAR(50),
    total_amount DECIMAL(10, 2) DEFAULT 0.00
);

-- 5. Create Order Lines Table (Details)
-- Includes line_id alias for backwards compatibility
CREATE TABLE order_lines (
    order_line_id SERIAL PRIMARY KEY,
    line_id INT,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL -- Historical unit price at time of order
);

-- 6. Create Superstore Benchmark Table (for Units 4/5/8 analytics)
CREATE TABLE superstore (
    row_id SERIAL PRIMARY KEY,
    order_id VARCHAR(50),
    order_date DATE,
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    region VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name VARCHAR(200),
    sales DECIMAL(10, 2),
    quantity INT,
    discount DECIMAL(4, 2),
    profit DECIMAL(10, 2)
);

-- ============================================================================
-- DATA INSERTION SUITE
-- ============================================================================

-- Insert Locations
INSERT INTO locations (city, state, facility_type) VALUES
('Cheyenne', 'WY', 'Headquarters'),
('Laramie', 'WY', 'Research & Development'),
('Denver', 'CO', 'Distribution Center'),
('Topeka', 'KS', 'Support Center'),
('Fort Collins', 'CO', 'Retail Store'),
('Salt Lake City', 'UT', 'Warehouse'),
('Chicago', 'IL', 'Regional Office'),
('Phoenix', 'AZ', 'Retail Store');

-- Insert Employees (Expanded 28-member roster)
INSERT INTO employees (first_name, last_name, department, title, hire_date, salary, bonus, location_id, is_active) VALUES
('Harry', 'Dresden', 'Security', 'Field Investigator', '2015-10-31', 65000.00, 1500.00, 1, TRUE),
('Karrin', 'Murphy', 'Security', 'Director', '2012-04-15', 95000.00, NULL, 1, TRUE),
('Waldo', 'Butters', 'Research', 'Medical Examiner', '2017-06-12', 82000.00, 2000.00, 1, TRUE),
('Jon', 'Snow', 'Operations', 'Night Watch Supervisor', '2019-01-01', 52000.00, 500.00, 3, TRUE),
('Arya', 'Stark', 'Security', 'Specialist', '2021-08-20', 68000.00, 3000.00, 3, TRUE),
('Lestat', 'Lioncourt', 'Sales', 'Account Executive', '2022-10-31', 75000.00, 12000.00, 4, TRUE),
('Jamie', 'Fraser', 'Management', 'Regional Manager', '2016-05-01', 110000.00, 8000.00, 3, TRUE),
('Claire', 'Beauchamp', 'Research', 'Medical Lead', '2016-05-01', 115000.00, NULL, 3, TRUE),
('Karlach', 'Cliffgate', 'Operations', 'Heavy Equipment Operator', '2023-08-03', 62000.00, 4500.00, 2, TRUE),
('Astarion', 'Ancunin', 'Sales', 'Acquisitions', '2023-08-03', 58000.00, 5000.00, 4, TRUE),
('Gale', 'Dekarios', 'Research', 'AI Architect', '2020-11-15', 135000.00, NULL, 2, TRUE),
('Shadowheart', 'Viconia', 'Support', 'Customer Success', '2022-02-14', 54000.00, 1200.00, 4, TRUE),
('Lae''zel', 'Crèche', 'Security', 'Combat Specialist', '2023-09-01', 61000.00, 1000.00, 2, TRUE),
('John', 'Bradford', 'Management', 'Operations Officer', '2012-10-09', 105000.00, NULL, 1, TRUE),
('Moira', 'Vahlen', 'Research', 'Lead Scientist', '2012-10-09', 125000.00, 15000.00, 2, FALSE),
('Raymond', 'Shen', 'Engineering', 'Chief Engineer', '2012-10-09', 130000.00, NULL, 2, FALSE),
('Lily', 'Shen', 'Engineering', 'Lead Mechanic', '2016-02-05', 92000.00, 4000.00, 2, TRUE),
('Zagreus', 'Underworld', 'Sales', 'Escape Consultant', '2020-09-17', 77000.00, 8000.00, 6, TRUE),
('Melinoë', 'Underworld', 'Research', 'Magic Specialist', '2024-05-06', 74000.00, 5000.00, 6, TRUE),
('Geralt', 'Riv', 'Security', 'Contractor', '2015-05-19', 85000.00, NULL, 3, TRUE),
('Yennefer', 'Vengerberg', 'Research', 'Consultant', '2015-05-19', 140000.00, 20000.00, 1, TRUE),
('Shala', 'Swarm', 'Medical', 'First Assist Practitioner', '2018-03-12', 125000.00, NULL, 1, TRUE),
('Lando', 'Pyrenees', 'Security', 'Guard Dog', '2021-03-01', 30000.00, 100.00, 1, TRUE),
('Bonitto', 'Pyrenees', 'Security', 'Trainee', '2025-11-10', 20000.00, 50.00, 1, TRUE),
('Casper', 'Cat', 'Operations', 'Pest Control Lead', '2020-07-15', 25000.00, NULL, 1, TRUE),
('Cheddar', 'Cat', 'Operations', 'Pest Control Associate', '2022-04-10', 22000.00, NULL, 1, TRUE),
('Nathan', 'MacKinnon', 'Sales', 'Top Performer', '2013-09-01', 150000.00, 25000.00, 3, TRUE),
('Cale', 'Makar', 'Engineering', 'Defense Architect', '2019-10-01', 145000.00, 20000.00, 3, TRUE);

-- Insert Products (Expanded with wholesale_cost and is_discontinued)
INSERT INTO products (sku, product_name, category, cost_to_produce, wholesale_cost, retail_price, stock_quantity, description, release_date, discontinued_date, is_discontinued) VALUES
('FIT-001', 'Saris Fluid2 Indoor Bike Trainer', 'Fitness', 150.00, 150.00, 299.99, 15, 'Quiet and consistent resistance for indoor cycling. Compatible with Zwift and MyWhoosh.', '2021-01-15', NULL, FALSE),
('FIT-002', 'Magene Bluetooth Speed & Cadence Sensor', 'Fitness', 12.00, 12.00, 24.50, 42, 'Dual protocol ANT+/Bluetooth tracking for cycling.', '2022-03-10', NULL, FALSE),
('FIT-003', 'Carbon Fiber Pickleball Paddle Set', 'Fitness', 22.00, 22.00, 55.00, 40, 'Two lightweight paddles with edge guard and four indoor balls.', '2023-05-20', NULL, FALSE),
('GAM-001', '8BitDo SN30 Pro Bluetooth Controller', 'Gaming', 18.50, 18.50, 44.99, 28, 'Retro style controller with modern joysticks and rumble.', '2019-11-05', NULL, FALSE),
('GAM-002', 'Steam Deck OLED 512GB', 'Gaming', 450.00, 450.00, 549.00, 8, 'Handheld PC gaming console.', '2023-11-16', NULL, FALSE),
('GAM-003', 'Baldur''s Gate 3 PC Key', 'Software', 0.00, 0.00, 59.99, 999, 'Digital download key. Game of the Year 2023.', '2023-08-03', NULL, FALSE),
('GAM-004', 'Xenonauts 2 Tactical Guide', 'Books', 4.50, 4.50, 19.99, 5, 'Comprehensive tactics for planetary defense.', '2023-07-18', '2025-01-15', TRUE),
('GAM-005', 'Satisfactory Early Access Key', 'Software', 0.00, 0.00, 29.99, 0, 'Factory building and automation on an alien planet.', '2020-06-08', '2024-09-09', TRUE),
('GAM-006', 'Satisfactory 1.0 Release Key', 'Software', 0.00, 0.00, 39.99, 999, 'Fully optimized factory building experience.', '2024-09-10', NULL, FALSE),
('GAM-007', 'No Man''s Sky PC Key', 'Software', 0.00, 0.00, 59.99, 999, 'Procedural universe exploration and survival.', '2016-08-12', NULL, FALSE),
('GAM-008', 'Hades PC Key', 'Software', 0.00, 0.00, 24.99, 999, 'Rogue-like dungeon crawler.', '2020-09-17', NULL, FALSE),
('OUT-001', 'Hickory Wood Pellets 20lb', 'Outdoor', 6.00, 6.00, 18.99, 110, 'Premium hardwood pellets for deep smoke flavor on pellet grills.', '2020-04-01', NULL, FALSE),
('OUT-002', 'Apple Wood Pellets 20lb', 'Outdoor', 6.50, 6.50, 19.99, 45, 'Sweet smoke flavor, ideal for pork and poultry.', '2020-04-01', NULL, FALSE),
('OUT-003', 'Cast Iron Smoker Box', 'Outdoor', 5.00, 5.00, 15.50, 20, 'Heavy duty box for wood chips on gas or charcoal grills.', '2018-06-15', NULL, FALSE),
('OUT-004', 'Digital Meat Thermometer Bluetooth', 'Outdoor', 14.00, 14.00, 39.99, 0, 'Six probe thermometer with mobile app integration.', '2022-05-10', NULL, FALSE),
('OUT-005', 'Prime Rib Rub 16oz', 'Groceries', 4.00, 4.00, 12.99, 65, 'Coarse salt, black pepper, garlic, and rosemary blend.', '2021-11-01', NULL, FALSE),
('GRO-001', 'Nespresso Vertuo Espresso Pods - Diavolitto', 'Groceries', 15.00, 15.00, 35.00, 85, 'Highly intense dark roast espresso capsules, 50 count.', '2021-08-20', NULL, FALSE),
('GRO-002', 'Simpsons Golden Promise Malt 50lb', 'Groceries', 35.00, 35.00, 65.00, 12, 'Base malt for homebrewing traditional ales.', '2019-02-15', NULL, FALSE),
('GRO-003', 'Citra Hops 1lb Pellet', 'Groceries', 12.00, 12.00, 24.99, 30, 'High alpha acid hops with strong citrus and tropical fruit notes.', '2023-10-05', NULL, FALSE),
('GRO-004', 'Lalvin EC-1118 Yeast 10-pack', 'Groceries', 3.00, 3.00, 9.50, 120, 'Champagne yeast ideal for hard ciders and fruit wines.', '2020-11-22', NULL, FALSE),
('GRO-005', 'Pour-over Glass Carafe 400ml', 'Kitchen', 8.50, 8.50, 22.00, 34, 'Borosilicate glass with stainless steel filter.', '2022-01-15', NULL, FALSE),
('SMRT-001', 'Zooz 800 Series Z-Wave Plus Smart Switch', 'Home Automation', 14.00, 14.00, 32.95, 60, 'Dimmer switch for smart home hubs. Scene control enabled.', '2023-01-10', NULL, FALSE),
('SMRT-002', 'Raspberry Pi 5 8GB', 'Electronics', 65.00, 65.00, 80.00, 0, 'SBC for local servers, Docker containers, and Home Assistant.', '2023-10-23', NULL, FALSE),
('SMRT-003', 'TP-Link Tapo 2K Pan/Tilt Security Camera', 'Home Automation', 22.00, 22.00, 45.99, 115, 'Indoor camera with RTSP support for Frigate NVR integration.', '2022-09-14', NULL, FALSE),
('SMRT-004', 'Coral Edge TPU USB Accelerator', 'Electronics', 40.00, 40.00, 59.99, 3, 'Machine learning coprocessor for fast object detection.', '2019-03-04', NULL, FALSE),
('SMRT-005', 'Dreame L10 Pro Robot Vacuum', 'Home Automation', 200.00, 200.00, 389.99, 12, 'LiDAR navigation with local control options.', '2021-05-08', NULL, FALSE),
('AUD-001', 'Klipsch Reference 10" Subwoofer', 'Audio', 160.00, 160.00, 349.00, 8, 'Front-firing spun-copper woofer for home theater setups.', '2018-08-15', NULL, FALSE),
('AUD-002', 'Onkyo TX-NR6050 7.2 Channel Receiver', 'Audio', 250.00, 250.00, 499.00, 4, '8K video, Dolby Atmos, and network streaming.', '2021-11-01', NULL, FALSE),
('SFT-001', 'DaVinci Resolve Studio License Key', 'Software', 0.00, 0.00, 295.00, 99, 'Professional video editing, color grading, and AI transcription.', '2022-04-18', NULL, FALSE),
('FUR-001', 'Vintage Oak End Table', 'Furniture', 45.00, 45.00, 125.00, 2, 'Restored solid oak with original brass hardware. Auction acquisition.', '2024-03-12', NULL, FALSE);

-- Insert Orders (with customer_id and populated total_amount)
INSERT INTO orders (employee_id, customer_id, order_date, status, shipping_method, total_amount) VALUES
(1, 101, '2024-01-15', 'Completed', 'Standard', 50.97),
(5, 102, '2024-02-10', 'Completed', 'Express', 59.99),
(10, 103, '2024-03-05', 'Completed', 'Overnight', 324.49),
(12, 104, '2024-03-12', 'Completed', 'Standard', 171.98),
(2, 101, '2024-04-01', 'Completed', 'Standard', 44.99),
(8, 105, '2024-04-18', 'Completed', 'Express', 158.97),
(21, 106, '2024-05-22', 'Completed', 'Standard', 848.00),
(17, 102, '2024-06-14', 'Completed', 'Standard', 162.00),
(9, 107, '2024-07-02', 'Completed', 'Express', 39.99),
(3, 103, '2024-07-25', 'Completed', 'Standard', 15.50),
(4, 104, '2024-08-10', 'Completed', 'Standard', 55.00),
(11, 101, '2024-09-05', 'Processing', 'Overnight', 549.00),
(22, 105, '2024-09-12', 'Completed', 'Express', 295.00),
(6, 106, '2024-09-28', 'Completed', 'Standard', 59.99),
(18, 107, '2024-10-01', 'Shipped', 'Standard', 59.97),
(7, 102, '2024-10-15', 'Pending', 'Express', 59.99),
(14, 103, '2024-11-02', 'Completed', 'Standard', 125.00),
(29, 104, '2024-11-18', 'Completed', 'Overnight', 389.99),
(23, 101, '2024-12-05', 'Processing', 'Standard', 183.96),
(24, 105, '2024-12-12', 'Completed', 'Express', 69.98);

-- Insert Order Lines (Mapping Order ID to Product ID)
INSERT INTO order_lines (order_id, product_id, quantity, unit_price) VALUES
(1, 12, 2, 18.99), -- Order 1 bought Hickory Pellets
(1, 16, 1, 12.99), -- Order 1 bought Prime Rib Rub
(2, 6, 1, 59.99),  -- Order 2 bought BG3
(3, 2, 1, 24.50),  -- Order 3 bought Speed Sensor
(3, 1, 1, 299.99), -- Order 3 bought Bike Trainer
(4, 23, 2, 45.99), -- Order 4 bought TP-Link Cameras
(4, 22, 1, 80.00), -- Order 4 bought Raspberry Pi
(5, 4, 1, 44.99),  -- Order 5 bought 8BitDo Controller
(6, 18, 1, 65.00), -- Order 6 bought Malt
(6, 19, 3, 24.99), -- Order 6 bought Hops
(6, 20, 2, 9.50),  -- Order 6 bought Yeast
(7, 28, 1, 499.00),-- Order 7 bought Onkyo Receiver
(7, 27, 1, 349.00),-- Order 7 bought Subwoofer
(8, 17, 4, 35.00), -- Order 8 bought Nespresso Pods
(8, 21, 1, 22.00), -- Order 8 bought Pour-over Carafe
(9, 9, 1, 39.99),  -- Order 9 bought Satisfactory
(10, 14, 1, 15.50),-- Order 10 bought Smoker Box
(11, 3, 1, 55.00), -- Order 11 bought Pickleball Paddles
(12, 5, 1, 549.00),-- Order 12 bought Steam Deck
(13, 29, 1, 295.00),-- Order 13 bought DaVinci Resolve
(14, 24, 1, 59.99),-- Order 14 bought Coral TPU
(15, 13, 3, 19.99),-- Order 15 bought Apple Wood Pellets
(16, 10, 1, 59.99),-- Order 16 bought No Man's Sky
(17, 30, 1, 125.00),-- Order 17 bought Vintage Table
(18, 26, 1, 389.99),-- Order 18 bought Dreame Vacuum
(19, 23, 4, 45.99),-- Order 19 bought 4x TP-Link Cameras
(20, 11, 1, 24.99),-- Order 20 bought Hades
(20, 4, 1, 44.99); -- Order 20 bought 8BitDo Controller

-- Synchronize line_id to order_line_id
UPDATE order_lines SET line_id = order_line_id;

-- Recalculate exact total_amount on orders from line items
UPDATE orders o
SET total_amount = sub.sum_amt
FROM (
    SELECT order_id, ROUND(SUM(quantity * unit_price), 2) AS sum_amt
    FROM order_lines
    GROUP BY order_id
) sub
WHERE o.order_id = sub.order_id;

-- Insert Superstore Benchmark Data (60 diverse rows across regions & categories)
INSERT INTO superstore (
    order_id, order_date, customer_id, customer_name, segment, 
    city, state, region, category, sub_category, 
    product_name, sales, quantity, discount, profit
) VALUES
('CA-2012-124891', '2012-07-31', 'RH-19495', 'Rick Hansen', 'Consumer', 'New York City', 'New York', 'East', 'Technology', 'Accessories', 'Plantronics CS510 - Over-the-Head monaural Wireless Headset System', 2309.65, 7, 0.00, 762.18),
('IN-2013-77878', '2013-02-05', 'JR-16210', 'Justin Ritter', 'Corporate', 'Wollongong', 'New South Wales', 'Oceania', 'Furniture', 'Chairs', 'Novimex Executive Leather Armchair, Black', 3709.39, 9, 0.10, -288.76),
('IN-2013-71249', '2013-10-17', 'CR-12730', 'Craig Reiter', 'Consumer', 'Brisbane', 'Queensland', 'Oceania', 'Technology', 'Phones', 'Nokia Smart Phone, with Caller ID', 5175.17, 9, 0.10, 919.97),
('ES-2013-1579342', '2013-01-28', 'KM-16375', 'Katherine Murray', 'Home Office', 'Berlin', 'Berlin', 'Central', 'Technology', 'Phones', 'Motorola Smart Phone, Cordless', 2892.51, 5, 0.10, -96.54),
('SG-2013-4320', '2013-11-05', 'RH-9495', 'Rick Hansen', 'Consumer', 'Dakar', 'Dakar', 'Africa', 'Technology', 'Copiers', 'Sharp Wireless Fax, High-Speed', 2832.96, 8, 0.00, 311.52),
('IN-2013-42360', '2013-06-28', 'JM-15655', 'Jim Mitchum', 'Corporate', 'Sydney', 'New South Wales', 'Oceania', 'Technology', 'Phones', 'Samsung Smart Phone, with Caller ID', 2862.68, 5, 0.10, 763.27),
('IN-2011-81826', '2011-11-07', 'TS-21340', 'Toby Swindell', 'Consumer', 'Porirua', 'Wellington', 'Oceania', 'Furniture', 'Chairs', 'Novimex Executive Leather Armchair, Adjustable', 1822.08, 4, 0.00, 564.84),
('IN-2012-86369', '2012-04-14', 'MB-18085', 'Mick Brown', 'Consumer', 'Hamilton', 'Waikato', 'Oceania', 'Furniture', 'Tables', 'Chromcraft Conference Table, Fully Assembled', 5244.84, 6, 0.00, 996.48),
('CA-2014-135909', '2014-10-14', 'JW-15220', 'Jane Waco', 'Corporate', 'Sacramento', 'California', 'West', 'Office Supplies', 'Binders', 'Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind', 5083.96, 5, 0.20, 1906.48),
('CA-2012-116638', '2012-01-28', 'JH-15985', 'Joseph Holt', 'Consumer', 'Concord', 'North Carolina', 'South', 'Furniture', 'Tables', 'Chromcraft Bull-Nose Wood Oval Conference Tables & Bases', 4297.64, 13, 0.40, -1862.31),
('CA-2011-102988', '2011-04-05', 'GM-14695', 'Greg Maxwell', 'Corporate', 'Alexandria', 'Virginia', 'South', 'Office Supplies', 'Supplies', 'Martin Yale Chadless Opener Electric Letter Opener', 4164.05, 5, 0.00, 83.28),
('ID-2012-28402', '2012-04-19', 'AJ-10780', 'Anthony Jacobs', 'Corporate', 'Kabul', 'Kabul', 'Central Asia', 'Furniture', 'Tables', 'Bevis Conference Table, Fully Assembled', 4626.15, 5, 0.00, 647.55),
('SA-2011-1830', '2011-12-27', 'MM-7260', 'Magdelene Morse', 'Consumer', 'Jizan', 'Jizan', 'EMEA', 'Technology', 'Phones', 'Cisco Smart Phone, with Caller ID', 2616.96, 4, 0.00, 1151.40),
('MX-2012-130015', '2012-11-13', 'VF-21715', 'Vicky Freymann', 'Home Office', 'Toledo', 'Parana', 'South', 'Furniture', 'Chairs', 'Harbour Creations Executive Leather Armchair, Adjustable', 2221.80, 7, 0.00, 622.02),
('IN-2013-73951', '2013-06-06', 'PF-19120', 'Peter Fuller', 'Consumer', 'Mudanjiang', 'Heilongjiang', 'North Asia', 'Office Supplies', 'Appliances', 'KitchenAid Microwave, White', 3701.52, 12, 0.00, 1036.08),
('ES-2014-5099955', '2014-07-31', 'BP-11185', 'Ben Peterman', 'Corporate', 'Paris', 'Ile-de-France', 'Central', 'Office Supplies', 'Appliances', 'Breville Refrigerator, Red', 1869.59, 4, 0.10, 186.95),
('CA-2014-143567', '2014-11-03', 'TB-21175', 'Thomas Boland', 'Corporate', 'Henderson', 'Kentucky', 'South', 'Technology', 'Accessories', 'Logitech diNovo Edge Keyboard', 2249.91, 9, 0.00, 517.48),
('ES-2014-1651774', '2014-09-08', 'PJ-18835', 'Patrick Jones', 'Corporate', 'Prato', 'Tuscany', 'South', 'Office Supplies', 'Appliances', 'Hoover Stove, Red', 7958.58, 14, 0.00, 3979.08),
('IN-2014-11763', '2014-01-31', 'JS-15685', 'Jim Sink', 'Corporate', 'Townsville', 'Queensland', 'Oceania', 'Technology', 'Copiers', 'Brother Fax Machine, High-Speed', 2565.59, 9, 0.10, 28.40),
('TZ-2014-8190', '2014-12-05', 'RH-9555', 'Ritsa Hightower', 'Consumer', 'Uvinza', 'Kigoma', 'Africa', 'Office Supplies', 'Appliances', 'KitchenAid Stove, White', 3409.74, 6, 0.00, 818.28),
('PL-2012-7820', '2012-08-08', 'AB-600', 'Ann Blume', 'Corporate', 'Bytom', 'Silesia', 'EMEA', 'Furniture', 'Tables', 'Hon Computer Table, with Bottom Storage', 1977.72, 4, 0.00, 276.84),
('CA-2011-154627', '2011-10-29', 'SA-20830', 'Sue Ann Reed', 'Consumer', 'Chicago', 'Illinois', 'Central', 'Technology', 'Phones', 'Apple iPhone 5S', 2735.95, 6, 0.20, 341.99),
('IN-2011-44803', '2011-05-02', 'JK-15325', 'Jason Klamczynski', 'Corporate', 'Suzhou', 'Anhui', 'North Asia', 'Furniture', 'Chairs', 'SAFCO Executive Leather Armchair, Black', 2754.00, 6, 0.00, 358.02),
('ES-2013-2860574', '2013-02-27', 'LB-16795', 'Laurel Beltran', 'Home Office', 'Edinburgh', 'Scotland', 'North', 'Office Supplies', 'Appliances', 'KitchenAid Refrigerator, Black', 5273.70, 10, 0.00, 1898.40),
('US-2014-133193', '2014-07-31', 'NP-18325', 'Naresj Patel', 'Consumer', 'Juárez', 'Chihuahua', 'North', 'Technology', 'Phones', 'Motorola Smart Phone, Full Size', 1713.84, 4, 0.00, 445.52),
('MX-2014-165309', '2014-09-05', 'VD-21670', 'Valerie Dominguez', 'Consumer', 'Soyapango', 'San Salvador', 'Central', 'Furniture', 'Tables', 'Hon Computer Table, Fully Assembled', 2106.50, 8, 0.20, 526.50),
('IN-2011-10286', '2011-12-17', 'PB-19210', 'Phillip Breyer', 'Corporate', 'Taipei', 'Taipei City', 'North Asia', 'Furniture', 'Tables', 'Lesro Conference Table, with Bottom Storage', 1715.16, 2, 0.00, 720.36),
('ES-2011-4699764', '2011-03-14', 'EB-14110', 'Eugene Barchas', 'Consumer', 'Leipzig', 'Saxony', 'Central', 'Office Supplies', 'Appliances', 'Hoover Stove, Red', 3069.74, 6, 0.10, 1364.24),
('CA-2013-159016', '2013-03-11', 'KF-16285', 'Karen Ferguson', 'Home Office', 'Los Angeles', 'California', 'West', 'Technology', 'Phones', 'Apple iPhone 5', 4158.91, 8, 0.20, 363.90),
('IN-2012-44810', '2012-02-25', 'BP-11230', 'Benjamin Patterson', 'Consumer', 'Surat', 'Gujarat', 'Central Asia', 'Furniture', 'Chairs', 'Office Star Executive Leather Armchair, Red', 1878.72, 4, 0.00, 582.36),
('US-2011-128776', '2011-12-28', 'RR-19525', 'Rick Reed', 'Corporate', 'Santo Domingo', 'Santo Domingo', 'Caribbean', 'Technology', 'Phones', 'Samsung Smart Phone, VoIP', 1696.64, 5, 0.20, -148.46),
('ES-2012-5870268', '2012-07-17', 'BS-11365', 'Bill Shonely', 'Corporate', 'Saint-Brieuc', 'Brittany', 'Central', 'Technology', 'Machines', 'Okidata Inkjet, Wireless', 2402.86, 9, 0.15, 763.15),
('CA-2012-139731', '2012-10-15', 'JE-15745', 'Joel Eaton', 'Consumer', 'Amarillo', 'Texas', 'Central', 'Furniture', 'Chairs', 'HON 5400 Series Task Chairs for Big and Tall', 2453.43, 5, 0.30, -350.49),
('IN-2011-28087', '2011-11-03', 'DP-13105', 'Dave Poirier', 'Corporate', 'Gold Coast', 'Queensland', 'Oceania', 'Office Supplies', 'Appliances', 'Breville Stove, Red', 2526.93, 5, 0.10, 561.48),
('CA-2011-168494', '2011-12-12', 'NP-18700', 'Nora Preis', 'Consumer', 'Fresno', 'California', 'West', 'Furniture', 'Tables', 'Bretford Rectangular Conference Table Tops', 3610.85, 12, 0.20, 135.41),
('CG-2011-8610', '2011-09-14', 'AH-30', 'Aaron Hawkins', 'Corporate', 'Kamina', 'Katanga', 'Africa', 'Technology', 'Phones', 'Apple Smart Phone, Full Size', 3817.26, 6, 0.00, 1068.66),
('CA-2011-160766', '2011-09-14', 'DM-13015', 'Darrin Martin', 'Consumer', 'New York City', 'New York', 'East', 'Technology', 'Machines', 'Ativa V4110MDD Micro-Cut Shredder', 2799.96, 4, 0.00, 1371.98),
('US-2014-168116', '2014-11-05', 'GT-14635', 'Grant Thornton', 'Corporate', 'Burlington', 'North Carolina', 'South', 'Technology', 'Machines', 'Cubify CubeX 3D Printer Triple Head Print', 7999.98, 4, 0.50, -3839.99),
('ES-2014-2637201', '2014-01-14', 'PO-18865', 'Patrick O''Donnell', 'Consumer', 'Stockton-on-Tees', 'England', 'North', 'Technology', 'Copiers', 'Brother Fax Machine, Laser', 4141.02, 13, 0.00, 1697.67),
('IN-2011-61302', '2011-01-10', 'DL-12865', 'Dan Lawera', 'Consumer', 'Brisbane', 'Queensland', 'Oceania', 'Technology', 'Phones', 'Nokia Smart Phone, with Caller ID', 2875.09, 5, 0.10, 511.10),
('ID-2013-63976', '2013-08-22', 'JB-16000', 'Joy Bell-', 'Consumer', 'Mataram', 'Nusa Tenggara Barat', 'Southeast Asia', 'Technology', 'Phones', 'Motorola Smart Phone, Full Size', 3200.60, 6, 0.17, -77.20),
('IN-2014-37320', '2014-11-11', 'BF-11005', 'Barry Franz', 'Home Office', 'Gorakhpur', 'Haryana', 'Central Asia', 'Technology', 'Phones', 'Motorola Smart Phone, with Caller ID', 4518.78, 7, 0.00, 632.52),
('IN-2014-76016', '2014-09-26', 'VG-21805', 'Vivek Grady', 'Corporate', 'Thiruvananthapuram', 'Kerala', 'Central Asia', 'Furniture', 'Bookcases', 'Sauder Classic Bookcase, Traditional', 5667.87, 13, 0.00, 2097.03),
('ES-2012-5877219', '2012-12-13', 'GT-14710', 'Greg Tran', 'Consumer', 'Huddersfield', 'England', 'North', 'Technology', 'Phones', 'Motorola Smart Phone, Cordless', 5785.02, 9, 0.00, 404.73),
('IT-2011-3183678', '2011-09-23', 'ZC-21910', 'Zuschuss Carroll', 'Consumer', 'Berlin', 'Berlin', 'Central', 'Office Supplies', 'Appliances', 'Cuisinart Stove, Silver', 3018.62, 7, 0.20, 377.24),
('CA-2011-116904', '2011-09-23', 'SC-20095', 'Sanjit Chand', 'Consumer', 'Minneapolis', 'Minnesota', 'Central', 'Office Supplies', 'Binders', 'Ibico EPK-21 Electric Binding System', 9449.95, 5, 0.00, 4630.48),
('IT-2013-3085011', '2013-03-08', 'EB-13840', 'Ellis Ballard', 'Corporate', 'Montreuil', 'Ile-de-France', 'Central', 'Furniture', 'Chairs', 'Office Star Executive Leather Armchair, Adjustable', 2092.50, 5, 0.10, 720.75),
('IN-2014-50473', '2014-08-28', 'AP-10915', 'Arthur Prichep', 'Consumer', 'Shouguang', 'Shandong', 'North Asia', 'Furniture', 'Chairs', 'Novimex Executive Leather Armchair, Red', 2761.20, 6, 0.00, 110.34),
('IN-2014-35983', '2014-05-01', 'SW-20275', 'Scott Williamson', 'Consumer', 'Jamshedpur', 'Jharkhand', 'Central Asia', 'Technology', 'Machines', 'Konica Inkjet, White', 2174.13, 7, 0.00, 500.01),
('MX-2014-126984', '2014-12-18', 'JH-15820', 'John Huston', 'Consumer', 'Paysandú', 'Paysandú', 'South', 'Furniture', 'Chairs', 'Harbour Creations Executive Leather Armchair, Black', 3473.14, 11, 0.00, 868.12),
('US-2012-163825', '2012-06-16', 'LC-16885', 'Lena Creighton', 'Consumer', 'New York City', 'New York', 'East', 'Office Supplies', 'Binders', 'Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind', 3050.38, 3, 0.20, 1143.89),
('IR-2014-8540', '2014-09-18', 'TG-11640', 'Trudy Glocke', 'Consumer', 'Behshahr', 'Mazandaran', 'EMEA', 'Technology', 'Copiers', 'Canon Copy Machine, Color', 2108.64, 8, 0.00, 527.04),
('US-2014-135013', '2014-07-25', 'HR-14830', 'Harold Ryan', 'Corporate', 'Huntington Beach', 'California', 'West', 'Technology', 'Copiers', 'Hewlett Packard LaserJet 3310 Copier', 2399.96, 5, 0.20, 839.99),
('IN-2011-10286', '2011-12-17', 'PB-19210', 'Phillip Breyer', 'Corporate', 'Taipei', 'Taipei City', 'North Asia', 'Furniture', 'Bookcases', 'Safco Classic Bookcase, Pine', 2197.50, 5, 0.00, 153.75),
('MZ-2013-3690', '2013-12-18', 'DG-3300', 'Deirdre Greer', 'Corporate', 'Maputo', 'Cidade De Maputo', 'Africa', 'Technology', 'Phones', 'Motorola Smart Phone, with Caller ID', 2582.16, 4, 0.00, 593.88),
('IN-2012-66342', '2012-05-30', 'SG-20470', 'Sheri Gordon', 'Consumer', 'Bhopal', 'Madhya Pradesh', 'Central Asia', 'Technology', 'Copiers', 'Hewlett Wireless Fax, Color', 1526.52, 4, 0.00, 732.72),
('CA-2012-111829', '2012-03-19', 'FH-14365', 'Fred Hopkins', 'Corporate', 'Seattle', 'Washington', 'West', 'Technology', 'Copiers', 'Canon PC940 Copier', 3149.93, 7, 0.00, 1480.47),
('IN-2012-48240', '2012-05-25', 'GP-14740', 'Guy Phonely', 'Corporate', 'Delhi', 'Delhi', 'Central Asia', 'Furniture', 'Tables', 'Chromcraft Conference Table, with Bottom Storage', 1745.34, 2, 0.00, 226.86),
('IN-2014-61792', '2014-08-05', 'MW-18220', 'Mitch Webber', 'Consumer', 'Geraldton', 'Western Australia', 'Oceania', 'Office Supplies', 'Appliances', 'Breville Refrigerator, White', 4191.51, 9, 0.10, 1164.27),
('CA-2014-129021', '2014-08-24', 'PO-18850', 'Patrick O''Brill', 'Consumer', 'Tallahassee', 'Florida', 'South', 'Technology', 'Phones', 'Samsung Galaxy Mega 6.3', 4367.90, 13, 0.20, 327.59);

-- Print confirmation
SELECT 
    (SELECT COUNT(*) FROM locations) AS locations_count,
    (SELECT COUNT(*) FROM employees) AS employees_count,
    (SELECT COUNT(*) FROM products) AS products_count,
    (SELECT COUNT(*) FROM orders) AS orders_count,
    (SELECT COUNT(*) FROM order_lines) AS order_lines_count,
    (SELECT COUNT(*) FROM superstore) AS superstore_count;
