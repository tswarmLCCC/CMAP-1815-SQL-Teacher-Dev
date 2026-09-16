# The Proxmox Student Database Lab
**An End-to-End Guide for Building a Linux Desktop & PostgreSQL Environment**

This guide outlines how to build an all-in-one database sandbox for students using Proxmox VE. We will provision a full Virtual Machine (VM) with a graphical desktop, install PostgreSQL 17, configure network access, and set up DBeaver as the primary Graphical User Interface (GUI) for executing SQL scripts.

---

## Part 1: Understanding the Environment
Before we build, it is important to understand the technology stack:

*   **Proxmox VE (Type 1 Hypervisor):** This is the operating system installed directly on the server's bare metal. It manages the hardware (CPU, RAM, Storage) and allocates it to virtual machines.
*   **Virtual Machine (KVM/QEMU):** Unlike lightweight containers (LXC) that share the host's kernel and lack a graphical interface, a VM acts as a completely independent computer. We are using a VM so we can install a full Linux Desktop (like Ubuntu or Linux Mint) that students can interact with visually.
*   **PostgreSQL:** The relational database management system running in the background.
*   **DBeaver:** The visual database client students will use to write queries, replacing the need for Microsoft SQL Server Management Studio (SSMS).

---

## Part 2: Creating the Desktop Virtual Machine
Since students need a graphical desktop, we must start with an ISO file rather than a container template.

1.  **Download a Desktop ISO:** Download a Linux desktop ISO (e.g., Ubuntu Desktop or Linux Mint) to your local computer.
2.  **Upload to Proxmox:** In the Proxmox web interface, select your `local` storage drive on the left, click **ISO Images**, and upload the file.
3.  **Create the VM:** Click **Create VM** in the top right corner.
    *   **OS:** Select the ISO file you just uploaded.
    *   **System:** Leave as default.
    *   **Disks:** Allocate at least 25GB to accommodate the desktop environment and database.
    *   **CPU:** Assign 2 to 4 cores.
    *   **Memory:** Allocate 4096 MB (4GB) to ensure the graphical desktop runs smoothly.
    *   **Network:** Leave as default (bridged).
4.  **Install the OS:** Start the VM, open the **Console**, and click through the standard Linux desktop installation wizard.

---

## Part 3: Installing PostgreSQL 17
Once the Linux desktop is installed and you are logged in, open the Terminal application to install the database engine.

1.  **Update Package Lists:** Ensure the system is up to date.
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
2.  **Install PostgreSQL:** Download the core server and contribution tools.
    ```bash
    sudo apt install postgresql postgresql-contrib -y
    ```
3.  **Verify Installation:** Check that version 17 is running.
    ```bash
    psql --version
    ```

---

## Part 4: Configuring Network and Authentication
Even though students will use DBeaver on the exact same machine, configuring network access is a crucial learning step for database administration.

1.  **Enable Network Listening:** Open the main configuration file.
    ```bash
    sudo nano /etc/postgresql/17/main/postgresql.conf
    ```
    Find `#listen_addresses = 'localhost'`, remove the `#`, and change it to listen to all interfaces:
    ```text
    listen_addresses = '*'
    ```
    Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

2.  **Authorize Connections:** Open the host-based authentication file.
    ```bash
    sudo nano /etc/postgresql/17/main/pg_hba.conf
    ```
    Scroll to the bottom. Add a rule to allow connections from the local machine and network (replace `192.168.1.0/24` with your classroom subnet if you want external access):
    ```text
    host    all             all             127.0.0.1/32            scram-sha-256
    host    all             all             192.168.1.0/24          scram-sha-256
    ```
    Save and exit.

3.  **Restart the Service:** Apply the networking changes.
    ```bash
    sudo systemctl restart postgresql
    ```

---

## Part 5: Setting Up Database Users
We need to set a password for the default `postgres` administrator and optionally create a specific student user.

1.  **Open the SQL Prompt:**
    ```bash
    sudo su - postgres
    psql
    ```
