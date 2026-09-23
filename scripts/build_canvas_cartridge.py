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
        
        # Prepare options and identifiers
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
    print("CMAP 1815: Modern SQL - Canvas Cartridge (.imscc) Builder")
    print("=================================================================")

    # Ensure build directories exist
    os.makedirs(OUTPUT_BUILD_DIR, exist_ok=True)
    wiki_dir = os.path.join(OUTPUT_BUILD_DIR, "wiki_content")
    settings_dir = os.path.join(OUTPUT_BUILD_DIR, "course_settings")
    non_cc_dir = os.path.join(OUTPUT_BUILD_DIR, "non_cc_assessments")
    os.makedirs(wiki_dir, exist_ok=True)
    os.makedirs(settings_dir, exist_ok=True)
    os.makedirs(non_cc_dir, exist_ok=True)

    # Assignment Groups
    group_labs_id = make_id("group_labs")
    group_quizzes_id = make_id("group_quizzes")
    group_prep_id = make_id("group_prep")
    group_capstone_id = make_id("group_capstone")

    # 1. Generate course_settings/assignment_groups.xml
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

    # 2. Generate course_settings/course_settings.xml
    course_id = make_id("cmap_1815_course")
    course_settings_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<course identifier="{course_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>CMAP 1815: Introduction to Modern SQL</title>
  <course_code>CMAP 1815</course_code>
  <is_public>false</is_public>
  <default_view>modules</default_view>
  <license>private</license>
  <grading_standard_enabled>true</grading_standard_enabled>
