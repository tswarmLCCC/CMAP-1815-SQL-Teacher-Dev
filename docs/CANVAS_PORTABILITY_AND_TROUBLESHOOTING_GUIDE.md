# 📘 Canvas Course Builder Portability & Migration Guide
**Comprehensive Procedure for Replicating Native Common Cartridge (`.imscc`) Packaging Across Any Course**

---

## 1. Executive Summary & Problem Diagnosis

When developing course content in external repositories and compiling into Canvas Common Cartridge packages (`.imscc`), instructors frequently encounter several frustrating defects in Canvas LMS:

| Defect Observed in Canvas | Root Cause in Cartridge | The Solution Implemented in this Toolkit |
| :--- | :--- | :--- |
| **"HTML File Links Bug"**: Pages appear in Modules with a file/document icon; clicking them forces a file download or raw iframe preview. | Cartridge declares the file as a generic `<resource type="webcontent">` in `imsmanifest.xml` without the proprietary Canvas `<content_type>WikiPage</content_type>` tag in `course_settings/module_meta.xml`. | The compiler builds a synchronized pair: `course_settings/module_meta.xml` specifying `<content_type>WikiPage</content_type>` and `imsmanifest.xml` pointing to `wiki_content/` using deterministic 32-character MD5 IDs. |
| **Stripped Styles & Broken Layouts**: Custom fonts, CSS grid layouts, or linked `.css` files are ignored or stripped upon Canvas import. | Canvas LMS sanitizes imported HTML, actively stripping external `<link rel="stylesheet">` tags and unknown custom CSS rules for security. | The compiler embeds inline CSS directly onto HTML tags while applying standard DesignPLUS structural classes (`dp-header dp-basic-bar`, etc.). This guarantees stunning visual presentation with or without DesignPLUS installed on the campus instance. |
| **Un-graded Quizzes**: Quizzes import as static surveys or fail to import entirely. | Incomplete QTI schema missing Canvas-specific `assessment_meta.xml` or lacking the required duplicate QTI file in `non_cc_assessments/`. | Zero-dependency QTI compiler builds dual QTI 1.2 XML files plus `assessment_meta.xml` (configuring allowed attempts, grading policy, and point values). |
| **Broken SpeedGrader File Uploads**: Assignments lack point values, gradebook weights, or file type restrictions. | Missing `[assign_id]/assignment_settings.xml`. | Dedicated assignment descriptors configure submission types (`online_upload,online_text_entry`), allowed extensions (`.sql`, `.py`, `.pdf`), and link to weighted assignment groups. |
| **Overwritten Builds without History**: Running a build script accidentally destroys previous releases. | Hardcoded single-file output overwrites without archival. | Automated backup routine copies existing `.imscc` with timestamp into `archive/cartridge_backups/` before compiling. |

---

## 2. The Anatomy of the Canvas "HTML File Link" Bug

Canvas LMS distinguishes between a **Course File** (stored in the Files tool) and a **Wiki Page** (stored in the Pages tool).

### The Failing Approach (Generic Common Cartridge)
In generic Common Cartridge, a module item links directly to a file:
```xml
<!-- Generic Cartridge imsmanifest.xml (DOES NOT WORK PROPERLY IN CANVAS) -->
<resource identifier="page_1" type="webcontent" href="page1.html">
  <file href="page1.html"/>
</resource>
```
When imported into Canvas, Canvas sees `type="webcontent"` without Canvas-specific metadata. Canvas concludes: *"This is a static HTML file."* It uploads `page1.html` to the student-accessible **Files** repository, and creates a **File Attachment Item** in the module. Students cannot edit, Canvas navigation headers are missing, and page styles are broken.

### The Working Canvas Native Contract
Canvas requires **two synchronized files** with matching deterministic identifiers:

#### A. `course_settings/module_meta.xml`
Declares the item inside the Canvas module and specifies `<content_type>WikiPage</content_type>`:
```xml
<module identifier="g_mod_unit_1">
  <title>Unit 1: Fundamentals</title>
  <workflow_state>active</workflow_state>
  <position>1</position>
  <items>
    <item identifier="g_item_mod1_page1">
      <content_type>WikiPage</content_type>
      <workflow_state>active</workflow_state>
      <title>Unit 1 Overview</title>
      <identifierref>g_page_u1_overview</identifierref>
      <position>1</position>
      <indent>0</indent>
    </item>
  </items>
</module>
```

#### B. `imsmanifest.xml`
Declares the page resource located in `wiki_content/`:
```xml
<resource identifier="g_page_u1_overview" type="webcontent" href="wiki_content/unit-01-overview.html">
  <file href="wiki_content/unit-01-overview.html"/>
</resource>
```
When Canvas imports this package:
1. It reads `module_meta.xml` and identifies `g_page_u1_overview` as a `WikiPage`.
2. It looks up `g_page_u1_overview` in `imsmanifest.xml`.
3. It creates a native **Canvas Page** under the Pages tool, named using the `<title>` tag from the HTML `<head>`.
4. It places a native Page link into the Module. When clicked, it renders natively inside the Canvas interface!

---

## 3. Formatting & DesignPLUS Styling Architecture

Canvas strips external stylesheets. To ensure your course looks top-tier without relying on Canvas theme overrides, our styler (`html_styler.py`) applies inline CSS tokens:

