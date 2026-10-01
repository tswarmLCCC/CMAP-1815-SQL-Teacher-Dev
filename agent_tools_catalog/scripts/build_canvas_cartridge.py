import os
import sys
import re
import hashlib
import zipfile
import html
import shutil
import datetime
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UNITS_DIR = os.path.join(BASE_DIR, "units")
COURSE_SPECS_DIR = os.path.join(BASE_DIR, "course_specs")
OUTPUT_BUILD_DIR = os.path.join(BASE_DIR, "build", "canvas_cartridge")
IMSCC_OUTPUT_FILE = os.path.join(BASE_DIR, "CMAP_1815_Complete.imscc")

def make_id(seed: str) -> str:
    """Generate a deterministic 32-char hex identifier matching Canvas format."""
    return "g" + hashlib.md5(seed.encode("utf-8")).hexdigest()[1:]

# Master Unit Metadata: Readings, Descriptions & Embedded YouTube Video Timestamps
UNIT_METADATA = [
    {
        "num": 1,
        "folder": "unit_01_selection_and_fundamentals",
        "date_range": "10/19 to 10/25",
        "title": "10/19 to 10/25 Unit 1: Selection & Relational Fundamentals",
        "short_title": "Unit 1",
        "topic": "Selection & Relational Fundamentals",
        "due_date_str": "Friday, October 23, 2026 at 11:59 PM (Midnight MT)",
        "due_iso": "2026-10-23T23:59:00",
        "readings": [
            ("PostgreSQL SELECT", "https://neon.tech/postgresql/tutorial/select",
             "Learn how the SELECT statement retrieves data from relational tables and why specifying columns is superior to SELECT *."),
            ("Column Alias (AS)", "https://neon.tech/postgresql/tutorial/column-alias",
             "Understand how to assign descriptive temporary names to projected columns and calculated arithmetic expressions."),
            ("ORDER BY Sorting", "https://neon.tech/postgresql/tutorial/order-by",
             "Master sorting result sets in ASC and DESC order, handling multiple sort columns, and controlling NULL placement."),
            ("DISTINCT Deduplication", "https://neon.tech/postgresql/tutorial/select-distinct",
             "Evaluate multi-column uniqueness and eliminate duplicate rows from query projections.")
        ],
        "videos": [
            ("What is a Relational Database", "qw--VYLpxG4", 317, "0:05:17"),
            ("What is PostgreSQL", "qw--VYLpxG4", 550, "0:09:10"),
            ("The SELECT Statement & Projection", "qw--VYLpxG4", 4348, "1:12:28"),
            ("Sorting with ORDER BY", "qw--VYLpxG4", 4518, "1:15:18"),
            ("Deduplication with DISTINCT", "qw--VYLpxG4", 4793, "1:19:53")
        ]
    },
    {
        "num": 2,
        "folder": "unit_02_filtering_and_logic",
        "date_range": "10/26 to 11/1",
        "title": "10/26 to 11/1 Unit 2: Targeted Retrieval & Logic Gates",
        "short_title": "Unit 2",
        "topic": "Targeted Retrieval & Three-Valued Logic",
        "due_date_str": "Friday, October 30, 2026 at 11:59 PM (Midnight MT)",
        "due_iso": "2026-10-30T23:59:00",
        "readings": [
            ("WHERE Clause", "https://neon.tech/postgresql/tutorial/where",
             "Filter row streams using comparison operators (=, !=, <, >, <=, >=) to extract precise records."),
            ("BETWEEN Operator", "https://neon.tech/postgresql/tutorial/between",
             "Filter values within continuous numerical and temporal ranges, noting timestamp boundary rules."),
            ("IN Operator", "https://neon.tech/postgresql/tutorial/in",
             "Match values against discrete lists or dynamic subqueries without writing repetitive OR chains."),
            ("LIKE & ILIKE Pattern Matching", "https://neon.tech/postgresql/tutorial/like",
             "Search string data using wildcard pattern matching (% for multi-character, _ for single-character) and case-insensitive ILIKE."),
            ("IS NULL & Three-Valued Logic", "https://neon.tech/postgresql/tutorial/is-null",
             "Master ANSI Three-Valued Logic (TRUE, FALSE, UNKNOWN) and avoid catastrophic NULL propagation bugs.")
        ],
        "videos": [
            ("WHERE Clause and Logic Gates", "qw--VYLpxG4", 4919, "1:21:59"),
            ("Comparison Operators Deep Dive", "qw--VYLpxG4", 5129, "1:25:29"),
            ("Pagination: LIMIT & OFFSET", "qw--VYLpxG4", 5375, "1:29:35"),
            ("IN and BETWEEN Range Operators", "qw--VYLpxG4", 5563, "1:32:43"),
            ("Pattern Matching: LIKE and ILIKE", "qw--VYLpxG4", 5865, "1:37:45"),
            ("Handling NULLs: COALESCE & NULLIF", "qw--VYLpxG4", 7952, "2:12:32")
        ]
    },
    {
        "num": 3,
        "folder": "unit_03_joins_and_relations",
        "date_range": "11/2 to 11/8",
        "title": "11/2 to 11/8 Unit 3: Relational Joins & Set Relationships",
        "short_title": "Unit 3",
        "topic": "Relational Joins & Foreign Key Relationships",
        "due_date_str": "Friday, November 6, 2026 at 11:59 PM (Midnight MT)",
        "due_iso": "2026-11-06T23:59:00",
        "readings": [
            ("Visual Joins Overview", "https://neon.tech/postgresql/tutorial/joins",
             "Conceptualize relational interconnectivity across tables using Venn diagrams and set intersection."),
            ("INNER JOIN", "https://neon.tech/postgresql/tutorial/inner-join",
             "Join multiple tables based on primary key to foreign key matches across shared join keys."),
            ("LEFT JOIN & Anti-Joins", "https://neon.tech/postgresql/tutorial/left-join",
             "Retain unmatched records from the left table and implement the Anti-Join pattern to identify orphaned records."),
            ("Table Aliases", "https://neon.tech/postgresql/tutorial/column-alias",
             "Use compact table aliases to qualify ambiguous column names across multi-table queries.")
        ],
        "videos": [
            ("What Are Primary Keys", "qw--VYLpxG4", 8964, "2:29:24"),
            ("Foreign Keys & Relational Integrity", "qw--VYLpxG4", 11801, "3:16:41"),
            ("INNER JOINs in Action", "qw--VYLpxG4", 12570, "3:29:30"),
            ("LEFT JOINs & Unmatched Records", "qw--VYLpxG4", 12917, "3:35:17")
        ]
    },
    {
        "num": 4,
        "folder": "unit_04_aggregation_and_pivoting",
        "date_range": "11/9 to 11/15",
        "title": "11/9 to 11/15 Unit 4: Summarization, Aggregation & Pivoting",
        "short_title": "Unit 4",
        "topic": "Summarization, Aggregation & Pivoting",
        "due_date_str": "Friday, November 13, 2026 at 11:59 PM (Midnight MT)",
        "due_iso": "2026-11-13T23:59:00",
        "readings": [
            ("GROUP BY Tutorial", "https://neon.tech/postgresql/tutorial/group-by",
             "Group vertical rows into summary buckets and understand the Golden Rule of GROUP BY."),
            ("HAVING Clause", "https://neon.tech/postgresql/tutorial/having",
             "Filter aggregated groups after summarization, contrasting HAVING with pre-aggregation WHERE filters."),
            ("Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)", "https://neon.tech/postgresql/tutorial/aggregate-functions",
             "Compute statistical summarizations and understand how NULL values interact with aggregate computations."),
            ("CASE Conditional Expressions", "https://neon.tech/postgresql/tutorial/case",
             "Implement conditional logic and matrix cross-tab pivoting (CASE WHEN inside SUM) for executive reporting.")
        ],
        "videos": [
            ("Aggregate Functions: MIN, MAX & AVG", "qw--VYLpxG4", 6940, "1:55:40"),
            ("SUM Function & Numeric Rollups", "qw--VYLpxG4", 7188, "1:59:48"),
            ("GROUP BY Foundations", "qw--VYLpxG4", 6190, "1:43:10"),
            ("Filtering Aggregated Groups with HAVING", "qw--VYLpxG4", 6401, "1:46:41")
        ]
    },
    {
        "num": 5,
        "folder": "unit_05_safe_dml_and_modifications",
        "date_range": "11/16 to 11/22",
        "title": "11/16 to 11/22 Unit 5: Safe DML, Transaction Integrity & Staging",
        "short_title": "Unit 5",
        "topic": "Safe DML, Transaction Integrity & Staging Tables",
        "due_date_str": "Friday, November 20, 2026 at 11:59 PM (Midnight MT)",
        "due_iso": "2026-11-20T23:59:00",
        "readings": [
            ("INSERT Statement", "https://neon.tech/postgresql/tutorial/insert",
             "Insert single and batch records with explicit column lists and atomic upserts (ON CONFLICT DO UPDATE)."),
            ("UPDATE Statement & RETURNING", "https://neon.tech/postgresql/tutorial/update",
             "Safely modify records and use the RETURNING clause to audit changes in real time."),
            ("DELETE Statement", "https://neon.tech/postgresql/tutorial/delete",
             "Safely remove records using the 3-step pre-execution protocol to prevent accidental table wipes."),
            ("Transactions (BEGIN, COMMIT, ROLLBACK)", "https://neon.tech/postgresql/tutorial/transaction",
             "Enforce ACID transaction boundaries to guarantee atomic database updates and prevent data corruption."),
            ("Temporary Staging Tables", "https://neon.tech/postgresql/tutorial/temporary-table",
             "Stage ETL transformations inside session-scoped temporary tables before committing to production.")
        ],
        "videos": [
            ("INSERT INTO Operations & Syntax", "qw--VYLpxG4", 3355, "0:55:55"),
            ("How to Safely Delete Records", "qw--VYLpxG4", 10485, "2:54:45"),
            ("How to Safely Update Records", "qw--VYLpxG4", 10896, "3:01:36"),
            ("ON CONFLICT & Upserts", "qw--VYLpxG4", 11155, "3:05:55")
        ]
    },
    {
        "num": 6,
        "folder": "unit_06_subqueries_and_window_functions",
        "date_range": "11/30 to 12/6",
        "title": "11/30 to 12/6 Unit 6: Query Modularity, CTEs & Window Functions",
        "short_title": "Unit 6",
        "topic": "Query Modularity, CTEs & Analytical Window Functions",
        "due_date_str": "Friday, December 4, 2026 at 11:59 PM (Midnight MT)",
        "due_iso": "2026-12-04T23:59:00",
        "readings": [
            ("Common Table Expressions (WITH)", "https://neon.tech/postgresql/tutorial/cte",
             "Decompose complex nested subqueries into readable, sequential CTE pipelines."),
            ("Window Functions Overview", "https://neon.tech/postgresql/tutorial/window-function",
             "Compute non-collapsing aggregations, running totals, and moving averages across row partitions."),
            ("ROW_NUMBER Function", "https://neon.tech/postgresql/tutorial/row_number",
             "Assign sequential integers to rows and implement the ROW_NUMBER() = 1 deduplication pattern."),
            ("RANK & DENSE_RANK", "https://neon.tech/postgresql/tutorial/rank",
             "Evaluate ranking semantics, tied values, and gapless competitive rankings across partitions.")
        ],
        "videos": [
            ("Subqueries & Nested SELECT Statements", "qw--VYLpxG4", 4348, "1:12:28"),
            ("Query Modularization & Pipelines", "qw--VYLpxG4", 6190, "1:43:10"),
            ("Running Aggregates & Analytical Partitions", "qw--VYLpxG4", 6940, "1:55:40")
        ]
    },
    {
        "num": 7,
        "folder": "unit_07_schema_design_and_integrity",
        "date_range": "12/7 to 12/13",
        "title": "12/7 to 12/13 Unit 7: Schema Design, DDL & Data Integrity",
        "short_title": "Unit 7",
        "topic": "Schema Design, Normalization (1NF–3NF), DDL & Constraints",
        "due_date_str": "Friday, December 11, 2026 at 11:59 PM (Midnight MT)",
        "due_iso": "2026-12-11T23:59:00",
        "readings": [
            ("CREATE TABLE & Data Types", "https://neon.tech/postgresql/tutorial/create-table",
             "Define relational table architectures using optimal PostgreSQL data types (INT, NUMERIC, VARCHAR, TIMESTAMPTZ)."),
            ("Primary Key Constraints", "https://neon.tech/postgresql/tutorial/primary-key",
             "Declare surrogate and natural primary keys to enforce entity uniqueness."),
            ("Foreign Key & Referential Actions", "https://neon.tech/postgresql/tutorial/foreign-key",
             "Establish relational links and configure cascading referential actions (ON DELETE RESTRICT, CASCADE, SET NULL)."),
            ("CHECK & UNIQUE Constraints", "https://neon.tech/postgresql/tutorial/check-constraint",
             "Enforce declarative business rules and domain integrity directly at the database engine level."),
            ("CREATE VIEW for Abstraction", "https://neon.tech/postgresql/tutorial/views",
             "Encapsulate multi-table JOINs and security boundaries inside reusable virtual views.")
        ],
        "videos": [
            ("How To Create Tables with DDL", "qw--VYLpxG4", 2497, "0:41:37"),
            ("Declaring Table Constraints", "qw--VYLpxG4", 2952, "0:49:12"),
            ("Adding Primary Keys", "qw--VYLpxG4", 9386, "2:36:26"),
            ("Unique & Check Constraints", "qw--VYLpxG4", 9655, "2:40:55")
        ]
    },
    {
        "num": 8,
        "folder": "unit_08_performance_indexing_and_capstone",
        "date_range": "12/14 to 12/18",
        "title": "12/14 to 12/18 Unit 8: Performance Tuning, Indexing & Capstone Defense",
        "short_title": "Unit 8",
        "topic": "Query Optimization, EXPLAIN ANALYZE, Indexes & Capstone Defense",
        "due_date_str": "Friday, December 18, 2026 at 11:59 PM (Midnight MT)",
        "due_iso": "2026-12-18T23:59:00",
        "readings": [
            ("EXPLAIN & Query Plans", "https://neon.tech/postgresql/tutorial/explain",
             "Interpret cost-based query execution trees, comparing Sequential Scans against Index Scans."),
            ("PostgreSQL Indexes Overview", "https://neon.tech/postgresql/tutorial/indexes",
             "Understand B-Tree indexing mechanisms, index selectivity, and query planner cost models."),
            ("CREATE INDEX Best Practices", "https://neon.tech/postgresql/tutorial/create-index",
             "Balance read optimization against the Write Penalty imposed on INSERT, UPDATE, and DELETE operations."),
            ("Composite Indexes", "https://neon.tech/postgresql/tutorial/composite-index",
             "Design multi-column indexes adhering to the Leftmost Prefix Rule.")
        ],
        "videos": [
            ("Index Structures & Selectivity", "qw--VYLpxG4", 9386, "2:36:26"),
            ("Exporting Query Results to CSV", "qw--VYLpxG4", 13647, "3:47:27")
        ]
    }
]

