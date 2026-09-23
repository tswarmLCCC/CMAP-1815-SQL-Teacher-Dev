# Internal Development Tools & Agent Catalog

This directory houses the curated, **best-of-breed skills, automation engines, templates, and playbooks** developed across your course engineering repositories.

---

## Catalog Directory Architecture

```
agent_tools_catalog/
├── skills/                                      # Antigravity Progressive-Disclosure Skills
│   ├── canvas-course-builder/SKILL.md          # Full Canvas .imscc Cartridge Generator
│   ├── slide-deck-generator/SKILL.md           # Programmatic 16:9 Slide Presentation Engine
│   ├── course-intake-scanner/SKILL.md          # Knowledge Dump Intake Scanner & Scaffolder
│   └── syllabus-docx-cloner/SKILL.md           # Institutional Word (.docx) Syllabus Cloner
├── scripts/                                     # Reusable Python CLI Automation Engines
│   ├── build_canvas_cartridge.py               # Complete Canvas package & XML builder
│   ├── slide_engine.py                         # High-contrast PPTX generator with 5 archetypes
│   ├── intake_scanner.py                       # Knowledge dump analyzer & course plan generator
│   └── audit_deck.py                           # Slide deck compliance & contrast auditor
├── templates/                                   # Production-Grade Curriculum Templates
│   ├── syllabi/
│   │   └── LCCC_Master_Syllabus_Template.docx  # Accredited Word syllabus base template
│   ├── rubrics/
│   │   ├── capstone_defense_rubric_template.md # 100-point capstone defense rubric
│   │   ├── peer_review_rubric_template.md      # Peer code-review evaluation rubric
│   │   └── course_audit_rubric.md              # 8-dimensional course quality scorecard
│   ├── instructional/
│   │   ├── competency_map_template.md          # Weekly learning outcomes & Bloom's taxonomy
│   │   ├── instructional_guide_template.md     # Educator lecture delivery runbook
│   │   └── demo_contingency_runbook_template.md# Live demo disaster recovery plan
│   └── code_labs/
│       └── code_lab_template.py                # Student self-grading code laboratory template
└── playbooks/                                   # Institutional Design & Pedagogical Standards
    ├── COURSE_PRODUCTION_WORKFLOW.md           # Complete Canvas course production handbook
    ├── SLIDE_DESIGN_PLAYBOOK.md                # 5 universal slide archetypes & typography rules
    ├── WHY_WHAT_HOW_PEDAGOGY.md                # Why-What-How 4-step scaffolding framework
    └── ZERO_COST_INFRASTRUCTURE.md             # GitHub Codespaces devcontainer lab blueprint
```

---

## How to Point Antigravity & Agents to This Tooling

### Strategy 1: Central GitHub Repository (Recommended)
Host this folder as an independent repository (e.g. `github.com/tswarmLCCC/agent-tools` or `internal-dev-tools`). You can then clone it or add it as a git submodule across course repositories.

### Strategy 2: Global Antigravity Discovery (Zero-Copy)
To make these skills automatically available in **every project** you open on your machine without needing to copy them into each course repository:
- Copy or symlink the `skills/` folders to `C:\Users\tswar.KAIASCOMPUTER\.gemini\antigravity\skills\` (or `~/.gemini/config/skills/`).
- Antigravity will discover them dynamically via progressive disclosure.

### Strategy 3: Project-Specific Customizations
Copy relevant skills into `.agents/skills/<skill-name>/SKILL.md` in any specific course repository. Antigravity will load them immediately when in that workspace.