### Visual Design Principles
1. **The Selective Ribbon Policy:**
   - **Apply Banner Ribbons (`dp-header dp-basic-bar`) ONLY on:**
     - Course Front Page (`home-page.html`)
     - Syllabus Page (`course_settings/syllabus.html`)
     - Unit Overview Pages (`unit-XX-overview.html`)
   - **Use Clean Standard Layout (`render_standard_page_html`) on all Inner Subpages:**
     - Standard system font stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`)
     - Navy blue section dividers (`<h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.3rem;">`)
     - Shaded lead cards (`<div style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 0.75rem 1.25rem; ...">`)
     - Avoid repetitive heavy banner headers on subpages.

2. **Markdown-to-HTML Automated Transformations:**
   - **Tables & Rubrics:** Automatically converted from Markdown `| Col 1 | Col 2 |` into styled HTML tables with navy headers (`#1e3a8a`), cell padding (`0.75rem`), and alternating zebra shading (`#f8fafc`).
   - **Code Blocks:** Converted from triple-backticks into dark-themed syntax boxes (`background: #0f172a; color: #f8fafc; border-radius: 6px; font-family: Consolas, monospace;`).
   - **Drills & Accordions:** Converted from `<details><summary>` into interactive collapsible cards with subtle borders.

---

## 4. What Files to Move to Another Course Repository

To drop this workflow into another course (e.g. Python, Java, Web Development, Networking), copy the `portable_canvas_toolkit` into your new course root:

```text
your_course_repo/
├── portable_canvas_toolkit/           <-- COPY THIS WHOLE FOLDER
│   ├── build_course.py                <-- Master CLI Compiler
│   ├── course_config.example.json     <-- Configuration Template
│   ├── README.md                      <-- Quickstart instructions
│   ├── scripts/
│   │   ├── build_cartridge.py         <-- Common Cartridge Engine
│   │   ├── html_styler.py             <-- DesignPLUS & Markdown Styler
│   │   ├── qti_builder.py             <-- QTI 1.2 Quiz Engine
│   │   └── docx_syllabus.py           <-- OpenXML Word Syllabus Builder
│   ├── templates/
│   │   ├── unit_quiz_template.md      <-- Quiz Authoring Template
│   │   └── course_config.example.json
│   └── references/
│       ├── canvas_cc_architecture.md
│       └── designplus_guide.md
├── course_config.json                 <-- Your course settings (copied from example)
└── units/                             <-- Your weekly course content
    ├── unit_01_orientation/
    │   ├── overview.md
    │   ├── readings.md
    │   ├── lab_guide.md
    │   ├── lab_rubric.md
    │   ├── quiz.md
    │   └── instructor_solution.sql (or .py)
    └── unit_02_fundamentals/
        └── ...
```

---

## 5. Step-by-Step Procedure for a New Course

### Step 1: Create `course_config.json`
Configure your course code, title, institutional details, and weighted gradebook groups:
```json
{
  "course_code": "CS 1010",
  "course_title": "Introduction to Computer Science",
  "term": "Fall 2026",
  "institution": "Laramie County Community College",
  "domain": "lccc-wy.instructure.com",
  "credits": "3.0 Credit Hours",
  "assignment_groups": [
    { "key": "labs", "name": "Applied Programming Labs", "weight": 40.0 },
    { "key": "quizzes", "name": "Unit Knowledge Checks", "weight": 20.0 },
    { "key": "prep", "name": "Preparation Drills", "weight": 10.0 },
    { "key": "capstone", "name": "Final Capstone Project", "weight": 30.0 }
  ]
}
```

### Step 2: Author Unit Content in Standard Markdown
For each week in `units/unit_XX/`:
- `overview.md`: Summary, learning objectives, contact hours budget.
- `readings.md`: Concept breakdown, tutorial links, embedded video lectures.
- `study_guide.md`: Focus questions and `<details><summary>` self-check drills.
- `lab_guide.md`: Business/technical scenario and step-by-step challenges.
- `lab_rubric.md`: Standard markdown table with 50-point SpeedGrader criteria.
- `quiz.md`: Multiple choice questions formatted as:
  ```markdown
  ### Question 1
  What keyword retrieves columns in SQL?
  * A) GET
  * B) SELECT
  * C) RETRIEVE
  * D) FIND

  ## Answer Key
  | Question | Correct Answer | Rationale |
  | :--- | :--- | :--- |
  | 1 | B | SELECT is the standard ANSI SQL projection keyword. |
  ```
- `instructor_solution.*`: Solution code and instructor notes (automatically published as `unpublished` instructor-only pages in Canvas!).

### Step 3: Run the Compiler
```bash
python portable_canvas_toolkit/build_course.py --config course_config.json --units-dir units --output CS_1010_Complete.imscc
```

### Step 4: Import into Canvas LMS
1. In your Canvas course, click **Settings** $\rightarrow$ **Import Course Content**.
2. Select **Common Cartridge 1.x Package**.
3. Browse and select `CS_1010_Complete.imscc`.
4. Select **All content**.
5. Click **Import**.

Within ~30 seconds, your course modules will display published native pages, SpeedGrader assignments, and QTI quizzes with zero missing-file errors!
