# Unit 1: Micro-Lecture Video Scripts

This document contains recording scripts for **three bite-sized, topical micro-lectures** for Unit 1. Each video is structured to run **6 to 9 minutes**, focusing on a single conceptual pillar with clear visual cues and teleprompter-ready narration.

---

## Video 1.1: The Relational Metaphor & Why AI Needs Databases
* **Duration:** ~7 minutes
* **Target Audience:** First-time SQL learners / aspiring AI practitioners
* **Accompanying SQL File:** `part1_relational_foundations.sql`
* **On-Screen Assets:** Slide with Spreadsheet vs. Database comparison, Diagram of the "Filing Cabinet" Metaphor, Terminal showing `psql $DATABASE_URL`.

### Teleprompter & Delivery Script

**[0:00 - 1:15] The Hook: Spreadsheets Are Great... Until They Aren't**
> "Welcome to CMAP 1815. If you've worked with data before, chances are you've used Excel or Google Sheets. And for small jobs, spreadsheets are wonderful. But imagine you are managing student records for a university with 50,000 students. You have emergency contacts, GPA history, financial aid, and parking permits all jammed into one file.
> 
> What happens? The file takes two minutes to open. Scrolling lags. Someone accidentally sorts Column B without sorting Column C, and suddenly John Smith has Mary Johnson's social security number.
> 
> Even worse—in the age of Artificial Intelligence—Large Language Models like ChatGPT hallucinate when you hand them messy, unverified documents. To give an AI reliable memory, you must ground it in structured, verified data. That foundation is a **Relational Database**, and the language we use to speak to it is **SQL: Structured Query Language**."

**[1:16 - 3:30] The Filing Cabinet Metaphor**
> "Let's build a mental model that will stick with you for the rest of your career.
> 
> Imagine a massive, pitch-black warehouse. That warehouse is your **Database**.
> Inside that warehouse, there are hundreds of distinct filing cabinets. Each filing cabinet represents a **Table**—for example, a cabinet for `employees`, a cabinet for `products`, and a cabinet for `orders`.
> 
> Inside each cabinet, there are vertical drawers labeled with specific pieces of information: `first_name`, `hire_date`, `salary`. Those drawers are your **Columns** (or Attributes).
> 
> And inside each drawer, every individual paper folder containing one person's record is a **Row** (or Tuple).
> 
> The core rule of the relational model is simple: **One concept per cabinet.** We don't store an employee's home address, company laptop model, and quarterly dental insurance claims all in the same folder. We separate them cleanly and connect them using relational keys."

**[3:31 - 5:30] Client vs. Server Architecture: Where Does SQL Live?**
> "Here is a distinction that trips up beginners: SQL is not a program installed on your desktop. It is a communication protocol between two computers:
> 
> 1. **The Database Server:** This is the powerful engine running in the cloud or in a server room—in our case, a **PostgreSQL 16** server running inside your GitHub Codespace. It manages the files on the hard drive, enforces security, and executes calculations.
> 2. **The Client:** This is your tool—whether it's the `psql` command-line terminal, VS Code's SQLTools, or DBeaver. The client is just a telephone. You type your query into the client, the client sends that text over the wire to the server, the server processes the data, and sends back a tabular result set.
> 
> When you run a query, you aren't doing the math on your laptop. The database server does all the heavy lifting."

**[5:31 - 7:00] Summary & First Terminal Connection**
> "In this course, we use **GitHub Codespaces**. With one click, you have an entire Linux cloud environment running PostgreSQL 16 ready to go. No driver installation, no port forwarding headaches.
> 
> In our next bite-sized video, we are going to pick up our flashlight and learn the most important command in SQL: the `SELECT` statement. Let's dive in!"

---

## Video 1.2: Anatomy of a Query & The Projection Flashlight
* **Duration:** ~8 minutes
* **Target Audience:** Beginners learning query syntax
* **Accompanying SQL File:** `part2_anatomy_of_select.sql`
* **On-Screen Assets:** VS Code / Codespace split screen (Editor on top, Terminal/Results on bottom).

### Teleprompter & Delivery Script

**[0:00 - 1:30] The Flashlight Metaphor (Projection)**
> "Welcome back. In Video 1.1, we pictured our database as a pitch-black warehouse filled with filing cabinets.
> 
> Now, walk into that dark warehouse holding a flashlight. If you turn on the overhead stadium lights, you see 50,000 folders all at once. That's overwhelming.
> 
> Instead, you turn on your flashlight and point the beam directly at the drawer labeled `first_name`. Everything else remains in the dark.
> 
> In database theory, shining your flashlight on specific columns is called **Projection**. In SQL, the command that controls the flashlight is **`SELECT`**."

**[1:31 - 3:45] The Two Indispensable Clauses: SELECT and FROM**
> "Every data retrieval query requires two basic clauses:
> 
> ```sql
> SELECT first_name, last_name
> FROM employees;
> ```
> 
> Let's break down the grammar:
> 1. **`SELECT`** tells the database *WHAT* attributes you want to see.
> 2. **`FROM`** tells the database *WHERE* the filing cabinet is located.
> 
> Notice two critical syntax rules:
> * **Separating Columns:** We separate each column with a comma: `first_name, last_name`.
> * **The Trailing Comma Trap:** Never put a comma after the last column before `FROM`! If you write `SELECT first_name, last_name, FROM employees`, PostgreSQL looks for a third column that doesn't exist and immediately throws a syntax error.
> * **The Semicolon (;):** The semicolon is the period at the end of the SQL sentence. It tells PostgreSQL: *'I am done with my thought; now go execute it.'*"

