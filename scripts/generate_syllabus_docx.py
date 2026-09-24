import os
import zipfile

def create_docx(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
        '  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
        '  <Default Extension="xml" ContentType="application/xml"/>\n'
        '  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>\n'
        '</Types>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>\n'
        '</Relationships>'
    )
    doc_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
        '  <w:body>\n'
        '    <w:p><w:r><w:rPr><w:b/><w:sz w:val="36"/></w:rPr><w:t>CMAP 1815: Introduction to Modern SQL</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:rPr><w:b/><w:sz w:val="28"/></w:rPr><w:t>Master Course Syllabus (Fall 2026)</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>Institution: Laramie County Community College (LCCC)</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>Course Credits: 3.0 Credit Hours (Asynchronous Online)</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:rPr><w:b/></w:rPr><w:t>Course Description:</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>This course provides comprehensive instruction in relational database querying, schema design, transactional integrity, and performance optimization using modern PostgreSQL 16. Students master projection, filtering, multi-table joins, aggregations, safe DML transactions, subqueries, CTEs, window functions, schema normalization (1NF-3NF), DDL constraints, views, and B-Tree indexing.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:rPr><w:b/></w:rPr><w:t>Course Learning Outcomes (CLOs):</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>1. Design, write, and debug SQL queries to retrieve, filter, and sort data from relational tables.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>2. Group and aggregate data, write modular subqueries, CTEs, and window functions to manipulate result sets.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>3. Translate real-world business requirements into correct, performant SQL statements.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>4. Safely execute data manipulation operations (INSERT, UPDATE, DELETE), manage transactions, and stage transformations using temporary tables.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>5. Design normalized relational schemas (1NF-3NF), write DDL scripts, declare integrity constraints, and create views.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>6. Profile query performance with EXPLAIN ANALYZE, engineer B-Tree indexes, and defend architectural choices in a comprehensive capstone.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:rPr><w:b/></w:rPr><w:t>Grading Policy &amp; Weighting:</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>- Hands-on SQL Labs (40%): Weekly verified SQL script submissions executed in PostgreSQL 16.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>- Unit Quizzes (20%): 15-question formative/evaluative knowledge checks.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>- Asynchronous Preparation &amp; AI Participation (10%): Weekly self-check drills and discussion posts.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>- Comprehensive Course Capstone (30%): End-of-course 3NF schema, DDL constraints, ETL staging, and index optimization project.</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:rPr><w:b/></w:rPr><w:t>Grade Scale:</w:t></w:r></w:p>\n'
        '    <w:p><w:r><w:t>A: 90 - 100% | B: 80 - 89% | C: 70 - 79% | D: 60 - 69% | F: 0 - 59%</w:t></w:r></w:p>\n'
        '  </w:body>\n'
        '</w:document>'
    )
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', doc_xml)

if __name__ == '__main__':
    create_docx('c:/dev/CMAP_1815_Autogen/course_specs/CMAP_1815_Master_Syllabus.docx')
    print('Generated CMAP_1815_Master_Syllabus.docx')
