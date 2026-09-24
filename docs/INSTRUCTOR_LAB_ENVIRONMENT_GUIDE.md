# Instructor Guide: Lab Delivery Architectures & Infrastructure Strategy

**Course:** CMAP 1815: Introduction to Modern SQL  
**Audience:** Instructor / Course Author  
**Target Environments:** GitHub Codespaces (Cloud / Hybrid) vs. Proxmox VE (On-Premises Campus Lab)  
**Last Updated:** Academic Year 2026–2027  

---

## Executive Summary & Strategic Verdict

You asked two core questions:
1. **"How should my students do these labs, and do you like the GitHub solution?"**
2. **"Should I build a Proxmox PostgreSQL image that they clone in a lab environment?"**

### The Short Verdict: **The Dual-Track Architecture**
* **The GitHub Solution (Codespaces + Dev Containers) is your essential Primary Daily Driver.**  
  Because CMAP 1815 is an **8-week accelerated hybrid course** with **150 minutes of synchronous active learning** and **150 minutes of asynchronous guided study** per week, students *must* be able to query PostgreSQL from anywhere—campus computer labs, home PCs, Macs, locked-down loaners, or Chromebooks. A cloud-native Dev Container eliminates the notorious "Week 1 Tech Support Hell," guarantees an identical PostgreSQL 16 runtime for every student, integrates natively with Git for portfolio building, and isolates destructive DDL/DML so mistakes in Unit 5 or Unit 7 never crash a classmate's database.
* **The Proxmox Solution is your high-value Secondary Campus Lab & Safety Net.**  
  Proxmox VE is outstanding for zero-latency classroom sessions, high-integrity air-gapped exams (preventing external AI/internet access during midterms or the capstone defense), campus network outage survivability, and advanced DBA demonstrations (e.g., inspecting physical WAL logs, server clustering, and `pg_hba.conf` configuration).
* **The Winning Formula:**  
  Use **GitHub Codespaces** as the default student workflow for all weekly asynchronous prep, synchronous class labs, and Canvas submissions. Deploy a **Proxmox PostgreSQL Lab Appliance** in your physical computer lab as an instant-failover local backup, an exam sandbox, and a demonstration environment.

---

## Architectural Comparison Matrix

| Evaluation Dimension | GitHub Codespaces (Dev Containers) | Proxmox VE (Student VM Clones) | Proxmox VE (Multi-Tenant Central LXC) |
| :--- | :--- | :--- | :--- |
| **Primary Deployment** | Cloud container per student (browser-based) | Full OS Virtual Machine per student | Single high-spec Linux container / DB instance |
| **Off-Campus / Remote Access** | **Flawless (10/10)** — Any browser, zero VPN | **Difficult (3/10)** — Requires campus VPN/firewall holes | **Difficult (3/10)** — Requires campus VPN/firewall holes |
| **BYOD / Device Diversity** | Windows, macOS, Linux, Chromebook, iPad | Lab PCs or campus network Wi-Fi only | Lab PCs or campus network Wi-Fi only |
| **Client UI** | VS Code Web + SQLTools GUI + `psql` CLI | DBeaver CE GUI on Linux Desktop (XFCE/Gnome) | DBeaver on Lab PC or CloudBeaver Web GUI |
| **Resource Overhead** | Managed by GitHub cloud (2 vCPU / 4–8 GB RAM) | **Heavy** — 4 GB RAM & 25 GB disk per student | **Ultralight** — 4–8 GB RAM for entire class |
| **Unit 5 / Unit 7 Sandbox Isolation** | **Complete** — Each student has private container | **Complete** — Each student has private VM | **Partial** — Shared instance; isolated by database name |
| **Mistake Recovery (e.g. `DROP SCHEMA`)** | Re-run `setup_chap1.sql` or rebuild in 60s | Instant Proxmox snapshot rollback (5s) | Re-create student database via SQL script |
| **Student Quota / Cost** | 60 core-hrs/mo free (180 hrs on GitHub Ed) | 100% Free on your own server hardware | 100% Free on your own server hardware |
| **Git & Submission Workflow** | Native `git commit` & Canvas `.sql` upload | Manual file export / USB / Web browser upload | Manual file export / Canvas upload |
| **Air-Gapped / Exam Control** | Low (Full internet access required) | **High** — Can disable external gateway routing | **High** — Can disable external gateway routing |