**[3:46 - 5:30] The Asterisk (`*`): Scalpel vs. Sledgehammer**
> "[Demonstrating live in editor]:
> If I type:
> ```sql
> SELECT * FROM employees;
> ```
> The asterisk `*` means 'give me every single column in the table.'
> 
> This is great for an initial 5-second check when you first explore a new database. But in production, `SELECT *` is considered an anti-pattern. Why?
> 
> 1. **Network Overhead:** If a table has 80 columns and 5 million rows, pulling every column sends gigabytes of unnecessary data over the network.
> 2. **Security & Privacy:** You might inadvertently pull sensitive data like social security numbers, passwords, or salary details when you only needed an email address.
> 3. **Application Fragility:** If a DBA adds a new column tomorrow, an application expecting 4 columns will break.
> 
> Always be a surgeon, not a demolition crew. Name your columns explicitly!"

**[5:31 - 7:45] How the Database Reads: Order of Execution**
> "Here is a secret that separates amateurs from real database developers:
> You write queries in this order:
> 1. `SELECT`
> 2. `FROM`
> 
> But the PostgreSQL engine *executes* your query in this order:
> 1. `FROM`
> 2. `SELECT`
> 
> Think about it: the database engine can't possibly know what columns you're talking about until it first walks over to the table and opens the cabinet! Keeping this mental order in mind—`FROM` first, then `SELECT`—will make complex joins and filtering effortless later in the course.
> 
> In Video 1.3, we'll see how to make SQL do math for us, rename our headers, and sort our results with mathematical precision."

---

## Video 1.3: Expressions, Aliases & Sorting with Precision
* **Duration:** ~8 minutes
* **Target Audience:** Beginners learning data transformation and presentation
* **Accompanying SQL File:** `part3_projection_and_sorting.sql`
* **On-Screen Assets:** Live execution showing query results changing in real-time.

### Teleprompter & Delivery Script

**[0:00 - 2:00] Using the Database as a Calculator: Expressions**
> "Welcome to Video 1.3. A common misconception is that SQL can only retrieve raw data exactly as it was typed in. But SQL is also an extremely high-performance mathematical engine.
> 
> Look at our `employees` table. We have a column called `salary`. What if management wants to see everyone's salary after an across-the-board 5% raise?
> 
> We can write:
> ```sql
> SELECT first_name, salary, salary * 1.05
> FROM employees;
> ```
> PostgreSQL computes that multiplication row-by-row in nanoseconds across millions of records.
> 
> But look at the output header on your screen: the column is literally named `?column?` or `salary * 1.05`. That looks terrible in an executive report."

**[2:01 - 3:45] Column Aliases with `AS`**
> "To fix messy headers, we use **Column Aliasing** with the keyword **`AS`**:
> 
> ```sql
> SELECT 
>     first_name, 
>     salary, 
>     salary * 1.05 AS projected_salary
> FROM employees;
> ```
> 
> The `AS` keyword creates a clean, self-documenting virtual column in the output result set. Note: it does NOT change the table on disk! Remember, `SELECT` never alters data in the database; it only changes what is projected onto your screen.
> 
> You can also concatenate text strings using PostgreSQL's double pipe operator `||`:
> ```sql
> SELECT first_name || ' ' || last_name AS full_name
> FROM employees;
> ```
> Now we've merged two separate columns into a single polished full name!"

**[3:46 - 5:30] Removing Duplicates with `DISTINCT`**
> "Now let's look at `department`:
> ```sql
> SELECT department FROM employees;
> ```
> If we have 25 employees, we see 'Security' 6 times, 'Research' 5 times, and 'Operations' 4 times.
> 
> If an AI or human analyst wants to know: *'What are the unique departments in this company?'*, you add the keyword **`DISTINCT`** immediately after `SELECT`:
> ```sql
> SELECT DISTINCT department 
> FROM employees;
> ```
> The database engine de-duplicates the stream on the fly and returns a single clean list of distinct categories. This is fundamental for building dropdown menus, categories, and AI query grounding."

**[5:31 - 8:00] Sorting Your Output: `ORDER BY`**
> "By default, relational databases return data in no guaranteed order. If you need rows in a predictable sequence, you must declare it with **`ORDER BY`**:
> 
> ```sql
> SELECT first_name, last_name, salary
> FROM employees
> ORDER BY salary DESC;
> ```
> * **`ASC` (Ascending):** The default. Smallest to largest, A to Z.
> * **`DESC` (Descending):** Largest to smallest, Z to A (e.g. highest earners first).
> 
> And you can even multi-sort:
> ```sql
> SELECT department, last_name, salary
> FROM employees
> ORDER BY department ASC, salary DESC;
> ```
> This first groups rows alphabetically by department, and then within each department, sorts the employees from highest to lowest salary.
> 
> You now have the foundational toolkit: `SELECT`, `FROM`, `AS`, `DISTINCT`, and `ORDER BY`. Check out the accompanying SQL files in the workspace and let's get into the live lab exercises!"
