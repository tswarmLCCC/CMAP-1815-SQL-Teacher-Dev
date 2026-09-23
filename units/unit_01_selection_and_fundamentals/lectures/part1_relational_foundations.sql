/*
====================================================================
CMAP 1815 - Unit 1: Lecture Walkthrough Part 1
Topic: Relational Foundations & Environment Inspection
Video Duration: ~7 minutes
====================================================================
*/

-- 1. Inspecting the Database Server Version
-- Confirms we are connected to a live PostgreSQL 16 server
SELECT version();

-- 2. Inspecting the Active Session
-- Proves client-server connection: shows who you are and where you are connected
SELECT current_user, current_database();

-- 3. Discovering the Tables in our Database
-- Instead of clicking through a GUI, query PostgreSQL's metadata catalog
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- 4. Inspecting the Structure of a Table
-- Let's inspect the "employees" filing cabinet to see its column drawers
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'employees'
ORDER BY ordinal_position;
