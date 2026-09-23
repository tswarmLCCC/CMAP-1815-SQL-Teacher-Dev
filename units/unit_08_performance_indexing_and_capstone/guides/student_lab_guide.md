# Unit 8 & Capstone Student Guide: Comprehensive Engineering & Performance Defense

## Capstone Overview
Congratulations on reaching the final milestone of CMAP 1815: Introduction to Modern SQL! In this Capstone Project, you synthesize every conceptual and technical pillar mastered throughout the semester:
1. Normalizing an enterprise domain model into Third Normal Form (3NF).
2. Implementing schema DDL with ironclad constraints (`PK`, `FK`, `CHECK`, `UNIQUE`, `NOT NULL`).
3. Safely ingesting and cleaning raw data using temporary staging tables and atomic transactions.
4. Generating executive analytical intelligence using chained Common Table Expressions (CTEs), window functions (`OVER`, `PARTITION BY`), and ranking.
5. Profiling query performance with `EXPLAIN ANALYZE`, engineering targeted B-Tree indexes, and defending against the Write Penalty.
6. Establishing an immutable compliance audit trail.

All work must be conducted in PostgreSQL 16.

---

## Deliverables & Submission Guidelines
1. Create a master SQL script named `capstone_submission.sql`.
2. Format all SQL keywords in UPPERCASE; all table and column names in snake_case.
3. Every section must include brief comment blocks explaining your architectural choices and performance findings.
4. Execute and verify your script in `psql`:
   ```bash
   psql -U postgres -d postgres -f capstone_submission.sql
   ```

---

## Capstone Project Tasks

### Part 1: Schema Architecture & Declarative Integrity (3NF)
Design and construct an enterprise logistics management schema consisting of three normalized entities:
1. `logistics_hubs`: `hub_id SERIAL PRIMARY KEY`, `hub_name VARCHAR(100) NOT NULL`, `region VARCHAR(50) NOT NULL`, `is_active BOOLEAN NOT NULL DEFAULT TRUE`.
2. `freight_shipments`: `shipment_id SERIAL PRIMARY KEY`, `hub_id INT NOT NULL REFERENCES logistics_hubs(hub_id) ON DELETE RESTRICT`, `tracking_code VARCHAR(50) NOT NULL UNIQUE`, `declared_value NUMERIC(10,2) NOT NULL CHECK (declared_value >= 0.00)`, `status VARCHAR(20) NOT NULL CHECK (status IN ('Pending', 'In Transit', 'Delivered', 'Cancelled'))`, `shipped_date DATE DEFAULT CURRENT_DATE`.
3. `shipment_audit_log`: `audit_id SERIAL PRIMARY KEY`, `shipment_id INT NOT NULL`, `old_status VARCHAR(20)`, `new_status VARCHAR(20)`, `modified_by VARCHAR(50) DEFAULT CURRENT_USER`, `modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`.

### Part 2: Safe Ingestion Pipeline via Temporary Staging Table
Simulate importing dirty vendor batch records:
1. Create a `CREATE TEMPORARY TABLE stage_vendor_freight` with string-based columns.
2. Ingest 3 raw rows containing unformatted tracking codes and dollar signs.
3. Write a cleaning transformation query that strips whitespace and currency symbols.
4. Promote the clean rows into `freight_shipments` inside an atomic transaction block (`BEGIN ... COMMIT`) using `RETURNING`.

### Part 3: Advanced Analytical Intelligence (CTEs & Windows)
The Chief Logistics Officer needs an analytical performance report:
1. Write a query utilizing a CTE named `regional_shipment_metrics`.
2. Calculate each hub's `total_shipments` and `total_declared_value`.
3. In the outer query, calculate:
   - `regional_rank`: Rank hubs within their region by `total_declared_value` descending using `DENSE_RANK()`.
   - `region_avg_value`: Regional average declared value using `AVG(...) OVER(PARTITION BY region)`.
   - `variance_from_reg_avg`: Hub's value minus `region_avg_value`.
4. Order by `region`, `regional_rank`.

### Part 4: Performance Profiling & B-Tree Index Engineering
Demonstrate your ability to profile and optimize database performance:
1. Write an `EXPLAIN ANALYZE` query searching for shipments in `freight_shipments` by `status` and `shipped_date`.
2. Inspect the scan type and latency.
3. Construct a targeted composite B-Tree index:
   ```sql
   CREATE INDEX idx_shipments_status_date ON freight_shipments(status, shipped_date);
   ```
4. Re-run `EXPLAIN ANALYZE` and document the performance improvement in a SQL comment block.
5. In a 2-sentence comment, explain the Write Penalty and identify when this index should be dropped.

### Part 5: Transactional Audit Event Capture
Execute a status update changing a shipment from `'In Transit'` to `'Delivered'`:
* Wrap the update and a companion insert into `shipment_audit_log` inside an atomic transaction (`BEGIN ... COMMIT`).
* Query `shipment_audit_log` to display the verified audit trail.
