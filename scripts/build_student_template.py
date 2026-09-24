#!/usr/bin/env python3
"""
build_student_template.py
-------------------------
Automated packaging script that extracts student-facing materials from the
master CMAP 1815 curriculum repository into a clean, standalone GitHub
Template Repository (build/student_template).

Guarantees:
1. Complete isolation: All instructor solutions, lesson plans, lecture notes,
   and quiz answer banks are strictly excluded.
2. Zero-Hoop Codespace: Generates a fully automated PostgreSQL 16 Dev Container
   with pre-seeded database, SQLTools GUI extension, and safe directory trust.
3. Clean Starter Files: Creates individual lab submission starter templates.
"""

import os
import shutil
import re

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "build", "student_template")

UNIT_DIRS = [
    "unit_01_selection_and_fundamentals",
    "unit_02_filtering_and_logic",
    "unit_03_joins_and_relations",
    "unit_04_aggregation_and_pivoting",
    "unit_05_safe_dml_and_modifications",
    "unit_06_subqueries_and_window_functions",
    "unit_07_schema_design_and_integrity",
    "unit_08_performance_indexing_and_capstone",
]

DEVCONTAINER_JSON = """{
  "name": "CMAP 1815: Modern SQL Student Sandbox",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu-22.04",

  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers-contrib/features/postgresql:2": {
      "version": "16"
    }
  },

  "customizations": {
    "vscode": {
      "settings": {
        "terminal.integrated.defaultProfile.linux": "bash",
        "sqltools.useNodeRuntime": true,
        "sqltools.connections": [
          {
            "name": "CMAP 1815 Local PostgreSQL",
            "driver": "PostgreSQL",
            "server": "localhost",
            "port": 5432,
            "database": "cmap1815",
            "username": "vscode",
            "askForPassword": false
          }
        ]
      },
      "extensions": [
        "mtxr.sqltools",
        "mtxr.sqltools-driver-pg"
      ]
    }
  },

  "remoteUser": "vscode",

  "containerEnv": {
    "PGUSER": "vscode",
    "PGDATABASE": "cmap1815",
    "PGHOST": "localhost",
    "PGPORT": "5432",
    "DATABASE_URL": "postgresql://vscode@localhost:5432/cmap1815"
  },

  "postCreateCommand": "bash .devcontainer/setup_database.sh"
}
"""

SETUP_DATABASE_SH = """#!/bin/bash
set -e

echo ">>> Configuring Git directory trust..."
git config --global --add safe.directory '*'

echo ">>> Starting PostgreSQL 16 service..."
sudo service postgresql start

echo ">>> Initializing database role and sandbox..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname = 'vscode'" | grep -q 1 || sudo -u postgres createuser -s vscode
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = 'cmap1815'" | grep -q 1 || sudo -u postgres createdb -O vscode cmap1815

echo ">>> Seeding starter dataset (setup_chap1.sql)..."
if [ -f "datasets/setup_chap1.sql" ]; then
    psql -d cmap1815 -f datasets/setup_chap1.sql
    echo ">>> Database seeded successfully: locations, employees, products, orders, order_lines."
fi

echo "======================================================================"
echo "  CMAP 1815: Modern SQL Student Sandbox Ready!"
echo "  • Terminal: type 'psql' to open the interactive SQL shell."
echo "  • Visual GUI: click the Database icon on the left sidebar (SQLTools)."
echo "======================================================================"
"""

VSCODE_SETTINGS_JSON = """{
  "terminal.integrated.defaultProfile.linux": "bash",
  "sqltools.useNodeRuntime": true,
  "sqltools.connections": [
    {
      "name": "CMAP 1815 Local PostgreSQL",
      "driver": "PostgreSQL",
      "server": "localhost",
      "port": 5432,
      "database": "cmap1815",
      "username": "vscode",
      "askForPassword": false
    }
  ]
}
"""

VSCODE_EXTENSIONS_JSON = """{
  "recommendations": [
    "mtxr.sqltools",
    "mtxr.sqltools-driver-pg"
  ]
}
"""

