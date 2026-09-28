#!/usr/bin/env python3
"""
=============================================================================
Portable Canvas Course Cartridge Compiler (build_course.py)
=============================================================================
Zero-dependency CLI tool that compiles a production-grade, DesignPLUS-styled
Canvas Common Cartridge (.imscc) package from standard Markdown files and a JSON config.

Solves the Common Canvas Cartridge Import Bugs:
1. "HTML File Links": Fixes the bug where Canvas imports pages as raw file
   attachments in "Files" rather than native Canvas WikiPages. (Enforces 
   <content_type>WikiPage</content_type> in module_meta.xml and synced manifest).
2. "Broken Styling": Injects robust, self-contained inline CSS and DesignPLUS
   helper classes so pages render with rich formatting even if custom CSS
   files are blocked or stripped by Canvas sanitization.
3. "Un-graded Quizzes": Compiles native QTI 1.2 XML with Canvas assessment_meta.xml
   settings directly from clean Markdown files.
4. "Generic Assignments": Packages native Canvas Assignments with SpeedGrader
   file upload filters (.sql, .py, .pdf, .txt) and weighted gradebook groups.
5. "Automated Cartridge Backups": Automatically preserves previous .imscc builds
   with timestamps in archive/cartridge_backups/ before generating new packages.

Usage:
  python build_course.py --config course_config.json --units-dir units --output Course_Export.imscc
=============================================================================
"""

import os
import sys
import re
import json
import argparse
import html
import shutil
import datetime
from typing import Dict, List, Any, Optional

# Add scripts directory to module path
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPT_DIR)

from build_cartridge import CanvasCourseBuilder
from html_styler import render_designplus_html, render_standard_page_html, parse_markdown_to_html
from qti_builder import parse_quiz_md, make_canvas_id
from docx_syllabus import create_syllabus_docx


def load_config(config_path: str) -> Dict[str, Any]:
    """Loads course configuration JSON."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_file(directory: str, patterns: List[str]) -> Optional[str]:
    """Finds first file in directory matching any pattern in patterns."""
    if not os.path.exists(directory):
        return None
    for root, _, files in os.walk(directory):
        for f in sorted(files):
            for pat in patterns:
                if re.search(pat, f, re.IGNORECASE):
                    return os.path.join(root, f)
    return None


def compile_course(config_path: str, units_dir: str, output_imscc: str, build_dir: Optional[str] = None):
    print("=" * 70)
    print("Portable Canvas Course Cartridge Compiler")
    print("=" * 70)

    config = load_config(config_path)
    c_code = config.get("course_code", "COURSE 1010")
    c_title = config.get("course_title", "Sample Course")
    print(f"Target Course: {c_code} - {c_title}")
    print(f"Units Folder:  {units_dir}")
    print(f"Output File:   {output_imscc}\n")

    builder = CanvasCourseBuilder(config, output_imscc, build_dir=build_dir)
    builder.prepare_directories()

    # 1. Assignment Groups (Gradebook Weighting)
    group_map = builder.build_assignment_groups()
    labs_gid = group_map.get("labs", list(group_map.values())[0])
    quizzes_gid = group_map.get("quizzes", list(group_map.values())[0])

    # 2. Core Settings
    builder.build_core_settings()

    # 3. Native Syllabus Page & Word Document
    syllabus_md_file = find_file(os.path.dirname(config_path), ["syllabus\\.md"])
    syllabus_body = "<p>Welcome to modern online coursework.</p>"
    if syllabus_md_file:
        with open(syllabus_md_file, "r", encoding="utf-8") as sf:
            syllabus_body = parse_markdown_to_html(sf.read())

    # Build Word Syllabus .docx
    docx_path = os.path.join(builder.syllabi_dir, f"{c_code.replace(' ', '_')}_Master_Syllabus.docx")
    try:
        create_syllabus_docx(config, docx_path)
        print(f"  [+] Generated Master Syllabus (.docx): {os.path.basename(docx_path)}")
    except Exception as e:
        print(f"  [!] Note: docx syllabus generation skipped: {e}")

    # Build Native Syllabus HTML
    docx_rel = os.path.relpath(docx_path, builder.web_res_dir).replace(os.sep, "/")
    syllabus_html = f"""<div class="dp-header dp-basic-bar" style="background: #1e3a8a; color: #ffffff; padding: 1.5rem; border-radius: 6px; margin-bottom: 1.5rem;">
  <h1 style="margin: 0; color: #ffffff; font-size: 1.8rem;">{html.escape(c_code)}: {html.escape(c_title)}</h1>
  <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Institutional Course Syllabus &amp; Policies</p>
