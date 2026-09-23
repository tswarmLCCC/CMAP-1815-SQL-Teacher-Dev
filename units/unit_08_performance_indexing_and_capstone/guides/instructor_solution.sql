-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 8 & Capstone Defense: Master Instructor Solution
-- ============================================================================

-- Clean environment
DROP TABLE IF EXISTS shipment_audit_log CASCADE;
DROP TABLE IF EXISTS freight_shipments CASCADE;
DROP TABLE IF EXISTS logistics_hubs CASCADE;

-- ----------------------------------------------------------------------------
-- PART 1: Schema Architecture & Declarative Integrity (3NF)
-- ----------------------------------------------------------------------------

-- Entity 1: Logistics Hubs
CREATE TABLE logistics_hubs (
    hub_id SERIAL PRIMARY KEY,
    hub_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Entity 2: Freight Shipments
CREATE TABLE freight_shipments (
    shipment_id SERIAL PRIMARY KEY,
    hub_id INT NOT NULL,
    tracking_code VARCHAR(50) NOT NULL,
    declared_value NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    shipped_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    CONSTRAINT fk_shipments_hub
        FOREIGN KEY (hub_id) 
        REFERENCES logistics_hubs(hub_id)
        ON DELETE RESTRICT,
        
    CONSTRAINT uq_shipments_tracking 
        UNIQUE (tracking_code),
        
    CONSTRAINT chk_shipments_value 
        CHECK (declared_value >= 0.00),
        
    CONSTRAINT chk_shipments_status 
        CHECK (status IN ('Pending', 'In Transit', 'Delivered', 'Cancelled'))
);

-- Entity 3: Shipment Audit Log
CREATE TABLE shipment_audit_log (
    audit_id SERIAL PRIMARY KEY,
    shipment_id INT NOT NULL,
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    modified_by VARCHAR(50) NOT NULL DEFAULT CURRENT_USER,
    modified_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Seed Initial Hubs
INSERT INTO logistics_hubs (hub_name, region)
VALUES 
    ('Cheyenne Central Gateway', 'Mountain West'),
    ('Denver Cargo Facility', 'Mountain West'),
    ('Salt Lake Logistics Center', 'Mountain West'),
    ('Seattle Marine Freight', 'Pacific Northwest'),
    ('Portland Distribution Hub', 'Pacific Northwest');

-- ----------------------------------------------------------------------------
-- PART 2: Safe Ingestion Pipeline via Temporary Staging Table
-- ----------------------------------------------------------------------------

CREATE TEMPORARY TABLE stage_vendor_freight (
    raw_hub_id VARCHAR(20),
    raw_tracking VARCHAR(50),
    raw_value VARCHAR(50),
    raw_status VARCHAR(50)
);

INSERT INTO stage_vendor_freight (raw_hub_id, raw_tracking, raw_value, raw_status)
VALUES 
    ('1', '  TRK-9001  ', ' $1250.50 ', 'In Transit'),
    ('2', 'TRK-9002', '$450.00', 'In Transit'),
    ('1', 'TRK-9003', '$3200.00', 'In Transit'),
    ('4', 'TRK-9004', ' $850.75 ', 'In Transit');

-- Promote clean staging rows to production inside an atomic transaction
BEGIN;

INSERT INTO freight_shipments (hub_id, tracking_code, declared_value, status)
SELECT 
    CAST(TRIM(raw_hub_id) AS INT),
    TRIM(raw_tracking),
    CAST(REPLACE(TRIM(raw_value), '$', '') AS NUMERIC(10,2)),
    TRIM(raw_status)
FROM stage_vendor_freight
RETURNING shipment_id, tracking_code, declared_value, status;

COMMIT;

-- ----------------------------------------------------------------------------
-- PART 3: Advanced Analytical Intelligence (CTEs & Windows)
-- ----------------------------------------------------------------------------

WITH regional_shipment_metrics AS (
    SELECT 
        h.region,
        h.hub_name,
        COUNT(s.shipment_id) AS total_shipments,
        ROUND(COALESCE(SUM(s.declared_value), 0.00), 2) AS total_declared_value
    FROM logistics_hubs h
    LEFT JOIN freight_shipments s ON h.hub_id = s.hub_id
    GROUP BY h.region, h.hub_name
)
SELECT 
    region,
    hub_name,
    total_shipments,
    total_declared_value,
    DENSE_RANK() OVER(
        PARTITION BY region 
        ORDER BY total_declared_value DESC
    ) AS regional_rank,
    ROUND(AVG(total_declared_value) OVER(
        PARTITION BY region
    ), 2) AS region_avg_value,
    ROUND(total_declared_value - AVG(total_declared_value) OVER(
        PARTITION BY region
    ), 2) AS variance_from_reg_avg
FROM regional_shipment_metrics
ORDER BY region, regional_rank;

-- ----------------------------------------------------------------------------
-- PART 4: Performance Profiling & B-Tree Index Engineering
-- ----------------------------------------------------------------------------

-- Baseline profile before composite index
EXPLAIN ANALYZE
SELECT shipment_id, tracking_code, declared_value
FROM freight_shipments
WHERE status = 'In Transit' AND shipped_date >= CURRENT_DATE;

-- Engineer composite B-Tree index
CREATE INDEX IF NOT EXISTS idx_shipments_status_date 
ON freight_shipments(status, shipped_date);

-- Optimized profile after index creation
EXPLAIN ANALYZE
SELECT shipment_id, tracking_code, declared_value
FROM freight_shipments
WHERE status = 'In Transit' AND shipped_date >= CURRENT_DATE;

-- Write Penalty Architecture Note:
-- The composite index speeds up dispatch and tracking queries. However,
-- every incoming shipment insertion must update idx_shipments_status_date.
-- If the application shifts to an archive-only cold store, or if batch inserts
-- exceed 10,000 records/sec, drop the index during bulk loading and rebuild it afterwards.

-- ----------------------------------------------------------------------------
-- PART 5: Transactional Audit Event Capture
-- ----------------------------------------------------------------------------

BEGIN;

-- Step 1: Update production shipment state
UPDATE freight_shipments
SET status = 'Delivered'
WHERE tracking_code = 'TRK-9001'
RETURNING shipment_id, tracking_code, status;

-- Step 2: Record immutable audit trail event
INSERT INTO shipment_audit_log (shipment_id, old_status, new_status)
VALUES (1, 'In Transit', 'Delivered');

COMMIT;

-- Verify Audit Trail
SELECT 
    a.audit_id,
    s.tracking_code,
    a.old_status,
    a.new_status,
    a.modified_by,
    a.modified_at
FROM shipment_audit_log a
JOIN freight_shipments s ON a.shipment_id = s.shipment_id;
