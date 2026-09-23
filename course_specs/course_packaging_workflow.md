# Canvas Course Packaging Workflow Guide: Native Course Export Packages (.imscc)

This document provides a comprehensive technical guide to the architecture, automated build pipeline, and deployment workflow for packaging Canvas LMS courses into native `.imscc` (IMS Common Cartridge) export files.

---

## 1. Executive Summary & Core Mechanics

### The Cartridge Architecture Problem: Iframes vs. Native Pages
When packaging content for Canvas LMS, courses can be exported/imported under two distinct formats:

1. **Common Cartridge 1.x / 1.3 Web Content (`webcontent`)**:
   - When imported as a generic "Common Cartridge 1.x Package", Canvas treats all HTML files as external static resources.
   - It serves them inside sandboxed `<iframe>` wrappers.
   - **Critical Failure Point**: CSS frameworks, DesignPLUS (Cidilabs) styles, institutional themes, JavaScript accordions, and responsive layout classes loaded in the Canvas parent frame **cannot** penetrate the iframe. Content appears unstyled, squished, or broken.

2. **Canvas Course Export Package (`canvas_export.txt` + `wiki_content`)**:
   - When structured with Canvas-specific export metadata (`course_settings/canvas_export.txt`, `course_settings/module_meta.xml`, `wiki_content/`, `course_settings/course_settings.xml`), Canvas's native migrator imports the HTML directly into the database as native **Canvas WikiPages** and native **Canvas Assignments**.
   - These pages are loaded into the standard Canvas layout without iframes.
   - **Result**: 100% full fidelity with Canvas CSS, DesignPLUS accordion expanders, alert callouts, responsive YouTube video embeds, and Rich Content Editor (RCE) tools.

---

## 2. Directory Layout of a Native Canvas Course Export Package

An `.imscc` file is a ZIP archive containing a structured file hierarchy. To be recognized as a native Canvas Course Export, it follows this directory schema:

```
CMAP_1815_Complete.imscc (ZIP archive)
│
├── imsmanifest.xml                       # Top-level manifest defining resources and items
│
├── course_settings/
│   ├── canvas_export.txt                 # Flag file signaling Canvas native export format
│   ├── context.xml                       # Canvas course configuration and metadata (LCCC domain)
│   ├── course_settings.xml               # Course settings (default_view: wiki for Front Page landing)
│   ├── files_meta.xml                    # File resource metadata and permissions
│   ├── assignment_groups.xml             # 4 weighted grade categories (Labs 40%, Quizzes 20%, Prep 10%, Capstone 30%)
│   ├── module_meta.xml                   # Modules, item ordering, indentation, and publishing state
│   └── syllabus.html                     # Native Canvas syllabus page with grade scale & download link
│
├── wiki_content/                         # Native Canvas Pages (HTML)
│   ├── home-page.html                    # Course Front Page (front_page: true) with DesignPLUS Module Accordion
│   ├── start-here.html                   # Start Here: Course Overview & Orientation (QM standards)
│   ├── unit-01-overview.html
│   ├── unit-01-readings-and-media.html   # Readings + Embedded Responsive YouTube player
│   ├── unit-01-async-study.html          # Focus questions & expandable drill solutions
│   ├── unit-01-applied-lab-guide.html    # Lab scenario & step-by-step query specifications
│   ├── unit-01-learn-with-ai.html        # Formative AI practice drill with prompt templates
│   ├── unit-01-instructor-guide.html     # Unpublished Teacher Guide (video blueprints & synchronous schedules)
│   └── ... (Units 02 to 08)
│
├── web_resources/
│   └── syllabi/
│       └── CMAP 1815 Syllabus Fall 2026 - Swarm.docx  # Downloadable Master Word Document Syllabus
│
├── g_assign_u1.../                       # Native Canvas Assignment (Unit 1 Lab Turn-in)
│   ├── unit-01-lab-assignment.html       # Assignment instructions and rubric requirements
│   └── assignment_settings.xml           # Submission types (online_upload, online_text_entry), 50 pts
│
├── g_quiz_u1.../                         # Canvas QTI Assessment (Unit 1 Quiz folder)
│   ├── assessment_qti.xml                # QTI 1.2 XML quiz specification (15 questions, rubrics, keys)
│   └── assessment_meta.xml               # Canvas quiz settings (time limit, attempts, 30 pts)
│
└── ... (Assignment & Quiz folders for Units 02 to 08)
```

---

## 3. Standard 8-Item Unit Module Architecture

Each unit follows a consistent, pedagogical 8-item sequence inside `course_settings/module_meta.xml`:

| # | Item Title | Type | Indent | Visibility | Pedagogical Role |
|---|---|---|---|---|---|
| **1** | `Unit 0X Overview: [Topic]` | `WikiPage` | 0 | Published | Unit roadmap, learning outcomes, asynchronous schedule |
| **2** | `Unit 0X: Required Readings & Video Lectures` | `WikiPage` | 1 | Published | Textbook chapters, documentation, and **embedded responsive video lectures** with exact topic timestamps |
| **3** | `Unit 0X: Asynchronous Preparation & Drills` | `WikiPage` | 1 | Published | Pre-lab self-check drills with expandable accordion answers |
| **4** | `Unit 0X: Applied SQL Lab Guide` | `WikiPage` | 1 | Published | Step-by-step laboratory scenarios, dataset context, and challenge queries to write in PostgreSQL 16 |
| **5** | `Unit 0X Applied SQL Lab Assignment` | `Assignment` | 1 | Published | **Native Canvas Assignment**: Upload `.sql` script or paste code for grading in SpeedGrader (50 pts, 40% weight) |
| **6** | `Unit 0X: Learn with AI — Supplemental Practice Drill` | `WikiPage` | 1 | Published | Optional, graded formative drill using free AI tools (persona prompts, edge cases) |
| **7** | `Unit 0X Knowledge Check: [Topic]` | `Quizzes::Quiz` | 1 | Published | 15-question Canvas QTI assessment testing syntax, concepts, and traps (30 pts, 20% weight) |
| **8** | `[Instructor Guide] Unit 0X Teaching Notes & Solutions` | `WikiPage` | 1 | **Unpublished** | Video production blueprints, synchronous classroom schedules, trap demos, and master SQL solutions |

---

## 4. Front Page & DesignPLUS Module Accordion Setup

The Course Front Page (`wiki_content/home-page.html`) is configured as the default landing view:
1. In `course_settings/course_settings.xml`, `<default_view>wiki</default_view>` instructs Canvas to land on the Wiki Front Page.
2. In `wiki_content/home-page.html`, `<meta name="front_page" content="true"/>` designates the page as the Front Page.
3. The page includes the DesignPLUS Quick Links Accordion:
   ```html
   <div class="dp-module-list dp-module-list-flag-completed dp-module-list-show-locked dp-quick-links-panels-accordion-plus dp-auto-update dp-panel-color-dp-primary dp-panel-active-color-dp-accent dp-panel-hover-color-dp-accent dp-quick-links-all dp-module-list-current-none">
     <nav class="dp-module-list-item-group">
       <ul class="fa-ul list-group">
         <li><a class="list-group-item list-group-item-action" href="$CANVAS_OBJECT_REFERENCE$/modules/{module_id}"><i class="fas fa-map-marker-alt"></i> Module Name</a></li>
       </ul>
     </nav>
   </div>
   ```

---

## 5. Automated Build Pipeline

The entire course cartridge is built programmatically via `scripts/build_canvas_cartridge.py`:

```bash
python scripts/build_canvas_cartridge.py
```

### Execution Pipeline Stages:
1. **Directory Staging**: Cleans and establishes temporary staging trees (`wiki_content`, `course_settings`, `web_resources`, assessment & assignment folders).
2. **Syllabus & Assets**: Generates the valid Word (.docx) syllabus file and native Canvas syllabus page.
3. **Front Page & Start Here**: Injects DesignPLUS banners, quick navigation grids, and dynamic module accordion links.
4. **Unit Pages & Lab Assignments**: Creates unit overview pages, reading pages with responsive video embeds, async drills, applied lab guides, and native Canvas Assignment turn-in objects (`assignment_settings.xml`).
5. **QTI Quizzes**: Generates 15-question QTI XML files for all 8 units.
6. **Teacher Guides**: Generates unpublished instructor guides with custom video production blueprints, synchronous classroom delivery schedules, and master SQL solutions.
7. **Manifest & Module Meta Assembly**: Writes `imsmanifest.xml` and `course_settings/module_meta.xml` with shared item identifiers and unpublished states.
8. **XML Syntax Validation**: Validates all 38 generated XML files using `xml.etree.ElementTree`.
9. **Cartridge Packaging**: Packs the staging directory into `CMAP_1815_Complete.imscc`.

---

## 6. Canvas Deployment: Step-by-Step Instructions

1. **Reset Course Shell**: In Canvas, click **Settings** $\rightarrow$ **Reset Course Content** (red button).
2. **Import Package**: Click **Import Course Content** $\rightarrow$ Content Type: **Canvas Course Export Package** $\rightarrow$ Choose `CMAP_1815_Complete.imscc` $\rightarrow$ Select **All content** $\rightarrow$ Click **Import**.
3. **Verify**:
   - Confirm Canvas opens directly to the **Home Page** with banner, quick links, and module list accordion.
   - Check **Modules** to verify all 8 units show their 8 items (with the Lab Assignment and Quiz both present).
   - Check that `[Instructor Guide]` items show the grey unpublished circle.