</div>
<div style="background: #eff6ff; border-left: 4px solid #2563eb; padding: 1rem 1.25rem; margin-bottom: 1.5rem; border-radius: 0 4px 4px 0;">
  <p style="margin: 0; font-weight: 600;">Download Official Word Document Syllabus:</p>
  <p style="margin: 0.25rem 0 0 0;"><a class="instructure_file_link" title="{os.path.basename(docx_path)}" href="$IMS-CC-FILEBASE$/{docx_rel}?canvas_=1&amp;canvas_qs_wrap=1" target="_blank" rel="noopener" style="color: #2563eb; font-weight: 600; text-decoration: underline;">\ud83d\udcc4 {os.path.basename(docx_path)}</a></p>
</div>
{syllabus_body}
"""
    with open(os.path.join(builder.settings_dir, "syllabus.html"), "w", encoding="utf-8") as f:
        f.write(syllabus_html)

    # 4. Discover & Process Weekly Units
    unit_folders = []
    if os.path.exists(units_dir):
        unit_folders = [f for f in sorted(os.listdir(units_dir)) if os.path.isdir(os.path.join(units_dir, f))]

    print(f"  [*] Discovered {len(unit_folders)} unit folders under {units_dir}/")

    for u_idx, u_folder in enumerate(unit_folders, 1):
        u_dir = os.path.join(units_dir, u_folder)
        u_title = u_folder.replace("_", " ").title()
        # Clean title prefix
        u_title_clean = re.sub(r"^Unit\s*\d+\s*", "", u_title, flags=re.IGNORECASE).strip()
        u_display_title = f"Unit {u_idx}: {u_title_clean}" if u_title_clean else f"Unit {u_idx}"

        print(f"  [+] Processing Unit {u_idx}: {u_folder}")
        module_items = []
        mod_id = make_canvas_id(f"mod_unit_{u_idx}")

        # Item 1: Unit Overview (WikiPage) - Uses DesignPLUS Banner
        ov_file = find_file(u_dir, ["overview.*\\.md$", "^overview\\.md$"])
        ov_id = make_canvas_id(f"page_u{u_idx}_overview")
        ov_html_file = f"unit-{u_idx:02d}-overview.html"
        ov_body = f"<p>Welcome to {u_display_title}. Review the weekly readings and complete all applied labs.</p>"
        if ov_file:
            with open(ov_file, "r", encoding="utf-8") as of:
                ov_body = parse_markdown_to_html(of.read())
        
        ov_page_content = f"""<div class="dp-header dp-basic-bar" style="background: #1e3a8a; color: #ffffff; padding: 1.5rem; border-radius: 6px; margin-bottom: 1.5rem;">
  <h1 style="margin: 0; color: #ffffff; font-size: 1.8rem;">{u_display_title}</h1>
  <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Weekly Roadmap, Learning Objectives &amp; Schedule</p>