RESET_DATABASE_SH = """#!/bin/bash
set -e

echo "======================================================================"
echo "  CMAP 1815: Resetting Database to Clean Starter State..."
echo "======================================================================"

echo ">>> Dropping existing tables and rebuilding schema..."
if [ -f "datasets/setup_chap1.sql" ]; then
    psql -d cmap1815 -f datasets/setup_chap1.sql
    echo ""
    echo "✅ SUCCESS! Database has been reset to clean starter state."
    echo "   All clean tables (locations, employees, products, orders, order_lines) are ready."
    echo "   Your .sql query files in the units/ folders were NOT touched."
else
    echo "❌ Error: datasets/setup_chap1.sql not found!"
    exit 1
fi
"""

GITIGNORE = """# Operating System Files
.DS_Store
Thumbs.db

# Logs and runtime caches
*.log
__pycache__/
*.pyc

# Local scratchpad files
scratch/
temp/
"""

STUDENT_README = """# CMAP 1815: Introduction to Modern SQL — Student Lab Sandbox

Welcome to the hands-on student repository for **CMAP 1815: Introduction to Modern SQL**. This sandbox is pre-configured with a live **PostgreSQL 16** server and interactive development tools so you can run queries, complete labs, and explore datasets directly in your web browser.

---

## 🚀 1-Click Quick Start (GitHub Codespaces)

Click the button below to launch your personal, cloud-hosted SQL development environment:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tswarmLCCC/CMAP-1815-Student-Sandbox?quickstart=1)

*Wait ~90 seconds for your container to spin up. Once the terminal displays `>>> CMAP 1815 Sandbox Ready!`, your database is live and pre-seeded!*

---

## 🛠️ Two Ways to Query PostgreSQL

### Option A: The Visual GUI (SQLTools Sidebar)
1. Click the **Database (plug/server) icon** in the left sidebar of VS Code.
2. Under **CONNECTIONS**, click **CMAP 1815 Local PostgreSQL** $\rightarrow$ **Connect**.
3. Expand **cmap1815** $\rightarrow$ **public** $\rightarrow$ **Tables** to see your live tables (`employees`, `orders`, `products`, `locations`).
4. Click any table name to inspect columns and click **Show Table Records** to view data in a spreadsheet grid!

### Option B: The Terminal CLI (`psql`)
1. Open a terminal in VS Code (`Ctrl + ~` or `Cmd + ~`).
2. Type:
   ```bash
   psql
   ```
3. Run a query:
   ```sql
   SELECT * FROM employees LIMIT 5;
   ```
4. Type `\\q` to exit the SQL prompt.

---

## 🔄 Disaster Recovery: Screwed up your data?
If you make a destructive mistake during DML (Unit 5) or Schema Design (Unit 7) experiments (like accidentally deleting records or dropping a table), you can restore your database to pristine condition anytime:
```bash
./reset_database.sh
```
*Note: This re-runs the initial seed script. It does NOT touch or delete your `.sql` lab query files in `units/`.*

---

## 📁 Repository Structure

```
.
├── .devcontainer/             # Automated PostgreSQL 16 server configuration
├── .vscode/                   # Pre-configured SQLTools database connection
├── datasets/                  # Core seed scripts (setup_chap1.sql)
├── reset_database.sh          # 1-click database recovery script
└── units/                     # Weekly Guided Learning & Lab Challenges
    ├── unit_01_selection_and_fundamentals/
    ├── unit_02_filtering_and_logic/
    ├── unit_03_joins_and_relations/
    ├── unit_04_aggregation_and_pivoting/
    ├── unit_05_safe_dml_and_modifications/
    ├── unit_06_subqueries_and_window_functions/
    ├── unit_07_schema_design_and_integrity/
    └── unit_08_performance_indexing_and_capstone/
```

Inside each unit folder, you will find:
* `lab_guide.md`: Detailed business scenario, challenge questions, and grading criteria.
* `lab_rubric.md`: The 100-point grading rubric used in Canvas SpeedGrader.
* `inclass_challenges.sql`: Guided exercises for our synchronous class sessions.
* `study_guide.md`: Asynchronous prep, readings, and focus questions.
* `self_check_drills.md`: Quick self-assessment questions before attending class.
* `lab_starter.sql`: Clean starter template for writing and saving your solutions.

---

## 📝 How to Complete and Submit Weekly Labs

1. Open the unit folder for the current week (e.g. `units/unit_01_selection_and_fundamentals/`).
2. Review the prompts in `lab_guide.md`.
3. Open `lab_starter.sql` and write your SQL queries under each challenge section.
4. **Test your code:** Run every query in PostgreSQL to confirm zero syntax errors.
5. Save a copy of your completed file as `lab{N}_{yourlastname}.sql` (e.g., `lab1_smith.sql`).
6. Upload your `.sql` file to the corresponding **Lab Assignment in Canvas**.
"""

