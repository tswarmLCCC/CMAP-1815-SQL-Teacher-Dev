-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 7: Schema Design, DDL & Data Integrity
-- Script 2: DDL Architecture & Constraint Enforcement
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: Robust Table DDL with Explicit Constraints
-- Enforcing business validation rules at the storage engine layer.
-- ----------------------------------------------------------------------------

-- Clean up any prior test tables
DROP TABLE IF EXISTS demo_order_items CASCADE;
DROP TABLE IF EXISTS demo_orders CASCADE;
DROP TABLE IF EXISTS demo_accounts CASCADE;

-- 1.1 Account Table Definition
CREATE TABLE demo_accounts (
    account_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    account_type VARCHAR(20) NOT NULL DEFAULT 'Standard',
    balance NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Explicitly named constraints
    CONSTRAINT uq_demo_accounts_email 
        UNIQUE (email),
        
    CONSTRAINT chk_demo_accounts_type 
        CHECK (account_type IN ('Standard', 'Premium', 'Enterprise')),
        
    CONSTRAINT chk_demo_accounts_balance 
        CHECK (balance >= 0.00)
);

-- 1.2 Orders Table with Foreign Key Referential Action
CREATE TABLE demo_orders (
    order_id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    order_status VARCHAR(20) NOT NULL DEFAULT 'Submitted',
    
    CONSTRAINT fk_demo_orders_account
        FOREIGN KEY (account_id) 
        REFERENCES demo_accounts(account_id)
        ON DELETE RESTRICT, -- Rejects account deletion if orders exist!
        
    CONSTRAINT chk_demo_orders_status
        CHECK (order_status IN ('Submitted', 'Paid', 'Shipped', 'Completed', 'Cancelled'))
);

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Testing Constraint Rejections (Defense in Action)
-- ----------------------------------------------------------------------------

-- Insert valid account
INSERT INTO demo_accounts (email, account_type, balance)
VALUES ('security_lead@corporate.com', 'Enterprise', 5000.00);

-- TEST 1: Unique constraint violation (Uncomment to inspect error)
-- INSERT INTO demo_accounts (email, account_type, balance)
-- VALUES ('security_lead@corporate.com', 'Standard', 100.00);
-- ERROR: duplicate key value violates unique constraint "uq_demo_accounts_email"

-- TEST 2: Check constraint violation (Negative balance)
-- INSERT INTO demo_accounts (email, account_type, balance)
-- VALUES ('test@corporate.com', 'Standard', -50.00);
-- ERROR: new row for relation "demo_accounts" violates check constraint "chk_demo_accounts_balance"

-- TEST 3: Referential Action test
INSERT INTO demo_orders (account_id, order_status) VALUES (1, 'Submitted');

-- Attempting to delete account 1 will be blocked because orders exist!
-- DELETE FROM demo_accounts WHERE account_id = 1;
-- ERROR: update or delete on table "demo_accounts" violates foreign key constraint "fk_demo_orders_account" on table "demo_orders"
