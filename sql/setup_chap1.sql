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
    unit_price DECIMAL(10, 2) NOT NULL 
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
('Phoenix', 'AZ', 'Retail Store'),
('Austin', 'TX', 'Engineering Hub'),
('Seattle', 'WA', 'Cloud Architecture'),
('Portland', 'OR', 'Retail Store'),
('Boston', 'MA', 'Research & Development'),
('Atlanta', 'GA', 'Distribution Center'),
('Dallas', 'TX', 'Regional Office');

-- Insert Employees
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
('Lando', 'Pyrenees', 'Security', 'Guard Dog', '2021-03-01', 30000.00, 100.00, 1, TRUE),
('Bonitto', 'Pyrenees', 'Security', 'Trainee', '2025-11-10', 20000.00, 50.00, 1, TRUE),
('Casper', 'Cat', 'Operations', 'Pest Control Lead', '2020-07-15', 25000.00, NULL, 1, TRUE),
('Cheddar', 'Cat', 'Operations', 'Pest Control Associate', '2022-04-10', 22000.00, NULL, 1, TRUE),
('Nathan', 'MacKinnon', 'Sales', 'Top Performer', '2013-09-01', 150000.00, 25000.00, 3, TRUE),
('Cale', 'Makar', 'Engineering', 'Defense Architect', '2019-10-01', 145000.00, 20000.00, 3, TRUE),
('Jane', 'Shepard', 'Management', 'Commander', '2007-11-20', 160000.00, 30000.00, 9, TRUE),
('Garrus', 'Vakarian', 'Engineering', 'Calibrations Expert', '2008-01-15', 95000.00, 5000.00, 9, TRUE),
('Liara', 'T''Soni', 'Research', 'Information Broker', '2008-03-22', 125000.00, NULL, 10, TRUE),
('Tali', 'Zorah', 'Engineering', 'Systems Technician', '2010-01-26', 88000.00, 3500.00, 9, TRUE),
('Wrex', 'Urdnot', 'Security', 'Tactical Consultant', '2007-12-01', 110000.00, 1500.00, 9, FALSE),
('Arthur', 'Morgan', 'Operations', 'Logistics Lead', '2018-10-26', 65000.00, 2500.00, 14, TRUE),
('John', 'Marston', 'Operations', 'Logistics Associate', '2019-02-15', 55000.00, 1000.00, 14, TRUE),
('Sadie', 'Adler', 'Security', 'Bounty Hunter', '2019-05-10', 85000.00, 12000.00, 14, TRUE),
('Miles', 'Morales', 'Engineering', 'Intern', '2023-10-20', 45000.00, NULL, 12, TRUE),
('Peter', 'Parker', 'Research', 'Materials Scientist', '2018-09-07', 98000.00, 4000.00, 12, TRUE),
('Aloy', 'Sobeck', 'Engineering', 'Machine Learning Specialist', '2017-02-28', 135000.00, 15000.00, 11, TRUE),
('Sylens', 'Wanderer', 'Research', 'Data Archaeologist', '2018-01-15', 140000.00, NULL, 11, FALSE),
('Ellie', 'Williams', 'Security', 'Survival Expert', '2013-06-14', 72000.00, 2000.00, 10, TRUE),
('Joel', 'Miller', 'Operations', 'Transport Specialist', '2013-06-14', 68000.00, NULL, 10, FALSE),
('Abby', 'Anderson', 'Fitness', 'Strength Coach', '2020-06-19', 75000.00, 5000.00, 10, TRUE);