---

## Track 1: The GitHub Codespaces Solution (In-Depth Analysis)

### Why Codespaces is Ideal for CMAP 1815
1. **Zero-Install Onboarding:** In traditional introductory SQL courses, 20–30% of the first two weeks is consumed debugging local PostgreSQL installs, PATH errors, conflicting port 5432 bindings, homebrew permissions on macOS, and Windows WSL2 virtualization errors. Codespaces eliminates this entirely: students click one link, wait ~90 seconds, and have a running terminal with PostgreSQL 16 ready to go.
2. **Hybrid Course Alignment:** Students work on their sync challenges during Tuesday/Thursday class, close their laptop, open it at home on Saturday for the Asynchronous Study Guide and AI Drill, and their exact workspace, open files, and database state resume instantly.
3. **Student Isolation for Destructive SQL:**
   - **Unit 5 (Safe DML):** Students test `DELETE` and `UPDATE` statements, transactions, and rollback boundaries.
   - **Unit 7 (Schema Design & DDL):** Students run `CREATE TABLE`, `ALTER TABLE`, and `DROP TABLE`.
   - In a shared multi-tenant database, one student accidentally running `TRUNCATE TABLE employees CASCADE;` breaks the lab for everyone in the room. In Codespaces, every student has their own private container.
4. **Professional Developer Tooling:** Students learn standard VS Code keyboard shortcuts, integrated terminal navigation, and Git workflows (`git status`, `git add`, `git commit`, `git push`), graduating with a verifiable GitHub repository of their work.

### Real-World Codespaces Gotchas & How to Mitigate Them

> [!WARNING]
> **Free Quota Exhaustion (The "Running Out of Hours" Trap):**
> * GitHub free personal accounts receive **60 core-hours and 15 GB storage per month**.
> * A standard 2-core Codespace consumes 2 core-hours per clock hour. If left active, 60 core-hours equals **30 real-world clock hours per month** (~7.5 hours per week).
> * In an intensive 8-week course (5 hours/week of active class and homework), a student who leaves Codespaces running in an open browser tab will exhaust their free quota by Week 3 or 4!

