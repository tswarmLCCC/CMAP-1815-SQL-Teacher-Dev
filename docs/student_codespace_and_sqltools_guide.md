# Student Guide: Navigating GitHub Codespaces & SQLTools

Welcome to **CMAP 1815: Introduction to Modern SQL**! In this course, you will write and execute queries against a live, production-grade **PostgreSQL 16** relational database. 

To ensure everyone has an identical, high-performance environment with zero driver headaches or configuration errors, we use **GitHub Codespaces**. With one click, Codespaces provides a complete, cloud-hosted Linux workstation pre-loaded with PostgreSQL 16, VS Code, and the **SQLTools** database GUI.

This guide walks you through every step of navigating your Codespace, connecting to your database with SQLTools, running queries, using the command-line terminal (`psql`), and completing your weekly lab assignments.

---

## 1. Launching Your Personal Codespace

1. **Log in to GitHub** and navigate to your course/student repository (e.g., `student-test-1815` or `CMAP-1815-Student-Sandbox`).
2. Click the green **Code** button at the top right of the file listing.
3. Select the **Codespaces** tab.
4. Click **Create codespace on main** (or click your existing Codespace to resume it).
5. **Initial Setup:** The first time you launch your Codespace, it automatically provisions the Linux container, starts the PostgreSQL database, and installs the required database tools. This typically takes 1–2 minutes. Subsequent launches resume in just a few seconds.

> **Tip:** You can run Codespaces directly in any modern web browser (Chrome, Edge, Firefox, Safari) or open it inside your desktop Visual Studio Code application if you prefer.

---

## 2. Navigating the Codespace Interface

When your Codespace loads, you are looking at the Visual Studio Code web editor:

```
+-----------------------------------------------------------------------------------+
|  [Menu] [File] [Edit] [Selection] ...                           [Codespace Name]  |
+----+------------------------------------+-----------------------------------------+
|    | EXPLORER                           | EDITOR                                  |
| 📁 | v STUDENT-SANDBOX                  | sql/lab_solutions_annotated.sql         |
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
   - 📁 **Explorer (`Ctrl + Shift + E` / `Cmd + Shift + E`):** Browse folders, open scripts, create new files.
   - 🔍 **Search (`Ctrl + Shift + F` / `Cmd + Shift + F`):** Search for text across your entire workspace.
   - 🔀 **Source Control (`Ctrl + Shift + G`):** Commit and push your saved query files to GitHub.
   - 🗄️ **SQLTools Icon (Database Cylinder):** Open your database connections, browse tables, and inspect schemas.
   - ⚙️ **Settings (Bottom Left):** Manage color themes, hotkeys, and account settings.
2. **Editor Area (Center/Top):** Where you view, write, format, and execute SQL statements.
3. **Panel Area (Bottom):** Displays the **SQLTools Results** table, **Terminal** (`bash` command prompt), and **Ports** tab.
4. **Status Bar (Bottom Strip):** Shows your current git branch (`main`), active SQL connection, and notification status.

---

## 3. Using SQLTools (Your Visual Database GUI)

**SQLTools** is an integrated database client built directly into your Codespace. It functions just like desktop tools such as DBeaver or pgAdmin, allowing you to browse tables and run queries without leaving the browser.

### Connecting to Your Database:
1. Click the **SQLTools icon** (the stacked cylinder/database icon) in the far-left Activity Bar.
2. Under the **CONNECTIONS** panel, you will see your pre-configured connection:
   - Name: **`cmap1815`** (or **`mydb`**)
   - Driver: **PostgreSQL**
3. Click the connection name, or click the small **plug/connect icon** next to it.
4. Once connected, a green active status dot will appear next to the connection name!

### Exploring Tables & Columns:
1. In the SQLTools panel, expand your active connection &rarr; expand **`public`** (the default schema).
2. Expand **`Tables`**. You will see the core course tables:
   - `employees`
   - `locations`
   - `order_lines`
   - `orders`
   - `products`
3. Expand any table (e.g., `employees`) &rarr; **`Columns`** to see every column, its data type (`varchar`, `numeric`, `integer`), and primary key icons.
4. **Quick Preview:** Click the small table icon next to any table name to instantly open a 50-row preview in the results tab.

---

## 4. Writing & Executing Queries

### Running Queries in `.sql` Files:
1. Open any SQL file from the Explorer (or create your lab submission file, e.g. `lab1_yourname.sql`).
2. Type or paste your SQL statement. Always remember:
   - SQL keywords must be in **UPPERCASE** (`SELECT`, `FROM`, `WHERE`, `ORDER BY`).
   - Clauses belong on separate lines.
   - End each statement with a semicolon (`;`).
3. **Execute:** Place your blinking text cursor inside the query you want to run.
4. Press:
   - **`Ctrl + Enter`** (Windows / Linux / Chromebook)
   - **`Cmd + Enter`** (Mac)
   *(Or click the floating **"Run on active connection"** link that appears right above the statement).*

```sql
SELECT product_name, category, retail_price
FROM products
WHERE retail_price > 100.00
ORDER BY retail_price DESC;
```

### Inspecting Results in the SQLTools Results Panel:
- A new panel titled **`SQLTools Results`** will automatically open at the bottom or side of your screen.
- You will see:
  - Exact column names and types.
  - Total number of rows returned (e.g. `7 records`).
  - Execution time (in milliseconds).
- **Interactive features:** Click any column header to sort ascending or descending, use the search box to find specific text within the results, or click the copy icon to copy rows to your clipboard.

---

## 5. Using the Integrated Terminal (`psql`)

In addition to the visual SQLTools GUI, you have full access to the official PostgreSQL command-line tool: **`psql`**. Learning `psql` is an essential professional skill for database administrators and data engineers.

### Opening the Terminal:
- Press **`Ctrl + \``** (Backtick, key above Tab) or go to the top menu: **Terminal &rarr; New Terminal**.