-- Insert Products
INSERT INTO products (sku, product_name, category, cost_to_produce, retail_price, stock_quantity, description, release_date, discontinued_date) VALUES
('FIT-001', 'Saris Fluid2 Indoor Bike Trainer', 'Fitness', 150.00, 299.99, 15, 'Quiet and consistent resistance for indoor cycling. Compatible with Zwift and MyWhoosh.', '2021-01-15', NULL),
('FIT-002', 'Magene Bluetooth Speed & Cadence Sensor', 'Fitness', 12.00, 24.50, 42, 'Dual protocol ANT+/Bluetooth tracking for cycling.', '2022-03-10', NULL),
('FIT-003', 'Carbon Fiber Pickleball Paddle Set', 'Fitness', 22.00, 55.00, 40, 'Two lightweight paddles with edge guard and four indoor balls.', '2023-05-20', NULL),
('FIT-004', 'Adjustable Dumbbell Set 50lbs', 'Fitness', 85.00, 199.99, 25, 'Space-saving adjustable weights with quick-select dials.', '2020-11-15', NULL),
('FIT-005', 'Yoga Mat High Density', 'Fitness', 8.00, 29.99, 150, 'Non-slip exercise mat with carrying strap.', '2019-04-10', NULL),
('GAM-001', '8BitDo SN30 Pro Bluetooth Controller', 'Gaming', 18.50, 44.99, 28, 'Retro style controller with modern joysticks and rumble.', '2019-11-05', NULL),
('GAM-002', 'Steam Deck OLED 512GB', 'Gaming', 450.00, 549.00, 8, 'Handheld PC gaming console.', '2023-11-16', NULL),
('GAM-003', 'Baldur''s Gate 3 PC Key', 'Software', 0.00, 59.99, 999, 'Digital download key. Game of the Year 2023.', '2023-08-03', NULL),
('GAM-004', 'Xenonauts 2 Tactical Guide', 'Books', 4.50, 19.99, 5, 'Comprehensive tactics for planetary defense.', '2023-07-18', '2025-01-15'),
('GAM-005', 'Satisfactory Early Access Key', 'Software', 0.00, 29.99, 0, 'Factory building and automation on an alien planet.', '2020-06-08', '2024-09-09'),
('GAM-006', 'Satisfactory 1.0 Release Key', 'Software', 0.00, 39.99, 999, 'Fully optimized factory building experience.', '2024-09-10', NULL),
('GAM-007', 'No Man''s Sky PC Key', 'Software', 0.00, 59.99, 999, 'Procedural universe exploration and survival.', '2016-08-12', NULL),
('GAM-008', 'Hades PC Key', 'Software', 0.00, 24.99, 999, 'Rogue-like dungeon crawler.', '2020-09-17', NULL),
('GAM-009', 'Hollow Knight PC Key', 'Software', 0.00, 14.99, 999, 'Atmospheric metroidvania action adventure.', '2017-02-24', NULL),
('GAM-010', 'Nintendo Switch Pro Controller', 'Gaming', 25.00, 69.99, 45, 'Official wireless controller for Nintendo Switch.', '2017-03-03', NULL),
('OUT-001', 'Hickory Wood Pellets 20lb', 'Outdoor', 6.00, 18.99, 110, 'Premium hardwood pellets for deep smoke flavor on pellet grills.', '2020-04-01', NULL),
('OUT-002', 'Apple Wood Pellets 20lb', 'Outdoor', 6.50, 19.99, 45, 'Sweet smoke flavor, ideal for pork and poultry.', '2020-04-01', NULL),
('OUT-003', 'Cast Iron Smoker Box', 'Outdoor', 5.00, 15.50, 20, 'Heavy duty box for wood chips on gas or charcoal grills.', '2018-06-15', NULL),
('OUT-004', 'Digital Meat Thermometer Bluetooth', 'Outdoor', 14.00, 39.99, 0, 'Six probe thermometer with mobile app integration.', '2022-05-10', NULL),
('OUT-005', 'Prime Rib Rub 16oz', 'Groceries', 4.00, 12.99, 65, 'Coarse salt, black pepper, garlic, and rosemary blend.', '2021-11-01', NULL),
('OUT-006', 'Traeger Pro 575 Pellet Grill', 'Outdoor', 350.00, 799.99, 5, 'WiFIRE enabled wood pellet grill.', '2019-03-15', NULL),
('GRO-001', 'Nespresso Vertuo Espresso Pods - Diavolitto', 'Groceries', 15.00, 35.00, 85, 'Highly intense dark roast espresso capsules, 50 count.', '2021-08-20', NULL),
('GRO-002', 'Simpsons Golden Promise Malt 50lb', 'Groceries', 35.00, 65.00, 12, 'Base malt for homebrewing traditional ales.', '2019-02-15', NULL),
('GRO-003', 'Citra Hops 1lb Pellet', 'Groceries', 12.00, 24.99, 30, 'High alpha acid hops with strong citrus and tropical fruit notes.', '2023-10-05', NULL),
('GRO-004', 'Lalvin EC-1118 Yeast 10-pack', 'Groceries', 3.00, 9.50, 120, 'Champagne yeast ideal for hard ciders and fruit wines.', '2020-11-22', NULL),
('GRO-005', 'Pour-over Glass Carafe 400ml', 'Kitchen', 8.50, 22.00, 34, 'Borosilicate glass with stainless steel filter.', '2022-01-15', NULL),
('GRO-006', 'Whole Bean Coffee Dark Roast 2lb', 'Groceries', 12.00, 28.50, 40, 'Locally roasted organic dark beans.', '2023-11-01', NULL),
('SMRT-001', 'Zooz 800 Series Z-Wave Plus Smart Switch', 'Home Automation', 14.00, 32.95, 60, 'Dimmer switch for smart home hubs. Scene control enabled.', '2023-01-10', NULL),
('SMRT-002', 'Raspberry Pi 5 8GB', 'Electronics', 65.00, 80.00, 0, 'SBC for local servers, Docker containers, and Home Assistant.', '2023-10-23', NULL),
('SMRT-003', 'TP-Link Tapo 2K Pan/Tilt Security Camera', 'Home Automation', 22.00, 45.99, 115, 'Indoor camera with RTSP support for Frigate NVR integration.', '2022-09-14', NULL),
('SMRT-004', 'Coral Edge TPU USB Accelerator', 'Electronics', 40.00, 59.99, 3, 'Machine learning coprocessor for fast object detection.', '2019-03-04', NULL),
('SMRT-005', 'Dreame L10 Pro Robot Vacuum', 'Home Automation', 200.00, 389.99, 12, 'LiDAR navigation with local control options.', '2021-05-08', NULL),
('SMRT-006', 'Aqara Door and Window Sensor', 'Home Automation', 6.00, 17.99, 85, 'Zigbee contact sensor for security automation.', '2020-08-20', NULL),
('AUD-001', 'Klipsch Reference 10" Subwoofer', 'Audio', 160.00, 349.00, 8, 'Front-firing spun-copper woofer for home theater setups.', '2018-08-15', NULL),
('AUD-002', 'Onkyo TX-NR6050 7.2 Channel Receiver', 'Audio', 250.00, 499.00, 4, '8K video, Dolby Atmos, and network streaming.', '2021-11-01', NULL),
('AUD-003', 'Sony WH-1000XM5 Headphones', 'Audio', 180.00, 398.00, 22, 'Wireless noise-canceling over-ear headphones.', '2022-05-20', NULL),
('SFT-001', 'DaVinci Resolve Studio License Key', 'Software', 0.00, 295.00, 99, 'Professional video editing, color grading, and AI transcription.', '2022-04-18', NULL),
('SFT-002', 'Docker Pro Annual Subscription', 'Software', 0.00, 60.00, 999, 'Containerization software license for professional developers.', '2021-01-01', NULL),
('FUR-001', 'Vintage Oak End Table', 'Furniture', 45.00, 125.00, 2, 'Restored solid oak with original brass hardware. Auction acquisition.', '2024-03-12', NULL),
('FUR-002', 'Herman Miller Aeron Chair', 'Furniture', 450.00, 1200.00, 6, 'Ergonomic office chair with lumbar support.', '2015-06-01', NULL);