</course>
"""
    with open(os.path.join(settings_dir, "course_settings.xml"), "w", encoding="utf-8") as f:
        f.write(course_settings_xml)

    # 3. Generate Course Welcome & Orientation Pages in wiki_content
    pages_manifest = []  # List of (filename, title, ident)
    
    # Page: Start Here Welcome
    p_welcome_id = make_id("page_welcome")
    p_welcome_file = "course-orientation-and-syllabus.html"
    welcome_lead = "<p>Welcome to <strong>CMAP 1815: Introduction to Modern SQL</strong>. This 8-week hybrid course trains you in professional relational database engineering using modern PostgreSQL 16.</p><p>Each week consists of 150 minutes of guided asynchronous preparation (interactive video chapters, tutorials, and formative drills) followed by 150 minutes of active classroom paired coding and hands-on laboratory exercises.</p>"
    welcome_panels = [
        ("Course Learning Outcomes (CLOs)", 
         "<ol><li><strong>CLO 1:</strong> Design, write, and debug SQL queries to retrieve, filter, and sort data from relational tables.</li><li><strong>CLO 2:</strong> Group and aggregate data, write modular subqueries, CTEs, and window functions to manipulate result sets.</li><li><strong>CLO 3:</strong> Translate real-world business requirements into correct, performant SQL statements.</li><li><strong>CLO 4:</strong> Safely execute data manipulation operations (INSERT, UPDATE, DELETE), manage transactions, and stage transformations using temporary tables.</li><li><strong>CLO 5:</strong> Design normalized relational schemas (1NF–3NF), write DDL scripts, declare integrity constraints, and create views.</li><li><strong>CLO 6:</strong> Profile query performance with EXPLAIN ANALYZE, engineer B-Tree indexes, and defend architectural choices in a comprehensive capstone.</li></ol>"),
        ("Grading & Evaluation Breakdown",
         "<ul><li><strong>Hands-on SQL Labs (40%):</strong> Weekly verified scripts executed in PostgreSQL 16.</li><li><strong>Unit Quizzes (20%):</strong> 15-question formative/evaluative knowledge checks.</li><li><strong>Asynchronous Preparation & Drills (10%):</strong> Pre-class study guides and self-checks.</li><li><strong>Comprehensive Course Capstone (30%):</strong> 3NF schema, DDL constraints, ETL staging, advanced window analytics, and index performance defense.</li></ul>"),
        ("Institutional Hybrid Time Commitment",
         "<p>In accordance with institutional accreditation standards, each week is budgeted for:</p><ul><li><strong>150 Minutes Asynchronous Guided Study:</strong> Micro-videos, PostgreSQLTutorial readings, and 5 self-check drills.</li><li><strong>150 Minutes Synchronous Active Lab:</strong> Interactive live coding, pair programming challenges, and lab completion.</li></ul>")
    ]
    with open(os.path.join(wiki_dir, p_welcome_file), "w", encoding="utf-8") as f:
        f.write(render_designplus_html("Course Orientation & Master Syllabus", welcome_lead, welcome_panels, p_welcome_id))
    pages_manifest.append((p_welcome_file, "Course Orientation & Master Syllabus", p_welcome_id))

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

    # 4. Generate Pages and Quizzes for Units 1 to 8
    modules_data = [] # List of modules for module_meta.xml
    modules_data.append({
        "id": make_id("module_orientation"),
        "title": "Course Orientation & Database Setup",
        "items": [
            {"type": "WikiPage", "title": "Course Orientation & Master Syllabus", "ref": p_welcome_id},
            {"type": "WikiPage", "title": "Database Setup & Environment Guide", "ref": p_setup_id},
            {"type": "WikiPage", "title": "External Learning Resources & Media Guide", "ref": p_res_id}
        ]
    })

    quiz_manifest = [] # List of (quiz_id, quiz_meta_id, title)

    for unit in UNIT_METADATA:
        u_num = unit["num"]
        u_folder = unit["folder"]
        u_title = unit["title"]
        u_short = unit["short_title"]
        u_topic = unit["topic"]

        print(f"Processing {u_short} ({u_folder})...")

        # --- Unit Overview Page ---
        overview_id = make_id(f"page_u{u_num}_overview")
        overview_file = f"unit-{u_num:02d}-overview.html"
        overview_lead = f"<p>Welcome to <strong>{u_title}</strong>. This unit focuses on mastering <em>{u_topic}</em> in modern PostgreSQL.</p><p>Please review the weekly learning objectives, complete the asynchronous preparatory study guide, attend the active learning lab session, and complete the unit knowledge check.</p>"
        overview_panels = [
            ("Weekly Learning Objectives", 
             f"<p>Upon completing this unit, you will be able to apply core competencies in {u_topic}, analyze relational schema relationships, and execute production-grade queries with verified precision.</p>"),
            ("150-Minute Asynchronous Preparation",
             f"<p>Prior to class, watch the designated video chapters, complete the readings on PostgreSQLTutorial.com, and verify your understanding using the 5 formative self-check drills.</p>"),
            ("150-Minute Synchronous Active Coding Lab",
             f"<p>During our interactive class sessions, you will participate in live coding demonstrations, collaborate on paired coding challenges, and submit your verified SQL laboratory script.</p>")
        ]
        with open(os.path.join(wiki_dir, overview_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(f"{u_short} Overview: {u_topic}", overview_lead, overview_panels, overview_id))
        pages_manifest.append((overview_file, f"{u_short} Overview: {u_topic}", overview_id))

        # --- Unit Async Study Guide Page ---
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
        drills_html = "<p>Complete the 5 formative self-check drills provided in your local repository repository under <code>async/self_check_drills.md</code>.</p>"
        if os.path.exists(drills_path):
            with open(drills_path, "r", encoding="utf-8") as df:
                d_text = df.read()
                drills_html = f"<pre><code>{html.escape(d_text[:1500])}... (Refer to repository for full drills)</code></pre>"

        study_panels = [
            ("Required Readings & Tutorials", readings_html),
            ("Required Micro-Lecture Video Chapters", videos_html),
            ("Formative Self-Check Drills", drills_html)
        ]
        with open(os.path.join(wiki_dir, study_file), "w", encoding="utf-8") as f:
            f.write(render_designplus_html(f"{u_short} Async Study & Preparation", study_lead, study_panels, study_id))
        pages_manifest.append((study_file, f"{u_short} Async Study & Preparation", study_id))

        # --- Unit Lab Guide Page ---
        lab_id = make_id(f"page_u{u_num}_lab")
        lab_file = f"unit-{u_num:02d}-hands-on-lab.html"
        lab_lead = f"<p>In this laboratory session, you will implement production-grade SQL solutions applying <strong>{u_topic}</strong>. Review the tasks and rubric below, and submit your verified <code>.sql</code> script.</p>"

        # Load student lab guide
        lab_path = os.path.join(UNITS_DIR, u_folder, "guides", "student_lab_guide.md")
        lab_content_html = "<p>Refer to your course repository for the complete laboratory guide and scenario specifications.</p>"
        if os.path.exists(lab_path):
            with open(lab_path, "r", encoding="utf-8") as lf:
                l_text = lf.read()
                lab_content_html = f"<pre><code>{html.escape(l_text[:2000])}...</code></pre>"

        # Load rubric
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

        # --- Unit Quiz (QTI 1.2 XML) ---
        quiz_path = os.path.join(UNITS_DIR, u_folder, "assessments", "unit_quiz.md")
        questions = parse_quiz_md(quiz_path)
        quiz_id = make_id(f"quiz_u{u_num}")
        quiz_meta_id = make_id(f"quiz_meta_u{u_num}")
        quiz_title = f"{u_short} Knowledge Check: {u_topic}"

        # Create quiz folder
        q_dir = os.path.join(OUTPUT_BUILD_DIR, quiz_id)
        os.makedirs(q_dir, exist_ok=True)

        qti_xml_str = build_qti_xml(quiz_id, quiz_title, questions)
        with open(os.path.join(q_dir, "assessment_qti.xml"), "w", encoding="utf-8") as qf:
            qf.write(qti_xml_str)

        meta_xml_str = build_assessment_meta_xml(quiz_id, quiz_title, group_quizzes_id)
        with open(os.path.join(q_dir, "assessment_meta.xml"), "w", encoding="utf-8") as mf:
            mf.write(meta_xml_str)

        # Write non_cc_assessment copy
        with open(os.path.join(non_cc_dir, f"{quiz_id}.xml.qti"), "w", encoding="utf-8") as ncf:
            ncf.write(qti_xml_str)

        quiz_manifest.append((quiz_id, quiz_meta_id, quiz_title))

        # Add Module Definition
        modules_data.append({
            "id": make_id(f"module_u{u_num}"),
            "title": u_title,
            "items": [
                {"type": "WikiPage", "title": f"{u_short} Overview: {u_topic}", "ref": overview_id},
                {"type": "WikiPage", "title": f"{u_short} Async Study & Preparation", "ref": study_id},
                {"type": "WikiPage", "title": f"{u_short} Hands-on SQL Lab", "ref": lab_id},
                {"type": "Quizzes::Quiz", "title": quiz_title, "ref": quiz_id}
            ]
        })

    # 5. Generate course_settings/module_meta.xml
    modules_xml_items = []
    for pos, mod in enumerate(modules_data, 1):
        items_xml = []
        for i_pos, item in enumerate(mod["items"], 1):
            item_id = make_id(f"mod_item_{mod['id']}_{i_pos}")
            items_xml.append(f"""      <item identifier="{item_id}">
        <content_type>{item['type']}</content_type>
        <workflow_state>published</workflow_state>
        <title>{html.escape(item['title'])}</title>
        <identifierref>{item['ref']}</identifierref>
        <position>{i_pos}</position>
        <new_tab>false</new_tab>
        <indent>0</indent>
      </item>""")
        items_joined = "\n".join(items_xml)
        modules_xml_items.append(f"""  <module identifier="{mod['id']}">
    <title>{html.escape(mod['title'])}</title>
    <workflow_state>published</workflow_state>
    <position>{pos}</position>
    <items>
{items_joined}
    </items>
  </module>""")

    modules_meta_joined = "\n".join(modules_xml_items)
    modules_meta_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<modules xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
{modules_meta_joined}
</modules>
"""
    with open(os.path.join(settings_dir, "module_meta.xml"), "w", encoding="utf-8") as f:
        f.write(modules_meta_str)

    # 6. Generate course_settings/syllabus.html
    syllabus_html = render_designplus_html(
        "CMAP 1815 Master Syllabus",
        welcome_lead,
        welcome_panels,
        make_id("syllabus_page")
    )
    with open(os.path.join(settings_dir, "syllabus.html"), "w", encoding="utf-8") as f:
        f.write(syllabus_html)

    # 7. Generate imsmanifest.xml
    manifest_id = make_id("cmap_1815_manifest")
    org_items = []
    for mod in modules_data:
        m_items = []
        for item in mod["items"]:
            item_node_id = make_id(f"man_item_{mod['id']}_{item['ref']}")
            m_items.append(f"""          <item identifier="{item_node_id}" identifierref="{item['ref']}">
            <title>{html.escape(item['title'])}</title>
          </item>""")
        m_items_joined = "\n".join(m_items)
        org_items.append(f"""        <item identifier="{mod['id']}">
          <title>{html.escape(mod['title'])}</title>
{m_items_joined}
        </item>""")

    # Resources
    resources_xml = []
    # Settings & Syllabus
    resources_xml.append(f"""    <resource identifier="{course_id}_syllabus" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/syllabus.html" intendeduse="syllabus">
      <file href="course_settings/syllabus.html"/>
    </resource>""")

    # Wiki Pages
    for p_file, p_title, p_id in pages_manifest:
        resources_xml.append(f"""    <resource identifier="{p_id}" type="webcontent" href="wiki_content/{p_file}">
      <file href="wiki_content/{p_file}"/>
    </resource>""")

    # Quizzes
    for q_id, q_meta_id, q_title in quiz_manifest:
        resources_xml.append(f"""    <resource identifier="{q_id}" type="imsqti_xmlv1p2/imscc_xmlv1p1/assessment">
      <file href="{q_id}/assessment_qti.xml"/>
      <dependency identifierref="{q_meta_id}"/>
    </resource>
    <resource identifier="{q_meta_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{q_id}/assessment_meta.xml">
      <file href="{q_id}/assessment_meta.xml"/>
      <file href="non_cc_assessments/{q_id}.xml.qti"/>
    </resource>""")

    org_items_joined = "\n".join(org_items)
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
                except ET.ParseError as e:
                    print(f"FATAL: XML Parse Error in {file_path}: {e}")
                    sys.exit(1)
    print(f"SUCCESS: Verified {xml_files_tested} XML files. Zero syntax errors!")

    # 9. Pack into .imscc ZIP Archive
    print(f"\n--- Packaging into {IMSCC_OUTPUT_FILE} ---")
    file_count = 0
    with zipfile.ZipFile(IMSCC_OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(OUTPUT_BUILD_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, OUTPUT_BUILD_DIR)
                zipf.write(full_path, rel_path)
                file_count += 1

    file_size_mb = os.path.getsize(IMSCC_OUTPUT_FILE) / (1024 * 1024)
    print(f"SUCCESS: Created {IMSCC_OUTPUT_FILE} ({file_count} files, {file_size_mb:.2f} MB)")
    print("Canvas Cartridge build complete!\n")

if __name__ == "__main__":
    main()