#### The 3-Step Instructor Mitigation Plan for GitHub Quotas:
1. **Require the GitHub Student Developer Pack:**  
   Direct all students during Week 1 orientation to apply at [education.github.com/pack](https://education.github.com/pack). Verification with their `.edu` email grants **180 free core-hours per month**, which is more than enough for the entire semester.
2. **Enforce a 15-Minute Idle Timeout:**  
   Configure `.devcontainer/devcontainer.json` or instruct students to set their personal Codespaces default idle timeout from 30 minutes down to 15 minutes (**Settings $\rightarrow$ Codespaces $\rightarrow$ Default idle timeout $\rightarrow$ 15 minutes**).
3. **Pre-Build Containers (GitHub Organization / Classroom):**  
   If you host the course repository under a GitHub Organization (or GitHub Classroom), enable **Codespaces Prebuilds**. This cuts container launch time from 2 minutes down to **5 seconds** and prevents build-time CPU charges.

---

### Upgrading the Repository's Dev Container Configuration

The current `.devcontainer/devcontainer.json` in this repository only installs Python. To give students an out-of-the-box PostgreSQL 16 server with a graphical SQL query editor (SQLTools), update your `.devcontainer` configuration as follows.

#### 1. Recommended `.devcontainer/devcontainer.json`
```json
{
  "name": "CMAP 1815 Modern SQL Sandbox",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu-22.04",

  // Install PostgreSQL 16 server directly into the container
  "features": {
    "ghcr.io/devcontainers/features/sshd:1": {},
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
        "mtxr.sqltools-driver-pg",
        "cweijan.vscode-database-client2"
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

  // Initialize database and auto-load Unit 1 Superstore dataset
  "postCreateCommand": "bash .devcontainer/setup_database.sh"
}
```

#### 2. Accompanying `.devcontainer/setup_database.sh`
```bash
#!/bin/bash
set -e

echo ">>> Starting PostgreSQL 16 service..."
sudo service postgresql start

echo ">>> Creating CMAP 1815 database and role..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname = 'vscode'" | grep -q 1 || sudo -u postgres createuser -s vscode
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = 'cmap1815'" | grep -q 1 || sudo -u postgres createdb -O vscode cmap1815

echo ">>> Seeding starter schema and datasets..."
if [ -f "shared_assets/datasets/setup_chap1.sql" ]; then
    psql -d cmap1815 -f shared_assets/datasets/setup_chap1.sql
    echo ">>> Database seeded successfully with locations, employees, products, orders, order_lines."
fi

echo ">>> Setup Complete! Type 'psql' or use the VS Code SQLTools panel to run queries."
```

#### Why this GUI integration matters:
With the `mtxr.sqltools` extension configured, students do **not** have to rely solely on the raw command line `psql` client. They get an interactive sidebar in VS Code displaying:
* Interactive table treeview (schema, tables, columns, data types).
* One-click "Show Table Records" viewer (tabular grid output).
* An inline query scratchpad with syntax highlighting and run buttons.
This gives students the visual polish of **DBeaver** without needing to install or manage an external desktop application!

---

## Track 2: The Proxmox VE Solution (On-Premises Lab Appliance)

If you have dedicated Proxmox VE hypervisor hardware in your campus lab, you have a powerful tool for localized control. Let's look at how to deploy it properly.

### When Proxmox is the Superior Choice
1. **Air-Gapped Assessment & Capstone Defense (Anti-Cheating):**  
   During high-stakes assessments (e.g., the Unit 8 Capstone live query defense or midterm exams), you can isolate the Proxmox lab virtual network (VLAN) from the public internet. Students cannot consult external AI tools (ChatGPT, Claude) or external repositories—they must rely strictly on their internal knowledge and local PostgreSQL documentation.
2. **Zero Internet Dependency:**  
   If campus construction cuts the fiber line or the college Wi-Fi is experiencing an outage, in-person lab sessions continue without interruption.
3. **Real Enterprise DBA Training:**  
   For Unit 7 and Unit 8, you can grant students root access inside their personal Proxmox container so they can configure `postgresql.conf`, inspect disk buffers, monitor OS-level CPU/IO thrashing under unindexed queries, and examine WAL (Write-Ahead Logging) archives.

---

### Choosing the Right Proxmox Architecture

In your earlier draft ([`proxmox_student_db_lab_guide.md`](file:///workspaces/CMAP_1815_Autogen/legacy/github_source/archive/v1_original_drafts/units/proxmox_student_db_lab_guide.md)), you outlined building a **Full Linux Desktop VM (Ubuntu/Mint) with DBeaver**. 

Here is an objective engineering comparison of the three ways to run Proxmox for this class:

```
Proxmox Architectural Options:
├── Option A: Full Desktop VM per Student (KVM/QEMU + XFCE/Gnome + DBeaver) [Heavyweight]
├── Option B: Lightweight Linux Container per Student (LXC + code-server + Postgres) [Recommended for 1:1]
└── Option C: Central Multi-Tenant Database Appliance (Single LXC + CloudBeaver Web GUI) [Simplest to Manage]
```

#### Architecture Comparison

| Metric | Option A: Desktop VM + DBeaver | Option B: LXC + Web VS Code | Option C: Central Multi-Tenant LXC |
| :--- | :--- | :--- | :--- |
| **RAM per Student** | **4,096 MB (4 GB)** | **512 MB – 1,024 MB** | **~250 MB per active connection** |
| **Class of 25 Students** | **100 GB RAM** required on host | **12.5 – 25 GB RAM** required | **8 GB RAM** total for the VM |
| **Disk Storage** | 25 GB per VM (or ZFS linked clone) | 2–4 GB per container | 30 GB total disk |
| **Student Access Method** | Proxmox NoVNC console / RDP | Web browser to `http://ip:8080` | DBeaver on Lab PC or Web Browser |
| **Isolation** | 100% OS & Database isolation | 100% OS & Database isolation | Database level only (`CREATE DATABASE`) |
| **Instructor Maintenance** | High (25 OS installs / updates) | Low (ZFS linked clone template) | **Very Low** (Single system to update) |

---

### Option B: The "Modern Proxmox" Blueprint (LXC + code-server)

Rather than forcing 25 full graphical desktop environments to run on your server hardware, the most elegant Proxmox setup is a **Debian 12 LXC Golden Template** running PostgreSQL 16 and **code-server** (VS Code in the browser):

1. **Create Base Template (CT 9000):**
   * OS: Debian 12 Standard LXC Template.
   * Specs: 1 vCPU, 1024 MB RAM, 8 GB SSD disk.
2. **Install Components inside Template:**
   ```bash
   # Update & Install PostgreSQL 16
   apt update && apt install -y curl sudo gnupg postgresql postgresql-contrib
   
   # Install code-server (Browser VS Code)
   curl -fsSL https://code-server.dev/install.sh | sh
   
   # Configure systemd service for student user
   systemctl enable --now code-server@student
   ```
3. **Pre-seed CMAP 1815 Repository:**
   Clone your course repo directly into `/home/student/workspace` and run `setup_chap1.sql`.
4. **Convert to Template & Deploy:**
   * Right-click CT 9000 $\rightarrow$ **Convert to Template**.
   * Run a 5-line bash loop in the Proxmox Shell to generate linked clones for all 25 students:
     ```bash
     for i in $(seq 101 125); do
         pct clone 9000 $i --hostname "student-$i" --full 0
         pct set $i --net0 name=eth0,bridge=vmbr0,ip=192.168.10.$i/24,gw=192.168.10.1
         pct start $i
     done
     ```
5. **Student Access:**
   Students simply open their browser on lab computers and navigate to `http://192.168.10.1XX:8080`. They see the exact same VS Code interface as Codespaces, completely hosted on your on-premises Proxmox server!

---

### Option C: The Central Multi-Tenant Proxmox Database (Zero-Maintenance)

If you have existing physical computer lab PCs that already have VS Code or DBeaver installed:
1. Spin up **one** high-performance Ubuntu/Debian LXC container (e.g. 4 vCPUs, 8 GB RAM).
2. Install PostgreSQL 16 and configure `postgresql.conf` (`listen_addresses = '*'`) and `pg_hba.conf` (`host all all 192.168.1.0/24 scram-sha-256`).
3. Run an automated instructor provisioning script that generates student credentials:
   ```sql
   -- Loop for students
   CREATE USER student01 WITH PASSWORD 'CoursePass2026!';
   CREATE DATABASE student01_db OWNER student01;
   \c student01_db
   \i /shared_assets/datasets/setup_chap1.sql
   ```
4. Each student connects their lab PC client to `192.168.1.50:5432`, database `studentXX_db`.
5. **Optional Web Interface:** Install **CloudBeaver** (the web-based version of DBeaver) in a Docker container on the same Proxmox host. Students visit `http://proxmox-db.lab:8978` in their browser and immediately have a full DBeaver interface without downloading any software!

---

## Pedagogical Lab Delivery: Unit-by-Unit Infrastructure Playbook

Here is how each environment handles the specific curricular challenges across the 8-week schedule:

| Week & Topic | Curricular Demand | GitHub Codespaces Behavior | Proxmox Environment Behavior | Recommended Instructor Action |
| :---: | :--- | :--- | :--- | :--- |
| **Unit 1: Selection & Fundamentals** | System Catalog inspection (`information_schema`), `version()`, projection. | Fast launch; students inspect version 16. | Identical execution; students test local connection. | Emphasize client vs. server architecture (VS Code / DBeaver is the *client*; Postgres is the *server*). |
| **Unit 2: Targeted Retrieval & Logic** | Filtering, three-valued logic, `NULL` handling, `LIKE`/`ILIKE`. | Clean dataset filtering. | Clean dataset filtering. | Demonstrate string pattern matching performance in live demo. |
| **Unit 3: Relational Joins** | 4-table join on Superstore schema, anti-joins for dead inventory. | Multiple open editor tabs with ERD diagrams. | DBeaver ERD diagram generator is particularly visual here. | Have students view the Mermaid ERD in `database_schema_spec.md`. |
| **Unit 4: Summarization & Pivoting** | `GROUP BY`, `HAVING`, `CASE` cross-tab pivoting. | High-performance execution on small-to-mid datasets. | High-performance execution. | Teach students to run aggregations before formatting in application layers. |
| **Unit 5: Safe DML & Transactions** | `INSERT`, `UPDATE`, `DELETE`, `BEGIN`/`ROLLBACK`, temp tables. | **Crucial:** Private container guarantees students do not overwrite each other's data. | Private VM/LXC guarantees isolation. In Multi-Tenant, ensure private DB. | Teach the "Safety Checklist": Always run `SELECT` before `DELETE`, wrap in `BEGIN ... ROLLBACK`. |
| **Unit 6: CTEs & Window Functions** | Subqueries, `WITH` CTEs, `ROW_NUMBER()`, `PARTITION BY`. | Advanced query plans execute cleanly. | Advanced query plans execute cleanly. | Compare procedural loops with set-based window operations. |
| **Unit 7: Schema Design & DDL** | 3NF normalization, `CREATE TABLE`, constraints, `DROP TABLE`. | Students have full `CREATE/DROP` rights in their sandbox. | Students have full superuser rights in private container. | Teach `DROP TABLE IF EXISTS ... CASCADE` safely. |
| **Unit 8: Indexing & Capstone** | B-Tree indexing, `EXPLAIN ANALYZE`, buffer cache hits, capstone defense. | Containers show query plans and timing. Slight variance due to cloud virtualization. | **Gold Standard:** Bare-metal timing on Proxmox gives consistent execution costs. | Ideal place for a live classroom competition on query plan optimization! |

---

## Student Submission & Grading Workflow for the Instructor

Regardless of whether students run their queries on GitHub Codespaces or in your Proxmox lab, the submission standard must remain uniform and painless to grade:

### 1. Student Submission Standard
* Students save their final queries in a single script: `lab{N}_{student_lastname}.sql` (e.g., `lab1_smith.sql`).
* Require strict SQL style standards (as outlined in [`lab_rubric.md`](file:///workspaces/CMAP_1815_Autogen/units/unit_01_selection_and_fundamentals/assessments/lab_rubric.md)):
  * All SQL keywords in **UPPERCASE** (`SELECT`, `FROM`, `WHERE`).
  * Clauses on new lines.
  * Meaningful column aliases using `AS`.
  * No trailing commas.
* Students upload their `.sql` file directly to the corresponding Canvas Lab Assignment (configured for `.sql` file extensions).

### 2. Instructor Grading Methods in Canvas SpeedGrader
* **SpeedGrader Native Highlighting:** Canvas renders `.sql` files directly in SpeedGrader with monospace syntax highlighting.
* **The "One-Click Verification" Technique:**
  Keep your instructor Codespace or Proxmox terminal open. If you want to verify a student's questionable query:
  ```bash
  # In your instructor terminal:
  psql -d cmap1815
  -- Paste student query directly to test execution and row counts!
  ```
* **Rubric Grading:** Use the embedded 5-criteria Canvas rubric (40 pts Query Accuracy, 20 pts Formatting/Style, 20 pts Projection/Aliases, 10 pts Logic, 10 pts Catalog/Questions) to grade each lab in under 2 minutes.

---

## Final Recommendation & Next Steps for the Instructor

### Action Plan
1. **Adopt GitHub Codespaces as the Official Primary Platform:**
   * It provides 100% equity for students regardless of hardware (PC, Mac, Chromebook).
   * It natively supports the 50/50 hybrid split (in-class labs + asynchronous home study).
   * It trains students on modern Git/VS Code industry workflows.
2. **Update `.devcontainer/devcontainer.json`:**
   * Add the PostgreSQL 16 feature and auto-seeding script as detailed in Track 1 above.
3. **Build the Proxmox Lab Appliance as Secondary Infrastructure:**
   * If you prefer visual GUIs in the physical lab room, set up a **single Proxmox LXC with PostgreSQL 16 + CloudBeaver** (Option C) or individual LXC linked clones with **code-server** (Option B).
   * Use Proxmox for the **Unit 8 Capstone live defense** and as a zero-downtime safety net whenever campus internet is degraded.

---

### Related Course Specifications & Documents
* [Master Syllabus & 8-Week Hybrid Schedule](file:///workspaces/CMAP_1815_Autogen/course_specs/syllabus_master.md)
* [Database Schema Specification & ERD](file:///workspaces/CMAP_1815_Autogen/course_specs/database_schema_spec.md)
* [Unit 1 Lab Rubric & Scoring Criteria](file:///workspaces/CMAP_1815_Autogen/units/unit_01_selection_and_fundamentals/assessments/lab_rubric.md)
* [Legacy Proxmox Desktop Lab Draft](file:///workspaces/CMAP_1815_Autogen/legacy/github_source/archive/v1_original_drafts/units/proxmox_student_db_lab_guide.md)
* [Course Production Workflow & Canvas Integration](file:///workspaces/CMAP_1815_Autogen/docs/COURSE_PRODUCTION_WORKFLOW.md)