LAB_STARTER_TEMPLATE = """/* ============================================================================
   CMAP 1815: Introduction to Modern SQL
   Unit {unit_num} Lab: {unit_title}
   
   Student Name: [YOUR NAME HERE]
   Date:         [SUBMISSION DATE]
   Canvas Course: CMAP 1815
   ----------------------------------------------------------------------------
   Submission Rules:
   1. All SQL keywords MUST be uppercase (SELECT, FROM, WHERE, ORDER BY, AS).
   2. Every clause must begin on a new line.
   3. Always alias calculated expressions with meaningful snake_case names.
   4. Test every query against your live PostgreSQL database before turning in!
   5. Save this completed file as: lab{unit_num}_yourlastname.sql
   ============================================================================ */

-- Test connection to verify server state
SELECT version(), current_database(), current_user;

/* ----------------------------------------------------------------------------
   CHALLENGE QUERIES
   (Refer to lab_guide.md for prompt specifications)
   ---------------------------------------------------------------------------- */

-- Challenge 1:
-- [Write query here]


-- Challenge 2:
-- [Write query here]


-- Challenge 3:
-- [Write query here]


-- Challenge 4:
-- [Write query here]


-- Challenge 5:
-- [Write query here]

"""

def clean_and_make_dirs():
    if os.path.exists(OUTPUT_DIR):
        # Preserve .git directory if already initialized
        git_dir = os.path.join(OUTPUT_DIR, ".git")
        temp_git = None
        if os.path.exists(git_dir):
            temp_git = os.path.join(WORKSPACE_ROOT, "scratch", "temp_student_git")
            if os.path.exists(temp_git):
                shutil.rmtree(temp_git)
            shutil.copytree(git_dir, temp_git)

        shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        if temp_git and os.path.exists(temp_git):
            shutil.copytree(temp_git, os.path.join(OUTPUT_DIR, ".git"))
            shutil.rmtree(temp_git)
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    os.makedirs(os.path.join(OUTPUT_DIR, ".devcontainer"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, ".vscode"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "datasets"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "units"), exist_ok=True)

