# COSC-2409-SQL-Labs

A GitHub Codespaces environment for SQL labs. Everything runs in the browser — no local installs needed.

---

## Getting Started

1. Go to this repo → click **"Use this template"** → **"Create a new repository"**
2. Open your new repo → click **"Code"** → **"Open in Codespaces"**
3. Wait ~2 minutes for setup to complete (you'll see `>>> Done!` in the terminal)
4. Open a `lab.sql` file, write your queries, run them with SQLTools (**Ctrl+Shift+P → SQLTools: Run Current File**)
5. Commit and push when done

---

## Connecting to the Database

Your Codespace runs a PostgreSQL server automatically. Connect to it from the terminal:

```bash
psql $DATABASE_URL
```

You'll see a prompt like:

```
psql (16.x)
Type "help" for help.

mydb=#
```

Type `\q` to exit.

The `DATABASE_URL` environment variable is pre-configured — you don't need to set anything up.

---

## Basic psql Commands

Once connected with `psql $DATABASE_URL`:

| Command | What it does |
|--------|--------------|
| `\l` | List all databases |
| `\c dbname` | Switch to a different database |
| `\dt` | List tables in the current database |
| `\d tablename` | Describe a table's columns |
| `\i file.sql` | Run a SQL file |
| `\q` | Quit |

---

## Working with Databases

### The default database

The default database is called `mydb`. It's created automatically when the Codespace starts.

### Creating a new database

```sql
CREATE DATABASE lab2;
```

### Switching to a different database

```bash
psql $DATABASE_URL   -- connects to mydb by default
```

Or connect directly to a specific database:

```bash
psql postgresql://postgres:postgres@db:5432/lab2
```

Or switch inside psql:

```sql
\c lab2
```

### Dropping a database

```sql
DROP DATABASE lab2;
```

---

## Loading Data

### Run a SQL file from the terminal

```bash
psql $DATABASE_URL -f yourfile.sql
```

### Run a SQL file from inside psql

```sql
\i yourfile.sql
```

### Paste SQL directly

Just connect with `psql $DATABASE_URL` and type or paste your SQL at the prompt.

### Load a CSV file into a table

First create the table, then use `COPY`:

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name TEXT,
    grade INTEGER
);

COPY students FROM '/workspace/data/students.csv' DELIMITER ',' CSV HEADER;
```

Make sure your CSV is inside the `/workspace` folder in your Codespace.

---

## Exporting Data

### Export a table to CSV

```bash
psql $DATABASE_URL -c "\COPY tablename TO '/workspace/output.csv' CSV HEADER"
```

### Export query results to CSV

```bash
psql $DATABASE_URL -c "\COPY (SELECT * FROM students WHERE grade > 80) TO '/workspace/results.csv' CSV HEADER"
```

### Dump an entire database to a SQL file

```bash
pg_dump $DATABASE_URL > /workspace/backup.sql
```

### Restore a database from a dump

```bash
psql $DATABASE_URL < /workspace/backup.sql
```

---

## Seed Data (Auto-loaded on Start)

Any `.sql` files placed in the `sql/` folder at the root of the repo are automatically run when the database first starts. Use this to pre-load schema and sample data for labs:

```
sql/
  01_schema.sql    ← CREATE TABLE statements
  02_seed.sql      ← INSERT sample data
```

Files run in alphabetical order. **This only runs on the very first start** — if you need to reset, see below.

---

## Resetting the Database

If you need a clean slate:

```bash
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

Then reload your seed data:

```bash
psql $DATABASE_URL -f sql/01_schema.sql
psql $DATABASE_URL -f sql/02_seed.sql
```

---

## Troubleshooting

**`psql: command not found`** — the Codespace didn't finish building. Wait for the terminal to show `>>> Done!` and try again, or run **Ctrl+Shift+P → "Codespaces: Rebuild Container"**.

**`could not connect to server`** — the database container isn't running yet. Wait 30 seconds and try again. If it keeps failing, rebuild the container.

**`psql $DATABASE_URL` hangs** — same as above. Rebuild the container.

**Changes disappeared after reopening** — data in the database persists as long as the Codespace exists. If you deleted and recreated the Codespace, the database is fresh. Re-run your seed files.
