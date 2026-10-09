#!/usr/bin/env python3
"""
Updates CMAP_1815_Master_Syllabus.docx with official B8 asynchronous course data:
- B8 schedule: October 19 – December 18
- Modality: Fully Asynchronous Online via Canvas
- Drop deadline: October 23, 2026
- Withdrawal deadline: November 24, 2026
- Course Content Outline: 8 Units of Modern SQL + Thanksgiving Break
- Course Notes: PostgreSQL 16, Codespaces, Orientation Video (https://youtu.be/_u3g4LZ142Q)
- Course Competencies: 7 Relational SQL Learning Outcomes
- Class Cancellation Announcements: Stripped red instruction prompt
- Grading: 40% Labs, 30% Capstone, 20% Quizzes, 10% Asynchronous Preparation & AI
- Stripped CET deleted comment tag (<w:del>) between AI and Classroom Behavior
"""

import os
import copy
import shutil
import zipfile
import xml.etree.ElementTree as ET

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def w(tag):
    return f'{{{W_NS}}}{tag}'

def set_p_runs(p_elem, runs_spec):
    pPr = p_elem.find(w('pPr'))
    to_remove = [c for c in p_elem if c != pPr]
    for c in to_remove:
        p_elem.remove(c)

    for spec in runs_spec:
        r = ET.SubElement(p_elem, w('r'))
        rPr = ET.SubElement(r, w('rPr'))
        if spec.get('font'):
            rf = ET.SubElement(rPr, w('rFonts'))
            rf.attrib[w('cstheme')] = spec['font']
        if spec.get('bold'):
            ET.SubElement(rPr, w('b'))
            ET.SubElement(rPr, w('bCs'))
        if spec.get('italic'):
            ET.SubElement(rPr, w('i'))
            ET.SubElement(rPr, w('iCs'))
        if spec.get('color'):
            col = ET.SubElement(rPr, w('color'))
            col.attrib[w('val')] = spec['color']
        if spec.get('size'):
            sz = ET.SubElement(rPr, w('sz'))
            sz.attrib[w('val')] = str(spec['size'])
            szCs = ET.SubElement(rPr, w('szCs'))
            szCs.attrib[w('val')] = str(spec['size'])
        
        t = ET.SubElement(r, w('t'))
        txt = spec.get('text', '')
        if txt.startswith(' ') or txt.endswith(' ') or '  ' in txt:
            t.attrib['{http://www.w3.org/XML/1998/namespace}space'] = 'preserve'
        t.text = txt

def make_clone_p(template_p, runs_spec):
    new_p = copy.deepcopy(template_p)
    set_p_runs(new_p, runs_spec)
    return new_p

