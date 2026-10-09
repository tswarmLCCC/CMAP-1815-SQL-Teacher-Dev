# Video Mapping & Integration Rule

## 1. Authoritative Source of Truth
- The master index of all custom course videos is `shared_assets/VideoMap.md`.
- Every recorded video or lecture walkthrough produced by the instructor is added to this file using the format:
  ```text
  <Video Label / Pattern> - <URL>
  ```
  Example:
  ```text
  Course Orientation - https://youtu.be/_u3g4LZ142Q
  Unit 1: Selection & Relational Fundamentals - https://youtu.be/...
  Unit 1 Lab - https://youtu.be/...
  ```
- URL formats supported:
  - YouTube short URLs: `https://youtu.be/<VIDEO_ID>`
  - YouTube standard URLs: `https://www.youtube.com/watch?v=<VIDEO_ID>` (optional `&t=<SECONDS>s`)
  - YouTube embed URLs: `https://www.youtube.com/embed/<VIDEO_ID>`
  - Canvas Studio / Panopto / Kaltura / external embed URLs

## 2. Video Placement & Routing Rules
When videos appear in `shared_assets/VideoMap.md`, they must be integrated into course materials and Canvas pages according to their naming pattern:

1. **Course Orientation** (matching `Course Orientation` or `Orientation`):
   - **Start Here Page:** Embedded prominently as a responsive 16:9 player on the `Start Here: Course Overview & Orientation` page (`wiki_content/start-here.html`).
   - **Native Syllabus Page:** Directly referenced and linked on the native Canvas syllabus page (`course_settings/syllabus.html`).
   - **Master Syllabus Document:** Referenced in `course_specs/CMAP_1815_Master_Syllabus.docx` under Course Notes.

2. **Environment & Setup Videos** (matching `Codespaces` or `Github Codespaces`):
   - **Codespaces Guide:** Embedded prominently in `Student Guide: Navigating Codespaces & SQLTools` (`wiki_content/student-codespaces-sqltools-guide.html`) under Section 1.
   - **Lab Setup Guide:** Linked or embedded in `Student Guide: How to Complete & Submit Weekly SQL Labs` (`wiki_content/student-lab-setup-guide.html`).

3. **Unit Lecture / Overview Videos** (matching `Unit X` or `Unit X: [Topic]` or `Micro-Video X.Y`):
   - **Readings & Media Page:** Embedded directly in `Unit X: Required Readings, Concepts & Video Lectures` (`wiki_content/unit-XX-readings-and-media.html`), populating Section 4 ("Institutional Video Lecture Embeds") and replacing the dashed placeholder block.
   - If multiple custom lecture videos exist for the same unit, stack them neatly within Section 4.

4. **Unit Lab Walkthrough Videos** (matching `Unit X Lab` or `Lab X`):
   - **Applied Lab Guide:** Embedded in `Unit X: Applied Lab Guide` (`wiki_content/unit-XX-student-lab-guide.html`) under an "Instructor Video Walkthrough" callout card at the start of the guide.

5. **Ambiguous or Unrecognized Video Labels:**
   - If a video entry in `shared_assets/VideoMap.md` does not clearly match any of the above patterns, the agent must ask the user for clarification before placing it.

## 3. Embedding and Styling Standards
All embedded video players must comply with DesignPLUS and responsive HTML standards:
- Wrap each video in a responsive 16:9 container card:
  ```html
  <div style="margin: 1.5rem 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <div style="background: #1e3a8a; color: #ffffff; padding: 0.6rem 1rem; font-weight: 600; font-size: 0.95em;">
      <i class="fas fa-play-circle"></i> [Video Title]
    </div>
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
      <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
              src="https://www.youtube.com/embed/[VIDEO_ID]"
              title="[Video Title]"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen="allowfullscreen"
              loading="lazy"></iframe>
    </div>
    <div style="padding: 0.5rem 1rem; background: #f8fafc; font-size: 0.85em; color: #64748b;">
      <a href="[URL]" target="_blank" rel="noopener">Open [Video Title] in new tab</a>
    </div>
  </div>
  ```

## 4. Automation & Cartridge Build Pipeline
- The cartridge build script (`scripts/build_canvas_cartridge.py` and its mirror `agent_tools_catalog/scripts/build_canvas_cartridge.py`) must parse `shared_assets/VideoMap.md` dynamically during the build process.
- Changes in `shared_assets/VideoMap.md` must automatically reflect in the generated wiki pages and the output cartridge (`CMAP_1815_Complete.imscc`).