2.  **Set the Admin Password:**
    ```sql
    \password postgres
    ```
    *(Type the new password, press Enter, and confirm).*
3.  **Create a Student User (Optional but Recommended):**
    ```sql
    CREATE USER student WITH PASSWORD 'student123' SUPERUSER;
    ```
4.  **Exit:**
    ```sql
    \q
    exit
    ```

---

## Part 6: Installing and Connecting DBeaver
With the database running in the background of the VM, we now install the graphical client.

1.  **Install DBeaver:** Open the Terminal and install DBeaver using Snap (which is pre-installed on Ubuntu).
    ```bash
    sudo snap install dbeaver-ce
    ```
2.  **Launch DBeaver:** Open the application from the Linux desktop menu.
3.  **Create a Connection:** 
    *   Click the **New Database Connection** plug icon.
    *   Select **PostgreSQL**.
    *   **Host:** `localhost` (since DBeaver and Postgres are on the same VM).
    *   **Port:** `5432`
    *   **Database:** `postgres`
    *   **Username:** `student` (or `postgres`)
    *   **Password:** The password you set in Part 5.
    *   Click **Test Connection**, then **Finish**.

---

## Part 7: The Student Starter Script
Students can now open a new SQL Editor tab in DBeaver and use the following script to learn the fundamentals of table creation, data manipulation, and querying.

```sql
/* ============================================================================
   POSTGRESQL BEGINNER STARTER SCRIPT
   ----------------------------------------------------------------------------
   How to use: Highlight each section block-by-block and execute it.
   ============================================================================ */

-- Clean up previous runs
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

/* ----------------------------------------------------------------------------
   SECTION 1: CREATING TABLES (DDL)
   ---------------------------------------------------------------------------- */
CREATE TABLE students (
    student_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    is_active  BOOLEAN DEFAULT TRUE
);

CREATE TABLE courses (
    course_id   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    title       VARCHAR(100) NOT NULL,
    credits     INT NOT NULL CHECK (credits > 0)
);

CREATE TABLE enrollments (
    enrollment_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_id  INT NOT NULL REFERENCES courses(course_id) ON DELETE RESTRICT,
    grade NUMERIC(3, 2),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (student_id, course_id)
);

/* ----------------------------------------------------------------------------
   SECTION 2: INSERTING DATA (DML)
   ---------------------------------------------------------------------------- */
INSERT INTO students (first_name, last_name, email, enrollment_date)
VALUES 
    ('Alice', 'Smith', 'alice@example.edu', '2026-08-25'),
    ('Bob', 'Jones', 'bob@example.edu', '2026-08-26'),
    ('Diana', 'Prince', 'diana@example.edu', '2026-08-28');

INSERT INTO courses (course_code, title, credits)
VALUES 
    ('CS101', 'Intro to CS', 3),
    ('MATH150', 'Discrete Math', 3);

INSERT INTO enrollments (student_id, course_id, grade)
VALUES 
    (1, 1, 3.80),
    (2, 1, 2.90),
    (3, 2, 4.00);

/* ----------------------------------------------------------------------------
   SECTION 3: QUERYING DATA
   ---------------------------------------------------------------------------- */
-- View all student data
SELECT * FROM students;

-- Filter for specific students
SELECT first_name, last_name 
FROM students 
WHERE is_active = TRUE;

/* ----------------------------------------------------------------------------
   SECTION 4: JOINS
   ---------------------------------------------------------------------------- */
-- See which students are in which courses
SELECT 
    s.first_name,
    s.last_name,
    c.course_code,
    e.grade
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c  ON e.course_id = c.course_id;

/* ----------------------------------------------------------------------------
   SECTION 5: AGGREGATE FUNCTIONS
   ---------------------------------------------------------------------------- */
-- Find the average grade per course
SELECT 
    c.course_code,
    ROUND(AVG(e.grade), 2) AS average_grade
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_code;
```