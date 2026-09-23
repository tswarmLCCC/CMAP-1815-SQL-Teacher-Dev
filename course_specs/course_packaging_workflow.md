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
   - When structured with Canvas-specific export metadata (`course_settings/canvas_export.txt`, `course_settings/module_meta.xml`, `wiki_content/`), Canvas's native migrator imports the HTML directly into the database as native **Canvas WikiPages**.
   - These pages are loaded into the standard Canvas layout without iframes.
   - **Result**: 100% full fidelity with Canvas CSS, DesignPLUS accordion expanders, alert callouts, responsive YouTube video embeds, and Rich Content Editor (RCE) tools.

---

## 2. Directory Layout of a Native Canvas Course Export Package

An `.imscc` file is a ZIP archive containing a structured file hierarchy. To be recognized as a native Canvas Course Export, it must follow this directory schema:

```
CMAP_1815_Complete.imscc (ZIP archive)
│
├── imsmanifest.xml                       # Top-level manifest defining resources and items
│
├── course_settings/
│   ├── canvas_export.txt                 # Flag file signaling Canvas native export format
│   ├── context.xml                       # Canvas course configuration and metadata
│   ├── files_meta.xml                    # File resource metadata and permissions
│   └── module_meta.xml                   # Modules, module item ordering, indentation, and publishing state
│
├── wiki_content/                         # Native Canvas Pages (HTML)
│   ├── unit-01-overview.html
│   ├── unit-01-readings.html
│   ├── unit-01-async-drills.html
│   ├── unit-01-sync-lab.html
│   ├── unit-01-learn-with-ai.html
│   └── unit-01-instructor-guide.html
│   └── ... (Units 02 to 08)
│
├── g4b7e801.../                          # QTI Assessment 1 (Unit 1 Quiz folder)
│   ├── g4b7e801....xml                   # QTI 1.2 XML quiz specification (questions, rubrics, keys)
│   └── assessment_meta.xml               # Canvas quiz settings (time limit, attempts, points)
│
└── ... (QTI folders for Units 02 to 08)
```

---

## 3. Standard 7-Item Unit Module Architecture

Each unit follows a consistent, pedagogical 7-item sequence inside `course_settings/module_meta.xml`:

| # | Item Title | Type | Indent | Visibility | Pedagogical Role |
|---|---|---|---|---|---|
| **1** | `Unit 0X Overview: [Topic]` | `WikiPage` | 0 | Published | Unit roadmap, learning outcomes, module agenda |
| **2** | `Unit 0X: Required Readings & Video Lectures` | `WikiPage` | 1 | Published | Textbook chapters, documentation, and **embedded responsive video lectures** with exact topic timestamps |
| **3** | `Unit 0X: Asynchronous Preparation & Drills` | `WikiPage` | 1 | Published | Pre-class self-check drills with expandable accordion answers |
| **4** | `Unit 0X: Synchronous Classroom Activities & Lab` | `WikiPage` | 1 | Published | In-class paired coding challenges, live setup instructions, grading rubric |
| **5** | `Unit 0X: Learn with AI — Supplemental Practice Drill` | `WikiPage` | 1 | Published | Optional, graded formative drill using free AI tools (persona prompts, edge cases) |
| **6** | `Unit 0X Knowledge Check: [Topic]` | `Quizzes::Quiz` | 1 | Published | 15-question Canvas QTI assessment testing syntax, concepts, and traps |
| **7** | `[Instructor Guide] Unit 0X Teaching Notes & Solutions` | `WikiPage` | 1 | **Unpublished** | Screen setups, live demo cues, common student traps, and master SQL solution keys |

---

## 4. Key Technical Requirements & Pitfalls

### A. Identifier Parity Between Manifest and Module Meta
Canvas matches module items to their corresponding resource files using the `<item identifier="...">` attribute.

- In `imsmanifest.xml`:
  ```xml
  <organization identifier="org_1" structure="rooted-hierarchy">
    <item identifier="item_u1_p1" identifierref="res_u1_p1">
      <title>Unit 01 Overview: Database Foundations &amp; The SELECT Query</title>
    </item>
  </organization>
  ```
- In `course_settings/module_meta.xml`:
  ```xml
  <module identifier="mod_u1">
    <items>
      <item identifier="item_u1_p1">
        <content_type>WikiPage</content_type>
        <identifierref>res_u1_p1</identifierref>
        <title>Unit 01 Overview: Database Foundations &amp; The SELECT Query</title>
        <indent>0</indent>
        <workflow_state>published</workflow_state>
      </item>
    </items>
  </module>
  ```
