# 📦 Portable Canvas Course Cartridge Toolkit

A zero-dependency Python toolchain for generating **Canvas Common Cartridge (`.imscc`)** packages with native pages, DesignPLUS-compliant styling, QTI 1.2 quizzes, SpeedGrader assignments, and automated backup management.

---

## 🛑 What Problem Does This Solve?

### The Notorious "Canvas HTML File Link" Bug
When creating courses for Canvas LMS via standard or naive Common Cartridge exports, Canvas frequently imports HTML pages as **static document downloads** in the course **"Files"** repository, placing a generic document attachment link in the Module instead of rendering a native **Canvas Page (`WikiPage`)**. When students click the module link, Canvas forces an HTML file download or opens an ugly framed preview, stripping page styles and breaking navigation.

### The Fix
This toolkit generates a synchronized duo of XML descriptors:
1. `course_settings/module_meta.xml` explicitly declaring `<content_type>WikiPage</content_type>` for every page item.
2. `imsmanifest.xml` referencing exact deterministic 32-character hexadecimal identifiers (`make_canvas_id`), routing resources into `wiki_content/`.
3. Inlined CSS styling adhering to **DesignPLUS** color ribbons and container cards, ensuring that your pages look gorgeous whether or not your Canvas instance has DesignPLUS enabled!

---

## 🚀 3-Step Quickstart: Dropping This Into Any Course

### Step 1: Copy the Toolkit into Your New Course Repository
Copy this `portable_canvas_toolkit` folder (or just `scripts/`, `templates/`, and `build_course.py`) into your course repo:
```text
my_new_course_repo/
├── course_config.json        # Your course metadata
├── build_course.py           # Master CLI builder
├── scripts/                  # Zero-dependency Python tools
│   ├── build_cartridge.py
│   ├── html_styler.py
│   ├── qti_builder.py
│   └── docx_syllabus.py
├── templates/                # Reusable authoring templates
│   ├── unit_quiz_template.md
│   └── course_config.example.json
└── units/                    # Your course content
    ├── unit_01_getting_started/
    │   ├── overview.md
    │   ├── readings.md
    │   ├── lab_guide.md
    │   ├── lab_rubric.md
    │   ├── quiz.md
    │   └── instructor_solution.py
    └── unit_02_advanced_topics/
        └── ...
```

### Step 2: Configure `course_config.json`
Edit `course_config.json` with your course code, title, institution, and grading weights:
```json
{
  "course_code": "COSC 1010",
  "course_title": "Introduction to Computer Science",
  "term": "Fall 2026",
  "institution": "Laramie County Community College",
  "domain": "lccc-wy.instructure.com",
  "credits": "3.0 Credit Hours",
  "assignment_groups": [
    { "key": "labs", "name": "Applied Programming Labs", "weight": 40.0 },
    { "key": "quizzes", "name": "Unit Knowledge Checks", "weight": 20.0 },
    { "key": "prep", "name": "Preparation Drills", "weight": 10.0 },
    { "key": "capstone", "name": "Comprehensive Capstone", "weight": 30.0 }
  ]
}
```

### Step 3: Run the Build Command
```bash
python build_course.py --config course_config.json --units-dir units --output COSC_1010_Complete.imscc
```

That's it! The script will:
- Parse all Markdown files in `units/`
- Convert tables into styled zebra HTML tables and code into syntax boxes
- Compile Markdown quizzes into native QTI 1.2 XML
- Configure native SpeedGrader assignments with file upload validation
- Validate all XML schemas with Python's ElementTree
- Automatically preserve any previous cartridge with a timestamp in `archive/cartridge_backups/`
- Output a single, production-grade `.imscc` file.

---

## 📥 Importing into Canvas LMS

1. Open your Canvas Course shell.
2. Go to **Settings** (bottom of left navigation).
3. Click **Import Course Content** (right sidebar).
4. Under **Content Type**, select **Common Cartridge 1.x Package**.
5. Choose your generated `.imscc` file.
6. Select **All content**.
7. Click **Import**.
8. Once completed, your Canvas Modules, Pages, SpeedGrader Assignments, Gradebook Groups, and Quizzes are live and 100% formatted!
