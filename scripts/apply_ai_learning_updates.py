import os
import sys
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UNITS_DIR = os.path.join(BASE_DIR, "units")
BUILDER_FILE = os.path.join(BASE_DIR, "scripts", "build_canvas_cartridge.py")

AI_LEARNING_DATA = {
    1: {
        "persona": "The Socratic Database Sensei (Professor Codd)",
        "technique": "Socratic Inversion & Execution Order Probing",
        "description": "Master relational query foundations by having the AI challenge your assumptions on how the database engine parses SQL versus how humans write it, focusing on projection, row deduplication, and production safety.",
        "free_tools": "ChatGPT Free (GPT-4o-mini), Claude Free, Google Gemini Free, Microsoft Copilot",
        "prompt_template": (
            "Act as a strict, Socratic SQL professor named Professor Codd. I am a student learning SQL SELECT statements "
            "and relational database fundamentals in PostgreSQL 16. Do NOT give me direct answers or write the SQL for me. "
            "Instead, ask me one challenging question at a time to test my understanding of:\n"
            "1. Why PostgreSQL evaluates FROM before SELECT during query execution.\n"
            "2. The fundamental difference between physical row storage and relational projection.\n"
            "3. Why 'SELECT *' is considered a dangerous anti-pattern in production microservices and reporting pipelines.\n"
            "Start by asking me your first question about query execution order. Wait for my response before evaluating my reasoning and asking the next question."
        ),
        "interactive_task": (
            "1. Open any free AI chat tool (ChatGPT Free, Claude Free, Gemini Free, or MS Copilot).\n"
            "2. Paste the prompt above.\n"
            "3. Answer Professor Codd's questions one at a time for at least 3 to 4 turns.\n"
            "4. If you get stuck, reply: 'Give me a real-world analogy to help me reason through this, but don't give me the answer yet!'"
        ),
        "participation_activity": (
            "In the Canvas Asynchronous Discussion for Unit 1, share: (1) The toughest question Professor Codd asked you, "
            "(2) The key insight you discovered about execution order or projection, and (3) One question you still have for our in-class session."
        )
    },
    2: {
        "persona": "The Pedantic QA Lead / Compiler",
        "technique": "Three-Valued Logic Red-Teaming & Edge-Case Traps",
        "description": "Stress-test your Boolean filtering logic against ANSI Three-Valued Logic (TRUE, FALSE, UNKNOWN), NULL propagation traps, and operator precedence.",
        "free_tools": "ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot",
        "prompt_template": (
            "Act as a pedantic Senior Database QA Engineer. I am writing PostgreSQL queries using WHERE, AND, OR, NOT, BETWEEN, LIKE, and IS NULL.\n"
            "Present me with 3 realistic SQL query snippets that contain subtle logic bugs related to:\n"
            "1. ANSI Three-Valued Logic (TRUE, FALSE, UNKNOWN) and NULL propagation (e.g., '= NULL' or 'NOT IN (subquery with NULL)').\n"
            "2. Operator precedence between AND and OR without proper parentheses.\n"
            "3. Inclusive vs. exclusive boundaries in BETWEEN with timestamps.\n"
            "Present the first buggy query snippet and ask me to identify the exact data trap and how to fix it. Do NOT reveal the fix until I attempt an answer."
        ),
        "interactive_task": (
            "1. Paste the prompt into your free AI tool.\n"
            "2. Analyze the QA Engineer's first puzzle. Explain why the query fails on edge-case data.\n"
            "3. Write the corrected SQL clause and submit it to the AI for verification.\n"
            "4. Work through all 3 puzzles."
        ),
        "participation_activity": (
            "In the Unit 2 Discussion, share: (1) One of the three-valued logic traps the AI gave you, "
            "(2) Why standard Boolean intuition (True/False) breaks down when NULL is involved, and (3) The corrected WHERE clause."
        )
    },
    3: {
        "persona": "The Demanding Business Client (VP of Operations)",
        "technique": "Non-Technical Stakeholder Role-Play & Entity-Relationship Mapping",
        "description": "Role-play with an AI acting as a frantic non-technical VP who speaks exclusively in vague business jargon. Translate their chaotic requirements into correct relational JOINs without creating a Cartesian product explosion.",
        "free_tools": "ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot",
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
        "interactive_task": (
            "1. Paste the prompt and read the VP's frantic business request.\n"
            "2. Ask clarifying questions (e.g., 'If a customer placed multiple orders, should they appear once or multiple times?').\n"
            "3. Draft the SQL query using appropriate JOINs (INNER, LEFT JOIN ... WHERE right_table.id IS NULL).\n"
            "4. Have the AI evaluate whether your JOIN condition avoids a Cartesian product explosion."
        ),
        "participation_activity": (
            "Post to the Unit 3 Discussion: (1) The VP's initial business problem, (2) The join strategy you selected (INNER vs. LEFT vs. Anti-Join) and why, and (3) The final verified query."
        )
    },
    4: {
        "persona": "The CFO Financial Reporting Coach",
        "technique": "Cross-Tab Pivoting & Division-by-Zero Defense",
        "description": "Collaborate with an AI CFO to build executive dashboard queries featuring matrix pivoting (CASE WHEN inside SUM), group filtering (HAVING), and zero-division protection (NULLIF).",
        "free_tools": "ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot",
        "prompt_template": (
            "Act as a CFO and Lead Analytics Architect. I need to generate an executive quarterly financial report from our sales database using PostgreSQL 16.\n"
            "Table: sales_transactions (transaction_id, region, department, quarter, revenue, discount_amount, refund_count)\n\n"
            "Challenge me to write an advanced aggregation query that produces a single cross-tab pivot matrix showing:\n"
            "1. Total revenue per region broken down into distinct columns for Q1, Q2, Q3, and Q4 using conditional CASE aggregation.\n"
            "2. The refund rate percentage (refund_count / total transactions), safely protected against division-by-zero using NULLIF.\n"
            "3. A HAVING filter that excludes regions with fewer than 50 total sales.\n"
            "Provide the requirements step-by-step. Review my SQL syntax, check for GROUP BY violations, and verify whether my matrix matches CFO dashboard standards."
        ),
        "interactive_task": (
            "1. Paste the prompt into your free AI tool.\n"
            "2. Write the conditional aggregation query using SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END).\n"
            "3. Protect calculations against division-by-zero using NULLIF.\n"
            "4. Apply the HAVING clause to filter grouped results. Iterate with the AI until the report meets CFO standards."
        ),
        "participation_activity": (
            "Submit to the Unit 4 Discussion: (1) Your completed cross-tab SQL query, (2) An explanation of why CASE inside SUM eliminates the need for separate queries, and (3) How NULLIF saved your calculations from throwing a runtime division-by-zero exception."
        )
    },
    5: {
        "persona": "The Database Disaster Recovery Lead (Reliability SRE)",
        "technique": "Chaos Engineering & Transaction Rollback Drills",
        "description": "Practice safe data modification, transaction control (BEGIN, COMMIT, ROLLBACK), and ETL staging tables by having the AI inject simulated production crashes and data corruption threats.",
        "free_tools": "ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot",
        "prompt_template": (
            "Act as a Database Reliability Engineer (SRE). We are running critical data maintenance and ETL pipeline updates on a live production PostgreSQL 16 database.\n"
            "I will write DML scripts (INSERT, UPDATE, DELETE) using temporary staging tables, explicit transactions (BEGIN, COMMIT, ROLLBACK), and RETURNING clauses.\n"
            "Your role:\n"
            "1. Act as the safety reviewer: Red-team every query I write. If I write an UPDATE or DELETE without a verified WHERE clause, or without running inside a transaction, reject it with a catastrophic failure scenario.\n"
            "2. Introduce unexpected runtime anomalies (e.g., 'Constraint violation on row 452!', 'Network timeout during bulk insert!').\n"
            "3. Force me to demonstrate how my transaction script rolls back cleanly leaving zero orphaned records.\n"
            "Start by presenting me with our first maintenance mission: Purging inactive users while archiving their billing records into an audit staging table."
        ),
        "interactive_task": (
            "1. Paste the prompt and inspect the maintenance mission.\n"
            "2. Wrap your DML in a defensive transaction block (BEGIN; ... ROLLBACK;) with RETURNING verification.\n"
            "3. Respond to the AI's simulated runtime failure by demonstrating a clean rollback.\n"
            "4. Refactor the script to use a staging table before committing."
        ),
        "participation_activity": (
            "Post to the Unit 5 Discussion: (1) The disaster scenario simulated by the AI, (2) The safe transaction script you engineered, and (3) The safety difference between modifying live tables directly vs. staging transformations in a temporary table."
        )
    },
    6: {
        "persona": "The Staff SQL Architect",
        "technique": "Query Refactoring & Window Partitioning Deconstruction",
        "description": "Refactor unreadable, slow nested subqueries into elegant Common Table Expressions (CTEs) and calculate running totals, moving averages, and ranks with analytical window functions.",
        "free_tools": "ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot",
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
        "interactive_task": (
            "1. Paste the prompt and review the AI's complex nested subquery.\n"
            "2. Break the query down into modular, sequential CTE steps using WITH.\n"
            "3. Apply analytical window functions (DENSE_RANK() OVER (...), AVG() OVER (...)).\n"
            "4. Submit your refactored SQL for architectural code review."
        ),
        "participation_activity": (
            "In the Unit 6 Discussion, share: (1) The original nested subquery vs. your clean CTE/Window function query, "
            "(2) Why PARTITION BY does not collapse rows like GROUP BY, and (3) When you would choose DENSE_RANK() over ROW_NUMBER()."
        )
    },
    7: {
        "persona": "The Enterprise Data Modeler",
        "technique": "Normalization Breakdown (1NF–3NF) & Constraint Hardening",
        "description": "Transform messy, unnormalized spreadsheet chaos into a clean Third Normal Form (3NF) relational model with bulletproof DDL constraints.",
        "free_tools": "ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot",
        "prompt_template": (
            "Act as a Senior Enterprise Data Modeler. I am learning Relational Database Design, Normalization (1NF, 2NF, 3NF), and DDL constraint declaration in PostgreSQL 16.\n"
            "Give me a messy, denormalized 10-column spreadsheet table from a hospital clinic or university containing repeating groups, multi-valued fields, partial key dependencies, and transitive dependencies.\n"
            "Walk me through an interactive schema design challenge:\n"
            "Step 1: Ask me to identify the 1NF, 2NF, and 3NF violations in the spreadsheet.\n"
            "Step 2: Have me propose a normalized relational schema with entity tables, primary keys, and foreign keys.\n"
            "Step 3: Have me write the complete PostgreSQL DDL (CREATE TABLE) statements with strict constraints (CHECK, NOT NULL, UNIQUE, ON DELETE CASCADE/SET NULL) and a reporting VIEW.\n"
            "Critique my schema at each step. Do NOT write the DDL for me; guide me with design questions."
        ),
        "interactive_task": (
            "1. Paste the prompt into your free AI tool.\n"
            "2. Identify insertion, update, and deletion anomalies in the unnormalized spreadsheet.\n"
            "3. Propose normalized 3NF entity tables with primary and foreign keys.\n"
            "4. Write production DDL with constraints and create a reporting VIEW. Submit to the modeler for review."
        ),
        "participation_activity": (
            "Post to the Unit 7 Discussion: (1) The denormalized spreadsheet sample, (2) Your 3NF entity-relationship breakdown, "
            "(3) Your production DDL script with constraints, and (4) Why your chosen ON DELETE referential action was the safest choice."
        )
    },
    8: {
        "persona": "The Senior Performance DBA & Capstone Defense Panel",
        "technique": "Execution Plan Profiling & Technical Architecture Defense",
        "description": "Subject your capstone project architecture, indexing decisions, and query execution plans (EXPLAIN ANALYZE) to a rigorous technical defense panel.",
        "free_tools": "ChatGPT Free, Claude Free, Google Gemini Free, Microsoft Copilot",
        "prompt_template": (
            "Act as a demanding Database Administrator (DBA) and Technical Review Board conducting my final Capstone Defense for CMAP 1815.\n"
            "I have built a complete PostgreSQL database system with a normalized schema, DDL constraints, ETL transaction pipeline, analytical window queries, and B-Tree indexes.\n"
            "Conduct a 10-minute technical defense simulation:\n"
            "1. Ask me to provide one of my heaviest analytical queries and explain what EXPLAIN ANALYZE reveals about it (Seq Scan vs. Index Scan, Cost, Execution Time).\n"
            "2. Challenge me to defend my B-Tree indexing strategy: Explain composite index column order (Leftmost Prefix rule) and the Write Penalty on INSERT/UPDATE.\n"
            "3. Grill me with edge cases: What happens if table statistics are outdated (ANALYZE)? When would the query planner intentionally ignore an index?\n"
            "Ask one probing question at a time. Evaluate my answers rigorously like a real technical interview!"
        ),
        "interactive_task": (
            "1. Paste the prompt into your free AI tool.\n"
            "2. Provide one of your heavy Unit 8 lab queries or capstone queries.\n"
            "3. Defend your index choices, composite column ordering, and EXPLAIN ANALYZE interpretations against the DBA panel.\n"
            "4. Complete 4 to 5 turns of technical defense."
        ),
        "participation_activity": (
            "Post to the Unit 8 Capstone Discussion: (1) The toughest technical question the DBA panel asked you, "
            "(2) Your defense explaining index column ordering or execution plans, and (3) Your key takeaway on how B-Tree indexes affect read performance vs. write throughput."
        )
    }
}