> [!IMPORTANT]
> If `identifier` in `module_meta.xml` does not match `identifier` in `imsmanifest.xml`, Canvas fails to associate the module item with the resource, resulting in empty modules or broken links.

### B. Unpublished Instructor Guides
To ensure instructor guides are hidden from students upon initial cartridge import:
1. In `course_settings/module_meta.xml`, set:
   ```xml
   <item identifier="item_u1_p6">
     <content_type>WikiPage</content_type>
     <workflow_state>unpublished</workflow_state>
   </item>
   ```
2. In the corresponding HTML header (`wiki_content/unit-01-instructor-guide.html`), include:
   ```html
   <meta name="workflow_state" content="unpublished" />
   ```

### C. Responsive Video Embeds (No Third-Party Cookies or Iframe Issues)
Video embeds should use the standard 16:9 responsive wrapper with YouTube embed syntax:
```html
<div class="dp-embed-wrapper" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 6px; margin-bottom: 1.5rem;">
  <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
          src="https://www.youtube.com/embed/{VIDEO_ID}?start={START_SECONDS}"
          title="{TITLE}"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen="allowfullscreen">
  </iframe>
</div>
```

### D. DesignPLUS CSS Accordions & Callouts
To ensure accordions render cleanly in Canvas:
- Main container: `<div class="kl_wrapper kl_flat_sections">`
- Accordion component:
  ```html
  <div class="dp-accordion" style="margin-bottom: 1.5rem;">
    <details style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 0.5rem; padding: 0.75rem 1rem;">
      <summary style="font-weight: 600; cursor: pointer; color: #1e3a8a;">
        [Click to Expand] Drill Solution &amp; Explanation
      </summary>
      <div style="margin-top: 0.75rem; border-top: 1px solid #e2e8f0; padding-top: 0.75rem;">
        ...
      </div>
    </details>
  </div>
  ```

---

## 5. Automated Build Pipeline

The course is built programmatically using `scripts/build_canvas_cartridge.py`:

```bash
python scripts/build_canvas_cartridge.py
```

### Execution Pipeline Stages:
1. **Directory Staging**: Cleans and establishes temporary staging trees (`temp_cartridge_build/course_settings`, `temp_cartridge_build/wiki_content`, etc.).
2. **Page Content Generation**: Injects unit topics, reading descriptions, video timestamps, lab exercises, AI prompt templates, and instructor solutions into DesignPLUS HTML templates.
3. **QTI Quiz Generation**: Generates 15-question QTI XML files for all 8 units with question metadata, distractors, and correct answer keys.
4. **Manifest & Module Meta Assembly**: Writes `imsmanifest.xml` and `course_settings/module_meta.xml` with shared item identifiers and unpublished states.
5. **XML Syntax & Integrity Validation**: Parses all 30 generated XML files using `xml.etree.ElementTree` to verify syntax correctness prior to packaging.
6. **Cartridge Packaging**: Packs the staging directory into `CMAP_1815_Complete.imscc` using standard ZIP compression.

---

## 6. Canvas Deployment: Step-by-Step Instructions

To import or re-import the generated cartridge into Canvas:

### Step 1: Clean the Course Shell (Optional, for fresh re-import)
1. In Canvas, navigate to **Settings** in the left-hand course navigation.
2. On the right-side navigation sidebar, click **Reset Course Content**.
3. Confirm the reset. (This purges old duplicate modules, pages, and iframes).

### Step 2: Import the Cartridge
1. In **Settings**, click **Import Course Content** (on the right sidebar).
2. Under **Content Type**, select **Canvas Course Export Package** (DO NOT select *Common Cartridge 1.x*).
3. Under **Source**, click **Choose File** and select `CMAP_1815_Complete.imscc`.
4. Under **Content**, select **All content**.
5. Click **Import**.

### Step 3: Verify the Import
1. Navigate to **Modules**:
   - Check that all 8 units display with their 7 items.
   - Verify that Item 7 (`[Instructor Guide]...`) shows the **Unpublished** icon (grey circle with a slash).
   - Verify that all other items show the **Published** icon (green checkmark).
2. Open a **Readings & Video Lectures** page:
   - Verify that the YouTube video player loads natively on the page.
   - Verify that clicking play starts at the designated unit topic timestamp.
3. Open an **Asynchronous Preparation** page:
   - Click an accordion header to verify it smoothly expands and reveals the SQL drill solution.
