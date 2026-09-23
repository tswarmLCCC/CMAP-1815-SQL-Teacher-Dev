---
name: canvas-course-builder
description: >-
  End-to-end workflow and architectural standard for generating production-grade,
  DesignPLUS-compliant Canvas Common Cartridge (.imscc) courses with native assignments,
  QTI quizzes, markdown-to-HTML formatting, and institutional syllabus templates.
---

# Canvas Course Cartridge Production Workflow

This skill defines the complete blueprint, structural rules, formatting standards, and automation scripts required to author, format, package, and deploy a complete college course into Canvas LMS via Common Cartridge (`.imscc`).

---

## 1. Core Architecture & Module Taxonomy

Each weekly unit follows a strict, proven **8-Item Sequence** inside Canvas Modules:

| Sequence # | Item Title Convention | Type | Workflow State | Description |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `Unit X Overview: [Topic]` | `WikiPage` | `active` (Published) | High-level roadmap, contact hour budget (150m study / 150m lab), learning objectives. Uses DesignPLUS banner ribbon. |
| **2** | `Unit X: Required Readings & Video Lectures` | `WikiPage` | `active` (Published) | Direct links to tutorials + responsive 16:9 embedded YouTube micro-video chapters with start timestamps. Clean standard layout. |
| **3** | `Unit X: Asynchronous Preparation & Drills` | `WikiPage` | `active` (Published) | Conceptual focus questions + formative self-check drills with interactive `<details>/<summary>` answer keys. |
| **4** | `Unit X: Applied SQL Lab Guide` | `WikiPage` | `active` (Published) | Complete scenario instructions, in-class active learning challenges, and native HTML grading rubric table. |
| **5** | `Unit X Applied SQL Lab Assignment` | `Assignment` | `active` (Published) | Native Canvas Assignment (50 pts) for SpeedGrader file upload (`.sql`) or text entry, linked to Labs group. |
| **6** | `Unit X: Learn with AI — Supplemental Practice Drill` | `WikiPage` | `active` (Published) | Socratic roleplay scenario, free tools guide, copy-paste master prompt, and weekly discussion debrief task. |
| **7** | `Unit X Knowledge Check: [Topic]` | `Quizzes::Quiz` | `active` (Published) | Native QTI 1.2 multiple-choice assessment (15 questions, 30 pts, 3 attempts, highest score kept). |
| **8** | `[Instructor Guide] Unit X Teaching Notes & Solutions` | `WikiPage` | `unpublished` | Hidden from students. Custom video production blueprint, synchronous class delivery agenda, and master solution key. |

---

## 2. Page Formatting & Visual Design Guidelines

### A. Selective Ribbon Policy
* **Apply DesignPLUS Banner Ribbon (`dp-header dp-basic-bar`) ONLY on:**
  - `home-page.html` (Front Page)
  - `start-here.html` (Course Orientation)
  - `unit-XX-overview.html` (Weekly Unit Overviews)
  - `course_settings/syllabus.html` (Native Syllabus Page)