-- Insert Orders (Expanded dataset for better grouping exercises)
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
(24, '2024-12-12', 'Completed', 'Express'),
(28, '2024-12-15', 'Completed', 'Overnight'),
(30, '2024-12-18', 'Completed', 'Standard'),
(35, '2025-01-05', 'Processing', 'Express'),
(38, '2025-01-10', 'Completed', 'Standard'),
(40, '2025-01-12', 'Shipped', 'Standard');

-- Insert Order Lines
INSERT INTO order_lines (order_id, product_id, quantity, unit_price) VALUES
(1, 16, 2, 18.99), 
(1, 20, 1, 12.99), 
(2, 8, 1, 59.99),  
(3, 2, 1, 24.50),  
(3, 1, 1, 299.99), 
(4, 30, 2, 45.99), 
(4, 29, 1, 80.00), 
(5, 6, 1, 44.99),  
(6, 23, 1, 65.00), 
(6, 24, 3, 24.99), 
(6, 25, 2, 9.50),  
(7, 35, 1, 499.00),
(7, 34, 1, 349.00),
(8, 22, 4, 35.00), 
(8, 26, 1, 22.00), 
(9, 11, 1, 39.99), 
(10, 18, 1, 15.50),
(11, 3, 1, 55.00), 
(12, 7, 1, 549.00),
(13, 37, 1, 295.00),
(14, 31, 1, 59.99),
(15, 17, 3, 19.99),
(16, 12, 1, 59.99),
(17, 39, 1, 125.00),
(18, 32, 1, 389.99),
(19, 30, 4, 45.99),
(20, 13, 1, 24.99),
(20, 6, 1, 44.99), 
(21, 36, 1, 398.00),
(22, 15, 1, 69.99),
(23, 21, 1, 799.99),
(24, 38, 5, 60.00),
(25, 4, 1, 199.99);