# Supplemental Graded AI Practice Data
LEARN_WITH_AI_DATA = {
    1: {
        "persona": "Professor Codd (The Socratic SQL Master)",
        "drill_topic": "Execution Order & Projection Hazards",
        "prompt": (
            "Act as a strict, Socratic SQL professor named Professor Codd. I am a student learning SQL SELECT statements "
            "and relational database fundamentals in PostgreSQL 16. Do NOT give me direct answers or write the SQL for me. "
            "Instead, ask me one challenging question at a time to test my understanding of:\n"
            "1. Why PostgreSQL evaluates FROM before SELECT during query execution.\n"
            "2. The fundamental difference between physical row storage and relational projection.\n"
            "3. Why 'SELECT *' is considered a dangerous anti-pattern in production microservices and reporting pipelines.\n"
            "Start by asking me your first question about query execution order. Wait for my response before evaluating my reasoning and asking the next question."
        ),
        "discussion_prompt": "In the Unit 1 Discussion, post: (1) The toughest question Professor Codd asked you, (2) What you realized about how PostgreSQL executes queries behind the scenes, and (3) Why SELECT * causes production microservice failures."
    },
    2: {
        "persona": "The Pedantic Database QA Lead",
        "drill_topic": "ANSI Three-Valued Logic & NULL Traps",
        "prompt": (
            "Act as a pedantic Senior Database QA Engineer. I am writing PostgreSQL queries using WHERE, AND, OR, NOT, BETWEEN, LIKE, and IS NULL.\n"
            "Present me with 3 realistic SQL query snippets that contain subtle logic bugs related to:\n"
            "1. ANSI Three-Valued Logic (TRUE, FALSE, UNKNOWN) and NULL propagation (e.g., '= NULL' or 'NOT IN (subquery with NULL)').\n"
            "2. Operator precedence between AND and OR without proper parentheses.\n"
            "3. Inclusive vs. exclusive boundaries in BETWEEN with timestamps.\n"
            "Present the first buggy query snippet and ask me to identify the exact data trap and how to fix it. Do NOT reveal the fix until I attempt an answer."
        ),
        "discussion_prompt": "In the Unit 2 Discussion, share: (1) One of the three-valued logic traps the AI gave you, (2) Why standard Boolean intuition breaks down when NULL is involved, and (3) The corrected WHERE clause."
    },
    3: {
        "persona": "Stressed VP of Operations at OmniRetail",
        "drill_topic": "Translating Vague Business Requests into Multi-Table JOINs",
        "prompt": (
            "Act as a stressed-out VP of Operations at an e-commerce company called 'OmniRetail'. You do NOT know SQL; you only understand business problems.\n"
            "Here is our database schema:\n"
            "- customers (customer_id, full_name, email, state)\n"
            "- orders (order_id, customer_id, order_date, total_amount)\n"
            "- order_items (item_id, order_id, product_id, quantity, unit_price)\n"
            "- products (product_id, product_name, category, unit_cost)\n\n"
            "Give me a messy, real-world business request (e.g., 'Find all customers who signed up but never bought anything, plus our top customers who bought electronics in California, and make sure we don't accidentally duplicate orders!').\n"
            "I will ask you clarifying business questions, determine the necessary JOIN types (INNER, LEFT, Anti-Join), and write the query. "
            "Critique my questions and verify if my final SQL fulfills your business need without generating duplicate rows. Start by stating your urgent request!"
        ),
        "discussion_prompt": "Post to the Unit 3 Discussion: (1) The VP's initial business problem, (2) The join strategy you selected (INNER vs. LEFT vs. Anti-Join) and why, and (3) The final verified query."
    },
    4: {
        "persona": "Chief Financial Officer (CFO)",
        "drill_topic": "Cross-Tab Pivoting & Safe Division Math",
        "prompt": (
            "Act as a CFO and Lead Analytics Architect. I need to generate an executive quarterly financial report from our sales database using PostgreSQL 16.\n"
            "Table: sales_transactions (transaction_id, region, department, quarter, revenue, discount_amount, refund_count)\n\n"
            "Challenge me to write an advanced aggregation query that produces a single cross-tab pivot matrix showing:\n"
            "1. Total revenue per region broken down into distinct columns for Q1, Q2, Q3, and Q4 using conditional CASE aggregation.\n"
            "2. The refund rate percentage (refund_count / total transactions), safely protected against division-by-zero using NULLIF.\n"
            "3. A HAVING filter that excludes regions with fewer than 50 total sales.\n"
            "Provide the requirements step-by-step. Review my SQL syntax, check for GROUP BY violations, and verify whether my matrix matches CFO dashboard standards."
        ),
        "discussion_prompt": "Submit to the Unit 4 Discussion: (1) Your completed cross-tab SQL query, (2) An explanation of why CASE inside SUM eliminates the need for separate queries, and (3) How NULLIF saved your calculations from throwing a runtime exception."
    },
    5: {
        "persona": "Chaos Database SRE",
        "drill_topic": "Safe DML Staging & Transaction Rollback Drills",
        "prompt": (
            "Act as a Database Reliability Engineer (SRE). We are running critical data maintenance and ETL pipeline updates on a live production PostgreSQL 16 database.\n"
            "I will write DML scripts (INSERT, UPDATE, DELETE) using temporary staging tables, explicit transactions (BEGIN, COMMIT, ROLLBACK), and RETURNING clauses.\n"
            "Your role:\n"
            "1. Act as the safety reviewer: Red-team every query I write. If I write an UPDATE or DELETE without a verified WHERE clause, or without running inside a transaction, reject it with a catastrophic failure scenario.\n"
            "2. Introduce unexpected runtime anomalies (e.g., 'Constraint violation on row 452!', 'Network timeout during bulk insert!').\n"
            "3. Force me to demonstrate how my transaction script rolls back cleanly leaving zero orphaned records.\n"
            "Start by presenting me with our first maintenance mission: Purging inactive users while archiving their billing records into an audit staging table."
        ),
        "discussion_prompt": "Post to the Unit 5 Discussion: (1) The disaster scenario simulated by the AI, (2) The safe transaction script you engineered, and (3) The safety difference between modifying live tables directly vs. using an intermediate staging table."
    },
    6: {
        "persona": "Staff Database Architect",
        "drill_topic": "Refactoring Nested Subqueries into CTEs & Window Functions",
        "prompt": (
            "Act as a Principal Database Architect at a high-scale tech company. I am learning modular SQL, Common Table Expressions (WITH clauses), and analytical Window Functions (ROW_NUMBER, RANK, DENSE_RANK, SUM() OVER).\n"
            "Please provide me with an ugly, 4-level deeply nested subquery that calculates:\n"
            "- Top 3 highest-earning employees in each department.\n"
            "- The department's average salary alongside each employee's salary.\n"
            "- The salary difference between each employee and the highest earner in their department.\n"
            "Challenge me to:\n"
            "1. Refactor this unreadable query into clean, modular CTEs (WITH dept_metrics AS (...)).\n"
            "2. Replace redundant group-by subqueries with appropriate OVER (PARTITION BY ... ORDER BY ...) window frames.\n"
            "Review my refactored query, evaluate its readability and efficiency, and explain how the database processes the window frame."
        ),
        "discussion_prompt": "In the Unit 6 Discussion, share: (1) The original nested subquery vs. your clean CTE/Window function query, (2) Why PARTITION BY does not collapse rows like GROUP BY, and (3) When you would choose DENSE_RANK() over ROW_NUMBER()."
    },
    7: {
        "persona": "Senior Enterprise Data Modeler",
        "drill_topic": "3NF Normalization & DDL Constraints",
        "prompt": (
            "Act as a Senior Enterprise Data Modeler. I am learning Relational Database Design, Normalization (1NF, 2NF, 3NF), and DDL constraint declaration in PostgreSQL 16.\n"
            "Give me a messy, denormalized 10-column spreadsheet table from a hospital clinic or university containing repeating groups, multi-valued fields, partial key dependencies, and transitive dependencies.\n"
            "Walk me through an interactive schema design challenge:\n"
            "Step 1: Ask me to identify the 1NF, 2NF, and 3NF violations in the spreadsheet.\n"
            "Step 2: Have me propose a normalized relational schema with entity tables, primary keys, and foreign keys.\n"
            "Step 3: Have me write the complete PostgreSQL DDL (CREATE TABLE) statements with strict constraints (CHECK, NOT NULL, UNIQUE, ON DELETE CASCADE/SET NULL) and a reporting VIEW.\n"
            "Critique my schema at each step. Do NOT write the DDL for me; guide me with design questions."
        ),
        "discussion_prompt": "Post to the Unit 7 Discussion: (1) The denormalized spreadsheet sample, (2) Your 3NF entity-relationship breakdown, (3) Your production DDL script with constraints, and (4) Why your chosen ON DELETE referential action was the safest choice."
    },
    8: {
        "persona": "Senior Performance DBA Panel",
        "drill_topic": "Capstone Technical Defense & EXPLAIN ANALYZE",
        "prompt": (
            "Act as a demanding Database Administrator (DBA) and Technical Review Board conducting my final Capstone Defense for CMAP 1815.\n"
            "I have built a complete PostgreSQL database system with a normalized schema, DDL constraints, ETL transaction pipeline, analytical window queries, and B-Tree indexes.\n"
            "Conduct a 10-minute technical defense simulation:\n"
            "1. Ask me to provide one of my heaviest analytical queries and explain what EXPLAIN ANALYZE reveals about it (Seq Scan vs. Index Scan, Cost, Execution Time).\n"
            "2. Challenge me to defend my B-Tree indexing strategy: Explain composite index column order (Leftmost Prefix rule) and the Write Penalty on INSERT/UPDATE.\n"
            "3. Grill me with edge cases: What happens if table statistics are outdated (ANALYZE)? When would the query planner intentionally ignore an index?\n"
            "Ask one probing question at a time. Evaluate my answers rigorously like a real technical interview!"
        ),
        "discussion_prompt": "Post to the Unit 8 Capstone Discussion: (1) The toughest technical challenge or question the DBA panel asked you, (2) Your defense explaining index column ordering or execution plans, and (3) Your key takeaway on how B-Tree indexes affect read performance vs. write throughput."
    }
}

# Teacher Guide Video & Synchronous Delivery Data per Unit
TEACHER_GUIDE_DATA = {
    1: {
        "videos": [
            ("Micro-Video 1.1: Relational Foundations & The Projection Metaphor", "4-6 mins", "Explain tables as mathematical relations, rows as tuples, and columns as attributes. Use the 'flashlight' metaphor for SELECT projection vs SELECT *."),
            ("Micro-Video 1.2: Live Coding SELECT & ORDER BY in psql", "5-7 mins", "Open Codespaces terminal, run psql -U postgres, query employees, demonstrate column aliases (AS), string concatenation (||), and multi-column sorting."),
            ("Micro-Video 1.3: Lab 1 Walkthrough & Submission Protocol", "3-4 mins", "Tour the 5 base tables in public schema, explain the Lab 1 deliverables, and demonstrate how to submit answers into the Canvas Lab Practical.")
        ],
        "sync_agenda": "0:00-0:20 Concept Debrief & Warm-up | 0:20-0:50 Live Demo & Semicolon/Alias traps | 0:50-1:40 Paired Challenges (inclass_challenges.sql) | 1:40-2:20 Lab 1 Hands-on | 2:20-2:30 Practical Turn-in Debrief"
    },
    2: {
        "videos": [
            ("Micro-Video 2.1: The Scalpel - WHERE Filtering & Logic Gates", "4-6 mins", "Contrast WHERE with SELECT projection. Teach AND/OR operator precedence and why parentheses are mandatory."),
            ("Micro-Video 2.2: Live Demo - The Mystery of Three-Valued Logic & NULLs", "5-7 mins", "Demonstrate in psql why '= NULL' always yields UNKNOWN (zero rows) and how IS NULL / IS NOT NULL fixes it."),
            ("Micro-Video 2.3: Lab 2 Walkthrough & Pattern Matching (LIKE/ILIKE)", "3-4 mins", "Walk through wildcards (% and _), case-insensitive ILIKE, and LIMIT/OFFSET pagination.")
        ],
        "sync_agenda": "0:00-0:20 3VL Truth Table Warm-up | 0:20-0:50 Live Trap Demo (Unparenthesized OR bug) | 0:50-1:40 Paired Filtering Challenges | 1:40-2:20 Lab 2 Execution | 2:20-2:30 Wrap-up"
    },
    3: {
        "videos": [
            ("Micro-Video 3.1: Visualizing Relational Interconnectivity (Joins)", "4-6 mins", "Explain Primary Key to Foreign Key relationships using Venn diagrams and set intersection."),
            ("Micro-Video 3.2: Live Demo - INNER vs LEFT vs The Anti-Join Pattern", "6-8 mins", "Demonstrate 3-table joins (orders -> order_lines -> products) and how 'WHERE parent.id IS NULL' identifies orphaned records."),
            ("Micro-Video 3.3: Lab 3 Walkthrough & Multi-Table Order Subtotals", "3-4 mins", "Review schema ERD and show how line_subtotal (quantity * unit_price) is calculated across tables.")
        ],
        "sync_agenda": "0:00-0:20 ERD Entity Mapping | 0:20-0:50 Live Cartesian Product Trap Demo | 0:50-1:40 Paired Multi-Table Joins | 1:40-2:20 Lab 3 Execution | 2:20-2:30 Anti-Join Debrief"
    },
    4: {
        "videos": [
            ("Micro-Video 4.1: Transforming Granular Rows into Executive Summaries", "4-6 mins", "The Golden Rule of GROUP BY (every non-aggregated SELECT column must appear in GROUP BY)."),
            ("Micro-Video 4.2: Live Demo - WHERE vs HAVING & Conditional CASE Pivoting", "6-8 mins", "Demonstrate pre-aggregation WHERE filtering vs post-aggregation HAVING filtering, and SUM(CASE WHEN...) matrix pivoting."),
            ("Micro-Video 4.3: Lab 4 Walkthrough & Safe Division Math (NULLIF)", "3-4 mins", "Explain division-by-zero crashes in financial queries and how NULLIF(denominator, 0) prevents runtime errors.")
        ],
        "sync_agenda": "0:00-0:20 Aggregation Warm-up | 0:20-0:50 Live GROUP BY Error Trap Demo | 0:50-1:40 Paired Pivoting Challenges | 1:40-2:20 Lab 4 Executive Reporting | 2:20-2:30 Summary Review"
    },
    5: {
        "videos": [
            ("Micro-Video 5.1: Safe Data Engineering & Transaction Protocols", "4-6 mins", "ACID principles, explicit transaction boundaries (BEGIN, COMMIT, ROLLBACK), and why running raw UPDATEs in production is forbidden."),
            ("Micro-Video 5.2: Live Demo - The 3-Step DML Protocol & RETURNING Clauses", "6-8 mins", "Step 1: SELECT count(*); Step 2: BEGIN; UPDATE... RETURNING; Step 3: Verify count & COMMIT. Demonstrate rolling back an accidental whole-table delete."),
            ("Micro-Video 5.3: Lab 5 Walkthrough & Temporary Staging Tables", "3-4 mins", "How session-scoped TEMP TABLEs allow multi-step ETL cleansing before touching production tables.")
        ],
        "sync_agenda": "0:00-0:20 Disaster Recovery Discussion | 0:20-0:50 Live Catastrophic DELETE & Rollback Demo | 0:50-1:40 Paired Staging Transformation Clinic | 1:40-2:20 Lab 5 Safe DML | 2:20-2:30 Wrap-up"
    },
    6: {
        "videos": [
            ("Micro-Video 6.1: Subqueries vs Common Table Expressions (CTEs)", "4-6 mins", "Explain scalar, multi-row, and correlated subqueries, then refactor them into sequential WITH clauses."),
            ("Micro-Video 6.2: Live Demo - Analytical Window Functions & Partitions", "6-8 mins", "Demonstrate OVER (PARTITION BY ... ORDER BY ...), ROW_NUMBER() = 1 deduplication, and cumulative running totals."),
            ("Micro-Video 6.3: Lab 6 Walkthrough & Advanced Analytics", "3-4 mins", "Guide students through ranking department compensation and calculating running order volume over time.")
        ],
        "sync_agenda": "0:00-0:20 CTE Pipeline Overview | 0:20-0:50 Live Window Framing Demo | 0:50-1:40 Paired Analytical Window Challenges | 1:40-2:20 Lab 6 Execution | 2:20-2:30 Analytics Review"
    },
    7: {
        "videos": [
            ("Micro-Video 7.1: From Spreadsheet Chaos to 3NF Normalization", "4-6 mins", "Explain 1NF (atomic columns), 2NF (no partial key dependencies), and 3NF (no transitive dependencies)."),
            ("Micro-Video 7.2: Live Demo - DDL Constraints & Referential Actions", "6-8 mins", "Write CREATE TABLE with PRIMARY KEY, FOREIGN KEY ON DELETE CASCADE, CHECK, and UNIQUE in PostgreSQL 16."),
            ("Micro-Video 7.3: Lab 7 Walkthrough & Creating Abstraction Views", "3-4 mins", "Explain how CREATE VIEW hides schema complexity and provides secure data access for business analysts.")
        ],
        "sync_agenda": "0:00-0:20 Denormalized Spreadsheet Clinic | 0:20-0:50 Live Constraint Violation Trap Demo | 0:50-1:40 Paired Schema DDL Design | 1:40-2:20 Lab 7 Execution | 2:20-2:30 Schema Architecture Review"
    },
    8: {
        "videos": [
            ("Micro-Video 8.1: Query Optimization, EXPLAIN Trees & B-Trees", "4-6 mins", "Explain how PostgreSQL cost models evaluate Sequential Scans vs Index Scans, and how B-Trees structure indexed data."),
            ("Micro-Video 8.2: Live Demo - The Write Penalty & Composite Index Leftmost Prefix", "6-8 mins", "Run EXPLAIN ANALYZE on a 10,000-row table, create a B-Tree index, show cost reduction, and test column order."),
            ("Micro-Video 8.3: Capstone Walkthrough & Architecture Defense Guide", "4-6 mins", "Walk through the 4 capstone deliverables: 3NF DDL, Staging ETL pipeline, Window analytics, and Index optimization defense.")
        ],
        "sync_agenda": "0:00-0:20 Query Planner Clinic | 0:20-0:50 Live EXPLAIN ANALYZE Tuning Demo | 0:50-1:40 Capstone Defense Working Session | 1:40-2:20 Capstone Execution | 2:20-2:30 Final Wrap-up"
    }
}

ARCHIVE_UNIT_FOLDERS = {
    1: "1_Intro_and_Select",
    2: "2_Filtering",
    3: "3_Joins",
    4: "4_Grouping_Set_Operation_and_Pivoting",
    5: "5_Insert_Update_Delete_Temp_Tables",
    6: "6_Modularity_Window_Functions_and_CTE",
    7: "7_Schema_Design_Data_Integrity_DataWarehouse_Intro",
    8: "8_Performance_Indexing_and_Audit_Trails"
}

def load_and_clean_unit_overview(unit_num: int) -> str:
    """Loads and cleans the curated instructor Unit_Overview markdown file."""
    folder_name = ARCHIVE_UNIT_FOLDERS.get(unit_num)
    if not folder_name:
        return ""
    file_path = os.path.join(BASE_DIR, "archive", "v1_original_drafts", "units", folder_name, "Unit_Overview.md")
    if not os.path.exists(file_path):
        return ""
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Clean up base64 image placeholders
    text = re.sub(r'\[image\d+\]:\s*<data:image/[^>]+>', '', text)
    
    # Replace markdown image placeholders with mathematical symbols or clean expressions
    text = text.replace('![][image1]', '')
    text = text.replace('![][image2]', '')
    text = text.replace('![][image3]', '')
    text = text.replace('![][image4]', '')
    text = text.replace('![][image5]', '')
    
    # Specific mathematical symbols and formula cleanups
    text = text.replace('Projection ()', 'Projection (&pi;)')
    text = text.replace('Aggregate Functions (, , , , )', 'Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)')
    text = text.replace('often does not equal  precisely', 'often does not equal 0.3 precisely')
    text = text.replace('Incremental integers ().', 'Incremental integers (1, 2, 3...).')
    text = text.replace('(![][image1] complexity)', '(linear O(N) complexity)')
    text = text.replace('(![][image2] complexity)', '(logarithmic O(log N) complexity)')
    text = text.replace('( complexity)', '(computational complexity)')

    # Unescape escaped markdown punctuation and operators
    text = re.sub(r'\\([*_#!\\[\\]\.\-+=\<\>~|`])', r'\1', text)

    # Remove duplicate title header lines if present
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.strip().startswith('# **Unit') or line.strip().startswith('# Unit'):
            continue
        cleaned_lines.append(line)
    
    return "\n".join(cleaned_lines).strip()