* **Use Clean Standard Layout (`render_standard_page_html`) on all Inner Pages:**
  - Standard typography (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`)
  - Navy blue section headers (`<h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; ...">`)
  - Lead card callouts (`<div style="background: #f8fafc; border-left: 4px solid #1e3a8a; ...">`)
  - Avoid heavy, repetitive banner ribbons on subpages.

### B. Markdown-to-HTML Translation Rules
Never dump raw markdown or large `<pre><code>` blocks on student-facing pages. Parse all markdown:
1. **Rubrics & Tables:** Convert `| Col 1 | Col 2 |` into styled `<table style="width: 100%; border-collapse: collapse; border: 1px solid #cbd5e1;">` with navy blue headers (`#1e3a8a`), cell borders, and alternating zebra rows (`#f8fafc`).
2. **Code Blocks:** Wrap in styled dark syntax boxes: `<div style="background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; font-family: Consolas, Monaco, monospace;"><pre><code>...</code></pre></div>`.
3. **Interactive Drills:** Convert `<details><summary>` into styled accordion cards with borders and hover cursor.
4. **Inline Syntax:** Convert `` `code` `` into `<code style="background: #f1f5f9; color: #0369a1; padding: 0.15rem 0.35rem; border-radius: 3px; font-weight: 600;">`.

---

## 3. Institutional Syllabus Standardization

To guarantee 100% style and branding consistency with college accreditation standards:
1. **Extract Existing .docx Template:** Extract `word/document.xml` from an existing approved course export (e.g. `AIML 1010 Syllabus Fall 2026 - Swarm.docx`).
2. **Transform XML String:** Replace course identifiers, titles, descriptions, and learning outcomes while preserving table structures, fonts, and header styling.
3. **Embed in Cartridge:** Save the resulting `.docx` into `web_resources/syllabi/` and declare it in `imsmanifest.xml` under type `webcontent`.
4. **Link in Native Syllabus Page:** Provide an immediate scribd/download link in `course_settings/syllabus.html`:
   ```html
   <a class="instructure_file_link instructure_scribd_file inline_disabled" 
      title="[File Name].docx" 
      href="$IMS-CC-FILEBASE$/syllabi/[File%20Name].docx?canvas_=1&amp;canvas_qs_wrap=1" 
      target="_blank">Download Master Syllabus (Word .docx)</a>
   ```

---

## 4. Canvas Gradebook & Assessment Configuration

### Weighted Assignment Groups (`course_settings/assignment_groups.xml`)
Enforce institutional 100% weighted distribution:
- **Hands-on Applied Labs:** 40.0%
- **Comprehensive Capstone:** 30.0%
- **Unit Knowledge Checks (Quizzes):** 20.0%
- **Asynchronous Preparation & AI Participation:** 10.0%

### Native Assignment Descriptors (`assignment_settings.xml`)
Every lab assignment directory (`[assign_id]/`) must include:
1. `assignment_settings.xml`: Sets `submission_types` (`online_text_entry,online_upload`), `allowed_extensions` (`sql,txt,pdf`), `points_possible` (50.0), and `assignment_group_identifierref`.
2. `[unit-xx-lab-assignment].html`: Clean assignment description with clear submission steps and the full grading rubric table.

### Native QTI 1.2 Quizzes
Each quiz directory (`[quiz_id]/`) must include:
1. `assessment_qti.xml`: QTI 1.2 compliant assessment items with single/multiple response tags.
2. `assessment_meta.xml`: Canvas quiz settings (`allowed_attempts="3"`, `scoring_policy="keep_highest"`, `points_possible="30.0"`, `quiz_type="assignment"`).
3. `non_cc_assessments/[quiz_id].xml.qti`: Duplicate QTI payload required for Canvas course import engines.

---

## 5. Automated Build & Packaging Pipeline

### Script Architecture (`scripts/build_canvas_cartridge.py`)
The master build script performs:
1. **Directory Provisioning:** Creates `wiki_content`, `course_settings`, `web_resources/syllabi`, `non_cc_assessments`, and individual assignment/quiz folders.
2. **Metadata Compilation:** Assembles readings, video timestamps, AI drill prompts, and instructor blueprints.
3. **HTML Generation:** Parses markdown to native HTML tables/code boxes and renders overview vs standard pages.
4. **XML Manifest Generation:** Synchronizes `imsmanifest.xml` and `module_meta.xml` with shared deterministic 32-character MD5 identifiers (`make_id()`).
5. **Schema Validation:** Iterates over all 38+ generated XML files using `xml.etree.ElementTree.parse()` to guarantee zero syntax errors.
6. **Cartridge Compression:** Archives the directory tree into `CMAP_1815_Complete.imscc` using standard ZIP deflate compression.

### How to Execute:
```bash
python scripts/build_canvas_cartridge.py
```

---

## 6. Canvas LMS Deployment Protocol

1. Navigate to Canvas Course &rarr; **Settings** &rarr; **Import Course Content**.
2. **Content Type:** Select **Common Cartridge 1.x Package**.
3. **Source:** Upload `CMAP_1815_Complete.imscc`.
4. **Content:** Choose **All content**.
5. Click **Import**.
6. Upon completion, verify that:
   - Front Page is set to `Home Page` with the module accordion.
   - Modules display all 8 items per unit in correct sequence.
   - SpeedGrader assignments accept `.sql` file uploads.
   - Rubrics display as clean, native HTML tables.
   - Word syllabus downloads cleanly from the Syllabus tab.
