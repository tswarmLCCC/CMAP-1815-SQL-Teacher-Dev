# Student Guide: Configuring and Using SQLTools in GitHub Codespaces

This guide provides instructions for configuring the GitHub Codespaces environment for database access. It covers establishing connections to the class database, executing specific queries, and adjusting the workspace layout for optimal use.

---

## 1. Connecting a File to the Database (cmap1815)

To execute queries successfully, the active `.sql` file must be connected to the target database. Connection errors typically indicate that the current file is detached.

**Instructions:**
1. Open the `.sql` file in the Codespaces editor.
2. Locate the status bar at the bottom right of the screen. 
3. Identify the **SQLTools** section. If the status reads "Detached" or prompts for a connection, click the text.
4. Select **`cmap1815`** from the drop-down menu that appears at the top center of the screen.

**Alternative Method:**
If the status bar is not visible, open the Command Palette (`Ctrl + Shift + P` on Windows/Linux, `Cmd + Shift + P` on Mac), type **`SQLTools: Select Connection`**, and select **`cmap1815`**.

---

## 2. Executing Specific SQL Queries

By default, executing a file may run all queries contained within it. To run individual queries, you must specify the lines to execute. 

*Note: The standard `Ctrl + R` shortcut is intercepted by GitHub Codespaces to open recent workspaces and will not execute SQL code in this environment.*

**Execution Methods:**
* **Keyboard Shortcut:** Highlight the specific lines of code to execute. Press **`Ctrl + E`**, and then press **`Ctrl + E`** a second time. (Mac: `Cmd + E`, `Cmd + E`).
* **Context Menu:** Highlight the specific lines of code, right-click the selected text, and choose **Run Selected Query** from the context menu.

---

## 3. Adjusting the Workspace Layout

SQLTools defaults to opening query results on the right side of the screen, which can compress the code editor horizontally. Moving the results pane to the bottom of the screen provides better visibility for wide data tables.

**Instructions:**
1. Click and hold the tab for the results window at the top of the editor pane.
2. Drag the cursor straight down toward the bottom-center of the editor space.
3. Release the mouse when a highlighted box appears covering the bottom half of the screen. Codespaces will typically retain this layout preference for future sessions.

---

## 4. Coding Efficiency Features

The following built-in features can assist with code formatting and syntax.

### Auto-Formatting Code
SQLTools includes a formatting feature to standardize indentation and capitalization.
* Highlight the SQL code to format.
* Right-click the selected text and choose **Format Selection**. 

### Using Auto-Complete
The auto-complete feature provides suggestions for table and column names directly from the connected database.
* Begin typing a table or column name.
* Press **`Ctrl + Space`** (Mac: `Cmd + Space`) to open the list of database suggestions.
* Use the arrow keys to navigate the list and press **`Enter`** to make a selection.