def update_syllabus(docx_path: str, backup: bool = True):
    if backup:
        bak_path = docx_path + ".orig"
        if not os.path.exists(bak_path):
            shutil.copy2(docx_path, bak_path)
            print(f"[Backup] Saved original to {bak_path}")

    with zipfile.ZipFile(docx_path, 'r') as z_in:
        all_files = {name: z_in.read(name) for name in z_in.namelist()}

    xml_content = all_files['word/document.xml']
    root = ET.fromstring(xml_content)
    body = root.find(w('body'))

    children = list(body)
    p_elements = [c for c in children if c.tag == w('p')]

    # 1. Block (P3)
    set_p_runs(p_elements[3], [
        {'text': 'Block: B8 October 19 – December 18', 'bold': False, 'color': '000000', 'size': 24}
    ])

    # 2. Course Number, Title, and Credit Hours (P5)
    set_p_runs(p_elements[5], [
        {'text': 'Course Number, Title, and Credit Hours: ', 'bold': True, 'size': 22},
        {'text': 'CMAP 1815: Introduction to Modern SQL – 3 Credit Hours', 'bold': True, 'size': 22}
    ])

    # 3. Time and Location (P6)
    set_p_runs(p_elements[6], [
        {'text': 'Time and Location: ', 'bold': True, 'size': 22},
        {'text': 'Online Asynchronous (Access online via Canvas only)', 'bold': False, 'size': 22}
    ])

    # 4. Drop / Withdraw Dates (P15)
    set_p_runs(p_elements[15], [
        {'text': 'Last Date to Drop or Withdraw: ', 'bold': True, 'size': 22},
        {'text': 'The last day to drop this course to receive a 100% refund and NOT receive a W on your transcript is October 23. The last day to withdraw from this course is November 24. Please consult with Enrollment Services or your Student Success Coach and Student Hub before initiating any schedule changes so you know how a change might affect your timing for graduating and financing.', 'bold': False, 'size': 22}
    ])

    # 5. Other Course Information (P17)
    set_p_runs(p_elements[17], [
        {'text': 'Other Course Information: ', 'bold': True, 'size': 22},
        {'text': 'This course is taught fully online asynchronously via Canvas. Students complete weekly guided learning, hands-on SQL labs, and knowledge check assessments on a structured 8-week schedule.', 'bold': False, 'size': 22}
    ])

    # 6. Duration & Learning Method (P19)
    set_p_runs(p_elements[19], [
        {'text': 'The course will take place over 8 weeks (B8 block). You will gain knowledge through video micro-lectures, curated PostgreSQL readings, interactive drills, and supplemental content pages, and will be assessed through weekly hands-on SQL labs executed against PostgreSQL 16, unit quizzes, asynchronous preparation discussions, and a comprehensive project-based course capstone.', 'bold': False, 'size': 22}
    ])

    # 7. Textbook (P25)
    set_p_runs(p_elements[25], [
        {'text': 'Textbook: ', 'bold': True, 'size': 22},
        {'text': 'None (Zero Textbook Cost / OER). All required reading materials, PostgreSQL 16 documentation, and interactive tutorials (Neon Serverless PostgreSQL guides) are provided directly in Canvas modules and course documentation.', 'bold': False, 'size': 22}
    ])

    # 8. Lab Manual (P27)
    set_p_runs(p_elements[27], [
        {'text': 'Lab Manual: ', 'bold': True, 'size': 22},
        {'text': 'Comprehensive lab guides and starter SQL challenge files are provided inside each weekly module in Canvas.', 'bold': False, 'size': 22}
    ])

    # 9. Other (P28)
    set_p_runs(p_elements[28], [
        {'text': 'Other / Software: ', 'bold': True, 'size': 22},
        {'text': 'PostgreSQL 16, pgAdmin 4 / psql, and GitHub Codespaces (or VS Code with SQLTools). A modern web browser with reliable Internet access to navigate Canvas and course resources.', 'bold': False, 'size': 22}
    ])

    # 10. Additional Requirements (P30)
    set_p_runs(p_elements[30], [
        {'text': 'Additional Requirements: ', 'bold': True, 'size': 22},
        {'text': 'A computer capable of running a modern web browser and accessing cloud or local PostgreSQL environments.', 'bold': False, 'size': 22}
    ])

    # 11. Course Content Outline (P33 to P38)
    outline_units = [
        ("Unit 1: Selection & Relational Fundamentals (10/19 – 10/25):", " The Relational Model, Projection, SELECT, Column Aliases (AS), Deduplication (DISTINCT), and Sorting (ORDER BY)."),
        ("Unit 2: Precision Filtering & Boolean Logic (10/26 – 11/1):", " Targeted Row Filtering (WHERE), Comparison Operators, Boolean Gates (AND, OR, NOT), Range/List Inclusion (BETWEEN, IN), Pattern Matching (LIKE/ILIKE), Three-Valued Logic (NULL), and Pagination (LIMIT/OFFSET)."),
        ("Unit 3: Relational Joins & Multi-Table Operations (11/2 – 11/8):", " Entity Relationships (PK/FK), ANSI Standard Joins, INNER JOIN, Outer Joins (LEFT, RIGHT, FULL OUTER), Self-Joins, Cross Joins, and the Anti-Join Pattern."),
        ("Unit 4: Aggregations, Grouping & Analytical Summaries (11/9 – 11/15):", " Summary Metrics (COUNT, SUM, AVG, MIN, MAX), Aggregation Boundaries (GROUP BY), Post-Aggregation Filtering (HAVING), Set Operations (UNION, INTERSECT, EXCEPT), and Conditional Aggregations (CASE WHEN)."),
        ("Unit 5: Safe DML, Modifications & Staging Architecture (11/16 – 11/22):", " Safe Data Manipulation (INSERT, UPDATE, DELETE, MERGE/UPSERT), Transaction Isolation & Safety (BEGIN, COMMIT, ROLLBACK), Pre-Execution Verification Protocol, and Session Staging (TEMPORARY TABLE)."),
        ("Thanksgiving Break (11/23 – 11/29):", " No Classes Scheduled / College Closed Nov 25–29."),
        ("Unit 6: Query Modularity, CTEs & Window Functions (11/30 – 12/6):", " Subqueries (Scalar, Correlated), Common Table Expressions (WITH CTE pipelines), Analytical Window Functions (OVER, PARTITION BY, ORDER BY), Ranking (ROW_NUMBER, RANK, DENSE_RANK), and Cumulative Running Totals."),
        ("Unit 7: Schema Design, DDL & Data Integrity (12/7 – 12/13):", " Relational Normalization (1NF–3NF), Data Definition Language (CREATE TABLE, ALTER TABLE), Constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL), Referential Integrity Actions (CASCADE, RESTRICT), and Virtual Views (CREATE VIEW)."),
        ("Unit 8: Query Performance, Indexing & Capstone Defense (12/14 – 12/18):", " Query Execution Plans (EXPLAIN ANALYZE), B-Tree Index Architecture, Index Selectivity, Write Penalties, Composite Indexes, and Comprehensive Capstone Project Submission & Defense.")
    ]
    template_outline_p = p_elements[33]
    new_outline_ps = []
    for u_title, u_desc in outline_units:
        p_clone = make_clone_p(template_outline_p, [
            {'text': u_title, 'bold': True, 'size': 22},
            {'text': u_desc, 'bold': False, 'size': 22}
        ])
        new_outline_ps.append(p_clone)

    # 12. Course Notes (P41 to P42)
    course_notes = [
        "Each unit module in Canvas contains structured video micro-lectures, interactive concept drills, PostgreSQL technical documentation, and applied lab guides.",
        "All queries and labs are designed to execute directly against PostgreSQL 16. Students may use GitHub Codespaces for instant zero-configuration development, or install PostgreSQL locally.",
        "Socratic AI practice drills ('Learn with AI') are provided in each unit as supplemental, low-stakes practice to reinforce syntax and debugging strategies.",
        "Course Orientation Video: Available in the Canvas Course Orientation module and at https://youtu.be/_u3g4LZ142Q."
    ]
    template_notes_p = p_elements[41]
    new_notes_ps = []
    for note in course_notes:
        p_clone = make_clone_p(template_notes_p, [
            {'text': note, 'bold': False, 'size': 22}
        ])
        new_notes_ps.append(p_clone)

    # 13. Course Competencies (P48 to P52)
    competencies = [
        "Retrieve, filter, and sort relational data using ANSI standard SQL SELECT, WHERE, and ORDER BY clauses while properly handling NULL values and three-valued boolean logic.",
        "Construct multi-table queries utilizing inner, outer, self, and anti-joins to resolve complex relational entity relationships.",
        "Aggregate and summarize datasets using GROUP BY, HAVING, and conditional expressions (CASE WHEN) to generate business-ready analytical metrics.",
        "Safely execute data manipulation language (DML) operations (INSERT, UPDATE, DELETE) within atomic transaction blocks (BEGIN, COMMIT, ROLLBACK) using staging architectures.",
        "Modularize complex analytical queries using subqueries, Common Table Expressions (CTEs), and analytical window functions (PARTITION BY, ROW_NUMBER, RANK).",
        "Design normalized relational database schemas (1NF–3NF), enforce data integrity constraints (PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE, NOT NULL), and encapsulate logic in views using DDL.",
        "Profile query execution plans using EXPLAIN ANALYZE, engineer performant B-Tree indexes, and defend architectural database decisions in a comprehensive capstone project."
    ]
    template_comp_p = p_elements[48]
    new_comp_ps = []
    for comp in competencies:
        p_clone = make_clone_p(template_comp_p, [
            {'text': comp, 'bold': False, 'size': 22}
        ])
        new_comp_ps.append(p_clone)

    # 14. Drop for Non-Attendance (P56)
    set_p_runs(p_elements[56], [
        {'text': 'Drop for Non-Attendance: ', 'bold': True, 'size': 22},
        {'text': 'To avoid being dropped from this class for non-attendance, students must participate in the class by submitting an assignment in Canvas by October 23. Students dropped for non-attendance will not be billed for the course.', 'bold': False, 'size': 22}
    ])

    # 15. Grading Intro (P65)
    set_p_runs(p_elements[65], [
        {'text': 'Your final grade in this course will reflect your engagement with the material, your mastery of relational database concepts, and your ability to write correct, performant SQL queries against PostgreSQL 16. We believe in a balanced approach that assesses both hands-on technical execution and theoretical understanding.', 'bold': False, 'size': 22}
    ])

    # 16. Grading Components (P68 to P70)
    grading_components = [
        ("Hands-on SQL Labs (40% of final grade):", " Weekly verified SQL scripts submitted and executed against PostgreSQL 16."),
        ("Comprehensive Course Capstone (30% of final grade):", " Production 3NF schema design, DDL constraints, ETL staging, and index tuning defense."),
        ("Unit Knowledge Checks & Quizzes (20% of final grade):", " 15-question concept assessments testing syntax, relational logic, and traps."),
        ("Asynchronous Preparation & AI Participation (10% of final grade):", " Pre-lab self-check drills and weekly discussion tasks.")
    ]
    template_grad_p = p_elements[68]
    new_grad_ps = []
    for g_title, g_desc in grading_components:
        p_clone = make_clone_p(template_grad_p, [
            {'text': g_title, 'bold': True, 'size': 22},
            {'text': g_desc, 'bold': False, 'size': 22}
        ])
        new_grad_ps.append(p_clone)

    # 17. Important notes under grading (P86, P87)
    set_p_runs(p_elements[86], [
        {'text': 'Specific due dates for weekly labs, quizzes, and the capstone project are posted in Canvas.', 'bold': False, 'size': 22}
    ])
    set_p_runs(p_elements[87], [
        {'text': 'We encourage you to review the weekly modules and lab guides on Canvas for detailed expectations regarding assignments and weekly preparation.', 'bold': False, 'size': 22}
    ])

    # 18. Due date note in P85
    for r in p_elements[85].iter(w('r')):
        for t in r.iter(w('t')):
            if t.text and 'Due dates are on Friday' in t.text:
                t.text = t.text.split('Due dates are on Friday')[0] + 'Weekly assignments, discussions, and quizzes are due on Friday at 11:59 PM MT.'

    # 19. Academic integrity duplicate cleanup (P106)
    set_p_runs(p_elements[106], [
        {'text': 'Additional information about academic integrity at LCCC is provided in the Syllabus Addendum. LCCC’s Administrative Procedure 3.16P pertains to academic integrity and is applicable to all classes at the College.', 'bold': False, 'size': 22}
    ])

    # Build new children list
    new_body_children = []
    for idx, child in enumerate(body):
        if child.tag != w('p'):
            new_body_children.append(child)
            continue
        
        p_idx = p_elements.index(child)

        # Drop P62 (red prompt cancellation announcement)
        if p_idx == 62:
            continue

        # Drop P107..P112 (duplicate academic integrity repeat block)
        if 107 <= p_idx <= 112:
            continue

        # Drop P123 and P124 (CET comment / del tag and empty spacer)
        if p_idx in (123, 124):
            continue

        # Outline replacement (P33..38)
        if p_idx == 33:
            new_body_children.extend(new_outline_ps)
            continue
        if 34 <= p_idx <= 38:
            continue

        # Notes replacement (P41..42)
        if p_idx == 41:
            new_body_children.extend(new_notes_ps)
            continue
        if p_idx == 42:
            continue

        # Competencies replacement (P48..52)
        if p_idx == 48:
            new_body_children.extend(new_comp_ps)
            continue
        if 49 <= p_idx <= 52:
            continue

        # Grading components replacement (P68..70)
        if p_idx == 68:
            new_body_children.extend(new_grad_ps)
            continue
        if 69 <= p_idx <= 70:
            continue

        new_body_children.append(child)

    body[:] = new_body_children

    # Ensure no <w:del> tags remain
    for d in list(root.iter(w('del'))):
        parent = root.find(f".//{w('del')}/..")
        if parent is not None:
            parent.remove(d)

    xml_out = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    all_files['word/document.xml'] = xml_out

    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for name, data in all_files.items():
            z_out.writestr(name, data)

    print(f"[Success] Updated {docx_path}")

if __name__ == '__main__':
    target = os.path.abspath('course_specs/CMAP_1815_Master_Syllabus.docx')
    update_syllabus(target)
