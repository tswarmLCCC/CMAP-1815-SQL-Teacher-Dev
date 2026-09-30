# Student Guide: Navigating GitHub Codespaces & SQLTools

Welcome to **CMAP 1815: Introduction to Modern SQL**! In this course, you will write and execute queries against a live, production-grade **PostgreSQL 16** relational database. 

To ensure everyone has an identical, high-performance environment with zero driver headaches or configuration errors, we use **GitHub Codespaces**. With one click, Codespaces provides a complete, cloud-hosted Linux workstation pre-loaded with PostgreSQL 16, VS Code, and the **SQLTools** database GUI.

This guide walks you through every step of spawning your personal repository from the course template, navigating your Codespace, connecting to your database with SQLTools, running queries, saving outputs, using the command-line terminal (`psql`), managing your cloud hours, and submitting your weekly lab assignments.

---

## 1. Initial Setup: Spawning Your Personal Student Repository

Before launching Codespaces, you must create your own copy of the course template repository:

1. **Navigate to the Template Repository:** Open [github.com/tswarmLCCC/CMAP-1815-Student-Sandbox](https://github.com/tswarmLCCC/CMAP-1815-Student-Sandbox) in your browser.
2. **Click "Use this template":** Located at the top right of the repository page, click the green **Use this template** button &rarr; select **Create a new repository**.
3. **Configure Your Personal Repository:**
   - **Repository name:** e.g., `CMAP-1815-Student-Sandbox` (or `CMAP-1815-YourLastName`).
   - **Visibility:** Set to **Private** (recommended for coursework) or Public.
   - Click **Create repository**.
4. **You now own your repository!** The URL in your address bar will now be `github.com/YOUR_USERNAME/CMAP-1815-Student-Sandbox`.

> [!CAUTION]
> **CRITICAL WARNING — ALWAYS WORK IN YOUR OWN REPOSITORY:**  
> Never launch Codespaces from the base instructor template (`tswarmLCCC/CMAP-1815-Student-Sandbox`). You do not have push permissions on the instructor template. If you work in the template repo, you will NOT be able to push your commits, and your work will be permanently lost when the temporary container shuts down! Always verify the repository URL has your GitHub username before launching!

---

## 2. Launching & Resuming Your Codespace

### First-Time Launch:
1. In **your personal repository**, click the green **Code** button at the top right.
2. Select the **Codespaces** tab.
3. Click **Create codespace on main**.
4. GitHub will provision your container, start PostgreSQL 16, and load sample datasets. This initial setup takes about 90 seconds. Once the terminal prints `CMAP 1815: Modern SQL Student Sandbox Ready!`, your database is live!

### Resuming Work in Future Sessions:
When you return to work on assignments later in the week, do **NOT** create a brand new Codespace every time:
1. Return to **your personal repository** on GitHub.
2. Click **Code** &rarr; **Codespaces** tab &rarr; click on your **existing Codespace** (it will say "Stopped").
3. Alternatively, visit [github.com/codespaces](https://github.com/codespaces) to see and resume all your active or stopped environments.
4. Resuming an existing Codespace takes only 10–15 seconds and preserves your open files and terminal history!

---

## 3. Codespace Lifecycle: Conserving Cloud Hours & Preventing Runaway

### Monthly Free Hours:
* Every free personal GitHub account receives **60 free core-hours per month**.
* **Upgrade to 180 Hours for Free:** Claim the **[GitHub Student Developer Pack](https://education.github.com/pack)** using your college `.edu` email address to receive **180 free core-hours per month**!

### Automatic 30-Minute Idle Shutdown:
* Codespaces automatically suspends itself after **30 minutes of inactivity**. If you step away from your computer, your hours will not run away indefinitely.
* When you return to a suspended tab, click **Restart Codespace** or refresh the browser to pick up right where you left off.

### Stopping Manually When Finished:
When you finish a study session or lab, cleanly stop your Codespace to conserve hours:
1. In VS Code, open the Command Palette (`Ctrl + Shift + P` on Windows/Linux or `Cmd + Shift + P` on Mac).
2. Type `Codespaces: Stop Current Codespace` and press Enter.
3. Or close the browser tab.

### Data Retention & Git Safety:
* Stopped codespaces are retained by GitHub for **30 days** before being scheduled for cleanup.
* **The Golden Safety Rule:** Always commit and push your completed SQL scripts to your GitHub repository (`git add .`, `git commit -m "Finish lab 1"`, `git push`). Once pushed to GitHub, your code is permanently safe on your repository page regardless of container lifecycle!

---

## 4. Navigating the Codespace Interface

```
+-----------------------------------------------------------------------------------+
|  [Menu] [File] [Edit] [Selection] ...                           [Codespace Name]  |
+----+------------------------------------+-----------------------------------------+
|    | EXPLORER                           | EDITOR                                  |
| 📁 | v STUDENT-SANDBOX                  | units/unit_01_.../lab1_starter.sql      |
|    |   > .devcontainer                  | --------------------------------------- |
| 🔍 |   > docs                           | 1  SELECT product_name, retail_price    |
|    |   v sql                            | 2  FROM products                        |
| 🔀 |     setup_chap1.sql                | 3  ORDER BY retail_price DESC;          |
|    |     lab_solutions_annotated.sql    |                                         |
| 🗄️ |     week1_orientation.sql          |                                         |
|    |                                    +-----------------------------------------+
| ⚙️ |                                    | SQLTOOLS RESULTS / TERMINAL             |
|    |                                    | [Results Tab] [Terminal: bash] [Ports]  |
+----+------------------------------------+-----------------------------------------+
| 🚀 main*  [0 ⚠️  0 ❌]                     | UTF-8   PostgreSQL   Spaces: 2   Port: 5432 |
+-----------------------------------------------------------------------------------+
```

### Key Interface Sections:
1. **Activity Bar (Far Left):**
   - 📁 **Explorer (`Ctrl + Shift + E` / `Cmd + Shift + E`):** Browse directories, open scripts, create new files.
   - 🔍 **Search (`Ctrl + Shift + F` / `Cmd + Shift + F`):** Search for text across your entire repository.
   - 🔀 **Source Control (`Ctrl + Shift + G`):** Commit and push your saved query files to GitHub.
   - 🗄️ **SQLTools Icon (Database Cylinder):** Open your database connections, browse tables, and inspect schemas.
   - ⚙️ **Settings (Bottom Left):** Manage color themes, hotkeys, and account settings.
2. **Editor Area (Center/Top):** Where you view, write, format, and execute SQL statements.
3. **Panel Area (Bottom):** Displays the **SQLTools Results** table, **Terminal** (`bash` command prompt), and **Ports** tab.
4. **Status Bar (Bottom Strip):** Shows your active branch (`main`), active SQL connection, and database port `5432`.

---

## 5. Using SQLTools (Your Visual Database GUI)

**SQLTools** is an integrated database client built directly into your Codespace. It functions just like desktop tools such as DBeaver or pgAdmin, allowing you to browse tables and run queries without leaving the browser.

### Connecting to Your Database:
1. Click the **SQLTools icon** (the stacked cylinder/database icon) in the far-left Activity Bar.
2. Under the **CONNECTIONS** panel, click **cmap1815** (or **mydb**) &rarr; click **Connect**.
3. Once connected, a green active status indicator will appear next to the connection name!

### Exploring Tables & Columns:
1. In SQLTools, expand your active connection &rarr; expand **`public`** (the default schema).
2. Expand **`Tables`**. You will see the five course tables:
   - `employees`
   - `locations`
   - `order_lines`
   - `orders`
   - `products`
3. Expand any table (e.g., `employees`) &rarr; **`Columns`** to inspect every column name, data type (`varchar`, `numeric`, `integer`), and primary key.
4. **Quick Preview:** Click the small table icon next to any table name to instantly open a 50-row preview in the results tab.

---

## 6. Writing, Executing & Saving Queries

### Running Queries in `.sql` Files:
1. Open any SQL file (e.g. `units/unit_01_selection_and_fundamentals/lab1_starter.sql` or your own `lab1_yourlastname.sql`).
2. Type or paste your SQL statement. Always follow standard formatting:
   - SQL keywords in **UPPERCASE** (`SELECT`, `FROM`, `WHERE`, `ORDER BY`, `AS`).
   - Major clauses on separate lines.
   - Terminating semicolon (`;`) at the end of each statement.
3. **Execute:** Place your text cursor inside the query you want to run.
4. Press:
   - **`Ctrl + Enter`** (Windows / Linux / Chromebook)
   - **`Cmd + Enter`** (Mac)
   *(Or click the floating **"Run on active connection"** link that appears right above the statement).*

### Saving & Exporting Query Output from SQLTools GUI:
When a query executes, the **SQLTools Results** tab opens at the bottom:
* **Exporting to CSV or JSON:** In the top-right toolbar of the Results panel, click **Export Results** (or the download icon) and select **Save as CSV** or **Save as JSON**. You can save this file directly into your workspace to document your outputs.
* **Copying Results to Clipboard:** Click **Copy All** or click and drag across rows, then right-click &rarr; **Copy** to paste tabular results directly into homework submissions or Canvas discussion posts.

---

## 7. Using the Integrated Terminal (`psql`) & Capturing Output

In addition to the visual SQLTools GUI, you have full access to the official PostgreSQL command-line tool: **`psql`**.

### Opening the Terminal:
* Press **`Ctrl + \``** (Backtick, key above Tab) or go to top menu: **Terminal &rarr; New Terminal**.

### Starting an Interactive `psql` Session:
At the bash prompt, type:
```bash
psql -U postgres -d cmap1815
```
*(Or simply type `psql` if environment variables are active).*

You are now at the interactive `cmap1815=#` prompt!

### Essential `psql` Meta-Commands:
Every `psql` meta-command starts with a backslash (`\`):

| Command | Action | Description |
| :--- | :--- | :--- |
| **`\l`** | List Databases | Shows all databases on the PostgreSQL server. |
| **`\c <dbname>`** | Connect | Switch to a different database (e.g., `\c cmap1815`). |
| **`\dt`** | List Tables | Lists all base tables in the public schema. |
| **`\d <table_name>`** | Describe Table | Shows full column definitions, data types, and constraints (e.g., `\d employees`). |
| **`\x`** | Expanded Display | Toggles expanded mode (pivots rows vertically—great for wide tables). |
| **`\?`** | Help | Shows all available `psql` slash commands. |
| **`\q`** | Quit | Exits `psql` and returns you to the bash shell. |

### Saving Query Outputs from the Terminal:
There are two professional techniques to save output from the terminal:

1. **Method 1: The `\o` Output Command inside `psql`:**
   Inside an interactive `psql` session, direct all subsequent query output to a text file:
   ```sql
   -- Direct output to a file named lab1_output.txt
   \o lab1_output.txt

   -- Run your query (results will be written to the file instead of the screen)
   SELECT product_name, retail_price FROM products ORDER BY retail_price DESC;

   -- Turn off file redirection and return output to screen
   \o
   ```
2. **Method 2: Command-Line Shell Redirection (`>`):**
   From the bash terminal (outside `psql`), execute a query and redirect stdout into a file:
   ```bash
   psql -U postgres -d cmap1815 -c "SELECT * FROM employees;" > employees_export.txt
   ```
   This generates `employees_export.txt` right in your workspace.

---

## 8. Recommended Weekly Lab Workflow

Follow this 5-step workflow for every weekly lab assignment:

1. **Review Assignment & Rubric:** Open Canvas and review the weekly **Applied SQL Lab Guide** and 100-point rubric.
2. **Open the Starter Template:** In your Codespace Explorer, open `units/unit_{XX}_.../lab{N}_starter.sql` (e.g., `units/unit_01_selection_and_fundamentals/lab1_starter.sql`).
3. **Write & Verify Queries:** Write your query solution beneath each challenge block. Test every query with `Ctrl + Enter` to verify zero syntax errors.
4. **Save Your Script:** Save the file as `lab{N}_yourlastname.sql` (e.g., `lab1_smith.sql`) using `Ctrl + S`.
5. **Commit, Push & Submit to Canvas:**
   - In terminal, commit and push your work to your personal GitHub repository:
     ```bash
     git add .
     git commit -m "Complete Unit 1 Lab"
     git push origin main
     ```
   - Right-click `lab1_smith.sql` in the Explorer &rarr; select **Download...** &rarr; upload the `.sql` script file to the weekly Canvas Lab Assignment for SpeedGrader evaluation!

---

## 9. Troubleshooting & FAQ

### Q: "SQLTools says 'Connection Refused' or fails to connect."
PostgreSQL runs as a background service inside your container. If it temporarily stops, open the terminal (`Ctrl + \``) and run:
```bash
sudo service postgresql status
```
If it reports stopped, start it with:
```bash
sudo service postgresql start
```
Then reconnect in SQLTools.

### Q: "I accidentally deleted or modified data during an experiment. How do I reset?"
You can reset your database to its original, pristine state in 2 seconds:
```bash
./reset_database.sh
```
*(Or run `psql -U postgres -d cmap1815 -f sql/setup_chap1.sql`)*.  
This script drops all tables and re-seeds them with clean sample data. **It will NOT touch or delete your saved `.sql` query files in your `units/` folder.**
