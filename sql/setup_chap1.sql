-- Drop tables in reverse order of dependencies
DROP TABLE IF EXISTS order_lines;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS locations;

-- 1. Create Locations
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    facility_type VARCHAR(50)
);

-- 2. Create Employees
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

-- 3. Create Products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    cost_to_produce DECIMAL(10, 2),
    retail_price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    description TEXT,
    release_date DATE,
    discontinued_date DATE
);

-- 4. Create Orders (Header)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(employee_id),
    order_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Completed',
    shipping_method VARCHAR(50)
);

-- 5. Create Order Lines (Details)
CREATE TABLE order_lines (
    order_line_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL -- Historical price at time of order
);

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

-- Insert Employees (Expanded)
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

-- Insert Products (Expanded)
INSERT INTO products (sku, product_name, category, cost_to_produce, retail_price, stock_quantity, description, release_date, discontinued_date) VALUES
('FIT-001', 'Saris Fluid2 Indoor Bike Trainer', 'Fitness', 150.00, 299.99, 15, 'Quiet and consistent resistance for indoor cycling. Compatible with Zwift and MyWhoosh.', '2021-01-15', NULL),
('FIT-002', 'Magene Bluetooth Speed & Cadence Sensor', 'Fitness', 12.00, 24.50, 42, 'Dual protocol ANT+/Bluetooth tracking for cycling.', '2022-03-10', NULL),
('FIT-003', 'Carbon Fiber Pickleball Paddle Set', 'Fitness', 22.00, 55.00, 40, 'Two lightweight paddles with edge guard and four indoor balls.', '2023-05-20', NULL),
('GAM-001', '8BitDo SN30 Pro Bluetooth Controller', 'Gaming', 18.50, 44.99, 28, 'Retro style controller with modern joysticks and rumble.', '2019-11-05', NULL),
('GAM-002', 'Steam Deck OLED 512GB', 'Gaming', 450.00, 549.00, 8, 'Handheld PC gaming console.', '2023-11-16', NULL),
('GAM-003', 'Baldur''s Gate 3 PC Key', 'Software', 0.00, 59.99, 999, 'Digital download key. Game of the Year 2023.', '2023-08-03', NULL),
('GAM-004', 'Xenonauts 2 Tactical Guide', 'Books', 4.50, 19.99, 5, 'Comprehensive tactics for planetary defense.', '2023-07-18', '2025-01-15'),
('GAM-005', 'Satisfactory Early Access Key', 'Software', 0.00, 29.99, 0, 'Factory building and automation on an alien planet.', '2020-06-08', '2024-09-09'),
('GAM-006', 'Satisfactory 1.0 Release Key', 'Software', 0.00, 39.99, 999, 'Fully optimized factory building experience.', '2024-09-10', NULL),
('GAM-007', 'No Man''s Sky PC Key', 'Software', 0.00, 59.99, 999, 'Procedural universe exploration and survival.', '2016-08-12', NULL),
('GAM-008', 'Hades PC Key', 'Software', 0.00, 24.99, 999, 'Rogue-like dungeon crawler.', '2020-09-17', NULL),
('OUT-001', 'Hickory Wood Pellets 20lb', 'Outdoor', 6.00, 18.99, 110, 'Premium hardwood pellets for deep smoke flavor on pellet grills.', '2020-04-01', NULL),
('OUT-002', 'Apple Wood Pellets 20lb', 'Outdoor', 6.50, 19.99, 45, 'Sweet smoke flavor, ideal for pork and poultry.', '2020-04-01', NULL),
('OUT-003', 'Cast Iron Smoker Box', 'Outdoor', 5.00, 15.50, 20, 'Heavy duty box for wood chips on gas or charcoal grills.', '2018-06-15', NULL),
('OUT-004', 'Digital Meat Thermometer Bluetooth', 'Outdoor', 14.00, 39.99, 0, 'Six probe thermometer with mobile app integration.', '2022-05-10', NULL),
('OUT-005', 'Prime Rib Rub 16oz', 'Groceries', 4.00, 12.99, 65, 'Coarse salt, black pepper, garlic, and rosemary blend.', '2021-11-01', NULL),
('GRO-001', 'Nespresso Vertuo Espresso Pods - Diavolitto', 'Groceries', 15.00, 35.00, 85, 'Highly intense dark roast espresso capsules, 50 count.', '2021-08-20', NULL),
('GRO-002', 'Simpsons Golden Promise Malt 50lb', 'Groceries', 35.00, 65.00, 12, 'Base malt for homebrewing traditional ales.', '2019-02-15', NULL),
('GRO-003', 'Citra Hops 1lb Pellet', 'Groceries', 12.00, 24.99, 30, 'High alpha acid hops with strong citrus and tropical fruit notes.', '2023-10-05', NULL),
('GRO-004', 'Lalvin EC-1118 Yeast 10-pack', 'Groceries', 3.00, 9.50, 120, 'Champagne yeast ideal for hard ciders and fruit wines.', '2020-11-22', NULL),
('GRO-005', 'Pour-over Glass Carafe 400ml', 'Kitchen', 8.50, 22.00, 34, 'Borosilicate glass with stainless steel filter.', '2022-01-15', NULL),
('SMRT-001', 'Zooz 800 Series Z-Wave Plus Smart Switch', 'Home Automation', 14.00, 32.95, 60, 'Dimmer switch for smart home hubs. Scene control enabled.', '2023-01-10', NULL),
('SMRT-002', 'Raspberry Pi 5 8GB', 'Electronics', 65.00, 80.00, 0, 'SBC for local servers, Docker containers, and Home Assistant.', '2023-10-23', NULL),
('SMRT-003', 'TP-Link Tapo 2K Pan/Tilt Security Camera', 'Home Automation', 22.00, 45.99, 115, 'Indoor camera with RTSP support for Frigate NVR integration.', '2022-09-14', NULL),
('SMRT-004', 'Coral Edge TPU USB Accelerator', 'Electronics', 40.00, 59.99, 3, 'Machine learning coprocessor for fast object detection.', '2019-03-04', NULL),
('SMRT-005', 'Dreame L10 Pro Robot Vacuum', 'Home Automation', 200.00, 389.99, 12, 'LiDAR navigation with local control options.', '2021-05-08', NULL),
('AUD-001', 'Klipsch Reference 10" Subwoofer', 'Audio', 160.00, 349.00, 8, 'Front-firing spun-copper woofer for home theater setups.', '2018-08-15', NULL),
('AUD-002', 'Onkyo TX-NR6050 7.2 Channel Receiver', 'Audio', 250.00, 499.00, 4, '8K video, Dolby Atmos, and network streaming.', '2021-11-01', NULL),
('SFT-001', 'DaVinci Resolve Studio License Key', 'Software', 0.00, 295.00, 99, 'Professional video editing, color grading, and AI transcription.', '2022-04-18', NULL),
('FUR-001', 'Vintage Oak End Table', 'Furniture', 45.00, 125.00, 2, 'Restored solid oak with original brass hardware. Auction acquisition.', '2024-03-12', NULL);

