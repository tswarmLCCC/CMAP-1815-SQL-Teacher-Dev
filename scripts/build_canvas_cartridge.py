import os
import sys
import re
import hashlib
import zipfile
import html
import xml.etree.ElementTree as ET

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UNITS_DIR = os.path.join(BASE_DIR, "units")
COURSE_SPECS_DIR = os.path.join(BASE_DIR, "course_specs")
OUTPUT_BUILD_DIR = os.path.join(BASE_DIR, "build", "canvas_cartridge")
IMSCC_OUTPUT_FILE = os.path.join(BASE_DIR, "CMAP_1815_Complete.imscc")

def make_id(seed: str) -> str:
    """Generate a deterministic 32-char hex identifier matching Canvas format."""
    return "g" + hashlib.md5(seed.encode("utf-8")).hexdigest()[1:]

UNIT_METADATA = [
    {
        "num": 1,
        "folder": "unit_01_selection_and_fundamentals",
        "title": "Unit 1: Selection & Relational Fundamentals",
        "short_title": "Unit 1",
        "topic": "Selection & Relational Fundamentals",
        "readings": [
            ("PostgreSQL SELECT", "https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-select/"),
            ("Column Alias (AS)", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-alias/"),
            ("ORDER BY Sorting", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-order-by/"),
            ("DISTINCT Deduplication", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select-distinct/")
        ],
        "videos": [
            ("What is a Relational Database", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=317s", "0:05:17"),
            ("What is PostgreSQL", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=550s", "0:09:10"),
            ("The SELECT Statement", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=6190s", "1:43:10")
        ]
    },
    {
        "num": 2,
        "folder": "unit_02_filtering_and_logic",
        "title": "Unit 2: Targeted Retrieval & Logic Gates",
        "short_title": "Unit 2",
        "topic": "Targeted Retrieval & Three-Valued Logic",
        "readings": [
            ("WHERE Clause", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-where/"),
            ("BETWEEN Operator", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-between/"),
            ("IN Operator", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-in/"),
            ("LIKE & ILIKE Pattern Matching", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-like/"),
            ("IS NULL & Three-Valued Logic", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-is-null/")
        ],
        "videos": [
            ("Comparison Operators & WHERE", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=6618s", "1:50:18"),
            ("Filtering with AND / OR", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=7280s", "2:01:20"),
            ("Handling NULL Values", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=8142s", "2:15:42")
        ]
    },
    {
        "num": 3,
        "folder": "unit_03_joins_and_relations",
        "title": "Unit 3: Relational Joins & Set Relationships",
        "short_title": "Unit 3",
        "topic": "Relational Joins & Foreign Key Relationships",
        "readings": [
            ("Joins Overview", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-joins/"),
            ("INNER JOIN", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-inner-join/"),
            ("LEFT JOIN & Anti-Joins", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-left-join/"),
            ("Table Aliases", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-alias/")
        ],
        "videos": [
            ("Understanding Primary Keys", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=9083s", "2:31:23"),
            ("Foreign Keys & Relationships", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=11801s", "3:16:41"),
            ("INNER JOINs in Action", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=12570s", "3:29:30"),
            ("LEFT JOINs & Missing Data", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=12917s", "3:35:17")
        ]
    },
    {
        "num": 4,
        "folder": "unit_04_aggregation_and_pivoting",
        "title": "Unit 4: Summarization, Aggregation & Pivoting",
        "short_title": "Unit 4",
        "topic": "Summarization, Aggregation & Pivoting",
        "readings": [
            ("GROUP BY Tutorial", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-group-by/"),
            ("HAVING Clause", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-having/"),
            ("Aggregate Functions (COUNT, SUM, AVG)", "https://www.postgresqltutorial.com/postgresql-aggregate-functions/"),
            ("UNION & UNION ALL", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-union/"),
            ("CASE Conditional Expressions", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-case/")
        ],
        "videos": [
            ("Aggregate Functions", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=9374s", "2:36:14"),
            ("GROUP BY & Group Filtering", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=9930s", "2:45:30")
        ]
    },
    {
        "num": 5,
        "folder": "unit_05_safe_dml_and_modifications",
        "title": "Unit 5: Safe DML, Transaction Integrity & Staging",
        "short_title": "Unit 5",
        "topic": "Safe DML, Transaction Integrity & Staging Tables",
        "readings": [
            ("INSERT Statement", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-insert/"),
            ("UPDATE Statement & RETURNING", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-update/"),
            ("DELETE Statement", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-delete/"),
            ("Transactions (BEGIN, COMMIT, ROLLBACK)", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-transaction/"),
            ("Temporary Staging Tables", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-temporary-table/")
        ],
        "videos": [
            ("Insert Into & Examples", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=3355s", "0:55:55"),
            ("How to Delete Records", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=10485s", "2:54:45"),
            ("How to Update Records", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=10896s", "3:01:36"),
            ("On Conflict & Upserts", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=11155s", "3:05:55")
        ]
    },
    {
        "num": 6,
        "folder": "unit_06_subqueries_and_window_functions",
        "title": "Unit 6: Query Modularity, CTEs & Window Functions",
        "short_title": "Unit 6",
        "topic": "Query Modularity, CTEs & Analytical Window Functions",
        "readings": [
            ("Common Table Expressions (WITH)", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-cte/"),
            ("Window Functions Overview", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-window-function/"),
            ("ROW_NUMBER Function", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-row_number/"),
            ("RANK & DENSE_RANK", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-rank/")
        ],
        "videos": [
            ("Subqueries & CTE Walkthrough", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-cte/", "Interactive Guide"),
            ("Analytical Window Functions", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-window-function/", "Visual Tutorial")
        ]
    },
    {
        "num": 7,
        "folder": "unit_07_schema_design_and_integrity",
        "title": "Unit 7: Schema Design, DDL & Data Integrity",
        "short_title": "Unit 7",
        "topic": "Schema Design, Normalization (1NF–3NF), DDL & Constraints",
        "readings": [
            ("CREATE TABLE & Data Types", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-table/"),
            ("Primary Key Constraints", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-primary-key/"),
            ("Foreign Key & Referential Actions", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-foreign-key/"),
            ("CHECK & UNIQUE Constraints", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-check-constraint/"),
            ("CREATE VIEW for Abstraction", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-views/")
        ],
        "videos": [
            ("How To Create Tables", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=2497s", "0:41:37"),
            ("Creating Tables with Constraints", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=2952s", "0:49:12"),
            ("Adding Primary Keys", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=9386s", "2:36:26"),
            ("Unique & Check Constraints", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=9655s", "2:40:55")
        ]
    },
    {
        "num": 8,
        "folder": "unit_08_performance_indexing_and_capstone",
        "title": "Unit 8: Performance Tuning, Indexing & Capstone Defense",
        "short_title": "Unit 8",
        "topic": "Query Optimization, EXPLAIN ANALYZE, Indexes & Capstone Defense",
        "readings": [
            ("EXPLAIN & Query Plans", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-explain/"),
            ("PostgreSQL Indexes Overview", "https://www.postgresqltutorial.com/postgresql-indexes/"),
            ("CREATE INDEX Best Practices", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-create-index/"),
            ("Composite Indexes", "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-composite-index/")
        ],
        "videos": [
            ("Exporting Query Results to CSV", "https://www.youtube.com/watch?v=qw--VYLpxG4&t=13647s", "3:47:27"),
            ("Indexing & Query Optimization", "https://www.postgresqltutorial.com/postgresql-indexes/", "Master Guide")
        ]
    }
]

# Comprehensive "Learn with AI" Curriculum Data
LEARN_WITH_AI_DATA = {
    1: {
        "page_title": "Unit 1: Learn with AI — The Socratic Database Sensei",
        "persona": "Professor Codd (The Socratic SQL Master)",
        "technique": "Socratic Questioning & Execution Order Inversion",
        "lead": "In this guided exercise, you will pair-program with an AI acting as a strict, Socratic database theorist. Rather than giving you SQL code, the AI will interrogate your mental model of how PostgreSQL parses queries versus how humans write them.",
        "why_it_matters": (
            "<p>The biggest roadblock beginners encounter in SQL is the syntax illusion: we write <code>SELECT</code> first, but the database engine executes <code>FROM</code> first. "
            "Because human English reads left-to-right and top-to-bottom, students assume the database starts by projecting columns. In reality, PostgreSQL must locate the physical table on disk, load data pages into memory buffers, and construct an intermediate record stream before it can even evaluate which columns you requested.</p>"
            "<p>Furthermore, junior developers frequently rely on <code>SELECT *</code> out of convenience. In production software, this anti-pattern saturates network bandwidth, thrashes cache pools, breaks backward compatibility when schemas evolve, and destroys index-only scan opportunities. This AI drill forces you to articulate these foundational realities before writing production code.</p>"
        ),
        "free_tools_guide": (
            "<p>You do <strong>not</strong> need a paid subscription or API key for this exercise. Use any of the following 100% free web chat interfaces:</p>"
            "<ul>"
            "<li><strong>ChatGPT Free:</strong> Visit <a href='https://chatgpt.com' target='_blank'>chatgpt.com</a> (select GPT-4o-mini / Free tier).</li>"
            "<li><strong>Claude Free:</strong> Visit <a href='https://claude.ai' target='_blank'>claude.ai</a> (free web tier).</li>"
            "<li><strong>Google Gemini Free:</strong> Visit <a href='https://gemini.google.com' target='_blank'>gemini.google.com</a> (free with any Google account).</li>"
            "<li><strong>Microsoft Copilot Free:</strong> Visit <a href='https://copilot.microsoft.com' target='_blank'>copilot.microsoft.com</a> (free web search & chat).</li>"
            "</ul>"
            "<p><em>Pro-Tip:</em> Start a brand new, empty chat session for this exercise so the AI doesn't carry over context from previous conversations.</p>"
        ),
        "prompt_template": (
            "Act as a strict, Socratic SQL professor named Professor Codd. I am a student learning SQL SELECT statements "
            "and relational database fundamentals in PostgreSQL 16. Do NOT give me direct answers or write the SQL for me. "
            "Instead, ask me one challenging question at a time to test my understanding of:\n"
            "1. Why PostgreSQL evaluates FROM before SELECT during query execution.\n"
            "2. The fundamental difference between physical row storage and relational projection.\n"
            "3. Why 'SELECT *' is considered a dangerous anti-pattern in production microservices and reporting pipelines.\n"
            "Start by asking me your first question about query execution order. Wait for my response before evaluating my reasoning and asking the next question."
        ),
        "playbook": (
            "<p>Follow this turn-by-turn playbook during your drill:</p>"
            "<ol>"
            "<li><strong>Turn 1 (Execution Order):</strong> The AI will ask why <code>FROM</code> executes first. Explain that PostgreSQL must identify the table location and scan blocks before it knows which columns exist.</li>"
            "<li><strong>Turn 2 (Projection vs Storage):</strong> The AI will probe what happens in memory when you calculate <code>salary * 1.10 AS projected_salary</code>. Does it change disk data? (Explain that projection creates a virtual result stream in RAM; underlying disk blocks are unmodified).</li>"
            "<li><strong>Turn 3 (The SELECT * Trap):</strong> The AI will ask what happens to a production microservice when a DBA adds a 50MB <code>BYTEA</code> column to a table if code uses <code>SELECT *</code>.</li>"
            "<li><strong>Getting Unstuck:</strong> If Professor Codd asks a question you cannot answer, reply: <em>'Give me a real-world warehouse analogy to help me reason through this, but do not give me the answer!'</em></li>"
            "</ol>"
        ),
        "participation_task": (
            "<p>To receive asynchronous participation credit for Unit 1, open the <strong>Unit 1 Discussion Board</strong> in Canvas and submit a post addressing:</p>"
            "<ol>"
            "<li><strong>The Toughest Question:</strong> Quote the most challenging question Professor Codd asked you during your session.</li>"
            "<li><strong>Your Mental Model Shift:</strong> Explain what you learned about how PostgreSQL executes queries behind the scenes.</li>"
            "<li><strong>Lingering Question:</strong> State one question or puzzle you want to explore during our live active lab session.</li>"
            "</ol>"
        )
    },
    2: {
        "page_title": "Unit 2: Learn with AI — The Pedantic QA Lead & Three-Valued Logic",
        "persona": "The Pedantic Database QA Lead / ANSI Compiler",
        "technique": "Three-Valued Logic Red-Teaming & Edge-Case Traps",
        "lead": "This exercise pairs you with an AI acting as a ruthless Senior Database QA Lead. Your mission is to analyze realistic SQL filtering snippets and hunt down subtle bugs rooted in ANSI Three-Valued Logic (3VL) and NULL propagation.",
        "why_it_matters": (
            "<p>In standard programming languages, Boolean logic is binary: a statement is either <code>TRUE</code> or <code>FALSE</code>. "
            "In relational database theory, however, missing or unknown data introduces a third state: <strong><code>UNKNOWN</code></strong>. "
            "This Three-Valued Logic (3VL) is responsible for more silent production data corruption than almost any other SQL feature.</p>"
            "<p>For example, if you query <code>WHERE status != 'Inactive'</code>, you might expect to receive all active and pending users. But if a user's <code>status</code> is <code>NULL</code>, the expression <code>NULL != 'Inactive'</code> evaluates to <code>UNKNOWN</code>. "
            "Because the SQL <code>WHERE</code> clause requires expressions to evaluate to strictly <code>TRUE</code>, that row is silently omitted! This drill trains you to catch these silent bugs before your code touches production.</p>"
        ),
        "free_tools_guide": (
            "<p>Use any free AI assistant (ChatGPT Free, Claude Free, Gemini Free, or Copilot Free). No subscription required.</p>"
            "<p>Paste the prompt template below into a fresh chat. Treat the AI as your senior code reviewer who will challenge your answers.</p>"
        ),
        "prompt_template": (
            "Act as a pedantic Senior Database QA Engineer. I am writing PostgreSQL queries using WHERE, AND, OR, NOT, BETWEEN, LIKE, and IS NULL.\n"
            "Present me with 3 realistic SQL query snippets that contain subtle logic bugs related to:\n"
            "1. ANSI Three-Valued Logic (TRUE, FALSE, UNKNOWN) and NULL propagation (e.g., '= NULL' or 'NOT IN (subquery with NULL)').\n"
            "2. Operator precedence between AND and OR without proper parentheses.\n"
            "3. Inclusive vs. exclusive boundaries in BETWEEN with timestamps.\n"
            "Present the first buggy query snippet and ask me to identify the exact data trap and how to fix it. Do NOT reveal the fix until I attempt an answer."
        ),
        "playbook": (
            "<p>Follow this turn-by-turn debugging playbook:</p>"
            "<ol>"
            "<li><strong>Puzzle 1 (The NULL Trap):</strong> Look for <code>WHERE col = NULL</code> or <code>WHERE col != 'X'</code>. Point out that equality with NULL yields <code>UNKNOWN</code>, and prescribe <code>IS NULL</code> or <code>IS NOT DISTINCT FROM</code>.</li>"
            "<li><strong>Puzzle 2 (Boolean Operator Precedence):</strong> Analyze how <code>AND</code> binds tighter than <code>OR</code>. Explain how missing parentheses alter which rows satisfy the condition.</li>"
            "<li><strong>Puzzle 3 (BETWEEN with Timestamps):</strong> Explain why <code>BETWEEN '2026-01-01' AND '2026-01-31'</code> silently misses records created at <code>2026-01-31 14:30:00</code> because the string literal defaults to midnight (<code>00:00:00</code>).</li>"
            "</ol>"
        ),
        "participation_task": (
            "<p>Post your findings to the <strong>Unit 2 Discussion Board</strong>:</p>"
            "<ol>"
            "<li><strong>The Buggy Snippet:</strong> Share the trickiest SQL puzzle the QA Engineer presented to you.</li>"
            "<li><strong>The Data Trap:</strong> Explain why human intuition failed on that snippet and why 3VL or operator precedence caused unexpected results.</li>"
            "<li><strong>The Verified Fix:</strong> Post your corrected SQL snippet and PostgreSQL explanation.</li>"
            "</ol>"
        )
    },
    3: {
        "page_title": "Unit 3: Learn with AI — The Frantic Business VP & Multi-Table Joins",
        "persona": "Stressed VP of Operations at OmniRetail (Non-Technical Client)",
        "technique": "Non-Technical Stakeholder Role-Play & Entity-Relationship Mapping",
        "lead": "In this real-world role-play, the AI acts as a stressed-out, non-technical Vice President of Operations. You must interview the VP, translate messy business complaints into relational relationships, and construct multi-table JOINs without causing a Cartesian explosion.",
        "why_it_matters": (
            "<p>In industry, non-technical stakeholders never ask for an <code>INNER JOIN</code> or a <code>LEFT JOIN</code>. "
            "They burst into your office saying: <em>'Why did our marketing promotion in Texas show zero sales for repeat buyers? And make sure we do not duplicate line items when orders have multiple tracking numbers!'</em></p>"
            "<p>If an engineer does not understand entity cardinality (one-to-one, one-to-many, many-to-many), joining orders to order items and shipments creates a <strong>Cartesian product explosion</strong>, artificially duplicating revenue figures by orders of magnitude. This simulation teaches you the consultative interview skills necessary to clarify data relationships before writing JOIN syntax.</p>"
        ),
        "free_tools_guide": (
            "<p>Open ChatGPT Free, Claude Free, Gemini Free, or Copilot Free in your browser. Copy and paste the prompt below.</p>"
            "<p>Remember: The AI is instructed to stay in character as a business manager who does not know SQL. You must guide the conversation technically.</p>"
        ),
        "prompt_template": (
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
        "playbook": (
            "<p>How to navigate the client role-play:</p>"
            "<ol>"
            "<li><strong>Step 1 (Clarify Cardinality):</strong> Ask the VP: <em>'Can a customer place multiple orders? If a customer bought electronics twice, should their name appear once or twice?'</em></li>"
            "<li><strong>Step 2 (Identify Missing Data & Nulls):</strong> Inquire whether customers with zero orders should be included (identifying the need for a <code>LEFT JOIN ... WHERE orders.order_id IS NULL</code> anti-join).</li>"
            "<li><strong>Step 3 (Draft & Test):</strong> Propose the SQL statement and ask the AI to verify whether your JOIN predicates preserve correct aggregate totals without row multiplication.</li>"
            "</ol>"
        ),
        "participation_task": (
            "<p>Submit to the <strong>Unit 3 Discussion Board</strong>:</p>"
            "<ol>"
            "<li><strong>The VP's Urgent Business Request:</strong> Summarize the scenario and business problem presented by the AI.</li>"
            "<li><strong>Your Relational Strategy:</strong> Detail which JOIN types (INNER, LEFT, Anti-Join) you selected and why.</li>"
            "<li><strong>The Verified Query:</strong> Provide the final SQL statement and explain how your join conditions prevented duplicate rows.</li>"
            "</ol>"
        )
    },
    4: {
        "page_title": "Unit 4: Learn with AI — The CFO Financial Matrix & Safe Calculations",
        "persona": "Chief Financial Officer (CFO) & Executive Analytics Director",
        "technique": "Cross-Tab Pivoting & Division-by-Zero Defensive Engineering",
        "lead": "Drill with an AI CFO to transform raw, vertical transactional rows into executive cross-tab matrix dashboards using conditional aggregation (CASE inside SUM), group-level filtering (HAVING), and defensive division protection (NULLIF).",
        "why_it_matters": (
            "<p>Executive reporting demands horizontal cross-tab matrix formats: columns for Q1, Q2, Q3, and Q4 side-by-side per region or product category. "
            "While raw data is stored vertically (one row per transaction), writing four separate queries and merging them in Excel is slow, manual, and unscalable.</p>"
            "<p>Mastering conditional aggregation (<code>SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END)</code>) allows PostgreSQL to pivot datasets in a single high-speed scan. "
            "Furthermore, computing financial KPIs like profit margin or refund rate without <code>NULLIF(val, 0)</code> risks catastrophic runtime exceptions (<code>ERROR: division by zero</code>) when new branches or products have zero transactions. This drill prepares you for executive financial analytics.</p>"
        ),
        "free_tools_guide": (
            "<p>Use any free conversational AI tool (ChatGPT, Claude, Gemini, or Copilot). No credit card or paid tier needed.</p>"
        ),
        "prompt_template": (
            "Act as a CFO and Lead Analytics Architect. I need to generate an executive quarterly financial report from our sales database using PostgreSQL 16.\n"
            "Table: sales_transactions (transaction_id, region, department, quarter, revenue, discount_amount, refund_count)\n\n"
            "Challenge me to write an advanced aggregation query that produces a single cross-tab pivot matrix showing:\n"
            "1. Total revenue per region broken down into distinct columns for Q1, Q2, Q3, and Q4 using conditional CASE aggregation.\n"
            "2. The refund rate percentage (refund_count / total transactions), safely protected against division-by-zero using NULLIF.\n"
            "3. A HAVING filter that excludes regions with fewer than 50 total sales.\n"
            "Provide the requirements step-by-step. Review my SQL syntax, check for GROUP BY violations, and verify whether my matrix matches CFO dashboard standards."
        ),
        "playbook": (
            "<p>Execute your financial dashboard build in three stages:</p>"
            "<ol>"
            "<li><strong>Stage 1 (Grouping Rules):</strong> Identify which columns belong in the <code>GROUP BY</code> clause (e.g. <code>region</code>) and which must be wrapped in aggregates.</li>"
            "<li><strong>Stage 2 (Matrix Pivoting):</strong> Build the four quarterly columns using <code>SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1_revenue</code>.</li>"
            "<li><strong>Stage 3 (Safe Division & HAVING):</strong> Calculate refund ratios using <code>refund_count::FLOAT / NULLIF(total_transactions, 0)</code> and filter groups using <code>HAVING COUNT(*) >= 50</code>.</li>"
            "</ol>"
        ),
        "participation_task": (
            "<p>Post to the <strong>Unit 4 Discussion Board</strong>:</p>"
            "<ol>"
            "<li><strong>Your Cross-Tab Query:</strong> Share the completed SQL query that produces the CFO's executive matrix.</li>"
            "<li><strong>The Architecture Breakdown:</strong> Explain why conditional aggregation inside <code>SUM</code> eliminates the need for four separate queries.</li>"
            "<li><strong>Defense Verification:</strong> Explain how <code>NULLIF</code> prevented a runtime crash on edge cases.</li>"
            "</ol>"
        )
    },
    5: {
        "page_title": "Unit 5: Learn with AI — The Chaos SRE & Transaction Rollback Drills",
        "persona": "Database Reliability Engineer (Chaos SRE / Disaster Recovery Lead)",
        "technique": "Chaos Engineering & Atomic Transaction Rollback Drills",
        "lead": "Work through a high-stakes operational drill with an AI Site Reliability Engineer. You will perform bulk data updates and deletions on a simulated production database, responding to injected crashes, foreign key failures, and lock timeouts using safe transaction blocks and staging tables.",
        "why_it_matters": (
            "<p>In a production database, an unhedged <code>UPDATE</code> or <code>DELETE</code> without a verified <code>WHERE</code> clause is catastrophic. "
            "Once committed in autocommit mode, millions of customer records can be overwritten in milliseconds, requiring hours or days of painful point-in-time recovery from backups.</p>"
            "<p>Professional database engineers never run raw, unverified DML against production tables. They utilize the <strong>3-Step Protocol</strong>: test the filter with <code>SELECT</code>, wrap executions in explicit transaction blocks (<code>BEGIN; ... ROLLBACK;</code>) with <code>RETURNING</code> inspection, and stage complex ETL transformations inside temporary staging tables. This chaos drill builds the muscle memory to protect live production data.</p>"
        ),
        "free_tools_guide": (
            "<p>Access any free conversational AI tool (ChatGPT Free, Claude Free, Gemini Free, Copilot Free). Zero subscription cost.</p>"
        ),
        "prompt_template": (
            "Act as a Database Reliability Engineer (SRE). We are running critical data maintenance and ETL pipeline updates on a live production PostgreSQL 16 database.\n"
            "I will write DML scripts (INSERT, UPDATE, DELETE) using temporary staging tables, explicit transactions (BEGIN, COMMIT, ROLLBACK), and RETURNING clauses.\n"
            "Your role:\n"
            "1. Act as the safety reviewer: Red-team every query I write. If I write an UPDATE or DELETE without a verified WHERE clause, or without running inside a transaction, reject it with a catastrophic failure scenario.\n"
            "2. Introduce unexpected runtime anomalies (e.g., 'Constraint violation on row 452!', 'Network timeout during bulk insert!').\n"
            "3. Force me to demonstrate how my transaction script rolls back cleanly leaving zero orphaned records.\n"
            "Start by presenting me with our first maintenance mission: Purging inactive users while archiving their billing records into an audit staging table."
        ),
        "playbook": (
            "<p>Navigating the Chaos SRE drill:</p>"
            "<ol>"
            "<li><strong>Defense 1 (The Transaction Block):</strong> Never send a standalone modification. Wrap your script in <code>BEGIN; ... ROLLBACK;</code> until verified.</li>"
            "<li><strong>Defense 2 (Inspection with RETURNING):</strong> Always add <code>RETURNING user_id, email, status</code> to inspect the exact modified row stream before committing.</li>"
            "<li><strong>Defense 3 (Staging Table Isolation):</strong> Create a temporary staging table (<code>CREATE TEMP TABLE staged_archival AS ...</code>) to validate business rules in isolation.</li>"
            "</ol>"
        ),
        "participation_task": (
            "<p>Submit to the <strong>Unit 5 Discussion Board</strong>:</p>"
            "<ol>"
            "<li><strong>The Simulated Anomaly:</strong> Describe the failure or edge case injected by the Chaos SRE.</li>"
            "<li><strong>Your Safe DML Script:</strong> Post your defensive transaction block demonstrating safe staging, inspection, and rollback.</li>"
            "<li><strong>Production Reflection:</strong> Why is modifying live tables directly considered an unacceptable operational risk in modern DevOps?</li>"
            "</ol>"
        )
    },
    6: {
        "page_title": "Unit 6: Learn with AI — The Staff SQL Architect & CTE Refactoring",
        "persona": "Staff Database Architect (Principal Code Reviewer)",
        "technique": "Query Refactoring & Window Partitioning Deconstruction",
        "lead": "Submit an ugly, deeply nested subquery to an AI Staff Database Architect for an architectural code review. You will refactor the 'pyramid of doom' into clean, modular Common Table Expressions (CTEs) and non-collapsing analytical window functions.",
        "why_it_matters": (
            "<p>In legacy SQL codebases, calculating rankings or comparing individual rows against group averages often produces deeply nested subqueries 4 or 5 levels deep. "
            "These queries are unreadable, difficult to debug, and force the database query planner to perform redundant table scans.</p>"
            "<p>Modern PostgreSQL provides two transformative tools: <strong>Common Table Expressions (CTEs)</strong>, which turn nested logic into readable step-by-step pipelines, and <strong>Window Functions</strong> (<code>ROW_NUMBER()</code>, <code>RANK()</code>, <code>DENSE_RANK()</code>, <code>OVER (PARTITION BY ... ORDER BY ...)</code>), which compute group metrics without collapsing rows like <code>GROUP BY</code>. This drill elevates your code to enterprise architectural standards.</p>"
        ),
        "free_tools_guide": (
            "<p>Use ChatGPT Free, Claude Free, Gemini Free, or Copilot Free. No paid accounts needed.</p>"
        ),
        "prompt_template": (
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
        "playbook": (
            "<p>Follow the architectural refactoring workflow:</p>"
            "<ol>"
            "<li><strong>Step 1 (Deconstruct the Subqueries):</strong> Identify the distinct business questions being solved and separate them into named CTE blocks using <code>WITH</code>.</li>"
            "<li><strong>Step 2 (Apply Window Framing):</strong> Replace subquery aggregations with <code>AVG(salary) OVER (PARTITION BY department_id)</code>.</li>"
            "<li><strong>Step 3 (Rank & Deduplicate):</strong> Use <code>DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC)</code> to isolate top earners cleanly.</li>"
            "</ol>"
        ),
        "participation_task": (
            "<p>Post to the <strong>Unit 6 Discussion Board</strong>:</p>"
            "<ol>"
            "<li><strong>Before vs. After:</strong> Present the original nested subquery alongside your clean CTE and Window function query.</li>"
            "<li><strong>Row Preservation Concept:</strong> Explain in your own words why <code>PARTITION BY</code> does not collapse rows like <code>GROUP BY</code>.</li>"
            "<li><strong>Function Selection:</strong> Why would you choose <code>DENSE_RANK()</code> over <code>ROW_NUMBER()</code> when determining top compensation?</li>"
            "</ol>"
        )
    },
    7: {
        "page_title": "Unit 7: Learn with AI — The Enterprise Data Modeler & Normalization",
        "persona": "Senior Enterprise Data Modeler & Database Architect",
        "technique": "Normalization (1NF–3NF) Decomposition & DDL Constraint Hardening",
        "lead": "Collaborate with an AI Enterprise Data Modeler to decompose an unnormalized, chaotic spreadsheet into a bulletproof Third Normal Form (3NF) relational schema, complete with declarative constraints and reporting Views.",
        "why_it_matters": (
            "<p>Organizations run into severe operational crises when databases are designed like spreadsheets. "
            "Flat tables with repeating columns, multi-valued fields, and transitive dependencies cause three destructive anomalies: "
            "<strong>Insertion Anomalies</strong> (unable to record a course without enrolling a student), "
            "<strong>Update Anomalies</strong> (updating an address in one row leaves duplicate rows outdated), and "
            "<strong>Deletion Anomalies</strong> (deleting the last enrolled student deletes all record of the course existing).</p>"
            "<p>Normalizing a schema to 3NF guarantees data integrity at the mathematical level. Complementing that schema with declarative DDL constraints (<code>PRIMARY KEY</code>, <code>FOREIGN KEY</code>, <code>CHECK</code>, <code>UNIQUE</code>, <code>NOT NULL</code>) ensures the database engine itself enforces business rules. This drill builds your enterprise schema engineering capability.</p>"
        ),
        "free_tools_guide": (
            "<p>Open any free AI tool (ChatGPT Free, Claude Free, Gemini Free, Copilot Free). No subscription required.</p>"
        ),
        "prompt_template": (
            "Act as a Senior Enterprise Data Modeler. I am learning Relational Database Design, Normalization (1NF, 2NF, 3NF), and DDL constraint declaration in PostgreSQL 16.\n"
            "Give me a messy, denormalized 10-column spreadsheet table from a hospital clinic or university containing repeating groups, multi-valued fields, partial key dependencies, and transitive dependencies.\n"
            "Walk me through an interactive schema design challenge:\n"
            "Step 1: Ask me to identify the 1NF, 2NF, and 3NF violations in the spreadsheet.\n"
            "Step 2: Have me propose a normalized relational schema with entity tables, primary keys, and foreign keys.\n"
            "Step 3: Have me write the complete PostgreSQL DDL (CREATE TABLE) statements with strict constraints (CHECK, NOT NULL, UNIQUE, ON DELETE CASCADE/SET NULL) and a reporting VIEW.\n"
            "Critique my schema at each step. Do NOT write the DDL for me; guide me with design questions."
        ),
        "playbook": (
            "<p>Master the 3-step normalization progression:</p>"
            "<ol>"
            "<li><strong>Step 1 (1NF - Atomicity):</strong> Eliminate repeating groups and concatenated comma-separated values; establish primary keys.</li>"
            "<li><strong>Step 2 (2NF - Full Functional Dependency):</strong> Remove partial key dependencies (every non-key attribute must depend on the whole primary key).</li>"
            "<li><strong>Step 3 (3NF - Transitive Dependency):</strong> Remove transitive dependencies (non-key attributes cannot depend on other non-key attributes).</li>"
            "<li><strong>Step 4 (Constraint Hardening):</strong> Declare foreign keys with deliberate referential actions (e.g. <code>ON DELETE RESTRICT</code> vs <code>CASCADE</code>).</li>"
            "</ol>"
        ),
        "participation_task": (
            "<p>Submit to the <strong>Unit 7 Discussion Board</strong>:</p>"
            "<ol>"
            "<li><strong>The Spreadsheets Violations:</strong> List the specific 1NF, 2NF, and 3NF violations you identified in the AI's sample data.</li>"
            "<li><strong>Your 3NF Schema:</strong> List the normalized tables, primary keys, and foreign key relationships.</li>"
            "<li><strong>DDL & Referential Action:</strong> Share your PostgreSQL <code>CREATE TABLE</code> script and justify why your chosen <code>ON DELETE</code> rule prevents orphan records.</li>"
            "</ol>"
        )
    },
    8: {
        "page_title": "Unit 8: Learn with AI — The Senior Performance DBA Capstone Defense",
        "persona": "Senior Performance DBA & Capstone Defense Panel",
        "technique": "Execution Plan Profiling & Technical Architecture Defense",
        "lead": "Subject your comprehensive course capstone architecture to an intense 10-minute technical defense simulation with an AI Senior Performance DBA. You will defend your indexing strategies, explain EXPLAIN ANALYZE execution trees, and justify architectural trade-offs.",
        "why_it_matters": (
            "<p>In senior engineering roles and technical capstones, writing queries that simply 'work' is only half the battle. "
            "A query that returns in 5 milliseconds on a 500-row test dataset can freeze a production cluster for 45 seconds when scaled to 10 million rows if the query planner relies on a Sequential Scan.</p>"
            "<p>Furthermore, indexes are not free: every B-Tree index created imposes a <strong>Write Penalty</strong> on every <code>INSERT</code>, <code>UPDATE</code>, and <code>DELETE</code>, and composite indexes only accelerate queries that filter on the leftmost indexed columns. Defending your schema, execution plans, and index selectivity before a simulated DBA panel prepares you for real technical job interviews and enterprise defenses.</p>"
        ),
        "free_tools_guide": (
            "<p>Use ChatGPT Free, Claude Free, Gemini Free, or Copilot Free in your browser. Zero payment or subscription required.</p>"
        ),
        "prompt_template": (
            "Act as a demanding Database Administrator (DBA) and Technical Review Board conducting my final Capstone Defense for CMAP 1815.\n"
            "I have built a complete PostgreSQL database system with a normalized schema, DDL constraints, ETL transaction pipeline, analytical window queries, and B-Tree indexes.\n"
            "Conduct a 10-minute technical defense simulation:\n"
            "1. Ask me to provide one of my heaviest analytical queries and explain what EXPLAIN ANALYZE reveals about it (Seq Scan vs. Index Scan, Cost, Execution Time).\n"
            "2. Challenge me to defend my B-Tree indexing strategy: Explain composite index column order (Leftmost Prefix rule) and the Write Penalty on INSERT/UPDATE.\n"
            "3. Grill me with edge cases: What happens if table statistics are outdated (ANALYZE)? When would the query planner intentionally ignore an index?\n"
            "Ask one probing question at a time. Evaluate my answers rigorously like a real technical interview!"
        ),
        "playbook": (
            "<p>How to defend your capstone architecture:</p>"
            "<ol>"
            "<li><strong>Defense 1 (Execution Plans):</strong> Present an actual query and interpret the <code>Seq Scan vs Index Scan</code>, startup cost vs total cost, and actual runtime in milliseconds.</li>"
            "<li><strong>Defense 2 (The Leftmost Prefix Rule):</strong> Explain why an index on <code>(department_id, hire_date)</code> accelerates searches on department, but is useless for queries filtering only by hire date.</li>"
            "<li><strong>Defense 3 (The Write Penalty):</strong> Articulate why adding 15 indexes to a table degrades bulk data ingestion throughput.</li>"
            "</ol>"
        ),
        "participation_task": (
            "<p>Post to the <strong>Unit 8 Capstone Discussion Board</strong>:</p>"
            "<ol>"
            "<li><strong>The Hardest Defense Question:</strong> Share the most challenging technical question the DBA panel asked you.</li>"
            "<li><strong>Your Architectural Defense:</strong> How did you defend your indexing choices and query execution plan?</li>"
            "<li><strong>Key Takeaway:</strong> What is the single most important lesson you learned about database performance and optimization in CMAP 1815?</li>"
            "</ol>"
        )
    }
}

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

def render_designplus_html(title: str, lead_html: str, panels: list, page_id: str) -> str:
    """Renders HTML strictly adhering to the DesignPLUS classes from the user's institution."""
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
<meta name="workflow_state" content="active"/>
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
  <div class="dp-panels-wrapper dp-accordion-default dp-panel-color-dp-primary dp-panel-active-color-dp-secondary">
{body_panels}
  </div>
</div>
</body>
</html>"""

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

def build_assessment_meta_xml(quiz_id: str, quiz_title: str, quiz_group_id: str) -> str:
    """Builds Canvas assessment_meta.xml."""
    assign_id = make_id(f"assign_{quiz_id}")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<quiz xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd" identifier="{quiz_id}">
  <title>{html.escape(quiz_title)}</title>
  <description>&lt;p&gt;This weekly assessment tests your mastery of the relational SQL concepts, syntax, and query patterns covered in this unit.&lt;/p&gt;&lt;p&gt;The quiz consists of 15 multiple-choice questions (30 points total, 2 points each). You have 3 attempts; your highest score will be kept.&lt;/p&gt;</description>
  <shuffle_questions>false</shuffle_questions>
  <shuffle_answers>false</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <quiz_type>assignment</quiz_type>
  <points_possible>30.0</points_possible>
  <allowed_attempts>3</allowed_attempts>
  <show_correct_answers>true</show_correct_answers>
  <assignment identifier="{assign_id}">
    <title>{html.escape(quiz_title)}</title>
    <workflow_state>published</workflow_state>
    <quiz_identifierref>{quiz_id}</quiz_identifierref>
    <points_possible>30.0</points_possible>
    <grading_type>points</grading_type>
    <submission_types>online_quiz</submission_types>
    <assignment_group_identifierref>{quiz_group_id}</assignment_group_identifierref>
  </assignment>
</quiz>
"""

def main():
    print("=================================================================")
    print("CMAP 1815: Modern SQL - Canvas Course Export Package Builder")
    print("=================================================================")

    # 1. Prepare directories
    os.makedirs(OUTPUT_BUILD_DIR, exist_ok=True)
    wiki_dir = os.path.join(OUTPUT_BUILD_DIR, "wiki_content")
    settings_dir = os.path.join(OUTPUT_BUILD_DIR, "course_settings")
    non_cc_dir = os.path.join(OUTPUT_BUILD_DIR, "non_cc_assessments")
    os.makedirs(wiki_dir, exist_ok=True)
    os.makedirs(settings_dir, exist_ok=True)
    os.makedirs(non_cc_dir, exist_ok=True)

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
    # canvas_export.txt (Required signature for native Canvas Course Export Package)
    with open(os.path.join(settings_dir, "canvas_export.txt"), "w", encoding="utf-8") as f:
        f.write("Q: What did the panda say when he was forced out of his natural habitat?\nA: This is un-BEAR-able\n")

    # context.xml (Institutional Context matching LCCC)
    context_xml = """<?xml version="1.0" encoding="UTF-8"?>
<context_info xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <course_id>1815</course_id>
  <course_name>CMAP 1815: Introduction to Modern SQL</course_name>
  <root_account_id>105390000000000001</root_account_id>
  <root_account_name>Laramie County Community College</root_account_name>
  <root_account_uuid>dOSfRmBEqg50Ei3MOkNZrYHbdOlZxhVp0XEVGbQX</root_account_uuid>
  <canvas_domain>lccc-wy.instructure.com</canvas_domain>
</context_info>
"""
    with open(os.path.join(settings_dir, "context.xml"), "w", encoding="utf-8") as f:
        f.write(context_xml)

    # files_meta.xml
    files_meta_xml = """<?xml version="1.0" encoding="UTF-8"?>
<fileMeta xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <folders>
  </folders>
  <files>
  </files>
</fileMeta>
"""
    with open(os.path.join(settings_dir, "files_meta.xml"), "w", encoding="utf-8") as f:
        f.write(files_meta_xml)

    # course_settings.xml
    course_id = make_id("cmap_1815_course")
    course_settings_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<course identifier="{course_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>CMAP 1815: Introduction to Modern SQL</title>
  <course_code>CMAP 1815</course_code>
  <is_public>false</is_public>
  <default_view>modules</default_view>
  <license>private</license>
  <grading_standard_enabled>true</grading_standard_enabled>
  <root_account_uuid>dOSfRmBEqg50Ei3MOkNZrYHbdOlZxhVp0XEVGbQX</root_account_uuid>
</course>
"""
    with open(os.path.join(settings_dir, "course_settings.xml"), "w", encoding="utf-8") as f:
        f.write(course_settings_xml)

    # 4. Generate Wiki Pages & Track Manifest
    pages_manifest = []  # List of (filename, title, ident)
    modules_data = []    # List of modules for module_meta.xml and imsmanifest.xml

    # --- Orientation Module Pages ---
    p_welcome_id = make_id("page_welcome")
    p_welcome_file = "course-orientation-and-syllabus.html"
    welcome_lead = "<p>Welcome to <strong>CMAP 1815: Introduction to Modern SQL</strong>. This 8-week hybrid course trains you in professional relational database engineering using modern PostgreSQL 16.</p><p>Each week consists of 150 minutes of guided asynchronous preparation followed by 150 minutes of active classroom paired coding and hands-on laboratory exercises.</p>"
    welcome_panels = [
        ("Course Learning Outcomes (CLOs)", 
         "<ol><li><strong>CLO 1:</strong> Design, write, and debug SQL queries to retrieve, filter, and sort data from relational tables.</li><li><strong>CLO 2:</strong> Group and aggregate data, write modular subqueries, CTEs, and window functions to manipulate result sets.</li><li><strong>CLO 3:</strong> Translate real-world business requirements into correct, performant SQL statements.</li><li><strong>CLO 4:</strong> Safely execute data manipulation operations (INSERT, UPDATE, DELETE), manage transactions, and stage transformations using temporary tables.</li><li><strong>CLO 5:</strong> Design normalized relational schemas (1NF–3NF), write DDL scripts, declare integrity constraints, and create views.</li><li><strong>CLO 6:</strong> Profile query performance with EXPLAIN ANALYZE, engineer B-Tree indexes, and defend architectural choices in a comprehensive capstone.</li></ol>"),
        ("Grading & Evaluation Breakdown",
         "<ul><li><strong>Hands-on SQL Labs (40%):</strong> Weekly verified scripts executed in PostgreSQL 16.</li><li><strong>Unit Quizzes (20%):</strong> 15-question formative/evaluative knowledge checks.</li><li><strong>Asynchronous Preparation & Drills (10%):</strong> Pre-class study guides and self-checks.</li><li><strong>Comprehensive Course Capstone (30%):</strong> 3NF schema, DDL constraints, ETL staging, advanced window analytics, and index performance defense.</li></ul>"),
        ("Institutional Hybrid Time Commitment",
         "<p>In accordance with institutional accreditation standards, each week is budgeted for:</p><ul><li><strong>150 Minutes Asynchronous Guided Study:</strong> Micro-videos, PostgreSQLTutorial readings, and formative self-check drills.</li><li><strong>150 Minutes Synchronous Active Lab:</strong> Interactive live coding, pair programming challenges, and lab completion.</li></ul>")
    ]
    with open(os.path.join(wiki_dir, p_welcome_file), "w", encoding="utf-8") as f:
        f.write(render_designplus_html("Course Orientation & Master Syllabus", welcome_lead, welcome_panels, p_welcome_id))
    pages_manifest.append((p_welcome_file, "Course Orientation & Master Syllabus", p_welcome_id))

    # Dedicated Orientation Page: Learn with AI
    p_orient_ai_id = make_id("page_orient_learn_with_ai")
    p_orient_ai_file = "orientation-learn-with-ai.html"
    orient_ai_lead = "<p>In CMAP 1815, artificial intelligence is your interactive co-pilot, Socratic coach, and code reviewer—not a shortcut to avoid critical thinking. This master guide establishes our course framework for practicing SQL with 100% free conversational AI assistants.</p>"
    orient_ai_panels = [
        ("The AI Pair Programmer Philosophy",
         "<p>Writing SQL with AI is NOT about asking an AI to 'do the homework for you.' Blindly pasting AI-generated SQL into production environments causes catastrophic data outages, Cartesian product server crashes, and silent NULL propagation bugs.</p><p>Instead, in this course you will practice <strong>Active Socratic Learning with AI</strong>: you will assign the AI specialized roles (The Socratic Database Sensei, The Pedantic QA Lead, The Frantic Business Stakeholder, The Chaos SRE) to challenge your reasoning, test edge cases, and simulate real-world team dynamics.</p>"),
        ("The Big Four 100% Free AI Platforms",
         "<p>Every AI exercise in this course is designed for <strong>100% free web chat tools</strong>. You do NOT need any paid account or API key:</p><ul><li><strong>ChatGPT Free:</strong> <a href='https://chatgpt.com' target='_blank'>chatgpt.com</a> (select GPT-4o-mini / Free tier).</li><li><strong>Claude Free:</strong> <a href='https://claude.ai' target='_blank'>claude.ai</a> (free web tier).</li><li><strong>Google Gemini Free:</strong> <a href='https://gemini.google.com' target='_blank'>gemini.google.com</a> (free with any Google account).</li><li><strong>Microsoft Copilot Free:</strong> <a href='https://copilot.microsoft.com' target='_blank'>copilot.microsoft.com</a> (free web chat).</li></ul>"),
        ("The Verification Protocol: Grounded in PostgreSQL 16",
         "<p>Never assume an AI's SQL answer is correct! AI models frequently hallucinate non-existent PostgreSQL functions or write syntactically invalid clauses. The Golden Rule of CMAP 1815: <strong>Every single SQL snippet must be executed and verified against your live PostgreSQL 16 database in GitHub Codespaces before submission!</strong></p>")
    ]
    with open(os.path.join(wiki_dir, p_orient_ai_file), "w", encoding="utf-8") as f:
        f.write(render_designplus_html("Orientation: Learn with AI — How to Use Free AI as Your SQL Pair Programmer", orient_ai_lead, orient_ai_panels, p_orient_ai_id))
    pages_manifest.append((p_orient_ai_file, "Orientation: Learn with AI — How to Use Free AI as Your SQL Pair Programmer", p_orient_ai_id))

    # Page: Database Setup Guide
    p_setup_id = make_id("page_db_setup")
    p_setup_file = "database-setup-guide.html"
    setup_lead = "<p>CMAP 1815 uses modern <strong>PostgreSQL 16</strong> hosted in a zero-configuration cloud environment via GitHub Codespaces, or running locally on your workstation.</p>"
    setup_panels = [
        ("GitHub Codespaces Cloud Environment (Recommended)",
         "<p>Your repository includes a pre-configured <code>.devcontainer</code> that provisions a PostgreSQL 16 server automatically upon startup.</p><ol><li>Open the course GitHub repository in your browser.</li><li>Click the green <strong>Code</strong> button, navigate to the <strong>Codespaces</strong> tab, and click <strong>Create codespace on main</strong>.</li><li>Once loaded, open the integrated terminal and type <code>psql -U postgres</code> to access the database immediately!</li></ol>"),
        ("Database Schema & Sample Datasets",
         "<p>The course schema includes five core relational entities: <code>employees</code>, <code>locations</code>, <code>products</code>, <code>orders</code>, and <code>order_lines</code>, alongside the 10,000-row <code>superstore</code> dataset.</p><p>To initialize or reset your database, run:</p><pre><code>psql -U postgres -d postgres -f shared_assets/datasets/setup_chap1.sql</code></pre>")
    ]
    with open(os.path.join(wiki_dir, p_setup_file), "w", encoding="utf-8") as f:
        f.write(render_designplus_html("Database Setup & Environment Guide", setup_lead, setup_panels, p_setup_id))
    pages_manifest.append((p_setup_file, "Database Setup & Environment Guide", p_setup_id))

    # Page: External Resources Guide
    p_res_id = make_id("page_resources")
    p_res_file = "external-resources-guide.html"
    res_lead = "<p>All external readings and video lectures in CMAP 1815 are 100% free and open-access. This page catalogs the verified URLs and exact video chapter timestamps.</p>"
    res_panels = [
        ("Authoritative FreeCodeCamp Video Chapters",
         "<p>Official PostgreSQL Course (Timestamps verified to video description):</p><ul><li><strong>Unit 1:</strong> What is a Database (0:03:16) &amp; Relational Databases (0:05:17)</li><li><strong>Unit 2:</strong> Comparison Operators (1:50:18) &amp; Handling NULLs (2:15:42)</li><li><strong>Unit 3:</strong> Primary Keys (2:31:23) &amp; Foreign Key Joins (3:16:41)</li><li><strong>Unit 4:</strong> Aggregate Functions (2:36:14) &amp; GROUP BY (2:45:30)</li><li><strong>Unit 5:</strong> INSERT Operations (0:55:55) &amp; Safe DELETE/UPDATE (2:54:45)</li><li><strong>Unit 7:</strong> CREATE TABLE (0:41:37) &amp; Constraints (0:49:12)</li><li><strong>Unit 8:</strong> Exporting Results to CSV (3:47:27)</li></ul>"),
        ("Authoritative PostgreSQL Tutorial Guides",
         "<p>All units link directly to <a href='https://www.postgresqltutorial.com/' target='_blank'>PostgreSQLTutorial.com</a> and the <a href='https://www.postgresql.org/docs/current/' target='_blank'>Official PostgreSQL 16 Documentation</a>.</p>")
    ]
    with open(os.path.join(wiki_dir, p_res_file), "w", encoding="utf-8") as f:
        f.write(render_designplus_html("External Learning Resources & Media Guide", res_lead, res_panels, p_res_id))
    pages_manifest.append((p_res_file, "External Learning Resources & Media Guide", p_res_id))

    # Orientation Module items
    modules_data.append({
        "id": make_id("module_orientation"),
        "title": "Course Orientation & Database Setup",
        "items": [
            {"type": "WikiPage", "title": "Course Orientation & Master Syllabus", "ref": p_welcome_id},
            {"type": "WikiPage", "title": "Orientation: Learn with AI — How to Use Free AI as Your SQL Pair Programmer", "ref": p_orient_ai_id},
            {"type": "WikiPage", "title": "Database Setup & Environment Guide", "ref": p_setup_id},
            {"type": "WikiPage", "title": "External Learning Resources & Media Guide", "ref": p_res_id}
        ]
    })

    quiz_manifest = [] # List of (quiz_id, quiz_meta_id, title)

    # 5. Build Units 1 to 8
    for unit in UNIT_METADATA:
        u_num = unit["num"]
        u_folder = unit["folder"]
        u_title = unit["title"]
        u_short = unit["short_title"]
        u_topic = unit["topic"]

        print(f"Processing {u_short} ({u_folder})...")

        # --- A. Unit Overview Page ---
        overview_id = make_id(f"page_u{u_num}_overview")
        overview_file = f"unit-{u_num:02d}-overview.html"
        overview_lead = f"<p>Welcome to <strong>{u_title}</strong>. This unit focuses on mastering <em>{u_topic}</em> in modern PostgreSQL.</p><p>Please review the weekly learning objectives, engage in the dedicated <strong>Learn with AI</strong> practice drill, complete the asynchronous preparatory study guide, attend the active learning lab session, and complete the unit knowledge check.</p>"
        overview_panels = [
            ("Weekly Learning Objectives", 
             f"<p>Upon completing this unit, you will be able to apply core competencies in {u_topic}, analyze relational schema relationships, and execute production-grade queries with verified precision.</p>"),
            ("150-Minute Asynchronous Preparation",
             f"<p>Prior to class, complete the <strong>Learn with AI</strong> drill, watch the designated video chapters, complete the readings on PostgreSQLTutorial.com, and verify your understanding using the formative self-check drills.</p>"),
            ("150-Minute Synchronous Active Coding Lab",
             f"<p>During our interactive class sessions, you will participate in live coding demonstrations, collaborate on paired coding challenges, and submit your verified SQL laboratory script.</p>")
        ]
        with open(os.path.join(wiki_dir, overview_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(f"{u_short} Overview: {u_topic}", overview_lead, overview_panels, overview_id))
        pages_manifest.append((overview_file, f"{u_short} Overview: {u_topic}", overview_id))

        # --- B. Dedicated "Learn with AI" Page (Prominent, High-Level Section) ---
        ai_data = LEARN_WITH_AI_DATA[u_num]
        ai_page_id = make_id(f"page_u{u_num}_learn_with_ai")
        ai_page_file = f"unit-{u_num:02d}-learn-with-ai.html"
        ai_page_title = ai_data["page_title"]
        ai_lead = f"<p>{ai_data['lead']}</p>"
        ai_panels = [
            ("The Pedagogical Why: Why Practice with AI?", ai_data["why_it_matters"]),
            ("Zero-Cost Free AI Setup Guide", ai_data["free_tools_guide"]),
            ("The AI Role-Play Persona & Scenario", f"<p><strong>Persona / Role:</strong> {ai_data['persona']}</p><p><strong>Core Technique:</strong> {ai_data['technique']}</p>"),
            ("Copy-and-Paste Master Prompt", f"<p>Copy the exact prompt below into your free AI tool (ChatGPT Free, Claude Free, Gemini Free, or Copilot Free):</p><pre><code>{html.escape(ai_data['prompt_template'])}</code></pre>"),
            ("Turn-by-Turn Guided Playbook", ai_data["playbook"]),
            ("Asynchronous Participation & Discussion Task", ai_data["participation_task"])
        ]
        with open(os.path.join(wiki_dir, ai_page_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(ai_page_title, ai_lead, ai_panels, ai_page_id))
        pages_manifest.append((ai_page_file, ai_page_title, ai_page_id))

        # --- C. Unit Async Study Guide Page ---
        study_id = make_id(f"page_u{u_num}_study")
        study_file = f"unit-{u_num:02d}-async-study.html"
        study_lead = f"<p>This study guide guides your 150 minutes of asynchronous preparation for <strong>{u_short}</strong>. Complete these readings, video modules, and drills before attending the live laboratory session.</p>"
        
        # Format readings html
        readings_lis = "\n".join([f'<li><a href="{url}" target="_blank"><strong>{name}</strong></a></li>' for name, url in unit["readings"]])
        readings_html = f"<ul>{readings_lis}</ul>"
        
        # Format videos html
        videos_lis = "\n".join([f'<li><a href="{url}" target="_blank"><strong>{name}</strong></a> (Timestamp: {ts})</li>' for name, url, ts in unit["videos"]])
        videos_html = f"<ul>{videos_lis}</ul>"

        # Load self check drills
        drills_path = os.path.join(UNITS_DIR, u_folder, "async", "self_check_drills.md")
        drills_html = "<p>Complete the 5 formative self-check drills provided in your local repository under <code>async/self_check_drills.md</code>.</p>"
        if os.path.exists(drills_path):
            with open(drills_path, "r", encoding="utf-8") as df:
                d_text = df.read()
                drills_html = f"<pre><code>{html.escape(d_text[:1500])}... (Refer to repository for full drills)</code></pre>"

        study_panels = [
            ("Required Readings & Tutorials", readings_html),
            ("Required Micro-Lecture Video Chapters", videos_html),
            ("Formative Self-Check Drills", drills_html),
            ("Interactive AI Practice Drill", f"<p>Be sure to complete the dedicated <a href='$WIKI_REFERENCE$/pages/{ai_page_id}'><strong>{ai_page_title}</strong></a> module page and post your response to the weekly discussion board!</p>")
        ]
        with open(os.path.join(wiki_dir, study_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(f"{u_short} Async Study & Preparation", study_lead, study_panels, study_id))
        pages_manifest.append((study_file, f"{u_short} Async Study & Preparation", study_id))

        # --- D. Unit Lab Guide Page ---
        lab_id = make_id(f"page_u{u_num}_lab")
        lab_file = f"unit-{u_num:02d}-hands-on-lab.html"
        lab_lead = f"<p>In this laboratory session, you will implement production-grade SQL solutions applying <strong>{u_topic}</strong>. Review the tasks and rubric below, and submit your verified <code>.sql</code> script.</p>"

        lab_path = os.path.join(UNITS_DIR, u_folder, "guides", "student_lab_guide.md")
        lab_content_html = "<p>Refer to your course repository for the complete laboratory guide and scenario specifications.</p>"
        if os.path.exists(lab_path):
            with open(lab_path, "r", encoding="utf-8") as lf:
                l_text = lf.read()
                lab_content_html = f"<pre><code>{html.escape(l_text[:2000])}...</code></pre>"

        rubric_path = os.path.join(UNITS_DIR, u_folder, "assessments", "lab_rubric.md")
        rubric_html = "<p>Refer to your course repository for the complete grading rubric.</p>"
        if os.path.exists(rubric_path):
            with open(rubric_path, "r", encoding="utf-8") as rf:
                r_text = rf.read()
                rubric_html = f"<pre><code>{html.escape(r_text[:1500])}...</code></pre>"

        lab_panels = [
            ("Laboratory Scenario & Task Specifications", lab_content_html),
            ("Grading Rubric & Submission Requirements", rubric_html)
        ]
        with open(os.path.join(wiki_dir, lab_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(f"{u_short} Hands-on SQL Lab", lab_lead, lab_panels, lab_id))
        pages_manifest.append((lab_file, f"{u_short} Hands-on SQL Lab", lab_id))

        # --- E. Unit Quiz (QTI 1.2 XML) ---
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

        meta_xml_str = build_assessment_meta_xml(quiz_id, quiz_title, group_quizzes_id)
        with open(os.path.join(q_dir, "assessment_meta.xml"), "w", encoding="utf-8") as mf:
            mf.write(meta_xml_str)

        with open(os.path.join(non_cc_dir, f"{quiz_id}.xml.qti"), "w", encoding="utf-8") as ncf:
            ncf.write(qti_xml_str)

        quiz_manifest.append((quiz_id, quiz_meta_id, quiz_title))

        # Add Module with Learn with AI as prominent top-level section
        modules_data.append({
            "id": make_id(f"module_u{u_num}"),
            "title": u_title,
            "items": [
                {"type": "WikiPage", "title": f"{u_short} Overview: {u_topic}", "ref": overview_id},
                {"type": "WikiPage", "title": ai_page_title, "ref": ai_page_id},
                {"type": "WikiPage", "title": f"{u_short} Async Study & Preparation", "ref": study_id},
                {"type": "WikiPage", "title": f"{u_short} Hands-on SQL Lab", "ref": lab_id},
                {"type": "Quizzes::Quiz", "title": quiz_title, "ref": quiz_id}
            ]
        })

    # 6. Generate course_settings/module_meta.xml & ensure item identifiers match imsmanifest.xml
    modules_xml_items = []
    org_items = []

    for pos, mod in enumerate(modules_data, 1):
        mod_id = mod["id"]
        mod_title = mod["title"]
        m_items_xml = []
        m_man_items = []

        for i_pos, item in enumerate(mod["items"], 1):
            # Deterministic, SHARED item identifier for both module_meta.xml AND imsmanifest.xml
            shared_item_id = make_id(f"item_{mod_id}_{item['ref']}")

            m_items_xml.append(f"""      <item identifier="{shared_item_id}">
        <content_type>{item['type']}</content_type>
        <workflow_state>active</workflow_state>
        <title>{html.escape(item['title'])}</title>
        <identifierref>{item['ref']}</identifierref>
        <position>{i_pos}</position>
        <new_tab>false</new_tab>
        <indent>0</indent>
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

    # 7. Generate course_settings/syllabus.html
    syllabus_html = render_designplus_html(
        "CMAP 1815 Master Syllabus",
        welcome_lead,
        welcome_panels,
        make_id("syllabus_page")
    )
    with open(os.path.join(settings_dir, "syllabus.html"), "w", encoding="utf-8") as f:
        f.write(syllabus_html)

    # 8. Generate imsmanifest.xml (With Native Canvas Course Export Resource & Matching Identifiers)
    manifest_id = make_id("cmap_1815_manifest")
    org_items_joined = "\n".join(org_items)

    resources_xml = []
    # Primary Canvas Native Course Settings Resource (pointing to canvas_export.txt)
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

    # Wiki Pages Resources
    for p_file, p_title, p_id in pages_manifest:
        resources_xml.append(f"""    <resource identifier="{p_id}" type="webcontent" href="wiki_content/{p_file}">
      <file href="wiki_content/{p_file}"/>
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

    # 9. Schema & XML Well-Formedness Verification Suite
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

    # 10. Package into .imscc
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