def write_infrastruture_files():
    # .devcontainer
    with open(os.path.join(OUTPUT_DIR, ".devcontainer", "devcontainer.json"), "w", encoding="utf-8") as f:
        f.write(DEVCONTAINER_JSON)
    
    setup_sh_path = os.path.join(OUTPUT_DIR, ".devcontainer", "setup_database.sh")
    with open(setup_sh_path, "w", encoding="utf-8") as f:
        f.write(SETUP_DATABASE_SH)
    os.chmod(setup_sh_path, 0o755)

    # reset_database.sh
    reset_sh_path = os.path.join(OUTPUT_DIR, "reset_database.sh")
    with open(reset_sh_path, "w", encoding="utf-8") as f:
        f.write(RESET_DATABASE_SH)
    os.chmod(reset_sh_path, 0o755)

    # .vscode
    with open(os.path.join(OUTPUT_DIR, ".vscode", "settings.json"), "w", encoding="utf-8") as f:
        f.write(VSCODE_SETTINGS_JSON)
    with open(os.path.join(OUTPUT_DIR, ".vscode", "extensions.json"), "w", encoding="utf-8") as f:
        f.write(VSCODE_EXTENSIONS_JSON)

    # .gitignore & README
    with open(os.path.join(OUTPUT_DIR, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(GITIGNORE)
    with open(os.path.join(OUTPUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(STUDENT_README)

def copy_datasets():
    src_datasets = os.path.join(WORKSPACE_ROOT, "shared_assets", "datasets")
    dst_datasets = os.path.join(OUTPUT_DIR, "datasets")
    
    if os.path.exists(src_datasets):
        for item in os.listdir(src_datasets):
            # Only copy safe dataset files (skip solutions, candidate folders)
            if item.endswith(".sql") and "solution" not in item.lower():
                shutil.copy(os.path.join(src_datasets, item), os.path.join(dst_datasets, item))
            elif item.endswith(".csv"):
                shutil.copy(os.path.join(src_datasets, item), os.path.join(dst_datasets, item))
    print(f"  [+] Datasets copied to {dst_datasets}")

def process_units():
    units_src_root = os.path.join(WORKSPACE_ROOT, "units")
    units_dst_root = os.path.join(OUTPUT_DIR, "units")

    for idx, unit_folder in enumerate(UNIT_DIRS, start=1):
        src_unit_path = os.path.join(units_src_root, unit_folder)
        dst_unit_path = os.path.join(units_dst_root, unit_folder)
        os.makedirs(dst_unit_path, exist_ok=True)

        unit_title = unit_folder.replace("_", " ").title()

        # 1. Copy Student Lab Guide
        guide_src = os.path.join(src_unit_path, "guides", "student_lab_guide.md")
        if os.path.exists(guide_src):
            shutil.copy(guide_src, os.path.join(dst_unit_path, "lab_guide.md"))

        # 2. Copy Lab Rubric
        rubric_src = os.path.join(src_unit_path, "assessments", "lab_rubric.md")
        if os.path.exists(rubric_src):
            shutil.copy(rubric_src, os.path.join(dst_unit_path, "lab_rubric.md"))

        # 3. Copy In-Class Challenges
        inclass_src = os.path.join(src_unit_path, "sync", "inclass_challenges.sql")
        if os.path.exists(inclass_src):
            shutil.copy(inclass_src, os.path.join(dst_unit_path, "inclass_challenges.sql"))

        # 4. Copy Study Guide & Self Check Drills
        study_guide_src = os.path.join(src_unit_path, "async", "study_guide.md")
        if os.path.exists(study_guide_src):
            shutil.copy(study_guide_src, os.path.join(dst_unit_path, "study_guide.md"))

        drills_src = os.path.join(src_unit_path, "async", "self_check_drills.md")
        if os.path.exists(drills_src):
            shutil.copy(drills_src, os.path.join(dst_unit_path, "self_check_drills.md"))

        # 5. Copy Lecture SQL scripts & slides (if any)
        lectures_src = os.path.join(src_unit_path, "lectures")
        if os.path.exists(lectures_src):
            lectures_dst = os.path.join(dst_unit_path, "lecture_code")
            os.makedirs(lectures_dst, exist_ok=True)
            for f in os.listdir(lectures_src):
                # Only include student-facing demo sql or slides
                if f.endswith(".sql") and "solution" not in f.lower():
                    shutil.copy(os.path.join(lectures_src, f), os.path.join(lectures_dst, f))
                elif f == "slides.md":
                    shutil.copy(os.path.join(lectures_src, f), os.path.join(lectures_dst, f))

        # 6. Generate Clean Student Starter SQL File
        starter_sql_content = LAB_STARTER_TEMPLATE.format(unit_num=idx, unit_title=unit_title)
        with open(os.path.join(dst_unit_path, f"lab{idx}_starter.sql"), "w", encoding="utf-8") as f:
            f.write(starter_sql_content)

        print(f"  [+] Packaged Unit {idx}: {unit_folder}")

def audit_student_template():
    """Verify that zero instructor solutions, quizzes, or lecture notes leaked into student package."""
    forbidden_patterns = [
        "instructor_solution",
        "instructor_lecture_notes",
        "lesson_plan",
        "unit_quiz",
        "micro_lecture_scripts",
        "week1_solution"
    ]
    leaks = []
    total_files = 0
    for root, _, files in os.walk(OUTPUT_DIR):
        for f in files:
            total_files += 1
            path = os.path.join(root, f)
            for pat in forbidden_patterns:
                if pat in f.lower():
                    leaks.append(path)

    print("\n" + "=" * 60)
    print("AUDIT REPORT: Student Template Package Integrity")
    print("=" * 60)
    print(f"Total files packaged: {total_files}")
    if leaks:
        print(f"❌ CRITICAL AUDIT FAILURE! Found {len(leaks)} instructor files:")
        for leak in leaks:
            print(f"   - {leak}")
        raise ValueError("Audit failed: instructor solution files found in student template.")
    else:
        print("✅ AUDIT PASSED: 100% clean. Zero instructor solution or quiz files present.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    print(">>> Building CMAP 1815 Student Codespace Template...")
    clean_and_make_dirs()
    write_infrastruture_files()
    copy_datasets()
    process_units()
    audit_student_template()
    print(f">>> Student Template successfully created at: {OUTPUT_DIR}")
