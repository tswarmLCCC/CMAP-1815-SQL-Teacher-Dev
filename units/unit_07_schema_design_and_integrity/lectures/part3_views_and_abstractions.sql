-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 7: Schema Design, DDL & Data Integrity
-- Script 3: Views, Virtual Tables & Security Abstraction
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Basic View Creation & Encapsulation
-- Encapsulating multi-table joins into a reusable virtual table.
-- ----------------------------------------------------------------------------

CREATE OR REPLACE VIEW v_customer_order_summary AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    COUNT(o.order_id) AS total_orders_placed,
    COALESCE(SUM(o.total_amount), 0.00) AS total_spent,
    MAX(o.order_date) AS most_recent_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email;

-- Querying the view just like a regular table:
SELECT customer_name, total_orders_placed, total_spent
FROM v_customer_order_summary
WHERE total_spent > 250.00
ORDER BY total_spent DESC;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Security Abstraction & Column Masking
-- Shielding confidential columns (e.g. salary, personal identifiers) from users.
-- ----------------------------------------------------------------------------

-- Publicly accessible directory view: omits salary, birth date, and SSN
CREATE OR REPLACE VIEW v_public_employee_directory AS
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.department,
    e.job_title,
    l.city,
    l.state
FROM employees e
LEFT JOIN locations l ON e.location_id = l.location_id
WHERE e.is_active = TRUE;

-- Verifying the view projection:
SELECT * FROM v_public_employee_directory LIMIT 5;

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Checking View Metadata in PostgreSQL
-- ----------------------------------------------------------------------------

-- In psql, use \dv to list views, or query the information schema:
SELECT table_name, view_definition
FROM information_schema.views
WHERE table_schema = 'public';