def format_inline(s: str) -> str:
    """Formats inline markdown syntax to HTML."""
    s = re.sub(r'\\([*_#!\\[\\]\.\-+=\<\>~|`])', r'\1', s)

    def replace_inline_code(match):
        code_text = html.escape(match.group(1))
        return f'<code style="background: #f1f5f9; color: #0369a1; padding: 0.15rem 0.35rem; border-radius: 3px; font-size: 0.9em; font-family: Consolas, monospace; font-weight: 600;">{code_text}</code>'

    s = re.sub(r'`([^`]+)`', replace_inline_code, s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', s)
    s = s.replace(r'$\rightarrow$', '&rarr;')
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s

def parse_markdown_to_html(md: str) -> str:
    """Converts structured markdown (tables, code blocks, lists, details) into clean styled HTML."""
    if not md:
        return ""

    # Unescape markdown punctuation and operators first (\+, \=, \*, 1\., \_, etc.)
    md = re.sub(r'\\([*_#!\\[\\]\.\-+=\<\>~|`])', r'\1', md)

    code_blocks = []
    def code_block_sub(match):
        lang = match.group(1) or ''
        code = match.group(2)
        idx = len(code_blocks)
        code_html = f'<div style="background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; overflow-x: auto; margin: 1.25rem 0; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5;"><pre style="margin: 0; background: transparent; color: inherit;"><code>{html.escape(code.strip())}</code></pre></div>'
        code_blocks.append(code_html)
        return f'__CODE_BLOCK_{idx}__'

    text = re.sub(r'^[ \t]*```([a-zA-Z0-9_-]*)\r?\n(.*?)\r?\n[ \t]*```', code_block_sub, md, flags=re.DOTALL | re.MULTILINE)

    lines = text.splitlines()
    output = []
    in_table = False
    table_rows = []
    in_list = False
    list_type = None

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return ''
        html_table = ['<div style="overflow-x: auto; margin: 1.25rem 0;"><table style="width: 100%; border-collapse: collapse; border: 1px solid #cbd5e1; font-size: 0.95em;">']
        header_cells = table_rows[0]
        html_table.append('<thead><tr style="background-color: #1e3a8a; color: #ffffff;">')
        for c in header_cells:
            html_table.append(f'<th style="padding: 10px 14px; border: 1px solid #94a3b8; font-weight: 600;">{format_inline(c)}</th>')
        html_table.append('</tr></thead><tbody>')
        for row_idx, row in enumerate(table_rows[1:]):
            bg = '#f8fafc' if row_idx % 2 == 0 else '#ffffff'
            html_table.append(f'<tr style="background-color: {bg};">')
            for c in row:
                html_table.append(f'<td style="padding: 8px 14px; border: 1px solid #cbd5e1;">{format_inline(c)}</td>')
            html_table.append('</tr>')
        html_table.append('</tbody></table></div>')
        in_table = False
        table_rows = []
        return ''.join(html_table)

    def flush_list():
        nonlocal in_list, list_type
        if not in_list:
            return ''
        tag = list_type
        in_list = False
        list_type = None
        return f'</{tag}>\n'

    for line in lines:
        trimmed = line.strip()

        if trimmed.startswith('|') and trimmed.endswith('|'):
            cells = [c.strip() for c in trimmed[1:-1].split('|')]
            if re.match(r'^[:\- ]+$', ''.join(cells)):
                pass
            else:
                if not in_table:
                    if in_list:
                        output.append(flush_list())
                    in_table = True
                    table_rows = [cells]
                else:
                    table_rows.append(cells)
            continue
        elif in_table:
            output.append(flush_table())

        if not trimmed:
            if in_list:
                output.append(flush_list())
            continue

        cb_match = re.match(r'^__CODE_BLOCK_(\d+)__$', trimmed)
        if cb_match:
            if in_list:
                output.append(flush_list())
            idx = int(cb_match.group(1))
            output.append(code_blocks[idx])
            continue

        h_match = re.match(r'^(#{1,6})\s+(.*)$', trimmed)
        if h_match:
            if in_list:
                output.append(flush_list())
            level = len(h_match.group(1))
            h_text = format_inline(h_match.group(2).strip())
            if level == 1:
                output.append(f'<h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.5rem; margin-bottom: 0.75rem;">{h_text}</h2>')
            elif level == 2:
                output.append(f'<h3 style="color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.3rem; margin-top: 1.5rem; margin-bottom: 0.75rem;">{h_text}</h3>')
            elif level == 3:
                output.append(f'<h4 style="color: #0f172a; margin-top: 1.25rem; margin-bottom: 0.5rem; font-size: 1.15em;">{h_text}</h4>')
            else:
                output.append(f'<h5 style="color: #334155; margin-top: 1rem; margin-bottom: 0.5rem; font-size: 1.05em;">{h_text}</h5>')
            continue

        if trimmed in ('---', '***', '___'):
            if in_list:
                output.append(flush_list())
            output.append('<hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 1.5rem 0;"/>')
            continue

        if trimmed.startswith('<details>'):
            if in_list:
                output.append(flush_list())
            output.append('<details style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 0.75rem 1.25rem; margin: 1rem 0;">')
            continue
        if trimmed.startswith('</details>'):
            if in_list:
                output.append(flush_list())
            output.append('</details>')
            continue
        if trimmed.startswith('<summary>') and trimmed.endswith('</summary>'):
            if in_list:
                output.append(flush_list())
            sum_text = trimmed[9:-10].strip()
            sum_text = re.sub(r'<\/?b>', '', sum_text)
            output.append(f'<summary style="cursor: pointer; font-weight: 600; color: #1e3a8a; padding: 0.25rem 0;">{format_inline(sum_text)}</summary><div style="margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px dashed #cbd5e1;">')
            continue
        if trimmed.startswith('</summary>'):
            continue

        if trimmed.startswith('>'):
            if in_list:
                output.append(flush_list())
            bq_text = format_inline(trimmed.lstrip('>').strip())
            output.append(f'<div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 0.75rem 1.25rem; margin: 1rem 0; border-radius: 0 4px 4px 0; color: #1e3a8a;">{bq_text}</div>')
            continue

        ul_match = re.match(r'^[*•-]\s+(.*)$', trimmed)
        ol_match = re.match(r'^\d+\.\s+(.*)$', trimmed)
        if ul_match:
            if not in_list or list_type != 'ul':
                if in_list:
                    output.append(flush_list())
                in_list = True
                list_type = 'ul'
                output.append('<ul style="padding-left: 1.5rem; margin: 0.75rem 0;">')
            output.append(f'<li style="margin-bottom: 0.35rem;">{format_inline(ul_match.group(1))}</li>')
            continue
        elif ol_match:
            item_text = ol_match.group(1).strip()
            # Strip redundant internal numbering like "1. ", "**1. ", "**1.**" to prevent double numbering (e.g. "1. 1.")
            item_text = re.sub(r'^(\*\*)?\d+[\.\)]\s*(\*\*)?\s*', '', item_text)
            if not in_list or list_type != 'ol':
                if in_list:
                    output.append(flush_list())
                in_list = True
                list_type = 'ol'
                output.append('<ol style="padding-left: 1.5rem; margin: 0.75rem 0;">')
            output.append(f'<li style="margin-bottom: 0.35rem;">{format_inline(item_text)}</li>')
            continue

        if in_list:
            output.append(flush_list())
        
        output.append(f'<p style="margin: 0.75rem 0; line-height: 1.6;">{format_inline(trimmed)}</p>')

    if in_table:
        output.append(flush_table())
    if in_list:
        output.append(flush_list())

    result = '\n'.join(output)
    result = result.replace('</details>', '</div></details>')

    for idx, cb in enumerate(code_blocks):
        result = result.replace(f'__CODE_BLOCK_{idx}__', cb)
    return result

def render_standard_page_html(title: str, lead_html: str, sections: list, page_id: str, workflow_state: str = "active") -> str:
    """
    Renders clean, modern, native Canvas HTML pages without the ribbon header,
    ideal for lab guides, reading pages, study drills, and AI practice.
    """
    sections_html = []
    for heading, content in sections:
        sec = f"""  <div style="margin-bottom: 2rem;">
    <h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.75rem; margin-bottom: 1rem;">{html.escape(heading)}</h2>
    <div style="line-height: 1.6; color: #1e293b;">
      {content}
    </div>
  </div>"""
        sections_html.append(sec)

    body_sections = "\n".join(sections_html)
    lead_block = ""
    if lead_html:
        lead_block = f"""  <div style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 1rem 1.25rem; margin-bottom: 1.75rem; border-radius: 0 4px 4px 0; font-size: 1.05em; line-height: 1.5; color: #334155;">
    {lead_html}
  </div>"""

    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{html.escape(title)}</title>
<meta name="identifier" content="{page_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="{workflow_state}"/>
<meta name="editor_type" content="rce"/>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; padding: 1.5rem; max-width: 1000px; margin: 0 auto;">
  <h1 style="color: #1e3a8a; margin-top: 0; margin-bottom: 1.25rem;">{html.escape(title)}</h1>
{lead_block}
{body_sections}
</body>
</html>"""

def render_designplus_html(title: str, lead_html: str, panels: list, page_id: str, workflow_state: str = "active") -> str:
    """Renders HTML strictly adhering to DesignPLUS styles for Unit Overviews, Home, and Start Here."""
    panels_html = []
    for heading, content in panels:
        panels_html.append(f"""    <div class="dp-panel-group">
      <h2 class="dp-panel-heading ">{html.escape(heading)}</h2>
      <div class="dp-panel-content ">
        {content}
      </div>
    </div>""")

    body_panels = "\n".join(panels_html)

    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{html.escape(title)}</title>
<meta name="identifier" content="{page_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="{workflow_state}"/>
<meta name="editor_type" content="rce"/>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper dp-hdg-i-cp-brdr-h2-dp-primary dp-hdg-txt-h3-dp-primary dp-hdg-txt-h4-dp-primary dp-hdg-txt-h5-dp-primary dp-hdg-i-cp-brdr-h5-dp-primary dp-hdg-b-h2-brdr-b dp-hdg-txt-h6-dp-primary dp-hdg-i-cp-brdr-h6-dp-primary dp-hdg-i-styl-h2-pill dp-hdg-i-styl-h3-pill dp-hdg-cp-brdr-h3-dp-secondary dp-hdg-cp-brdr-h2-dp-secondary dp-hdg-brdr-h2-1 dp-hdg-brdr-h3-1 dp-hdg-brdr-h4-1 dp-hdg-brdr-h5-1 dp-hdg-brdr-h6-1 dp-hdg-i-sz-h2-fill dp-hdg-i-sz-h3-fill dp-hdg-i-sz-h5-fill dp-hdg-i-sz-h6-fill dp-hdg-i-brdr-h5-2 dp-hdg-i-brdr-h6-2 dp-hdg-b-h3-brdr-b dp-hdg-txt-h2-dp-primary dp-hdg-i-brdr-h2-1 dp-hdg-i-brdr-h3-1 dp-hdg-i-sz-h4-fill dp-hdg-i-cp-brdr-h3-dp-primary dp-hdg-i-brdr-h4-1 dp-hdg-i-bg-h2-dp-primary dp-hdg-i-bg-h3-dp-primary dp-hdg-b-h4-brdr-b dp-hdg-d-h4-table-l dp-hdg-i-styl-h4-pill dp-hdg-i-cp-brdr-h4-dp-primary">
  <header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
    <h2 class="dp-heading dp-locked"><span class="dp-header-title">{html.escape(title)}</span></h2>
    <p>&nbsp;</p>
  </header>
  <div class="dp-content-block">
    {lead_html}
  </div>
  <div class="dp-panels-wrapper dp-accordion-plus dp-panel-color-dp-primary dp-panel-active-color-dp-accent dp-panel-hover-color-dp-accent">
{body_panels}
  </div>
</div>
</body>
</html>"""

def render_ribbon_sections_page_html(title: str, lead_html: str, sections: list, page_id: str, workflow_state: str = "active") -> str:
    """
    Renders HTML pages with DesignPLUS ribbon headers for each major section/chapter,
    with an overall descriptive lead card on top.
    """
    sections_html = []
    for heading, content in sections:
        sec = f"""  <div class="dp-header-wrapper" style="margin-top: 2.5rem; margin-bottom: 1.25rem;">
    <header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
      <h2 class="dp-heading dp-locked"><span class="dp-header-title">{html.escape(heading)}</span></h2>
    </header>
  </div>
  <div class="dp-section-body" style="line-height: 1.6; color: #1e293b; margin-bottom: 2rem; padding: 0 0.25rem;">
    {content}
  </div>"""
        sections_html.append(sec)

    body_sections = "\n".join(sections_html)
    lead_block = ""
    if lead_html:
        lead_block = f"""  <div class="dp-content-block" style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 1.25rem 1.5rem; margin-top: 1.5rem; margin-bottom: 2rem; border-radius: 0 6px 6px 0; font-size: 1.05em; line-height: 1.6; color: #334155;">
    {lead_html}
  </div>"""

    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{html.escape(title)}</title>
<meta name="identifier" content="{page_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="{workflow_state}"/>
<meta name="editor_type" content="rce"/>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper dp-hdg-i-cp-brdr-h2-dp-primary dp-hdg-txt-h3-dp-primary dp-hdg-txt-h4-dp-primary dp-hdg-txt-h5-dp-primary dp-hdg-i-cp-brdr-h5-dp-primary dp-hdg-b-h2-brdr-b dp-hdg-txt-h6-dp-primary dp-hdg-i-cp-brdr-h6-dp-primary dp-hdg-i-styl-h2-pill dp-hdg-i-styl-h3-pill dp-hdg-cp-brdr-h3-dp-secondary dp-hdg-cp-brdr-h2-dp-secondary dp-hdg-brdr-h2-1 dp-hdg-brdr-h3-1 dp-hdg-brdr-h4-1 dp-hdg-brdr-h5-1 dp-hdg-brdr-h6-1 dp-hdg-i-sz-h2-fill dp-hdg-i-sz-h3-fill dp-hdg-i-sz-h5-fill dp-hdg-i-sz-h6-fill dp-hdg-i-brdr-h5-2 dp-hdg-i-brdr-h6-2 dp-hdg-b-h3-brdr-b dp-hdg-txt-h2-dp-primary dp-hdg-i-brdr-h2-1 dp-hdg-i-brdr-h3-1 dp-hdg-i-sz-h4-fill dp-hdg-i-cp-brdr-h3-dp-primary dp-hdg-i-brdr-h4-1 dp-hdg-i-bg-h2-dp-primary dp-hdg-i-bg-h3-dp-primary dp-hdg-b-h4-brdr-b dp-hdg-d-h4-table-l dp-hdg-i-styl-h4-pill dp-hdg-i-cp-brdr-h4-dp-primary">
  <header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
    <h1 class="dp-heading dp-locked"><span class="dp-header-title">{html.escape(title)}</span></h1>
    <p>&nbsp;</p>
  </header>
{lead_block}
{body_sections}
</div>
</body>
</html>"""

def render_video_embed(title: str, video_id: str, start_sec: int) -> str:
    """Generates a clean responsive 16:9 embedded YouTube player."""
    mins = start_sec // 60
    secs = start_sec % 60
    return f"""<div style="margin-bottom: 2rem;">
  <h4 style="margin-bottom: 0.5rem; color: #1e293b;">{html.escape(title)} <span style="font-size: 0.9em; font-weight: normal; color: #64748b;">(Starts at {mins}:{secs:02d})</span></h4>
  <div class="dp-embed-wrapper" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 6px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 0.5rem;">
    <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" title="{html.escape(title)}" src="https://www.youtube.com/embed/{video_id}?start={start_sec}" loading="lazy" allowfullscreen="allowfullscreen" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"></iframe>
  </div>
  <p style="font-size: 0.85em; color: #64748b; margin-top: 0.25rem;"><a href="https://www.youtube.com/watch?v={video_id}&amp;t={start_sec}s" target="_blank" rel="noopener">Open video segment in new tab ({mins}:{secs:02d})</a></p>
</div>"""

def parse_quiz_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = re.split(r'#+\s*Answer Key', content, flags=re.IGNORECASE)
    questions_part = parts[0]
    key_part = parts[1] if len(parts) > 1 else ""

    key_map = {}
    for line in key_part.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 3:
            q_num_match = re.search(r'\d+', cells[0])
            ans_match = re.search(r'[A-D]', cells[1], re.IGNORECASE)
            if q_num_match and ans_match:
                q_num = int(q_num_match.group(0))
                ans = ans_match.group(0).upper()
                rationale = cells[2]
                key_map[q_num] = (ans, rationale)

    q_blocks = re.split(r'###\s*Question\s+(\d+)', questions_part)
    questions = []
    for i in range(1, len(q_blocks), 2):
        q_num = int(q_blocks[i])
        block_text = q_blocks[i+1].strip()

        opt_matches = list(re.finditer(r'^\s*[*•-]\s*([A-D])\)\s*(.+)$', block_text, flags=re.MULTILINE))
        if opt_matches:
            prompt_end = opt_matches[0].start()
            prompt = block_text[:prompt_end].strip()
            options = []
            for m in opt_matches:
                opt_letter = m.group(1).upper()
                opt_text = m.group(2).strip()
                options.append((opt_letter, opt_text))
        else:
            prompt = block_text
            options = []

        correct_ans, rationale = key_map.get(q_num, ('A', ''))
        questions.append({
            'num': q_num,
            'prompt': prompt,
            'options': options,
            'correct_answer': correct_ans,
            'rationale': rationale
        })

    return questions

def build_qti_xml(quiz_id: str, quiz_title: str, questions: list) -> str:
    """Generates standard QTI 1.2 XML matching the exact Canvas profile."""
    items_xml = []
    for q in questions:
        q_num = q["num"]
        item_id = make_id(f"{quiz_id}_q_{q_num}")
        
        opt_labels = []
        cond_elements = []
        for opt_letter, opt_text in q["options"]:
            opt_id = make_id(f"{item_id}_opt_{opt_letter}")
            opt_labels.append(f"""              <response_label ident="{opt_id}">
                <material>
                  <mattext texttype="text/plain">{html.escape(opt_text)}</mattext>
                </material>
              </response_label>""")
            
            if opt_letter == q["correct_answer"]:
                cond_elements.append(f"""                <varequal respident="response1">{opt_id}</varequal>""")
            else:
                cond_elements.append(f"""                <not>
                  <varequal respident="response1">{opt_id}</varequal>
                </not>""")

        options_block = "\n".join(opt_labels)
        condition_block = "\n".join(cond_elements)
        prompt_clean = html.escape(q["prompt"]).replace("\n", "<br/>")

        items_xml.append(f"""      <item ident="{item_id}" title="Question {q_num}">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>cc_profile</fieldlabel>
              <fieldentry>cc.multiple_response.v0p1</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <mattext texttype="text/html">&lt;div&gt;{prompt_clean}&lt;/div&gt;</mattext>
          </material>
          <response_lid ident="response1" rcardinality="Multiple">
            <render_choice>
{options_block}
            </render_choice>
          </response_lid>
        </presentation>
        <resprocessing>
          <outcomes>
            <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
          </outcomes>
          <respcondition continue="No">
            <conditionvar>
              <and>
{condition_block}
              </and>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
        </resprocessing>
      </item>""")

    items_joined = "\n".join(items_xml)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_qtiasiv1p2p1_v1p0.xsd">
  <assessment ident="{quiz_id}" title="{html.escape(quiz_title)}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>cc_profile</fieldlabel>
        <fieldentry>cc.exam.v0p1</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>qmd_assessmenttype</fieldlabel>
        <fieldentry>Examination</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>qmd_scoretype</fieldlabel>
        <fieldentry>Percentage</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>3</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
{items_joined}
    </section>
  </assessment>
</questestinterop>
"""

def build_assessment_meta_xml(quiz_id: str, quiz_title: str, quiz_group_id: str, due_at: str = None, lock_at: str = None) -> str:
    """Builds Canvas assessment_meta.xml."""
    assign_id = make_id(f"assign_{quiz_id}")
    due_block = f"  <due_at>{due_at}</due_at>\n  <lock_at>{lock_at}</lock_at>\n" if due_at else ""
    assign_due_block = f"    <due_at>{due_at}</due_at>\n    <lock_at>{lock_at}</lock_at>\n" if due_at else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<quiz xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd" identifier="{quiz_id}">
  <title>{html.escape(quiz_title)}</title>
  <description>&lt;p&gt;This weekly assessment tests your mastery of the relational SQL concepts, syntax, and query patterns covered in this unit.&lt;/p&gt;&lt;p&gt;The quiz consists of 15 multiple-choice questions (30 points total, 2 points each). You have 3 attempts; your highest score will be kept.&lt;/p&gt;</description>
{due_block}  <shuffle_questions>false</shuffle_questions>
  <shuffle_answers>false</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <quiz_type>assignment</quiz_type>
  <points_possible>30.0</points_possible>
  <allowed_attempts>3</allowed_attempts>
  <show_correct_answers>true</show_correct_answers>
  <assignment identifier="{assign_id}">
    <title>{html.escape(quiz_title)}</title>
{assign_due_block}    <workflow_state>published</workflow_state>
    <quiz_identifierref>{quiz_id}</quiz_identifierref>
    <points_possible>30.0</points_possible>
    <grading_type>points</grading_type>
    <submission_types>online_quiz</submission_types>
    <assignment_group_identifierref>{quiz_group_id}</assignment_group_identifierref>
  </assignment>
</quiz>
"""

def build_assignment_settings_xml(assign_id: str, title: str, group_id: str, points: float = 100.0, due_at: str = None, lock_at: str = None) -> str:
    """Generates standard Canvas assignment_settings.xml matching institutional format."""
    due_block = f"  <due_at>{due_at}</due_at>\n  <lock_at>{lock_at}</lock_at>\n" if due_at else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<assignment identifier="{assign_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{html.escape(title)}</title>
  <time_zone_edited>Mountain Time (US &amp; Canada)</time_zone_edited>
  <module_locked>false</module_locked>
  <assignment_group_identifierref>{group_id}</assignment_group_identifierref>
  <workflow_state>published</workflow_state>
{due_block}  <assignment_overrides>
  </assignment_overrides>
  <allowed_extensions>sql,txt,pdf</allowed_extensions>
  <has_group_category>false</has_group_category>
  <points_possible>{points:.1f}</points_possible>
  <grading_type>points</grading_type>
  <submission_types>online_text_entry,online_upload</submission_types>
  <turnitin_enabled>false</turnitin_enabled>
  <vericite_enabled>false</vericite_enabled>
  <peer_reviews>false</peer_reviews>
  <automatic_peer_reviews>false</automatic_peer_reviews>
  <anonymous_peer_reviews>false</anonymous_peer_reviews>
  <freeze_on_copy>false</freeze_on_copy>
  <omit_from_final_grade>false</omit_from_final_grade>
  <hide_in_gradebook>false</hide_in_gradebook>
  <post_policy>
    <post_manually>false</post_manually>
  </post_policy>
</assignment>
"""

def main():
    print("=================================================================")
    print("CMAP 1815: Modern SQL - Canvas Native Course Package Builder")
    print("=================================================================")

    # 1. Prepare directories
    os.makedirs(OUTPUT_BUILD_DIR, exist_ok=True)
    wiki_dir = os.path.join(OUTPUT_BUILD_DIR, "wiki_content")
    settings_dir = os.path.join(OUTPUT_BUILD_DIR, "course_settings")
    non_cc_dir = os.path.join(OUTPUT_BUILD_DIR, "non_cc_assessments")
    web_res_dir = os.path.join(OUTPUT_BUILD_DIR, "web_resources")
    syllabi_dir = os.path.join(web_res_dir, "syllabi")
    images_dir = os.path.join(web_res_dir, "images")
    os.makedirs(wiki_dir, exist_ok=True)
    os.makedirs(settings_dir, exist_ok=True)
    os.makedirs(non_cc_dir, exist_ok=True)
    os.makedirs(syllabi_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # 2. Assignment Groups
    group_labs_id = make_id("group_labs")
    group_quizzes_id = make_id("group_quizzes")
    group_prep_id = make_id("group_prep")
    group_capstone_id = make_id("group_capstone")

    assign_groups_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<assignmentGroups xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <assignmentGroup identifier="{group_labs_id}">
    <title>Hands-on SQL Labs</title>
    <position>1</position>
    <group_weight>40.0</group_weight>
  </assignmentGroup>
  <assignmentGroup identifier="{group_quizzes_id}">
    <title>Unit Knowledge Checks &amp; Quizzes</title>
    <position>2</position>
    <group_weight>20.0</group_weight>
  </assignmentGroup>
  <assignmentGroup identifier="{group_prep_id}">
    <title>Asynchronous Preparation &amp; Drills</title>
    <position>3</position>
    <group_weight>10.0</group_weight>
  </assignmentGroup>
  <assignmentGroup identifier="{group_capstone_id}">
    <title>Comprehensive Course Capstone</title>
    <position>4</position>
    <group_weight>30.0</group_weight>
  </assignmentGroup>
</assignmentGroups>
"""
    with open(os.path.join(settings_dir, "assignment_groups.xml"), "w", encoding="utf-8") as f:
        f.write(assign_groups_xml)

    # 3. Canvas Course Export Signature Files
    with open(os.path.join(settings_dir, "canvas_export.txt"), "w", encoding="utf-8") as f:
        f.write("Q: What did the panda say when he was forced out of his natural habitat?\nA: This is un-BEAR-able\n")

    context_xml = """<?xml version="1.0" encoding="UTF-8"?>
<context_info xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <course_name>CMAP 1815: Introduction to Modern SQL</course_name>
  <root_account_id>105390000000000001</root_account_id>
  <root_account_name>Laramie County Community College</root_account_name>
  <root_account_uuid>dOSfRmBEqg50Ei3MOkNZrYHbdOlZxhVp0XEVGbQX</root_account_uuid>
  <canvas_domain>lccc-wy.instructure.com</canvas_domain>
</context_info>
"""
    with open(os.path.join(settings_dir, "context.xml"), "w", encoding="utf-8") as f:
        f.write(context_xml)

    with open(os.path.join(settings_dir, "files_meta.xml"), "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<fileMeta xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <folders></folders>
  <files></files>
</fileMeta>
""")

    course_id = make_id("cmap_1815_course")
    course_settings_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<course identifier="{course_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>CMAP 1815: Introduction to Modern SQL</title>
  <course_code>CMAP 1815</course_code>
  <is_public>false</is_public>
  <default_view>wiki</default_view>
  <license>private</license>
  <grading_standard_enabled>true</grading_standard_enabled>
  <root_account_uuid>dOSfRmBEqg50Ei3MOkNZrYHbdOlZxhVp0XEVGbQX</root_account_uuid>
</course>
"""
    with open(os.path.join(settings_dir, "course_settings.xml"), "w", encoding="utf-8") as f:
        f.write(course_settings_xml)

    # Copy Word Document Syllabus to web_resources/syllabi
    src_docx = os.path.join(COURSE_SPECS_DIR, "CMAP_1815_Master_Syllabus.docx")
    dst_docx_name = "CMAP 1815 Syllabus Fall 2026 - Swarm.docx"
    dst_docx_path = os.path.join(syllabi_dir, dst_docx_name)
    if os.path.exists(src_docx):
        with open(src_docx, "rb") as sf, open(dst_docx_path, "wb") as df:
            df.write(sf.read())

    # Copy Course Banner & Thumbnail Images to web_resources/images
    src_banner = os.path.join(COURSE_SPECS_DIR, "sql_course_banner.jpg")
    dst_banner = os.path.join(images_dir, "sql_course_banner.jpg")
    if os.path.exists(src_banner):
        with open(src_banner, "rb") as sf, open(dst_banner, "wb") as df:
            df.write(sf.read())

    src_thumb = os.path.join(COURSE_SPECS_DIR, "sql_course_thumbnail.jpg")
    dst_thumb = os.path.join(images_dir, "sql_course_thumbnail.jpg")
    if os.path.exists(src_thumb):
        with open(src_thumb, "rb") as sf, open(dst_thumb, "wb") as df:
            df.write(sf.read())

    # Build Native Syllabus HTML
    syllabus_body = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Syllabus</title>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper dp-hdg-i-cp-brdr-h2-dp-primary dp-hdg-txt-h3-dp-primary dp-hdg-txt-h4-dp-primary dp-hdg-txt-h5-dp-primary dp-hdg-i-cp-brdr-h5-dp-primary dp-hdg-b-h2-brdr-b dp-hdg-txt-h6-dp-primary dp-hdg-i-cp-brdr-h6-dp-primary dp-hdg-i-styl-h2-pill dp-hdg-i-styl-h3-pill dp-hdg-cp-brdr-h3-dp-secondary dp-hdg-cp-brdr-h2-dp-secondary dp-hdg-brdr-h2-1 dp-hdg-brdr-h3-1 dp-hdg-brdr-h4-1 dp-hdg-brdr-h5-1 dp-hdg-brdr-h6-1 dp-hdg-i-sz-h2-fill dp-hdg-i-sz-h3-fill dp-hdg-i-sz-h5-fill dp-hdg-i-sz-h6-fill dp-hdg-i-brdr-h5-2 dp-hdg-i-brdr-h6-2 dp-hdg-b-h3-brdr-b dp-hdg-txt-h2-dp-primary dp-hdg-i-brdr-h2-1 dp-hdg-i-brdr-h3-1 dp-hdg-i-sz-h4-fill dp-hdg-i-cp-brdr-h3-dp-primary dp-hdg-i-brdr-h4-1 dp-hdg-i-bg-h2-dp-primary dp-hdg-i-bg-h3-dp-primary dp-hdg-b-h4-brdr-b dp-hdg-d-h4-table-l dp-hdg-i-styl-h4-pill dp-hdg-i-cp-brdr-h4-dp-primary">
<div class="dp-content-block">
<div class="dp-action-item dp-action-item-block dp-action-item-note dp-locked" style="display: none;" aria-hidden="true">
<p><em>Welcome to your Syllabus! This page was designed with the guidance of QM Standard: <strong>SRS1.4</strong>.</em></p>
</div>
<header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
<h2 class="dp-heading dp-locked"><span class="dp-header-title">Course Syllabus</span></h2>
</header>
<p>&nbsp;</p>
<h3 class="dp-has-icon dp-locked"><i class="far fa-file-alt"><span class="dp-icon-content" style="display: none;">&nbsp;</span></i> <span>Downloadable Syllabus</span></h3>
<p><span>The syllabus is a comprehensive guide to this course. It outlines class expectations, grading policy, course learning outcomes, and institutional policies. Review your syllabus carefully, and ask questions of your instructor to make sure your understanding is clear.</span></p>
<p><a class="instructure_file_link instructure_scribd_file inline_disabled" title="{dst_docx_name}" href="$IMS-CC-FILEBASE$/syllabi/{dst_docx_name.replace(' ', '%20')}?canvas_=1&amp;canvas_qs_wrap=1" target="_blank">Download Master Syllabus (Word .docx)</a></p>
<hr>
<h3 class="dp-has-icon dp-locked"><i class="far fa-check-circle"><span class="dp-icon-content" style="display: none;">&nbsp;</span></i><span style="color: var(--bs-heading-color); font-size: calc(1.3rem + 0.6vw);">Grade Scale &amp; Evaluation Breakdown</span></h3>
<hr>
<ul>
  <li><strong>Hands-on SQL Labs (40%):</strong> Weekly verified SQL scripts submitted and executed against PostgreSQL 16.</li>
  <li><strong>Unit Knowledge Checks &amp; Quizzes (20%):</strong> 15-question concept assessments testing syntax, relational logic, and traps.</li>
  <li><strong>Asynchronous Preparation &amp; AI Participation (10%):</strong> Pre-lab self-check drills and weekly discussion tasks.</li>
  <li><strong>Comprehensive Course Capstone (30%):</strong> Production 3NF schema design, DDL constraints, ETL staging, and index tuning defense.</li>
</ul>
<p><strong>LCCC Standard Grading Scale:</strong></p>
<p>A: 90 – 100%</p>
<p>B: 80 – 89%</p>
<p>C: 70 – 79%</p>
<p>D: 60 – 69%</p>
<p>F: 0 – 59%</p>
<p>&nbsp;</p>
<h3 class="dp-has-icon dp-locked"><i class="far fa-clock"><span class="dp-icon-content" style="display: none;">&nbsp;</span></i><span>Late Grading Policy</span></h3>
<p>Assignments, projects, and lab work should be turned in by the designated due date. Submissions will not be accepted late unless prior arrangements have been made with the instructor or accommodations have been issued by Disability Services.</p>
<hr class="dp-hr-solid-light">
<p><a class="btn btn-dp-primary btn-block cph-bg-dp-accent dp-locked" href="https://www.lccc.wy.edu/life/handbook/index.aspx#welcome" target="_blank">LCCC Student Handbook &amp; Policies</a></p>
<p>&nbsp;</p>
</div>
<p>&nbsp;</p>
</div>
</body>
</html>"""
    with open(os.path.join(settings_dir, "syllabus.html"), "w", encoding="utf-8") as f:
        f.write(syllabus_body)

    # 4. Generate Course Welcome & Orientation Pages in wiki_content
    pages_manifest = []       # List of (filename, title, ident)
    modules_data = []         # Modules for module_meta.xml and imsmanifest.xml
    assignment_manifest = []  # List of (assign_id, folder_name, html_file, title)
    quiz_manifest = []        # List of (quiz_id, quiz_meta_id, title)
    discussions_manifest = [] # List of (disc_id, disc_title, disc_file)

    # Pre-generate Module IDs so Home Page accordion can reference them
    mod_orient_id = make_id("module_orientation")
    unit_mod_ids = {u["num"]: make_id(f"module_u{u['num']}") for u in UNIT_METADATA}

    # Page: Start Here (start-here.html)
    p_start_here_id = make_id("page_start_here")
    p_start_here_file = "start-here.html"
    start_here_html = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Start Here: Course Overview &amp; Orientation</title>
<meta name="identifier" content="{p_start_here_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="active"/>
<meta name="editor_type" content="rce"/>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper dp-hdg-i-cp-brdr-h2-dp-primary dp-hdg-txt-h3-dp-primary dp-hdg-txt-h4-dp-primary dp-hdg-txt-h5-dp-primary dp-hdg-i-cp-brdr-h5-dp-primary dp-hdg-b-h2-brdr-b dp-hdg-txt-h6-dp-primary dp-hdg-i-cp-brdr-h6-dp-primary dp-hdg-i-styl-h2-pill dp-hdg-i-styl-h3-pill dp-hdg-cp-brdr-h3-dp-secondary dp-hdg-cp-brdr-h2-dp-secondary dp-hdg-brdr-h2-1 dp-hdg-brdr-h3-1 dp-hdg-brdr-h4-1 dp-hdg-brdr-h5-1 dp-hdg-brdr-h6-1 dp-hdg-i-sz-h2-fill dp-hdg-i-sz-h3-fill dp-hdg-i-sz-h5-fill dp-hdg-i-sz-h6-fill dp-hdg-i-brdr-h5-2 dp-hdg-i-brdr-h6-2 dp-hdg-b-h3-brdr-b dp-hdg-txt-h2-dp-primary dp-hdg-i-brdr-h2-1 dp-hdg-i-brdr-h3-1 dp-hdg-i-sz-h4-fill dp-hdg-i-cp-brdr-h3-dp-primary dp-hdg-i-brdr-h4-1 dp-hdg-i-bg-h2-dp-primary dp-hdg-i-bg-h3-dp-primary dp-hdg-b-h4-brdr-b dp-hdg-d-h4-table-l dp-hdg-i-styl-h4-pill dp-hdg-i-cp-brdr-h4-dp-primary">
  <div class="dp-action-item dp-action-item-block dp-action-item-note dp-locked" style="display: none;" aria-hidden="true">
    <p><em>Welcome to your Course Overview Page! This page was designed with the guidance of QM Standards: <strong>SRS1.2, SRS1.3, SRS1.5, SRS1.6, SRS1.7, SRS1.8, SRS1.9</strong>.</em></p>
  </div>
  <header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
    <h2 class="dp-heading dp-locked"><span class="dp-header-title">Course Overview &amp; Orientation</span></h2>
    <p>&nbsp;</p>
  </header>
  <div class="dp-content-block">
    <p><strong>Welcome to CMAP 1815: Introduction to Modern SQL!</strong> This 100% asynchronous course provides comprehensive training in professional relational database engineering using modern PostgreSQL 16.</p>
    <p>You will gain mastery through guided tutorials, embedded micro-video lectures, hands-on SQL laboratory assignments with direct Canvas check-in, supplemental AI practice, and weekly knowledge checks.</p>
  </div>
  <div class="dp-panels-wrapper dp-accordion-plus dp-panel-color-dp-primary dp-panel-active-color-dp-accent dp-panel-hover-color-dp-accent">
    <div class="dp-panel-group">
      <h3 class="dp-panel-heading dp-has-icon dp-locked"><i class="far fa-compass"></i>&nbsp; How to Navigate this Course</h3>
      <div class="dp-panel-content">
        <ul>
          <li><strong>Home:</strong> Returns to the course landing page with the interactive module accordion.</li>
          <li><strong>Modules:</strong> The primary hub of the course where all weekly readings, labs, assignments, and quizzes are organized in sequence.</li>
          <li><strong>Syllabus:</strong> Download your master Word (.docx) syllabus and review grading criteria.</li>
          <li><strong>Grades:</strong> Track your weekly scores and instructor feedback across labs and quizzes.</li>
        </ul>
      </div>
    </div>
    <div class="dp-panel-group">
      <h3 class="dp-panel-heading dp-has-icon dp-locked"><i class="fas fa-paperclip"></i>&nbsp; Required Resources (Zero-Cost Model)</h3>
      <div class="dp-panel-content">
        <p>There are <strong>zero textbook costs</strong> for this course. All tools and reading materials are 100% free and open-access:</p>
        <ul>
          <li><strong>PostgreSQL 16 in GitHub Codespaces:</strong> Pre-configured cloud Linux database environment with psql.</li>
          <li><strong>Authoritative Documentation:</strong> Neon PostgreSQL Tutorial (neon.tech) and official PostgreSQL 16 manuals.</li>
          <li><strong>Curated Video Lectures:</strong> High-definition video chapters embedded directly into each unit module.</li>
        </ul>
      </div>
    </div>
    <div class="dp-panel-group">
      <h3 class="dp-panel-heading dp-has-icon dp-locked"><i class="fas fa-tasks"></i>&nbsp; Hands-on SQL Labs &amp; Assignment Check-in</h3>
      <div class="dp-panel-content">
        <p>Each unit includes a dedicated <strong>Applied SQL Lab Assignment</strong> in Canvas where you will submit your verified queries. You can submit your work by uploading your <code>.sql</code> script or pasting your code directly into Canvas SpeedGrader for automated and instructor review.</p>
      </div>
    </div>
    <div class="dp-panel-group">
      <h3 class="dp-panel-heading dp-has-icon dp-locked"><i class="far fa-comment-dots"></i>&nbsp; Communication Expectations &amp; Support</h3>
      <div class="dp-panel-content">
        <p>Regular announcements will be broadcast via Canvas. For questions and assistance:</p>
        <ul>
          <li>Use the <strong>Canvas Inbox</strong> for private questions regarding grades.</li>
          <li>Participate in the <strong>Unit Discussion Boards</strong> for peer collaboration and AI practice debriefs.</li>
          <li>Virtual office hours links are available in our Course Orientation module.</li>
        </ul>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""
    with open(os.path.join(wiki_dir, p_start_here_file), "w", encoding="utf-8") as f:
        f.write(start_here_html)
    pages_manifest.append((p_start_here_file, "Start Here: Course Overview & Orientation", p_start_here_id))

    # Page: Front Page (home-page.html)
    p_home_id = make_id("page_home_front")
    p_home_file = "home-page.html"
    
    # Generate Front Page Module Accordion Links
    mod_links_lis = [
        f'<li><a class="list-group-item list-group-item-action" href="$CANVAS_OBJECT_REFERENCE$/modules/{mod_orient_id}"><i class="fas fa-map-marker-alt"></i> Getting Started - Course Orientation</a></li>'
    ]
    for unit in UNIT_METADATA:
        u_num = unit["num"]
        u_title = unit["title"]
        m_id = unit_mod_ids[u_num]
        mod_links_lis.append(f'<li><a class="list-group-item list-group-item-action" href="$CANVAS_OBJECT_REFERENCE$/modules/{m_id}"><i class="fas fa-map-marker-alt"></i> {html.escape(u_title)}</a></li>')
    
    mod_links_joined = "\n".join(mod_links_lis)

    home_html = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Home Page</title>
<meta name="identifier" content="{p_home_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="active"/>
<meta name="front_page" content="true"/>
<meta name="editor_type" content="rce"/>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper dp-hdg-i-cp-brdr-h2-dp-primary dp-hdg-txt-h3-dp-primary dp-hdg-txt-h4-dp-primary dp-hdg-txt-h5-dp-primary dp-hdg-i-cp-brdr-h5-dp-primary dp-hdg-b-h2-brdr-b dp-hdg-txt-h6-dp-primary dp-hdg-i-cp-brdr-h6-dp-primary dp-hdg-i-styl-h2-pill dp-hdg-i-styl-h3-pill dp-hdg-cp-brdr-h3-dp-secondary dp-hdg-cp-brdr-h2-dp-secondary dp-hdg-brdr-h2-1 dp-hdg-brdr-h3-1 dp-hdg-brdr-h4-1 dp-hdg-brdr-h5-1 dp-hdg-brdr-h6-1 dp-hdg-i-sz-h2-fill dp-hdg-i-sz-h3-fill dp-hdg-i-sz-h5-fill dp-hdg-i-sz-h6-fill dp-hdg-i-brdr-h5-2 dp-hdg-i-brdr-h6-2 dp-hdg-b-h3-brdr-b dp-hdg-txt-h2-dp-primary dp-hdg-i-brdr-h2-1 dp-hdg-i-brdr-h3-1 dp-hdg-i-sz-h4-fill dp-hdg-i-cp-brdr-h3-dp-primary dp-hdg-i-brdr-h4-1 dp-hdg-i-bg-h2-dp-primary dp-hdg-i-bg-h3-dp-primary dp-hdg-b-h4-brdr-b dp-hdg-d-h4-table-l dp-hdg-i-styl-h4-pill dp-hdg-i-cp-brdr-h4-dp-primary">
  <div class="dp-action-item dp-action-item-block dp-action-item-note dp-locked" style="display: none;" aria-hidden="true">
    <p><em>Welcome to your Home Page! This page was designed with the guidance of QM Standards: <strong>SRS1.1, SRS7.1, SRS7.2, SRS7.3, SRS7.4</strong>.</em></p>
  </div>
  <div id="dp-wrapper_1" class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
    <header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
      <h1 class="dp-heading"><span class="dp-header-pre"><span class="dp-header-pre-1">CMAP 1815</span></span><span class="dp-header-title">Introduction to Modern SQL</span></h1>
    </header>
  </div>
  <div class="dp-banner-image" style="text-align: center; margin: 1rem 0;"><img role="presentation" src="$IMS-CC-FILEBASE$/images/sql_course_banner.jpg" alt="CMAP 1815: Introduction to Modern SQL Course Banner" width="1100" height="220" style="max-width: 100%; height: auto; border-radius: 6px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);" loading="lazy"></div>
  <nav class="dp-link-grid container-fluid dp-link-grid-item-s-rounded dp-link-grid-item-bg-dp-primary dp-link-grid-hover-dp-accent dp-link-grid-icon-s-brdr-r dp-link-grid-icon-brdr-dp-secondary dp-link-grid-icon-brdr-w-2">
    <ul class="row">
      <li class="col-sm-12 col-md-4 col-lg-4"><a title="Course Overview" href="$WIKI_REFERENCE$/pages/{p_start_here_id}" data-course-type="wikiPages"><i class="fas fa-flag" aria-hidden="true"></i> Course Overview</a></li>
      <li class="col-sm-12 col-md-4 col-lg-4"><a title="Syllabus" href="$CANVAS_COURSE_REFERENCE$/assignments/syllabus" data-course-type="navigation"><i class="fas fa-file-alt" aria-hidden="true"></i> Syllabus</a></li>
      <li class="col-sm-12 col-md-4 col-lg-4"><a class="dp-has-icon" href="https://lcccwy.sharepoint.com/sites/StudentSuccessResources" target="_blank"><i class="fas fa-external-link-alt" aria-hidden="true"></i> Student Resources</a></li>
    </ul>
  </nav>
  <div class="dp-content-block">
    <p style="text-align: left;"><strong>Welcome to CMAP 1815: Introduction to Modern SQL! Please review the Course Overview, Syllabus, and Student Resources above to get started.</strong></p>
  </div>
  <div class="dp-module-list dp-module-list-flag-completed dp-module-list-show-locked dp-quick-links-panels-accordion-plus dp-auto-update dp-panel-color-dp-primary dp-panel-active-color-dp-accent dp-panel-hover-color-dp-accent dp-quick-links-all dp-module-list-current-none">
    <nav class="dp-module-list-item-group">
      <ul class="fa-ul list-group">
{mod_links_joined}
      </ul>
    </nav>
  </div>
</div>
</body>
</html>"""
    with open(os.path.join(wiki_dir, p_home_file), "w", encoding="utf-8") as f:
        f.write(home_html)
    pages_manifest.append((p_home_file, "Home Page", p_home_id))

    # Page: Orientation - Learn with AI
    p_orient_ai_id = make_id("page_orient_learn_with_ai")
    p_orient_ai_file = "orientation-learn-with-ai.html"
    orient_ai_lead = "<p>In CMAP 1815, artificial intelligence is an interactive co-pilot and code reviewer—not a shortcut to avoid critical thinking. This guide introduces how we practice with 100% free conversational AI tools.</p>"
    orient_ai_panels = [
        ("The AI Pair Programmer Philosophy",
         "<p>Writing SQL with AI is NOT about asking an AI to 'do the homework for you.' Blindly pasting AI-generated SQL into production environments causes catastrophic data outages, Cartesian product server crashes, and silent NULL propagation bugs.</p><p>Instead, in this course you will practice <strong>Active Socratic Learning with AI</strong>: you will assign the AI specialized roles to challenge your reasoning, test edge cases, and simulate real-world stakeholder requests.</p>"),
        ("The Big Four 100% Free AI Platforms",
         "<p>Every AI exercise in this course is designed for <strong>100% free web chat tools</strong>. You do NOT need any paid account or API key:</p><ul><li><strong>ChatGPT Free:</strong> <a href='https://chatgpt.com' target='_blank' rel='noopener'>chatgpt.com</a> (select GPT-4o-mini / Free tier).</li><li><strong>Claude Free:</strong> <a href='https://claude.ai' target='_blank' rel='noopener'>claude.ai</a> (free web tier).</li><li><strong>Google Gemini Free:</strong> <a href='https://gemini.google.com' target='_blank' rel='noopener'>gemini.google.com</a> (free with any Google account).</li><li><strong>Microsoft Copilot Free:</strong> <a href='https://copilot.microsoft.com' target='_blank' rel='noopener'>copilot.microsoft.com</a> (free web chat).</li></ul>"),
        ("The Permission to Struggle: How to Learn with Your AI Partner",
         """<p>The weekly AI practice drills are <strong>intentionally challenging, high-friction Socratic exercises</strong> designed to expose subtle relational traps and deepen your conceptual mastery. You are NOT expected to know all the answers immediately!</p>
<p>When interacting with the AI, remember that it is always completely okay and encouraged to:</p>
<ul style="line-height: 1.8;">
  <li><strong>Say "I don't know" or "I'm stuck":</strong> The AI is acting as your tutor. If you don't know where to start, tell it!</li>
  <li><strong>Ask for Explanations &amp; Hints:</strong> Ask: <em>"Can you explain the underlying concept without giving me the code?"</em> or <em>"Give me a hint to get started."</em></li>
  <li><strong>Ask for Simpler Step-by-Step Breakdowns:</strong> If a prompt feels overwhelming, ask: <em>"Can you break this challenge down into smaller, simpler steps?"</em></li>
  <li><strong>Ask for More Practice Problems:</strong> If a concept (like Three-Valued Logic or Anti-Joins) feels tricky, ask: <em>"Can you give me another practice puzzle like this to make sure I've got it?"</em></li>
  <li><strong>Request Authoritative Web Resources:</strong> Ask: <em>"Where in the official PostgreSQL 16 documentation or free tutorials can I read more about this?"</em></li>
  <li><strong>Probe Edge Cases:</strong> Ask: <em>"What happens if our data contains NULLs, empty strings, or duplicate rows?"</em></li>
</ul>"""),
        ("The Human-On-The-Loop (HOTL) Verification Protocol Grounded in PostgreSQL 16",
         """<p>Never assume an AI's SQL answer is correct! The Golden Rule of CMAP 1815: <strong>Every single SQL snippet must be executed and verified against your live PostgreSQL 16 database in GitHub Codespaces before submission!</strong></p>
<div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.85rem 1.25rem; margin: 1rem 0; border-radius: 0 6px 6px 0;">
  <p style="margin: 0 0 0.5rem 0; font-weight: 600; color: #991b1b;"><i class="fas fa-shield-alt"></i> The Understanding &amp; Defense Requirement:</p>
  <p style="margin: 0 0 0.5rem 0; color: #7f1d1d; font-size: 0.95em;">You are 100% accountable for every query you submit. <strong>The instructor reserves the right to question any submission for evidence of understanding</strong>—including asking you to explain your query line-by-line, defend your choice of clauses or joins, or write an equivalent query on the fly.</p>
  <p style="margin: 0; color: #7f1d1d; font-size: 0.95em; font-weight: 600;">Do NOT submit work you don't fully understand or could not write yourself!</p>
</div>""")
    ]
    with open(os.path.join(wiki_dir, p_orient_ai_file), "w", encoding="utf-8") as f:
        f.write(render_standard_page_html("Orientation: Learn with AI — Course Guidelines & Free Tools", orient_ai_lead, orient_ai_panels, p_orient_ai_id))
    pages_manifest.append((p_orient_ai_file, "Orientation: Learn with AI — Course Guidelines & Free Tools", p_orient_ai_id))

    # Page: Student Guide: How to Complete & Submit Weekly SQL Labs
    p_setup_id = make_id("page_db_setup")
    p_setup_file = "database-setup-guide.html"
    setup_lead = "<p>Welcome to your hands-on SQL laboratory! In CMAP 1815, you will write and execute queries against a live, industry-standard <strong>PostgreSQL 16</strong> database running in your browser via <strong>GitHub Codespaces</strong>. This guide walks you through launching your environment, querying visually or via terminal, using starter files, and submitting your weekly lab work.</p>"
    setup_panels = [
        ("🚀 Step 1: Create Your Personal Student Repository",
         """<p>Before launching Codespaces, create your own copy of the course template repository:</p>
<ol style="line-height: 1.7;">
  <li>Navigate to the template repository: <a href="https://github.com/tswarmLCCC/CMAP-1815-Student-Sandbox" target="_blank" rel="noopener" style="color: #2563eb; font-weight: 600;">github.com/tswarmLCCC/CMAP-1815-Student-Sandbox</a>.</li>
  <li>Click the green <strong>Use this template</strong> button at the top right &rarr; select <strong>Create a new repository</strong>.</li>
  <li>Name your repository (e.g. <code>CMAP-1815-Student-Sandbox</code>) and set visibility to <strong>Private</strong>. Click <strong>Create repository</strong>.</li>
</ol>
<div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.75rem 1rem; margin-top: 1rem; border-radius: 0 4px 4px 0;">
  <strong style="color: #991b1b;"><i class="fas fa-exclamation-triangle"></i> CRITICAL WARNING — DO NOT WORK IN THE BASE TEMPLATE:</strong>
  <p style="margin: 0.25rem 0 0 0; color: #7f1d1d; font-size: 0.95em;">Always launch and resume Codespaces from <strong>YOUR OWN personal repository</strong> (verify your username is in the URL). If you work in the instructor's base template, you cannot push git commits, and your work will be permanently deleted when the container shuts down!</p>
</div>"""),
        ("💻 Step 2: Launching & Resuming Your Codespace",
         """<h4 style="color: #1e3a8a; margin-top: 0.5rem;">First-Time Launch:</h4>
<ol style="line-height: 1.7;">
  <li>In <strong>your personal repository</strong> on GitHub, click the green <strong>Code</strong> button &rarr; select the <strong>Codespaces</strong> tab &rarr; click <strong>Create codespace on main</strong>.</li>
  <li>Wait ~90 seconds while GitHub provisions your container. When the terminal prints <code>CMAP 1815: Modern SQL Student Sandbox Ready!</code>, your environment is live!</li>
</ol>

<h4 style="color: #1e3a8a; margin-top: 1.25rem;">Resuming Work in Future Sessions:</h4>
<p style="margin-bottom: 0.5rem;">Do NOT create a new Codespace every time you study! To return to your existing work:</p>
<ol style="line-height: 1.7;">
  <li>Return to <strong>your personal repository</strong> on GitHub &rarr; click <strong>Code</strong> &rarr; <strong>Codespaces</strong> &rarr; click your existing Codespace.</li>
  <li>Or navigate to <a href="https://github.com/codespaces" target="_blank" rel="noopener" style="color: #2563eb;">github.com/codespaces</a> to see all active/stopped environments.</li>
</ol>

<div style="background: #f0fdf4; border-left: 4px solid #16a34a; padding: 0.75rem 1rem; margin-top: 1rem; border-radius: 0 4px 4px 0;">
  <strong>💡 Conserving Cloud Hours &amp; Auto-Suspension:</strong>
  <ul style="margin: 0.35rem 0 0 0; padding-left: 1.25rem; font-size: 0.95em;">
    <li>Codespaces automatically suspends itself after <strong>30 minutes of inactivity</strong> to prevent hour runaway.</li>
    <li>Personal accounts get 60 free hours/month. Claim the <a href="https://education.github.com/pack" target="_blank" rel="noopener" style="color: #15803d; text-decoration: underline;">GitHub Student Developer Pack</a> with your <code>.edu</code> email for <strong>180 free hours/month</strong>!</li>
    <li>To stop manually when finished: press <code>Ctrl+Shift+P</code> &rarr; select <code>Codespaces: Stop Current Codespace</code>, or close the browser tab.</li>
  </ul>
</div>"""),
        ("🛠️ Step 3: Two Ways to Query PostgreSQL",
         """<h4 style="color: #1e3a8a; margin-top: 0.5rem;">Option A: The Visual GUI (SQLTools Sidebar) — Recommended for Exploring</h4>
<ol style="line-height: 1.7;">
  <li>Click the <strong>Database (cylinder) icon</strong> on the far-left sidebar of VS Code.</li>
  <li>Under the <strong>CONNECTIONS</strong> section, click <strong>cmap1815</strong> &rarr; <strong>Connect</strong>.</li>
  <li>Expand <code>cmap1815</code> &rarr; <code>public</code> &rarr; <code>Tables</code> to inspect: <code>employees</code>, <code>locations</code>, <code>products</code>, <code>orders</code>, and <code>order_lines</code>.</li>
  <li>Click on any table to view columns, types, and primary keys, or click <strong>Show Table Records</strong> to preview data!</li>
</ol>

<h4 style="color: #1e3a8a; margin-top: 1.25rem;">Option B: The Terminal CLI (psql) — Recommended for Fast Query Testing</h4>
<ol style="line-height: 1.7;">
  <li>Open the integrated terminal in VS Code (press <code>Ctrl + `</code>).</li>
  <li>Type <code>psql</code> and press Enter to enter the interactive shell at the <code>cmap1815=#</code> prompt.</li>
  <li>Run any query: <code>SELECT first_name, last_name, salary FROM employees LIMIT 5;</code></li>
  <li>Type <code>\\q</code> and press Enter to exit back to bash.</li>
</ol>"""),
        ("💾 Step 4: Saving Query Outputs (Terminal & GUI)",
         """<h4 style="color: #1e3a8a; margin-top: 0.5rem;">Saving Output from the Terminal (psql):</h4>
<ul style="line-height: 1.7; padding-left: 1.25rem;">
  <li><strong>Inside psql with <code>\\o</code>:</strong> Type <code>\\o lab1_output.txt</code>, run your query, then type <code>\\o</code> to close file redirection.</li>
  <li><strong>From bash command line:</strong> Run <code>psql -U postgres -d cmap1815 -c "SELECT * FROM employees;" > employees_export.txt</code>.</li>
</ul>

<h4 style="color: #1e3a8a; margin-top: 1.25rem;">Saving Output from SQLTools GUI:</h4>
<ul style="line-height: 1.7; padding-left: 1.25rem;">
  <li>After running a query, the <strong>SQLTools Results</strong> panel displays the grid.</li>
  <li>Click <strong>Export Results</strong> (or the download icon) in the Results toolbar &rarr; choose <strong>Save as CSV</strong> or <strong>Save as JSON</strong>.</li>
  <li>Click <strong>Copy All</strong> or select rows and right-click &rarr; <strong>Copy</strong> to paste output directly into notes or submission comments.</li>
</ul>"""),
        ("📝 Step 5: The 5-Step Weekly Lab Submission Workflow (100 Points Total)",
         """<ol style="line-height: 1.8;">
  <li><strong>Open Starter Template:</strong> In the VS Code file explorer, open <code>units/{current_unit}/lab{N}_starter.sql</code> (or copy the starter template code block from Canvas).</li>
  <li><strong>Write &amp; Verify Every Query:</strong> Write your SQL statements beneath each challenge block. Run every query against PostgreSQL to ensure zero errors.</li>
  <li><strong>Format to Standards:</strong> Keywords in <strong>UPPERCASE</strong> (<code>SELECT</code>, <code>FROM</code>, <code>WHERE</code>, <code>AS</code>), clauses on new lines, and computed columns aliased with <code>AS snake_case</code>.</li>
  <li><strong>Commit &amp; Push to GitHub:</strong> In the terminal, run: <code>git add . &amp;&amp; git commit -m "Complete Lab {N}" &amp;&amp; git push origin main</code>. This permanently secures your work in the cloud.</li>
  <li><strong>Submit to Canvas:</strong> Save as <code>lab{N}_yourlastname.sql</code>, right-click &rarr; <strong>Download...</strong>, and upload the <code>.sql</code> file to the weekly Canvas Lab Assignment for SpeedGrader evaluation (100 Points).</li>
</ol>"""),
        ("🔄 Step 6: Disaster Recovery (./reset_database.sh)",
         """<p>Accidentally delete a table or corrupt rows during an experiment? Don't panic! You can restore all pristine tables in 2 seconds:</p>
<div style="background: #0f172a; color: #f8fafc; padding: 0.5rem 0.75rem; border-radius: 4px; font-family: Consolas, monospace; margin: 0.5rem 0;"><pre style="margin: 0; background: transparent; color: inherit;"><code>./reset_database.sh</code></pre></div>
<p style="color: #475569; font-size: 0.9em; margin-bottom: 0;">This script drops and recreates all starter tables (employees, locations, products, orders, order_lines). <strong>It will NOT delete your <code>.sql</code> files in your repository.</strong></p>""")
    ]
    with open(os.path.join(wiki_dir, p_setup_file), "w", encoding="utf-8") as f:
        f.write(render_standard_page_html("Student Guide: How to Complete & Submit Weekly SQL Labs", setup_lead, setup_panels, p_setup_id))
    pages_manifest.append((p_setup_file, "Student Guide: How to Complete & Submit Weekly SQL Labs", p_setup_id))

    # Page: Student Guide - Navigating Codespaces & SQLTools
    p_codespace_guide_id = make_id("page_student_codespace_guide")
    p_codespace_guide_file = "student-codespaces-sqltools-guide.html"
    codespace_lead = "<p>A visual, step-by-step walkthrough for launching your cloud development environment, browsing relational tables with the <strong>SQLTools</strong> GUI, executing live queries with <code>Ctrl+Enter</code>, using the <code>psql</code> terminal, and submitting weekly lab assignments.</p>"
    codespace_panels = [
        ("1. Launching Your Codespace & Interface Layout",
         "<p>In CMAP 1815, you have an entire Linux cloud workstation with PostgreSQL 16 and VS Code pre-configured—zero local software installation required!</p>"
         "<ol><li>Open your personal student sandbox repository on GitHub.</li>"
         "<li>Click the green <strong>Code</strong> button &rarr; select the <strong>Codespaces</strong> tab &rarr; click <strong>Create codespace on main</strong>.</li>"
         "<li>Your Codespace will open in any modern web browser. The primary workspace areas are:</li></ol>"
         "<ul><li><strong>Activity Bar (Far Left):</strong> Access the File Explorer (📁), Search (🔍), Git Source Control (🔀), and the <strong>SQLTools Database Manager</strong> (stacked cylinder icon).</li>"
         "<li><strong>Editor (Center/Top):</strong> Where you write, format, and execute your SQL queries.</li>"
         "<li><strong>Panel Area (Bottom):</strong> Displays interactive <strong>SQLTools Results</strong> tables and the integrated Linux <strong>Terminal</strong> (<code>Ctrl + `</code>).</li></ul>"),
        
        ("2. Connecting & Browsing Tables with SQLTools",
         "<p><strong>SQLTools</strong> is your built-in graphical database client (similar to DBeaver or pgAdmin):</p>"
         "<ol><li>Click the <strong>SQLTools icon</strong> (database cylinder) in the far-left Activity Bar.</li>"
         "<li>In the <strong>CONNECTIONS</strong> panel, locate the pre-configured connection (<strong>cmap1815</strong> or <strong>mydb</strong>).</li>"
         "<li>Click the connection name or the plug icon to connect. A green indicator confirms you are active!</li>"
         "<li>Expand the connection &rarr; expand <code>public</code> &rarr; expand <code>Tables</code>. You will see all 5 core tables: <code>employees</code>, <code>locations</code>, <code>products</code>, <code>orders</code>, and <code>order_lines</code>.</li>"
         "<li>Expand any table's <code>Columns</code> folder to inspect column names, types (e.g. <code>varchar</code>, <code>numeric</code>, <code>integer</code>), and primary keys.</li>"
         "<li>Click the small table icon next to any table name to instantly view a 50-row data preview!</li></ol>"),
        
        ("3. Writing & Executing Queries with Keyboard Shortcuts",
         "<p>Executing SQL in Codespaces is lightning-fast:</p>"
         "<ol><li>Open an existing query script (like <code>sql/week1_orientation.sql</code> or <code>sql/lab_solutions_annotated.sql</code>) or create a new file named <code>lab1_yourname.sql</code>.</li>"
         "<li>Type your query with keywords in <strong>UPPERCASE</strong> (<code>SELECT</code>, <code>FROM</code>, <code>WHERE</code>, <code>ORDER BY</code>).</li>"
         "<li>Place your text cursor anywhere inside the SQL statement.</li>"
         "<li>Press <strong>Ctrl + Enter</strong> (Windows / Linux / Chromebook) or <strong>Cmd + Enter</strong> (Mac) to execute! You can also click the floating <em>'Run on active connection'</em> link right above the query.</li>"
         "<li>The <strong>SQLTools Results</strong> panel immediately opens, displaying the live result table, column headers, and total row count. You can click column headers to sort, search within the results, or copy rows to your clipboard.</li></ol>"),
        
        ("4. Using the Integrated Terminal & psql",
         "<p>In addition to the visual GUI, you can interact with the PostgreSQL engine directly via the professional command-line utility, <strong>psql</strong>:</p>"
         "<ol><li>Open the terminal by pressing <strong>Ctrl + `</strong> (or menu: <strong>Terminal &rarr; New Terminal</strong>).</li>"
         "<li>Type <code>psql -U postgres -d cmap1815</code> (or <code>psql -U postgres</code>) and press Enter.</li></ol>"
         "<p><strong>Essential psql Meta-Commands:</strong></p>"
         "<table style='width: 100%; border-collapse: collapse; border: 1px solid #cbd5e1; margin: 1rem 0;'>"
         "<thead><tr style='background: #1e3a8a; color: #ffffff;'><th style='padding: 0.6rem 0.75rem; text-align: left; border: 1px solid #cbd5e1;'>Command</th><th style='padding: 0.6rem 0.75rem; text-align: left; border: 1px solid #cbd5e1;'>Name</th><th style='padding: 0.6rem 0.75rem; text-align: left; border: 1px solid #cbd5e1;'>Purpose</th></tr></thead>"
         "<tbody>"
         "<tr style='background: #ffffff;'><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'><code>\\l</code></td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>List Databases</td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>Displays all databases on the PostgreSQL instance.</td></tr>"
         "<tr style='background: #f8fafc;'><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'><code>\\dt</code></td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>List Tables</td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>Lists all user tables in the current schema.</td></tr>"
         "<tr style='background: #ffffff;'><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'><code>\\d [table]</code></td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>Describe Table</td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>Shows column types, nullability, defaults, and constraints (e.g., <code>\\d employees</code>).</td></tr>"
         "<tr style='background: #f8fafc;'><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'><code>\\x</code></td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>Expanded Display</td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>Toggles vertical record display (ideal for wide tables).</td></tr>"
         "<tr style='background: #ffffff;'><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'><code>\\q</code></td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>Quit</td><td style='padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1;'>Exits psql back to the bash terminal prompt.</td></tr>"
         "</tbody></table>"),
        
        ("5. Standard Lab Workflow & Submission Protocol",
         "<p>Follow this routine for every weekly laboratory assignment:</p>"
         "<ol><li><strong>Read the Lab Guide:</strong> Review the assignment objectives, scenarios, and challenge questions in Canvas.</li>"
         "<li><strong>Create Your Submission Script:</strong> In your Codespace Explorer, create a new file named <code>labX_yourname.sql</code> (e.g. <code>lab1_jane_doe.sql</code>).</li>"
         "<li><strong>Draft and Execute:</strong> Write each query one by one. Use <strong>Ctrl + Enter</strong> to test execution against live PostgreSQL.</li>"
         "<li><strong>Verify Outputs:</strong> Check your live row counts and data against the annotated lab solution reference (<code>sql/lab_solutions_annotated.sql</code>).</li>"
         "<li><strong>Save Frequently:</strong> Press <strong>Ctrl + S</strong> (Cmd + S on Mac) to save your work.</li>"
         "<li><strong>Submit to Canvas:</strong> Right-click your completed <code>.sql</code> file in the Codespace Explorer &rarr; select <strong>Download...</strong> &rarr; upload the file directly to the Canvas Applied SQL Lab Assignment!</li></ol>"),
        
        ("6. Troubleshooting & Emergency Database Reset",
         "<p><strong>Q: SQLTools says 'Connection Refused' or disconnects.</strong><br/>"
         "PostgreSQL runs inside your container. If it stopped, open the terminal (<code>Ctrl + `</code>) and run: <code>sudo service postgresql start</code>, then reconnect in SQLTools.</p>"
         "<p><strong>Q: I modified or corrupted table data during an experiment. How do I reset?</strong><br/>"
         "You can reset the entire database to factory condition in 2 seconds. Run this terminal command:<br/>"
         "<code style='background: #0f172a; color: #38bdf8; padding: 0.3rem 0.6rem; border-radius: 4px; display: inline-block; margin-top: 0.3rem;'>psql -U postgres -d cmap1815 -f sql/setup_chap1.sql</code></p>"
         "<p><strong>Q: My Codespace stopped after being idle. Did I lose my work?</strong><br/>"
         "No! Codespaces automatically suspends after 30 minutes of inactivity to save compute hours. All saved files and git commits are permanently stored on your persistent cloud volume. Simply click <strong>Restart Codespace</strong> to resume immediately.</p>")
    ]
    with open(os.path.join(wiki_dir, p_codespace_guide_file), "w", encoding="utf-8") as f:
        f.write(render_standard_page_html("Student Guide: Navigating Codespaces & SQLTools", codespace_lead, codespace_panels, p_codespace_guide_id))
    pages_manifest.append((p_codespace_guide_file, "Student Guide: Navigating Codespaces & SQLTools", p_codespace_guide_id))

    # Page: External Resources Guide
    p_res_id = make_id("page_resources")
    p_res_file = "external-resources-guide.html"
    res_lead = "<p>All external readings and video lectures in CMAP 1815 are 100% free and open-access. This page catalogs the verified URLs and exact video chapter timestamps.</p>"
    res_panels = [
        ("Authoritative FreeCodeCamp Video Chapters",
         "<p>Official PostgreSQL Course (Timestamps verified to video description):</p><ul><li><strong>Unit 1:</strong> What is a Database (0:03:16) &amp; Relational Databases (0:05:17)</li><li><strong>Unit 2:</strong> Comparison Operators (1:50:18) &amp; Handling NULLs (2:15:42)</li><li><strong>Unit 3:</strong> Primary Keys (2:31:23) &amp; Foreign Key Joins (3:16:41)</li><li><strong>Unit 4:</strong> Aggregate Functions (2:36:14) &amp; GROUP BY (2:45:30)</li><li><strong>Unit 5:</strong> INSERT Operations (0:55:55) &amp; Safe DELETE/UPDATE (2:54:45)</li><li><strong>Unit 7:</strong> CREATE TABLE (0:41:37) &amp; Constraints (0:49:12)</li><li><strong>Unit 8:</strong> Exporting Results to CSV (3:47:27)</li></ul>"),
        ("Authoritative PostgreSQL Tutorial Guides",
         "<p>All units link directly to the <a href='https://neon.tech/postgresql/tutorial/' target='_blank' rel='noopener'>Neon PostgreSQL Tutorial</a> and the <a href='https://www.postgresql.org/docs/current/' target='_blank' rel='noopener'>Official PostgreSQL 16 Documentation</a>.</p>")
    ]
    with open(os.path.join(wiki_dir, p_res_file), "w", encoding="utf-8") as f:
        f.write(render_standard_page_html("External Learning Resources & Media Guide", res_lead, res_panels, p_res_id))
    pages_manifest.append((p_res_file, "External Learning Resources & Media Guide", p_res_id))

    # Add Orientation Module
    modules_data.append({
        "id": mod_orient_id,
        "title": "Course Orientation & Database Setup",
        "items": [
            {"type": "WikiPage", "title": "Start Here: Course Overview & Orientation", "ref": p_start_here_id, "indent": 0, "state": "active"},
            {"type": "WikiPage", "title": "Orientation: Learn with AI — Course Guidelines & Free Tools", "ref": p_orient_ai_id, "indent": 1, "state": "active"},
            {"type": "WikiPage", "title": "Student Guide: How to Complete & Submit Weekly SQL Labs", "ref": p_setup_id, "indent": 1, "state": "active"},
            {"type": "WikiPage", "title": "Student Guide: Navigating Codespaces & SQLTools", "ref": p_codespace_guide_id, "indent": 1, "state": "active"},
            {"type": "WikiPage", "title": "External Learning Resources & Media Guide", "ref": p_res_id, "indent": 1, "state": "active"}
        ]
    })

    # 5. Generate Units 1 to 8 Pages, Canvas Assignments, Quizzes & Modules
    for unit in UNIT_METADATA:
        u_num = unit["num"]
        u_folder = unit["folder"]
        u_title = unit["title"]
        u_short = unit["short_title"]
        u_topic = unit["topic"]

        print(f"Processing {u_short} ({u_folder})...")

        # ----------------------------------------------------
        # Page 1: Unit Overview (DesignPLUS Ribbon Banner + Accordion)
        # ----------------------------------------------------
        overview_id = make_id(f"page_u{u_num}_overview")
        overview_file = f"unit-{u_num:02d}-overview.html"
        overview_lead = f"<p>Welcome to <strong>Unit {u_num}: {u_topic}</strong>. This unit focuses on mastering <em>{u_topic}</em> in modern PostgreSQL 16.</p><p>This overview guides you through the complete weekly learning sequence: review the assigned readings and embedded video lectures, complete the asynchronous preparatory drills, execute the applied hands-on SQL laboratory assignment, submit your work through Canvas, engage in supplemental AI practice, and complete the unit knowledge check.</p>"
        
        overview_panels = [
            ("Unit Learning Objectives", 
             f"<p>Upon completing this unit, you will be able to apply core competencies in <strong>{u_topic}</strong>, analyze relational schema relationships, and execute production-grade queries with verified precision.</p>"),
            ("Weekly Learning Sequence & Roadmap",
             f"""<ol>
  <li><strong>Required Readings &amp; Embedded Videos:</strong> Review the authoritative reading tutorials and watch the embedded video segments directly inside Canvas.</li>
  <li><strong>Asynchronous Preparation &amp; Drills:</strong> Complete the conceptual focus questions and self-check drills before starting your lab assignment.</li>
  <li><strong>Applied SQL Lab Assignment:</strong> Execute hands-on queries and scenario challenges against your live PostgreSQL 16 database.</li>
  <li><strong>Canvas Lab Turn-in:</strong> Submit your verified SQL script (<code>.sql</code>) or query answers through Canvas for grading.</li>
  <li><strong>Learn with AI (Supplemental Practice):</strong> Complete the interactive role-play prompt drill with a free AI assistant and post your findings to the weekly discussion board.</li>
  <li><strong>Unit Knowledge Check:</strong> Take the 15-question multiple-choice assessment to evaluate your mastery.</li>
</ol>"""),
            ("Time Budget & Contact Hours",
             f"<p>In accordance with our asynchronous curriculum model, each unit is budgeted for:</p><ul><li><strong>150 Minutes Guided Self-Study:</strong> Video micro-lectures, Neon PostgreSQL Tutorial readings, and formative self-check drills with expandable answers.</li><li><strong>150 Minutes Applied Laboratory Practice:</strong> Real-world database scenarios, hands-on query writing in PostgreSQL 16, and unit knowledge checks.</li></ul>")
        ]
        with open(os.path.join(wiki_dir, overview_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(f"{u_short} Overview: {u_topic}", overview_lead, overview_panels, overview_id))
        pages_manifest.append((overview_file, f"{u_short} Overview: {u_topic}", overview_id))

        # ----------------------------------------------------
        # Page 2: Required Readings, Concepts & Video Lectures - DesignPLUS Multi-Ribbon Page
        # ----------------------------------------------------
        reading_id = make_id(f"page_u{u_num}_readings")
        reading_file = f"unit-{u_num:02d}-readings-and-media.html"
        reading_lead = f"""<p><strong>Welcome to the core instructional lecture and study hub for Unit {u_num}: {u_topic}.</strong> This page organizes all weekly learning materials into four structured chapters:</p>
<ol style="padding-left: 1.5rem; margin: 0.75rem 0; line-height: 1.7;">
  <li><strong>Instructor Lecture &amp; Conceptual Deep Dive:</strong> Master the core concepts, mental models, syntax rules, and guided live exercises authored specifically for this unit.</li>
  <li><strong>Required Readings &amp; PostgreSQL Tutorial Guides:</strong> Review curated reference guides and official PostgreSQL 16 documentation links.</li>
  <li><strong>Required Micro-Video Lectures (Embedded):</strong> Watch high-definition video chapters with verified timestamp navigation to observe queries executed in live environments.</li>
  <li><strong>Institutional Video Lecture Embeds:</strong> Access campus-specific video recordings and announcements uploaded by your instructor.</li>
</ol>
<p style="margin-top: 0.75rem; margin-bottom: 0; color: #64748b; font-size: 0.95em;"><em>Work through each section in sequence as part of your 150-minute asynchronous self-study allocation before starting the applied laboratory assignment.</em></p>"""
        
        # Format Readings Descriptions HTML
        readings_lis = []
        for name, url, desc in unit["readings"]:
            readings_lis.append(f"""<li style="margin-bottom: 1rem;">
  <strong><a href="{url}" target="_blank" rel="noopener">{html.escape(name)}</a></strong>
  <p style="margin-top: 0.25rem; margin-bottom: 0; color: #475569;">{html.escape(desc)}</p>
</li>""")
        readings_body = f"<ul style='padding-left: 1.5rem; line-height: 1.6;'>{''.join(readings_lis)}</ul>"

        # Format Embedded Videos HTML
        video_embeds = []
        for v_title, v_id, v_start, v_ts in unit["videos"]:
            video_embeds.append(render_video_embed(v_title, v_id, v_start))
        videos_body = "\n".join(video_embeds)

        # Load and parse Curated Unit Overview markdown (Instructor Lecture)
        overview_md = load_and_clean_unit_overview(u_num)
        overview_html = parse_markdown_to_html(overview_md) if overview_md else ""

        # Section 4: Institutional Video Embeds Placeholder
        institutional_embed_html = """<div style="background: #f8fafc; border: 2px dashed #94a3b8; border-radius: 6px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
  <p style="font-size: 1.1em; font-weight: 600; color: #1e3a8a; margin-top: 0; margin-bottom: 0.5rem;"><i class="fas fa-video"></i> Custom Institutional Video Embed Slot</p>
  <p style="color: #475569; margin-bottom: 0.5rem; font-size: 0.95em;">This section is reserved for custom institutional lecture recordings (Canvas Studio, Panopto, Kaltura, or unlisted media embeds).</p>
  <p style="color: #64748b; font-size: 0.85em; margin-bottom: 0;"><em>[Instructor Notice: Use the Canvas Rich Content Editor to insert your Canvas Studio or campus video iframe directly into this placeholder.]</em></p>
</div>"""

        reading_panels = []
        if overview_html:
            reading_panels.append(("1. Instructor Lecture & Conceptual Deep Dive", overview_html))
        reading_panels.append(("2. Required Readings & PostgreSQL Tutorial Guides", readings_body))
        reading_panels.append(("3. Required Micro-Video Lectures (Embedded)", videos_body))
        reading_panels.append(("4. Institutional Video Lecture Embeds", institutional_embed_html))

        with open(os.path.join(wiki_dir, reading_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(f"{u_short}: Required Readings, Concepts & Video Lectures", reading_lead, reading_panels, reading_id))
        pages_manifest.append((reading_file, f"{u_short}: Required Readings, Concepts & Video Lectures", reading_id))

        # ----------------------------------------------------
        # Page 3: Asynchronous Preparation & Drills - Clean Standard Page
        # ----------------------------------------------------
        study_id = make_id(f"page_u{u_num}_async_study")
        study_file = f"unit-{u_num:02d}-async-study.html"
        study_lead = f"<p>Complete these conceptual reflection questions and formative self-check drills online before executing the lab assignment for <strong>{u_short}</strong>.</p>"

        # Load and parse Self Check Drills
        drills_path = os.path.join(UNITS_DIR, u_folder, "async", "self_check_drills.md")
        drills_html = "<p>Complete the formative self-check drills provided in your course repository under <code>async/self_check_drills.md</code>.</p>"
        if os.path.exists(drills_path):
            with open(drills_path, "r", encoding="utf-8") as df:
                drills_html = parse_markdown_to_html(df.read())

        # Load and parse Focus Questions
        study_guide_path = os.path.join(UNITS_DIR, u_folder, "async", "study_guide.md")
        focus_questions_html = "<p>Reflect on the core concepts covered in the readings and video lectures.</p>"
        if os.path.exists(study_guide_path):
            with open(study_guide_path, "r", encoding="utf-8") as sgf:
                sg_text = sgf.read()
                fq_match = re.search(r"## Step 4: Focus Questions.*?(?=## Step 5|\Z)", sg_text, re.DOTALL)
                if fq_match:
                    focus_questions_html = parse_markdown_to_html(fq_match.group(0).strip())

        study_panels = [
            ("Pre-Class Focus Questions", focus_questions_html),
            ("Formative Self-Check Drills", drills_html),
            ("Preparation Verification Checklist",
             "<p>Before proceeding to the lab assignment, verify that you have:</p><ul><li>Read all tutorial guides on the Neon PostgreSQL Tutorial.</li><li>Watched each embedded video chapter.</li><li>Answered the self-check drills without peeking at the solutions first.</li><li>Logged into your GitHub Codespaces PostgreSQL 16 environment.</li></ul>")
        ]
        with open(os.path.join(wiki_dir, study_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"{u_short}: Asynchronous Preparation & Drills", study_lead, study_panels, study_id))
        pages_manifest.append((study_file, f"{u_short}: Asynchronous Preparation & Drills", study_id))

        # ----------------------------------------------------
        # Page 4: Applied SQL Lab Assignment Guide - Clean Standard Page with Parsed Rubric Table
        # ----------------------------------------------------
        lab_guide_id = make_id(f"page_u{u_num}_applied_lab_guide")
        lab_guide_file = f"unit-{u_num:02d}-applied-lab-guide.html"
        lab_guide_lead = f"<p>This page contains the hands-on laboratory scenario, database schema specifications, and step-by-step query tasks for <strong>{u_short}</strong>. Complete these queries in PostgreSQL 16, then submit your work using the Canvas Assignment link below.</p>"

        # Load and parse Student Lab Guide
        lab_path = os.path.join(UNITS_DIR, u_folder, "guides", "student_lab_guide.md")
        lab_content_html = "<p>Refer to your course repository for the complete laboratory guide and scenario specifications.</p>"
        if os.path.exists(lab_path):
            with open(lab_path, "r", encoding="utf-8") as lf:
                lab_content_html = parse_markdown_to_html(lf.read())

        # Load Coding Clinic Walkthrough Challenges
        challenges_path = os.path.join(UNITS_DIR, u_folder, "sync", "inclass_challenges.sql")
        challenges_html = "<p>Refer to your course repository for self-paced coding clinic challenges.</p>"
        if os.path.exists(challenges_path):
            with open(challenges_path, "r", encoding="utf-8") as cf:
                challenges_html = f"""<p style="margin-bottom: 0.75rem;">These follow-along challenges follow the <strong>Gradual Release of Responsibility</strong> model (&quot;I Do, We Do, You Do&quot;). Attempt each query on your own in your Codespace sandbox before or while watching the instructor video walkthrough, then compare your query logic and formatting against the instructor's demonstration!</p>
<div style='background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; overflow-x: auto; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5;'><pre style='margin: 0; background: transparent; color: inherit;'><code>{html.escape(cf.read().strip())}</code></pre></div>"""

        # Check for starter template SQL file to embed copy-paste starter block
        starter_sql_path = os.path.join(UNITS_DIR, u_folder, f"lab{u_num}_starter.sql")
        if not os.path.exists(starter_sql_path):
            starter_sql_path = os.path.join(UNITS_DIR, u_folder, "guides", f"lab{u_num}_starter.sql")
        starter_box_html = ""
        if os.path.exists(starter_sql_path):
            with open(starter_sql_path, "r", encoding="utf-8") as stf:
                starter_box_html = f"""<div style="margin-top: 1.5rem; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 1rem;">
  <p style="font-weight: 600; color: #1e3a8a; margin-top: 0; margin-bottom: 0.5rem;"><i class="fas fa-file-code"></i> Copy-and-Paste Starter Template (<code>lab{u_num}_starter.sql</code>):</p>
  <p style="color: #475569; font-size: 0.9em; margin-bottom: 0.5rem;">Copy this starter template into a new file named <code>lab{u_num}_yourlastname.sql</code> in your Codespace, or open the template file already located in your repository under <code>units/{u_folder}/</code>.</p>
  <div style='background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 4px; overflow-x: auto; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5;'><pre style='margin: 0; background: transparent; color: inherit;'><code>{html.escape(stf.read().strip())}</code></pre></div>
</div>"""

        # Load and parse Rubric (Converts markdown table into beautiful styled HTML table)
        rubric_path = os.path.join(UNITS_DIR, u_folder, "assessments", "lab_rubric.md")
        rubric_html = "<p>Refer to your course repository for the complete grading rubric.</p>"
        if os.path.exists(rubric_path):
            with open(rubric_path, "r", encoding="utf-8") as rf:
                rubric_html = parse_markdown_to_html(rf.read())

        lab_panels = [
            ("1. Lecture Walkthroughs & Coding Clinic (Gradual Release: Try First, Then Watch)", challenges_html),
            ("2. Applied SQL Laboratory Challenges & Starter Script (Graded Submission — 100 Points)", lab_content_html + starter_box_html),
            ("3. Grading Rubric & Scoring Criteria (100 Points Total)", rubric_html)
        ]
        with open(os.path.join(wiki_dir, lab_guide_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"{u_short}: Applied SQL Lab Guide", lab_guide_lead, lab_panels, lab_guide_id))
        pages_manifest.append((lab_guide_file, f"{u_short}: Applied SQL Lab Guide", lab_guide_id))

        # ----------------------------------------------------
        # Item 5: Native Canvas Assignment (Turn-in / Check-in)
        # ----------------------------------------------------
        assign_id = make_id(f"canvas_assignment_u{u_num}")
        assign_folder = os.path.join(OUTPUT_BUILD_DIR, assign_id)
        os.makedirs(assign_folder, exist_ok=True)
        assign_title = f"{u_short} Applied SQL Lab Assignment"
        assign_html_filename = f"unit-{u_num:02d}-lab-assignment.html"

        # Write assignment_settings.xml with official B8 deadlines
        assign_settings_xml = build_assignment_settings_xml(
            assign_id, assign_title, group_labs_id, points=100.0,
            due_at=unit.get("due_iso"), lock_at=unit.get("due_iso")
        )
        with open(os.path.join(assign_folder, "assignment_settings.xml"), "w", encoding="utf-8") as af:
            af.write(assign_settings_xml)

        # Write assignment description HTML with clean layout, due date alert, and rubric
        assign_desc_html = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Assignment: {html.escape(assign_title)}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; padding: 1rem; max-width: 900px;">
  <h2 style="color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 0.3rem;">{html.escape(assign_title)} (100 Points)</h2>
  <div style="background: #eff6ff; border-left: 4px solid #2563eb; padding: 0.75rem 1.25rem; margin: 1rem 0; border-radius: 0 4px 4px 0;">
    <p style="margin: 0; font-weight: 600; color: #1e40af;"><i class="far fa-calendar-alt"></i> Due Date: {html.escape(unit["due_date_str"])}</p>
  </div>
  <div style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 0.75rem 1.25rem; margin: 1rem 0; border-radius: 0 4px 4px 0;">
    <p style="margin: 0 0 0.5rem 0;">Complete the SQL query challenges outlined in the <strong>{u_short}: Applied SQL Lab Guide</strong> against your live PostgreSQL 16 database in GitHub Codespaces.</p>
    <p style="margin: 0;"><a href="https://codespaces.new/tswarmLCCC/CMAP-1815-Student-Sandbox?quickstart=1" target="_blank" rel="noopener" style="display: inline-block; background: #2563eb; color: #ffffff; padding: 0.4rem 0.9rem; font-size: 0.9em; font-weight: 600; text-decoration: none; border-radius: 4px;"><i class="fab fa-github"></i> Open Student Sandbox in Codespaces</a> &nbsp; <a href="https://github.com/tswarmLCCC/CMAP-1815-Student-Sandbox" target="_blank" rel="noopener" style="color: #2563eb; font-weight: 500; font-size: 0.9em; text-decoration: underline;">View GitHub Repository</a></p>
  </div>
  <h3 style="color: #0f172a; margin-top: 1.5rem;">5-Step Lab Submission Recipe</h3>
  <ol style="padding-left: 1.5rem; line-height: 1.8;">
    <li>In your Codespace, open the starter template: <code>units/{u_folder}/lab{u_num}_starter.sql</code>.</li>
    <li>Write your query solutions directly beneath each challenge comment block.</li>
    <li><strong>Test every query</strong> using the visual <strong>SQLTools GUI</strong> or the terminal (<code>psql</code>) to ensure error-free execution.</li>
    <li>Format your code: SQL keywords in <strong>UPPERCASE</strong> (<code>SELECT</code>, <code>FROM</code>, <code>WHERE</code>) and clauses starting on new lines.</li>
    <li>Save your completed script as <code>lab{u_num}_yourlastname.sql</code> (e.g. <code>lab{u_num}_smith.sql</code>) and upload the file below for SpeedGrader evaluation.</li>
  </ol>
  <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.6rem 1rem; margin: 1rem 0; border-radius: 0 4px 4px 0; font-size: 0.9em; color: #991b1b;">
    <strong>Accidental Data Deletion or Dropped Table?</strong> Run <code>./reset_database.sh</code> in your terminal to instantly restore pristine database tables without losing your saved query files.
  </div>
  <h3 style="color: #0f172a; margin-top: 1.5rem;">Grading Criteria (100 Points Total)</h3>
  <div style="margin-top: 0.5rem;">
    {rubric_html}
  </div>
</body>
</html>"""
        with open(os.path.join(assign_folder, assign_html_filename), "w", encoding="utf-8") as ahf:
            ahf.write(assign_desc_html)

        assignment_manifest.append((assign_id, assign_html_filename, assign_title))

        # ----------------------------------------------------
        # Page 6: Learn with AI — Supplemental Practice Drill - Clean Standard Page
        # ----------------------------------------------------
        ai_data = LEARN_WITH_AI_DATA[u_num]
        ai_page_id = make_id(f"page_u{u_num}_learn_with_ai")
        ai_page_file = f"unit-{u_num:02d}-learn-with-ai.html"
        ai_lead = f"<p>This supplemental practice activity lets you test your knowledge of <strong>{u_topic}</strong> by interacting with a specialized AI persona. This is an optional/supplemental formative practice activity that contributes toward weekly participation credit.</p>"
        
        prompt_box_html = f"""<div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 1rem; margin: 0.75rem 0;">
  <p style="font-size: 0.9em; font-weight: 600; color: #475569; margin-top: 0; margin-bottom: 0.5rem;">COPY AND PASTE THIS PROMPT INTO YOUR AI CHAT ASSISTANT:</p>
  <div style="background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 4px; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5;">
    <pre style="margin: 0; white-space: pre-wrap; background: transparent; color: inherit; font-family: inherit;"><code>{html.escape(ai_data['prompt'])}</code></pre>
  </div>
</div>"""

        ai_coaching_html = """<p>This Socratic drill is an <strong>intentionally challenging exercise designed to deepen your learning</strong> and test subtle relational traps. You are NOT expected to know all the answers right away!</p>
<p>When working with your AI assistant, remember that it is always completely okay and encouraged to:</p>
<ul style="line-height: 1.8;">
  <li><strong>Say "I don't know" or "I'm stuck":</strong> The AI is acting as your tutor. If you don't know where to start, tell it!</li>
  <li><strong>Ask for Explanations &amp; Hints:</strong> Ask: <em>"Can you explain the underlying concept without giving me the code?"</em> or <em>"Give me a hint to get started."</em></li>
  <li><strong>Ask for More Practice Problems:</strong> Ask: <em>"Can you give me another practice puzzle like this to make sure I've got it?"</em></li>
  <li><strong>Ask for Web Resources &amp; Documentation:</strong> Ask: <em>"Where in the official PostgreSQL 16 documentation can I read more about this?"</em></li>
  <li><strong>Explore Edge Cases:</strong> Ask: <em>"What happens if our data contains NULLs, empty strings, or duplicate rows?"</em></li>
</ul>"""

        hotl_defense_html = """<p>Never assume an AI's SQL answer is correct! The Golden Rule of CMAP 1815: <strong>Every single SQL snippet must be executed and verified against your live PostgreSQL 16 database in GitHub Codespaces before submission!</strong></p>
<div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.85rem 1.25rem; margin: 1rem 0; border-radius: 0 6px 6px 0;">
  <p style="margin: 0 0 0.5rem 0; font-weight: 600; color: #991b1b;"><i class="fas fa-shield-alt"></i> The Human-On-The-Loop (HOTL) Defense Requirement:</p>
  <p style="margin: 0 0 0.5rem 0; color: #7f1d1d; font-size: 0.95em;">You are 100% accountable for every query you submit. <strong>The instructor reserves the right to question any submission for evidence of understanding</strong>—including asking you to explain your query line-by-line, defend your choice of clauses or joins, or write an equivalent query on the fly.</p>
  <p style="margin: 0; color: #7f1d1d; font-size: 0.95em; font-weight: 600;">Do NOT submit work you don't fully understand or could not write yourself!</p>
</div>"""

        debrief_panel_html = f"""<p>{html.escape(ai_data['discussion_prompt'])}</p>
<p>After completing your interactive drill, navigate to the <strong>{u_short} Discussion: Learn with AI Debrief &amp; Reflection</strong> in this module to post your findings and compare notes with classmates.</p>"""

        ai_panels = [
            ("The Role-Play Practice Scenario",
             f"<p><strong>AI Persona:</strong> {html.escape(ai_data['persona'])}</p>"
             f"<p><strong>Core Topic / Focus:</strong> {html.escape(ai_data['drill_topic'])}</p>"
             "<p>In this exercise, you assign the AI a specific technical persona that tests your reasoning and challenges you to debug or construct SQL queries.</p>"),
            ("How to Interact with Your AI Partner (Coaching & Permission to Struggle)", ai_coaching_html),
            ("The Human-On-The-Loop (HOTL) Verification & Defense Protocol", hotl_defense_html),
            ("100% Free AI Tool Setup",
             "<p>Use any free web chat assistant (no subscription or API key required):</p>"
             "<ul><li><strong>ChatGPT Free:</strong> <a href='https://chatgpt.com' target='_blank' rel='noopener'>chatgpt.com</a></li>"
             "<li><strong>Claude Free:</strong> <a href='https://claude.ai' target='_blank' rel='noopener'>claude.ai</a></li>"
             "<li><strong>Google Gemini Free:</strong> <a href='https://gemini.google.com' target='_blank' rel='noopener'>gemini.google.com</a></li>"
             "<li><strong>Microsoft Copilot Free:</strong> <a href='https://copilot.microsoft.com' target='_blank' rel='noopener'>copilot.microsoft.com</a></li></ul>"),
            ("Copy-and-Paste Master Prompt", prompt_box_html),
            ("Asynchronous Participation & Reflection Debrief", debrief_panel_html)
        ]
        with open(os.path.join(wiki_dir, ai_page_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"{u_short}: Learn with AI — Supplemental Practice Drill", ai_lead, ai_panels, ai_page_id))
        pages_manifest.append((ai_page_file, f"{u_short}: Learn with AI — Supplemental Practice Drill", ai_page_id))

        # ----------------------------------------------------
        # Discussion Topic: Learn with AI Debrief & Reflection
        # ----------------------------------------------------
        disc_id = make_id(f"disc_u{u_num}")
        disc_title = f"{u_short} Discussion: Learn with AI Debrief & Reflection"
        disc_dir = os.path.join(OUTPUT_BUILD_DIR, disc_id)
        os.makedirs(disc_dir, exist_ok=True)

        disc_html = f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 1rem; line-height: 1.6; color: #1e293b;">
  <div style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 1rem 1.25rem; margin-bottom: 1.5rem; border-radius: 0 6px 6px 0;">
    <h3 style="color: #1e3a8a; margin-top: 0; margin-bottom: 0.5rem;"><i class="far fa-comments"></i> {u_short} Collaborative Reflection: Learn with AI Debrief</h3>
    <p style="margin: 0; color: #475569;">This weekly discussion board is where you share insights, traps, and breakthroughs from your interactive practice session with our AI Persona: <strong>{html.escape(ai_data['persona'])}</strong>.</p>
  </div>

  <h4 style="color: #1e3a8a; margin-top: 1rem; margin-bottom: 0.5rem;">Discussion Prompts &amp; Deliverables:</h4>
  <p>{html.escape(ai_data['discussion_prompt'])}</p>

  <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.85rem 1.25rem; margin: 1.25rem 0; border-radius: 0 6px 6px 0;">
    <strong style="color: #991b1b;"><i class="fas fa-shield-alt"></i> The Human-On-The-Loop (HOTL) Defense Standard:</strong>
    <p style="margin: 0.35rem 0 0 0; color: #7f1d1d; font-size: 0.95em;">Never share or turn in SQL queries without verifying them! Every SQL snippet discussed or submitted must be executed against your live PostgreSQL 16 database in GitHub Codespaces. Make sure you fully understand and can defend every line of SQL you post.</p>
  </div>

  <h4 style="color: #1e3a8a; margin-top: 1.25rem; margin-bottom: 0.5rem;">Peer Collaboration Guidelines:</h4>
  <ul style="padding-left: 1.5rem; line-height: 1.7;">
    <li>Post your initial reflection answering the prompts above.</li>
    <li>Read through your classmates' findings. Reply to at least one classmate: did you encounter the same trap or persona question? How does their query approach compare to yours?</li>
    <li>Constructive debate and alternative query formulations are highly encouraged!</li>
  </ul>
</div>"""

        disc_xml_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<topic xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1 http://www.imsglobal.org/xsd/imsccv1p1/ccv1p1_imsdt_v1p1.xsd">
  <title>{html.escape(disc_title)}</title>
  <text texttype="text/html">{html.escape(disc_html)}</text>
</topic>
"""
        with open(os.path.join(disc_dir, "discussion_topic.xml"), "w", encoding="utf-8") as df:
            df.write(disc_xml_str)

        discussions_manifest.append((disc_id, disc_title, f"{disc_id}/discussion_topic.xml"))

        # ----------------------------------------------------
        # Item 7: Unit Knowledge Check (Quiz)
        # ----------------------------------------------------
        quiz_path = os.path.join(UNITS_DIR, u_folder, "assessments", "unit_quiz.md")
        questions = parse_quiz_md(quiz_path)
        quiz_id = make_id(f"quiz_u{u_num}")
        quiz_meta_id = make_id(f"quiz_meta_u{u_num}")
        quiz_title = f"{u_short} Knowledge Check: {u_topic}"

        q_dir = os.path.join(OUTPUT_BUILD_DIR, quiz_id)
        os.makedirs(q_dir, exist_ok=True)

        qti_xml_str = build_qti_xml(quiz_id, quiz_title, questions)
        with open(os.path.join(q_dir, "assessment_qti.xml"), "w", encoding="utf-8") as qf:
            qf.write(qti_xml_str)

        meta_xml_str = build_assessment_meta_xml(
            quiz_id, quiz_title, group_quizzes_id,
            due_at=unit.get("due_iso"), lock_at=unit.get("due_iso")
        )
        with open(os.path.join(q_dir, "assessment_meta.xml"), "w", encoding="utf-8") as mf:
            mf.write(meta_xml_str)

        with open(os.path.join(non_cc_dir, f"{quiz_id}.xml.qti"), "w", encoding="utf-8") as ncf:
            ncf.write(qti_xml_str)

        quiz_manifest.append((quiz_id, quiz_meta_id, quiz_title))

        # ----------------------------------------------------
        # Page 8: [Instructor Guide] Teaching Notes & Solutions (Unpublished) - Clean Standard Page
        # ----------------------------------------------------
        teacher_id = make_id(f"page_u{u_num}_teacher_guide")
        teacher_file = f"unit-{u_num:02d}-instructor-guide.html"
        teacher_lead = "<p><strong>[FOR INSTRUCTORS ONLY — UNPUBLISHED]</strong> This guide provides custom video production blueprints, synchronous classroom delivery schedules, live coding trap demos, and master SQL solution keys.</p>"

        # Format Video Production Blueprint
        tg_info = TEACHER_GUIDE_DATA[u_num]
        video_blueprint_lis = []
        for v_title, v_dur, v_notes in tg_info["videos"]:
            video_blueprint_lis.append(f"""<li style="margin-bottom: 0.75rem;">
  <strong>{html.escape(v_title)}</strong> <em>({html.escape(v_dur)})</em>
  <p style="margin: 0.25rem 0 0 0; color: #475569;">{html.escape(v_notes)}</p>
</li>""")
        video_blueprint_html = f"""<p>Record the following 3 micro-videos to customize this unit for your institution:</p>
<ul style="padding-left: 1.5rem;">{''.join(video_blueprint_lis)}</ul>
<p><strong>Where to Host &amp; Embed:</strong> Upload to <em>Canvas Studio</em>, <em>YouTube (Unlisted)</em>, or your campus media repository (Panopto/Kaltura). Replace or add the video embed iframe on the <code>{u_short}: Required Readings &amp; Video Lectures</code> page.</p>"""

        # Asynchronous Video Walkthrough & Coding Clinic Blueprint
        sync_blueprint_html = f"""<p>Use this blueprint when recording asynchronous lecture walkthroughs and coding clinics (Gradual Release: &quot;I Do, We Do, You Do&quot;):</p>
<pre style="white-space: pre-wrap; font-family: inherit; background: #f8fafc; padding: 1rem; border: 1px solid #cbd5e1; border-radius: 4px;"><code>{html.escape(tg_info['sync_agenda'])}</code></pre>
<p>In your video recording, demonstrate the queries from <code>sync/inclass_challenges.sql</code>. Encourage students to pause the video, attempt each query first on their own, and then resume to watch your demonstration and trap analysis.</p>
<p><em>Note: If delivering an optional live Q&amp;A or workshop session, this agenda also serves as a high-impact in-person schedule.</em></p>"""

        # Load Solution notes
        sol_path = os.path.join(UNITS_DIR, u_folder, "guides", "instructor_solution.sql")
        sol_html = "<p>Refer to course repository for master solution SQL.</p>"
        if os.path.exists(sol_path):
            with open(sol_path, "r", encoding="utf-8") as sf:
                s_text = sf.read()
                sol_html = f"<div style='background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; overflow-x: auto; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5;'><pre style='margin: 0; background: transparent; color: inherit;'><code>{html.escape(s_text.strip())}</code></pre></div>"

        teacher_panels = [
            ("Video Production Blueprint (What Videos to Record & Where to Host)", video_blueprint_html),
            ("Lecture Walkthrough Recording Guide & Coding Clinic Blueprint", sync_blueprint_html),
            ("Instructor Master Solution SQL & Answer Key", sol_html)
        ]
        with open(os.path.join(wiki_dir, teacher_file), "w", encoding="utf-8") as f:
            f.write(render_standard_page_html(f"[Instructor Guide] {u_short} Teaching Notes & Solutions", teacher_lead, teacher_panels, teacher_id, workflow_state="unpublished"))
        pages_manifest.append((teacher_file, f"[Instructor Guide] {u_short} Teaching Notes & Solutions", teacher_id))

        # ----------------------------------------------------
        # Assemble Clean Unit Module Items (Standard 9-Item Sequence with Discussion)
        # ----------------------------------------------------
        modules_data.append({
            "id": unit_mod_ids[u_num],
            "title": u_title,
            "items": [
                {"type": "WikiPage", "title": f"{u_short} Overview: {u_topic}", "ref": overview_id, "indent": 0, "state": "active"},
                {"type": "WikiPage", "title": f"{u_short}: Required Readings, Concepts & Video Lectures", "ref": reading_id, "indent": 1, "state": "active"},
                {"type": "WikiPage", "title": f"{u_short}: Asynchronous Preparation & Drills", "ref": study_id, "indent": 1, "state": "active"},
                {"type": "WikiPage", "title": f"{u_short}: Applied SQL Lab Guide", "ref": lab_guide_id, "indent": 1, "state": "active"},
                {"type": "Assignment", "title": assign_title, "ref": assign_id, "indent": 1, "state": "active"},
                {"type": "WikiPage", "title": f"{u_short}: Learn with AI — Supplemental Practice Drill", "ref": ai_page_id, "indent": 1, "state": "active"},
                {"type": "DiscussionTopic", "title": disc_title, "ref": disc_id, "indent": 1, "state": "active"},
                {"type": "Quizzes::Quiz", "title": quiz_title, "ref": quiz_id, "indent": 1, "state": "active"},
                {"type": "WikiPage", "title": f"[Instructor Guide] {u_short} Teaching Notes & Solutions", "ref": teacher_id, "indent": 1, "state": "unpublished"}
            ]
        })

    # 6. Generate course_settings/module_meta.xml (Synchronized with imsmanifest.xml)
    modules_xml_items = []
    org_items = []

    for pos, mod in enumerate(modules_data, 1):
        mod_id = mod["id"]
        mod_title = mod["title"]
        m_items_xml = []
        m_man_items = []

        for i_pos, item in enumerate(mod["items"], 1):
            shared_item_id = make_id(f"item_{mod_id}_{item['ref']}")
            item_state = item.get("state", "active")
            item_indent = item.get("indent", 0)

            m_items_xml.append(f"""      <item identifier="{shared_item_id}">
        <content_type>{item['type']}</content_type>
        <workflow_state>{item_state}</workflow_state>
        <title>{html.escape(item['title'])}</title>
        <identifierref>{item['ref']}</identifierref>
        <position>{i_pos}</position>
        <new_tab>false</new_tab>
        <indent>{item_indent}</indent>
        <link_settings_json>null</link_settings_json>
      </item>""")

            m_man_items.append(f"""          <item identifier="{shared_item_id}" identifierref="{item['ref']}">
            <title>{html.escape(item['title'])}</title>
          </item>""")

        items_joined = "\n".join(m_items_xml)
        modules_xml_items.append(f"""  <module identifier="{mod_id}">
    <title>{html.escape(mod_title)}</title>
    <workflow_state>active</workflow_state>
    <position>{pos}</position>
    <require_sequential_progress>false</require_sequential_progress>
    <locked>false</locked>
    <items>
{items_joined}
    </items>
  </module>""")

        man_items_joined = "\n".join(m_man_items)
        org_items.append(f"""        <item identifier="{mod_id}">
          <title>{html.escape(mod_title)}</title>
{man_items_joined}
        </item>""")

    modules_meta_joined = "\n".join(modules_xml_items)
    modules_meta_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<modules xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
{modules_meta_joined}
</modules>
"""
    with open(os.path.join(settings_dir, "module_meta.xml"), "w", encoding="utf-8") as f:
        f.write(modules_meta_str)

    # 7. Generate imsmanifest.xml (Canvas Native Package Standard)
    manifest_id = make_id("cmap_1815_manifest")
    org_items_joined = "\n".join(org_items)

    resources_xml = []
    # Native Canvas Export Descriptor Resource
    resources_xml.append(f"""    <resource identifier="{course_id}_syllabus" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/syllabus.html" intendeduse="syllabus">
      <file href="course_settings/syllabus.html"/>
    </resource>
    <resource identifier="{course_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/canvas_export.txt">
      <file href="course_settings/course_settings.xml"/>
      <file href="course_settings/module_meta.xml"/>
      <file href="course_settings/assignment_groups.xml"/>
      <file href="course_settings/context.xml"/>
      <file href="course_settings/canvas_export.txt"/>
      <file href="course_settings/files_meta.xml"/>
    </resource>""")

    # Word Syllabus File Resource
    syllabus_docx_res_id = make_id("res_syllabus_docx")
    resources_xml.append(f"""    <resource identifier="{syllabus_docx_res_id}" type="webcontent" href="web_resources/syllabi/{dst_docx_name}">
      <file href="web_resources/syllabi/{dst_docx_name}"/>
    </resource>""")

    # Course Banner Image Resource
    course_banner_res_id = make_id("res_course_banner")
    resources_xml.append(f"""    <resource identifier="{course_banner_res_id}" type="webcontent" href="web_resources/images/sql_course_banner.jpg">
      <file href="web_resources/images/sql_course_banner.jpg"/>
    </resource>""")

    # Course Thumbnail Image Resource
    course_thumb_res_id = make_id("res_course_thumbnail")
    resources_xml.append(f"""    <resource identifier="{course_thumb_res_id}" type="webcontent" href="web_resources/images/sql_course_thumbnail.jpg">
      <file href="web_resources/images/sql_course_thumbnail.jpg"/>
    </resource>""")

    # Wiki Pages Resources
    for p_file, p_title, p_id in pages_manifest:
        resources_xml.append(f"""    <resource identifier="{p_id}" type="webcontent" href="wiki_content/{p_file}">
      <file href="wiki_content/{p_file}"/>
    </resource>""")

    # Native Canvas Assignment Resources
    for a_id, a_html_file, a_title in assignment_manifest:
        resources_xml.append(f"""    <resource identifier="{a_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{a_id}/{a_html_file}">
      <file href="{a_id}/{a_html_file}"/>
      <file href="{a_id}/assignment_settings.xml"/>
    </resource>""")

    # Quizzes Resources
    for q_id, q_meta_id, q_title in quiz_manifest:
        resources_xml.append(f"""    <resource identifier="{q_id}" type="imsqti_xmlv1p2/imscc_xmlv1p1/assessment">
      <file href="{q_id}/assessment_qti.xml"/>
      <dependency identifierref="{q_meta_id}"/>
    </resource>
    <resource identifier="{q_meta_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{q_id}/assessment_meta.xml">
      <file href="{q_id}/assessment_meta.xml"/>
      <file href="non_cc_assessments/{q_id}.xml.qti"/>
    </resource>""")

    # Discussion Topics Resources
    for d_id, d_title, d_file in discussions_manifest:
        resources_xml.append(f"""    <resource identifier="{d_id}" type="imsdt_xmlv1p1">
      <file href="{d_file}"/>
    </resource>""")

    resources_xml_joined = "\n".join(resources_xml)

    imsmanifest_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{manifest_id}" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imscp_v1p2_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lommanifest_v1p0.xsd">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.1.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>CMAP 1815: Introduction to Modern SQL</lomimscc:string>
        </lomimscc:title>
      </lomimscc:general>
    </lomimscc:lom>
  </metadata>
  <organizations>
    <organization identifier="org_1" structure="rooted-hierarchy">
      <item identifier="LearningModules">
{org_items_joined}
      </item>
    </organization>
  </organizations>
  <resources>
{resources_xml_joined}
  </resources>
</manifest>
"""
    with open(os.path.join(OUTPUT_BUILD_DIR, "imsmanifest.xml"), "w", encoding="utf-8") as f:
        f.write(imsmanifest_str)

    # 8. Schema & XML Well-Formedness Verification Suite
    print("\n--- Running XML Validation Suite ---")
    xml_files_tested = 0
    for root, dirs, files in os.walk(OUTPUT_BUILD_DIR):
        for file in files:
            if file.endswith(".xml") or file.endswith(".qti"):
                file_path = os.path.join(root, file)
                try:
                    ET.parse(file_path)
                    xml_files_tested += 1
                except Exception as e:
                    print(f"ERROR in XML file {file_path}: {e}")
                    sys.exit(1)
    print(f"SUCCESS: Verified {xml_files_tested} XML files. Zero syntax errors!")

    # 9. Package into .imscc (with automated pre-build backup)
    if os.path.exists(IMSCC_OUTPUT_FILE):
        backup_dir = os.path.join(BASE_DIR, "archive", "cartridge_backups")
        os.makedirs(backup_dir, exist_ok=True)
        mtime = os.path.getmtime(IMSCC_OUTPUT_FILE)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"CMAP_1815_Complete_{mtime_str}.imscc")
        if not os.path.exists(backup_path):
            shutil.copy2(IMSCC_OUTPUT_FILE, backup_path)
            print(f"[Backup] Preserved previous cartridge to: {backup_path}")

    print(f"\n--- Packaging into {IMSCC_OUTPUT_FILE} ---")
    total_files = 0
    with zipfile.ZipFile(IMSCC_OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(OUTPUT_BUILD_DIR):
            for file in files:
                abs_path = os.path.join(root, file)
                arc_name = os.path.relpath(abs_path, OUTPUT_BUILD_DIR)
                zipf.write(abs_path, arc_name)
                total_files += 1

    size_mb = os.path.getsize(IMSCC_OUTPUT_FILE) / (1024 * 1024)
    print(f"SUCCESS: Created {IMSCC_OUTPUT_FILE} ({total_files} files, {size_mb:.2f} MB)")
    print("Canvas Native Course Export Package build complete!\n")

if __name__ == "__main__":
    main()