</div>
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b;">
{ov_body}
</div>
"""
        builder.add_wiki_page(ov_id, ov_html_file, f"Unit {u_idx} Overview: {u_title_clean}", ov_page_content)
        module_items.append({"type": "WikiPage", "title": f"Unit {u_idx} Overview: {u_title_clean}", "ref": ov_id, "indent": 0, "state": "active"})

        # Item 2: Required Readings & Lectures (WikiPage)
        readings_file = find_file(u_dir, ["reading", "lecture.*notes", "slides"])
        if readings_file:
            r_id = make_canvas_id(f"page_u{u_idx}_readings")
            r_html_file = f"unit-{u_idx:02d}-readings.html"
            with open(readings_file, "r", encoding="utf-8") as rf:
                r_body = parse_markdown_to_html(rf.read())
            r_panels = [("Core Reading & Lecture Content", r_body)]
            r_page_content = render_standard_page_html(f"Unit {u_idx}: Required Readings & Lectures", "<p>Review all instructional materials and concepts.</p>", r_panels, r_id)
            builder.add_wiki_page(r_id, r_html_file, f"Unit {u_idx}: Required Readings & Lectures", r_page_content)
            module_items.append({"type": "WikiPage", "title": f"Unit {u_idx}: Required Readings & Lectures", "ref": r_id, "indent": 1, "state": "active"})

        # Item 3: Asynchronous Preparation & Drills (WikiPage)
        drills_file = find_file(u_dir, ["study_guide", "drill", "self_check", "prep"])
        if drills_file:
            d_id = make_canvas_id(f"page_u{u_idx}_drills")
            d_html_file = f"unit-{u_idx:02d}-drills.html"
            with open(drills_file, "r", encoding="utf-8") as df:
                d_body = parse_markdown_to_html(df.read())
            d_panels = [("Formative Self-Check Drills & Exercises", d_body)]
            d_page_content = render_standard_page_html(f"Unit {u_idx}: Asynchronous Preparation & Drills", "<p>Self-check exercises with collapsible answer keys.</p>", d_panels, d_id)
            builder.add_wiki_page(d_id, d_html_file, f"Unit {u_idx}: Asynchronous Preparation & Drills", d_page_content)
            module_items.append({"type": "WikiPage", "title": f"Unit {u_idx}: Asynchronous Preparation & Drills", "ref": d_id, "indent": 1, "state": "active"})

        # Item 4: Applied Lab Guide (WikiPage)
        lab_file = find_file(u_dir, ["lab_guide", "student_lab", "project_guide"])
        if lab_file:
            lg_id = make_canvas_id(f"page_u{u_idx}_lab_guide")
            lg_html_file = f"unit-{u_idx:02d}-applied-lab-guide.html"
            with open(lab_file, "r", encoding="utf-8") as lf:
                lg_body = parse_markdown_to_html(lf.read())
            
            # Look for optional rubric
            rubric_file = find_file(u_dir, ["rubric"])
            rubric_html = ""
            if rubric_file:
                with open(rubric_file, "r", encoding="utf-8") as rf:
                    rubric_html = parse_markdown_to_html(rf.read())

            lg_panels = [("Laboratory Scenario & Task Specifications", lg_body)]
            if rubric_html:
                lg_panels.append(("Grading Rubric & Scoring Criteria", rubric_html))

            lg_page_content = render_standard_page_html(f"Unit {u_idx}: Applied Lab Guide", "<p>Hands-on technical scenario, tasks, and rubric criteria.</p>", lg_panels, lg_id)
            builder.add_wiki_page(lg_id, lg_html_file, f"Unit {u_idx}: Applied Lab Guide", lg_page_content)
            module_items.append({"type": "WikiPage", "title": f"Unit {u_idx}: Applied Lab Guide", "ref": lg_id, "indent": 1, "state": "active"})

        # Item 5: Native Canvas Assignment (Assignment)
        assign_id = make_canvas_id(f"assignment_u{u_idx}")
        assign_title = f"Unit {u_idx} Applied Lab Assignment"
        assign_desc = f"""<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><title>{html.escape(assign_title)}</title></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; padding: 1rem; max-width: 900px;">
  <h2 style="color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 0.3rem;">{html.escape(assign_title)} (50 Points)</h2>
  <div style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 0.75rem 1.25rem; margin: 1rem 0; border-radius: 0 4px 4px 0;">
    <p style="margin: 0;">Complete the exercises outlined in the <strong>Unit {u_idx}: Applied Lab Guide</strong> and upload your completed solution file below for evaluation.</p>
  </div>
  <h3 style="color: #0f172a; margin-top: 1.5rem;">Submission Instructions</h3>
  <ol style="padding-left: 1.5rem; line-height: 1.8;">
    <li>Write and test your solution code in your development environment.</li>
    <li>Verify that your solution satisfies all criteria in the grading rubric.</li>
    <li>Upload your solution file (.sql, .py, .txt, or .pdf) to this assignment.</li>
  </ol>