def update_study_guides():
    print("Updating study_guide.md files for Units 1 to 8...")
    unit_folders = sorted([f for f in os.listdir(UNITS_DIR) if f.startswith("unit_") and os.path.isdir(os.path.join(UNITS_DIR, f))])
    for f in unit_folders:
        match = re.match(r"unit_(\d+)", f)
        if not match:
            continue
        u_num = int(match.group(1))
        sg_path = os.path.join(UNITS_DIR, f, "async", "study_guide.md")
        if not os.path.exists(sg_path):
            print(f"Skipping {sg_path} (not found)")
            continue

        with open(sg_path, "r", encoding="utf-8") as file:
            content = file.read()

        ai = AI_LEARNING_DATA[u_num]

        # Check if already updated
        if "## Step 6: Learn with AI" in content or "## Step 6: Learning with AI" in content or "## Learning with AI" in content or "## Learn with AI" in content:
            print(f"Unit {u_num} already contains Learn with AI section. Updating section...")
            content = re.split(r"## (?:Step 6:\s*)?Learn(?:ing)? with AI", content)[0].rstrip()

        # Update Time Budget Breakdown table if not already including Step 6
        if "| **Step 6** |" not in content:
            content = re.sub(
                r"(\|\s*\*\*Step 5\*\*\s*\|[^\n]+\n)(\|\s*\*\*Total\*\*\s*\|[^\n]+\n)",
                r"\1| **Step 6** | Learn with AI: Interactive Practice Drill | **20 mins** | Persona-based prompt engineering & discussion post |\n\2",
                content
            )
        else:
            content = content.replace("Learning with AI", "Learn with AI")

        ai_markdown = f"""

---

## Step 6: Learn with AI — Interactive Practice & Prompt Craft (100% Free Tools)

### Role & Persona: {ai['persona']}
* **Pedagogical Technique:** {ai['technique']}
* **Core Goal:** {ai['description']}
* **Recommended Free Tools:** {ai['free_tools']} *(Zero subscription or paid API key required)*

#### Copy-and-Paste AI Prompt Template
```text
{ai['prompt_template']}
```

#### Step-by-Step Interactive Drill
{ai['interactive_task']}

#### Asynchronous Participation Deliverable
> **Canvas Discussion Prompt:**
> {ai['participation_activity']}
"""
        new_content = content + ai_markdown
        with open(sg_path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Updated {f}/async/study_guide.md successfully.")

if __name__ == "__main__":
    update_study_guides()