### Starting an Interactive `psql` Session:
At the bash prompt, type:
```bash
psql -U postgres -d cmap1815
```
*(If prompted or using the default database, `psql -U postgres` also connects).*

You are now at the interactive `cmap1815=#` prompt!

### Essential `psql` Meta-Commands (The Cheat Sheet):
Every `psql` meta-command starts with a backslash (`\`):

| Command | Action | Description |
| :--- | :--- | :--- |
| **`\l`** | List Databases | Shows all databases on the PostgreSQL server. |
| **`\c <dbname>`** | Connect | Switch to a different database (e.g., `\c cmap1815`). |
| **`\dt`** | List Tables | Lists all base tables in the current schema. |
| **`\d <table_name>`** | Describe Table | Shows full column definitions, data types, nullability, and constraints (e.g., `\d employees`). |
| **`\x`** | Expanded Display | Toggles expanded mode (pivots rows vertically—great for wide tables). |
| **`\?`** | Help | Shows all available `psql` slash commands. |
| **`\q`** | Quit | Exits `psql` and returns you to the regular terminal prompt. |

### Running an Entire Script File from Terminal:
You can execute an entire SQL file at once using the `-f` flag:
```bash
psql -U postgres -d cmap1815 -f sql/setup_chap1.sql
```

---

## 6. Recommended Lab Workflow (Step-by-Step)

Follow this 6-step workflow for every weekly lab assignment:

1. **Review the Assignment:** Open the weekly unit module in Canvas and read the **Applied SQL Lab Guide**.
2. **Create Your Solution File:** In your Codespace Explorer, right-click inside the `sql/` directory (or workspace root), select **New File**, and name it:
   ```text
   lab1_first_last.sql
   ```
3. **Author Your Queries:** Write each challenge query one by one. Include comment headers identifying the challenge:
   ```sql
   -- Challenge 1: Staff Directory
   SELECT first_name, last_name, title
   FROM employees
   ORDER BY last_name ASC;
   ```
4. **Execute & Self-Check:** Run the query (`Ctrl + Enter`). Compare your live output against the **Lab Solutions Walkthrough** (`sql/lab_solutions_annotated.sql`):
   - Did your query return the expected number of rows?
   - Are your column aliases formatted in `snake_case`?
   - Did you check for unexpected `NULL` behavior?
5. **Save Your Work:** Press `Ctrl + S` (`Cmd + S` on Mac).
6. **Submit to Canvas:**
   - **Method A (File Upload):** In the Explorer, right-click `lab1_first_last.sql` &rarr; click **Download...** &rarr; upload the downloaded `.sql` file to the Canvas Lab Assignment.
   - **Method B (GitHub Source Control):** Open the Source Control tab (`Ctrl + Shift + G`), type a commit message (e.g. `"Complete Unit 1 Lab"`), click **Commit**, and click **Sync Changes** to push directly to your repository!

---

## 7. Troubleshooting & FAQ

### Q: "SQLTools says 'Connection Refused' or fails to connect."
- PostgreSQL runs as a background service inside your container. If it temporarily stops, open the terminal (`Ctrl + \``) and run:
  ```bash
  sudo service postgresql status
  ```
- If it reports stopped, start it with:
  ```bash
  sudo service postgresql start
  ```
- Then click the reconnect icon in SQLTools.

### Q: "I accidentally deleted or modified data during an experiment. How do I reset?"
- You can reset your database to its original, pristine state in 2 seconds! Run:
  ```bash
  psql -U postgres -d cmap1815 -f sql/setup_chap1.sql
  ```
- This drops all tables and re-seeds them with clean data.

### Q: "My Codespace timed out and shut down."
- To save cloud resources, GitHub Codespaces automatically suspends instances after 30 minutes of inactivity.
- **Don't worry:** All of your saved files, queries, and git commits are completely safe on the persistent cloud drive.
- Simply click **Restart Codespace** or refresh your browser tab to pick up right where you left off.

### Q: "Can I use DBeaver on my local laptop instead of the browser?"
- Yes! Open your Codespace in VS Code Desktop. In the **Ports** tab, port `5432` is automatically forwarded to `localhost:5432`. You can connect your local DBeaver, TablePlus, or pgAdmin directly to `Host: localhost`, `Port: 5432`, `User: postgres`, `Password: password123`!
