/*
====================================================================
Module 1 Lab: PostgreSQL Environment and Orientation
====================================================================

Objective:
Familiarize yourself with the PostgreSQL database environment. 
Use system functions and the information schema to discover database 
metadata, user information, and table structures programmatically.

Instructions:
Execute the queries below in your SQL client. Submit the final SQL 
syntax for each challenge. Note: These rely on standard PostgreSQL 
system catalogs and functions rather than psql-specific meta-commands 
(like \d or \dt) so they will run in any GUI tool.
*/

/*
--------------------------------------------------------------------
Part 1: System and Session Information
--------------------------------------------------------------------
*/

-- 1. Verify the exact version of PostgreSQL running on the server.
SELECT version();

-- 2. Identify your current database user and the database you are connected to.
SELECT current_user, current_database();

-- 3. Check the current schema search path for your session.
SHOW search_path;
-- Alternatively: SELECT current_schema();

-- 4. Display the server's current timestamp and time zone setting.
SELECT current_timestamp, current_setting('TIMEZONE');

-- 5. Find out when the PostgreSQL server was last started.
SELECT pg_postmaster_start_time();


/*
--------------------------------------------------------------------
Part 2: Exploring the Information Schema
--------------------------------------------------------------------
*/

-- 6. List the names of all base tables located in the 'public' schema.
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- 7. Retrieve a list of all column names and their exact data types for the 'employees' table.
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'employees'
ORDER BY ordinal_position;

-- 8. Count the total number of columns that exist in the 'products' table.
SELECT count(*) AS column_count
FROM information_schema.columns 
WHERE table_name = 'products';

-- 9. Discover all primary key and foreign key constraints currently defined in the public schema.
SELECT constraint_name, table_name, constraint_type 
FROM information_schema.table_constraints 
WHERE table_schema = 'public'
  AND constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY');

-- 10. View a list of current active connections to the database to see who else is logged in.
SELECT datname AS database_name, usename AS user_name, state, client_addr 
FROM pg_stat_activity 
WHERE state = 'active';