</body>
</html>"""
        builder.build_assignment(assign_id, assign_title, labs_gid, assign_desc, points=50.0, allowed_ext="sql,py,txt,pdf")
        module_items.append({"type": "Assignment", "title": assign_title, "ref": assign_id, "indent": 1, "state": "active"})

        # Item 6: Knowledge Check (Quiz) via QTI 1.2
        quiz_file = find_file(u_dir, ["quiz.*\\.md$", "^quiz\\.md$"])
        if quiz_file:
            q_id = make_canvas_id(f"quiz_u{u_idx}")
            q_title = f"Unit {u_idx} Knowledge Check: {u_title_clean}"
            try:
                questions = parse_quiz_md(quiz_file)
                if questions:
                    builder.build_quiz(q_id, q_title, quizzes_gid, questions)
                    module_items.append({"type": "Quizzes::Quiz", "title": q_title, "ref": q_id, "indent": 1, "state": "active"})
                    print(f"     [>] Compiled QTI Quiz: {len(questions)} questions")
            except Exception as e:
                print(f"     [!] Warning: Quiz compilation skipped for {quiz_file}: {e}")

        # Item 7: Instructor Notes & Solutions (Unpublished WikiPage)
        sol_file = find_file(u_dir, ["instructor.*solution", "teaching.*notes", "solution.*\\.sql$", "solution.*\\.py$"])
        if sol_file:
            t_id = make_canvas_id(f"page_u{u_idx}_instructor_guide")
            t_html_file = f"unit-{u_idx:02d}-instructor-guide.html"
            with open(sol_file, "r", encoding="utf-8") as sf:
                sol_code = sf.read()
            sol_box = f"<div style='background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; overflow-x: auto; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5;'><pre style='margin: 0; background: transparent; color: inherit;'><code>{html.escape(sol_code.strip())}</code></pre></div>"
            t_panels = [("Instructor Master Solution Key & Answer Code", sol_box)]
            t_page_content = render_standard_page_html(f"[Instructor Guide] Unit {u_idx} Teaching Notes & Solutions", "<p><strong>[FOR INSTRUCTORS ONLY — UNPUBLISHED]</strong> Master answer keys and grading solutions.</p>", t_panels, t_id, workflow_state="unpublished")
            builder.add_wiki_page(t_id, t_html_file, f"[Instructor Guide] Unit {u_idx} Teaching Notes & Solutions", t_page_content)
            module_items.append({"type": "WikiPage", "title": f"[Instructor Guide] Unit {u_idx} Teaching Notes & Solutions", "ref": t_id, "indent": 1, "state": "unpublished"})

        # Register Module
        builder.add_module(mod_id, u_display_title, module_items)

    # 5. Generate Manifest and Synchronized Module Meta
    print("\n--- Generating Synchronized Canvas Manifest & Module Meta ---")
    builder.build_module_meta_and_manifest()

    # 6. Validate XML Files
    print("--- Running XML Validation Suite ---")
    xml_count = builder.validate_xml_files()
    print(f"SUCCESS: Verified {xml_count} XML files. Zero syntax errors!")

    # 7. Package into .imscc
    print(f"\n--- Compressing into Common Cartridge Package: {output_imscc} ---")
    total_files = builder.package_imscc()
    size_mb = os.path.getsize(output_imscc) / (1024 * 1024)
    print(f"SUCCESS: Created {output_imscc} ({total_files} files, {size_mb:.2f} MB)")
    print("\n[SUCCESS] Canvas Native Course Export Package build complete!\n")


def main():
    parser = argparse.ArgumentParser(description="Compile Canvas Common Cartridge (.imscc) with DesignPLUS formatting and QTI quizzes.")
    parser.add_argument("--config", default="course_config.json", help="Path to course configuration JSON file.")
    parser.add_argument("--units-dir", default="units", help="Directory containing unit subdirectories.")
    parser.add_argument("--output", default="", help="Path for output .imscc file (defaults to [code]_Complete.imscc).")
    parser.add_argument("--build-dir", default=None, help="Temporary staging build directory.")

    args = parser.parse_args()

    # Determine default output if not supplied
    output_imscc = args.output
    if not output_imscc:
        try:
            cfg = load_config(args.config)
            c_code = cfg.get("course_code", "Course").replace(" ", "_")
            output_imscc = f"{c_code}_Complete.imscc"
        except Exception:
            output_imscc = "Canvas_Course_Package.imscc"

    compile_course(args.config, args.units_dir, output_imscc, build_dir=args.build_dir)


if __name__ == "__main__":
    main()
