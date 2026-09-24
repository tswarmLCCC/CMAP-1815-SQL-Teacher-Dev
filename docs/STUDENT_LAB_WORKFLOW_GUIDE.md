# CMAP 1815: Student Guide — How to Complete & Submit Weekly SQL Labs

**Course:** CMAP 1815: Introduction to Modern SQL  
**Audience:** Students  
**Environment:** Cloud PostgreSQL 16 Sandbox (GitHub Codespaces + Dev Containers)  
**Student Sandbox Repository:** [tswarmLCCC/CMAP-1815-Student-Sandbox](https://github.com/tswarmLCCC/CMAP-1815-Student-Sandbox)

---

## 🚀 1-Click Quick Start (GitHub Codespaces)

In this course, you will write and execute queries against a live, industry-standard **PostgreSQL 16** server running directly in your browser. You do **not** need to install PostgreSQL, configure local system services, or open firewall ports on your computer.

Click the badge below to spin up your personal, cloud-hosted lab sandbox:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tswarmLCCC/CMAP-1815-Student-Sandbox?quickstart=1)

### What Happens on First Launch:
1. GitHub provisions a private Ubuntu Linux container with PostgreSQL 16 and VS Code Web.
2. The initial build takes approximately **60–90 seconds**.
3. Once the integrated terminal displays:
   ```text
   ======================================================================
     CMAP 1815: Modern SQL Student Sandbox Ready!
     • Terminal: type 'psql' to open the interactive SQL shell.
     • Visual GUI: click the Database icon on the left sidebar (SQLTools).
   ======================================================================
   ```
   your database is live, running, and pre-seeded with all course tables!