-- Insert Orders
INSERT INTO orders (employee_id, order_date, status, shipping_method) VALUES
(1, '2024-01-15', 'Completed', 'Standard'),
(5, '2024-02-10', 'Completed', 'Express'),
(10, '2024-03-05', 'Completed', 'Overnight'),
(12, '2024-03-12', 'Completed', 'Standard'),
(2, '2024-04-01', 'Completed', 'Standard'),
(8, '2024-04-18', 'Completed', 'Express'),
(21, '2024-05-22', 'Completed', 'Standard'),
(17, '2024-06-14', 'Completed', 'Standard'),
(9, '2024-07-02', 'Completed', 'Express'),
(3, '2024-07-25', 'Completed', 'Standard'),
(4, '2024-08-10', 'Completed', 'Standard'),
(11, '2024-09-05', 'Processing', 'Overnight'),
(22, '2024-09-12', 'Completed', 'Express'),
(6, '2024-09-28', 'Completed', 'Standard'),
(18, '2024-10-01', 'Shipped', 'Standard'),
(7, '2024-10-15', 'Pending', 'Express'),
(14, '2024-11-02', 'Completed', 'Standard'),
(29, '2024-11-18', 'Completed', 'Overnight'),
(23, '2024-12-05', 'Processing', 'Standard'),
(24, '2024-12-12', 'Completed', 'Express');

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