> [!TIP]
> **Maximize Your Free GitHub Hours:**  
> GitHub free personal accounts receive 60 free core-hours per month. Claim your free **[GitHub Student Developer Pack](https://education.github.com/pack)** with your LCCC `.edu` email to upgrade to **180 free core-hours per month**!  
> To prevent burning hours in the background:
> 1. Set your Codespace idle timeout to **15 minutes** in your personal GitHub settings (**Settings → Codespaces → Default idle timeout → 15 minutes**).
> 2. Always close your browser tab when you finish your study session; GitHub automatically pauses your container.

---

## 🛠️ Two Ways to Query Your PostgreSQL Database

### Option A: The Visual GUI (SQLTools Sidebar) — *Best for Exploring Tables*
1. Click the **Database (plug/server) icon** on the far-left sidebar of VS Code.
2. Under **CONNECTIONS**, click **CMAP 1815 Local PostgreSQL** $\rightarrow$ **Connect**.
3. Expand **cmap1815** $\rightarrow$ **public** $\rightarrow$ **Tables** to see your live tables:
   * `employees`: 50 corporate personnel records
   * `locations`: 10 corporate office branches
   * `products`: 20 retail inventory items
   * `orders`: 100 customer transaction headers
   * `order_lines`: 250 individual line items
4. Click any table name to inspect its column names, data types, and primary keys.
5. Click **Show Table Records** to view table rows in an interactive spreadsheet grid!

### Option B: The Terminal CLI (`psql`) — *Best for Fast Query Testing*
1. Open the integrated terminal in VS Code (`Ctrl + ~` on Windows/Linux or `Cmd + ~` on Mac).
2. Simply type:
   ```bash
   psql
   ```
3. You are now inside the PostgreSQL interactive shell connected to `cmap1815`. Run any query:
   ```sql
   SELECT first_name, last_name, salary FROM employees LIMIT 5;
   ```
4. To exit back to the Linux terminal prompt, type:
   ```text
   \q
   ```

---

## 📝 The 5-Step Weekly Lab Submission Workflow

Follow this uniform recipe for all weekly labs across Units 1 through 8:

```
Weekly Lab Submission Workflow:
├── 1. Open Unit Folder (units/unit_0X_...)
├── 2. Review Challenges (lab_guide.md or Canvas)
├── 3. Open Starter Template (labX_starter.sql)
├── 4. Write & Test Queries in PostgreSQL (SQLTools or psql)
└── 5. Save as labX_yourlastname.sql & Upload to Canvas Assignment
```

### Step 1: Open the Unit Folder
In the VS Code file explorer (left panel), expand the folder for the current week (e.g. `units/unit_01_selection_and_fundamentals/`).

### Step 2: Review the Challenges
Open `lab_guide.md` in the unit folder (or open the **Applied SQL Lab Guide** page in your Canvas module) to review the business scenario, challenge questions, and point values.

### Step 3: Open Your Starter Template
Open `lab{N}_starter.sql` (e.g. `lab1_starter.sql`). This file contains:
* Pre-formatted submission header (fill in your name and date).
* A connection test query (`SELECT version(), current_database(), current_user;`).
* Clean comment sections for Challenge 1, Challenge 2, etc.

### Step 4: Write & Verify Every Query
Write your SQL statement directly beneath each challenge comment block.
> [!IMPORTANT]
> **The Golden Rule of CMAP 1815:**  
> Never turn in code you haven't executed! Copy or run each query against your live PostgreSQL database to guarantee **zero syntax errors** before submitting.

### Step 5: Save & Submit to Canvas
1. Save your completed file with your last name: `lab{N}_{yourlastname}.sql` (e.g., `lab1_smith.sql`).
2. Navigate to Canvas, open the weekly **Applied SQL Lab Assignment**, and upload your `.sql` file.

---

## 📐 LCCC SQL Style & Grading Standards

All lab submissions are evaluated using the standard Canvas rubric (50 points total):

| Criterion | Points | Standard |
| :--- | :---: | :--- |
| **Query Accuracy & Execution** | **20 pts** | Queries execute with zero syntax errors and produce exact expected row counts. |
| **Relational Logic & Predicates** | **10 pts** | Accurate filters (`WHERE`), joins (`ON`), aggregations (`GROUP BY`), or set logic. |
| **Projection & Aliasing** | **10 pts** | Projections match prompt; computed expressions are aliased using meaningful `snake_case`. |
| **SQL Formatting & Style** | **10 pts** | SQL keywords in **UPPERCASE** (`SELECT`, `FROM`, `WHERE`); clauses start on new lines. |

### Example of Clean, Full-Credit SQL Formatting:
```sql
-- Challenge 1: Find high-earning employees in Engineering
SELECT
    first_name,
    last_name,
    salary,
    salary * 1.10 AS projected_salary
FROM
    employees
WHERE
    department = 'Engineering'
    AND salary >= 80000
ORDER BY
    salary DESC;
```

---

## 🔄 Disaster Recovery: Screwed Up Your Data? (`./reset_database.sh`)

In **Unit 5 (Safe DML)** and **Unit 7 (Schema Design)**, you will write real data modification and schema statements (`INSERT`, `UPDATE`, `DELETE`, `CREATE TABLE`, `DROP TABLE`).

If you accidentally delete all records, alter the wrong column, or drop a core table:
1. Open your VS Code terminal (`Ctrl + ~` / `Cmd + ~`).
2. Run the reset script:
   ```bash
   ./reset_database.sh
   ```
3. In **under 2 seconds**, your database schema and all 5 tables will be dropped and recreated back to pristine week 1 state!
4. **Safety Guarantee:** This script resets only the database tables. It **does NOT delete or touch** any of your `.sql` query files in `units/`.

---

## 🆘 Troubleshooting Quick Reference

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `psql: error: connection to server on socket failed` | PostgreSQL service stopped | Run: `sudo service postgresql start` |
| `fatal: password authentication failed for user vscode` | Role configuration glitch | Run: `./reset_database.sh` |
| Table `employees` does not exist | Dropped table or missed seed | Run: `./reset_database.sh` |
| SQLTools displays "Connection error" | Extension lost socket connection | In SQLTools panel, right-click **CMAP 1815 Local PostgreSQL** $\rightarrow$ **Disconnect**, then click **Connect** |
| Codespace running slowly | Browser tab cached or high RAM | In browser, press `Ctrl + Shift + R` / `Cmd + Shift + R` to reload window |
