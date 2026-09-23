# ETL Foundations: Moving Data in PostgreSQL
### From Raw Files to Structured Tables — Command Line & Python

---

## Introduction

ETL stands for **Extract, Transform, Load** — the three-phase process at the heart of every data pipeline. Before you can analyze data, build dashboards, or train models, you need to reliably get raw data *into* your database, *clean it up*, and *move it* into the right places.

This guide covers the full journey:

- Loading raw files into PostgreSQL from the **command line** and **Python**
- Using **staging tables** as a safe landing zone
- Using **temporary tables** for intermediate work
- Using **CTEs** (Common Table Expressions) to transform data in-query
- Moving data **from table to table** using `INSERT INTO ... SELECT`
- Validating data at every step

By the end, you will understand not just *how* to move data, but *why* each layer of this architecture exists.

---

## Part 1: The Architecture — Why Layers Matter

Before writing a single line of SQL, understand the pattern you are building toward. Professional ETL pipelines use multiple layers, not one giant table.

```
Raw File (CSV, JSON, etc.)
        │
        ▼
┌─────────────────┐
│  Staging Table  │  ← Everything as TEXT. No constraints. Just land the data.
└────────┬────────┘
         │  Validate, clean, cast
         ▼
┌─────────────────┐
│  Temp Table(s)  │  ← Session-scoped scratch space. Safe to experiment.
└────────┬────────┘
         │  Transform, deduplicate, enrich
         ▼
┌─────────────────┐
│ Production Table│  ← Typed, constrained, indexed. The real schema.
└─────────────────┘
```

### Why not load directly into the production table?

- Raw files are **dirty**. Dates come in as `"12/5/23"` or `"Dec 5, 2023"`. Numbers have commas. Fields are missing.
- If you load directly and one row fails a constraint, the **entire import fails**.
- A staging table absorbs everything first — then you clean on your own terms.

---

## Part 2: Setting Up Your Tables

### 2.1 The Staging Table

A staging table mirrors the shape of your source file but uses **`TEXT` for every column**. This is intentional. You are not trusting the source data yet.

```sql
-- sql/create_staging.sql

DROP TABLE IF EXISTS raw_staging;

CREATE TABLE raw_staging (
    order_id            TEXT,
    order_date          TEXT,
    ship_date           TEXT,
    customer_id         TEXT,
    customer_name       TEXT,
    customer_segment    TEXT,
    product_id          TEXT,
    product_name        TEXT,
    category            TEXT,
    sales               TEXT,
    quantity            TEXT,
    discount            TEXT,
    profit              TEXT,
    shipping_mode       TEXT,
    country             TEXT,
    city                TEXT,
    state               TEXT,
    postal_code         TEXT,
    region              TEXT
);
```

> **Rule of thumb:** If the column comes from a file you do not control, stage it as TEXT first.

### 2.2 The Production Table

This is your real schema — typed, constrained, and indexed.

```sql
-- sql/create_orders.sql

DROP TABLE IF EXISTS orders CASCADE;

CREATE TABLE orders (
    order_id         SERIAL PRIMARY KEY,
    order_date       DATE           NOT NULL,
    ship_date        DATE,
    customer_id      INTEGER        NOT NULL REFERENCES customers(customer_id),
    product_id       INTEGER        NOT NULL REFERENCES products(product_id),
    sales            NUMERIC(10, 2) NOT NULL CHECK (sales >= 0),
    quantity         INTEGER        NOT NULL CHECK (quantity > 0),
    discount         NUMERIC(4, 2)  DEFAULT 0,
    profit           NUMERIC(10, 2),
    shipping_mode    VARCHAR(50)
);

-- Index the foreign keys — these get hit on every JOIN
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_product  ON orders(product_id);
CREATE INDEX idx_orders_date     ON orders(order_date);
```

---

## Part 3: Loading Data — The Command Line

PostgreSQL's `\copy` command is the fastest way to load a flat file. It runs **client-side**, meaning the file lives on your machine (not the server).

### 3.1 Basic `\copy` syntax

```bash
PGPASSWORD=yourpassword psql \
  -U postgres \
  -h localhost \
  -d mydb \
  -c "\copy raw_staging FROM 'path/to/file.csv' WITH CSV HEADER;"
```

**Breaking down the flags:**

| Flag | Meaning |
|------|---------|
| `-U postgres` | Connect as the `postgres` user |
| `-h localhost` | Host (use `db` if running in Docker) |
| `-d mydb` | Target database name |
| `-c "..."` | Execute this command and exit |

### 3.2 Handling Encodings

Files with accented characters (Spanish, French, Portuguese) are often encoded in `LATIN1`, not `UTF-8`. Importing without specifying encoding causes silent corruption or errors.

```bash
PGPASSWORD=postgres psql -U postgres -h db -d mydb -c \
  "\copy raw_staging FROM 'data/dataset.csv' WITH CSV HEADER ENCODING 'LATIN1';"
```

**How to detect encoding before importing:**

```bash
# On Linux/Mac
file -i yourfile.csv

# Or use Python to detect it
python3 -c "
import chardet
with open('data/dataset.csv', 'rb') as f:
    result = chardet.detect(f.read(100000))
    print(result)
"
```

### 3.3 Handling Delimiters and Quoting

Not every file is comma-separated. The `WITH` clause gives you full control.

```bash
# Tab-separated file
\copy raw_staging FROM 'file.tsv' WITH DELIMITER E'\t' CSV HEADER;

# Pipe-separated file
\copy raw_staging FROM 'file.psv' WITH DELIMITER '|' CSV HEADER;

# Custom quote character
\copy raw_staging FROM 'file.csv' WITH CSV HEADER QUOTE '"' ESCAPE '\';
```

### 3.4 Loading Only Specific Columns

If your file has more columns than your table (or a different order), specify the column list explicitly:

```bash
\copy raw_staging (order_id, order_date, customer_name, sales)
FROM 'partial_file.csv' WITH CSV HEADER;
```

### 3.5 Verifying the Load

Always check your row count immediately after loading:

```sql
-- How many rows landed?
SELECT COUNT(*) FROM raw_staging;

-- Preview the first few rows
SELECT * FROM raw_staging LIMIT 5;

-- Check for completely empty rows (a common file artifact)
SELECT COUNT(*) FROM raw_staging
WHERE order_id IS NULL AND customer_name IS NULL;
```

---

## Part 4: Loading Data — Python

Python gives you programmatic control: loop over multiple files, validate before inserting, handle errors row by row, and log everything.

### 4.1 Environment Setup

```bash
pip install psycopg2-binary pandas sqlalchemy python-dotenv chardet
```

Store your credentials in a `.env` file — **never hardcode passwords**:

```
# .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=postgres
```

### 4.2 Method 1: `psycopg2` with `copy_expert` (Fastest)

`copy_expert` streams the file directly to PostgreSQL — it is essentially the Python equivalent of `\copy`.

```python
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def load_csv_to_staging(filepath: str, table: str, encoding: str = "latin-1") -> int:
    """
    Stream a CSV file into a PostgreSQL staging table.
    Returns the number of rows loaded.
    """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    try:
        with conn.cursor() as cur:
            # Truncate staging first — we want a clean slate each run
            cur.execute(f"TRUNCATE TABLE {table};")

            sql = f"COPY {table} FROM STDIN WITH CSV HEADER ENCODING 'LATIN1'"

            with open(filepath, "r", encoding=encoding) as f:
                cur.copy_expert(sql=sql, file=f)

            conn.commit()

            # Return row count
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            return cur.fetchone()[0]

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


if __name__ == "__main__":
    count = load_csv_to_staging(
        filepath="data/DataCoSupplyChainDataset.csv",
        table="raw_staging"
    )
    print(f"✓ Loaded {count:,} rows into raw_staging")
```

### 4.3 Method 2: pandas + `to_sql` (Most Flexible)

Use this when you need to inspect, filter, or reshape the data *before* it hits the database.

```python
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def load_with_pandas(filepath: str, table: str, chunksize: int = 10_000) -> int:
    """
    Load a CSV into PostgreSQL via pandas.
    Uses chunking to handle large files without memory issues.
    """
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    total_rows = 0

    # Read in chunks — crucial for files over ~500MB
    for i, chunk in enumerate(pd.read_csv(filepath, encoding="latin-1", chunksize=chunksize, dtype=str)):

        # Replace pandas NaN with None so psycopg2 inserts NULL (not 'nan')
        chunk = chunk.where(pd.notnull(chunk), None)

        # Write chunk — 'append' after first chunk, 'replace' on first
        mode = "replace" if i == 0 else "append"

        chunk.to_sql(
            name=table,
            con=engine,
            if_exists=mode,
            index=False,
            method="multi",   # Batch INSERT — faster than row-by-row
        )

        total_rows += len(chunk)
        print(f"  Chunk {i+1}: {total_rows:,} rows loaded so far...")

    return total_rows


if __name__ == "__main__":
    count = load_with_pandas("data/DataCoSupplyChainDataset.csv", "raw_staging")
    print(f"✓ Done. {count:,} total rows.")
```

### 4.4 Method 3: Row-by-Row with Validation (Most Control)

Use this when you need to log bad rows rather than fail the whole load.

```python
import psycopg2
import csv
import logging

logging.basicConfig(filename="etl_errors.log", level=logging.WARNING)

def load_with_validation(filepath: str) -> dict:
    """
    Load CSV row by row, logging failures instead of aborting.
    Returns a summary dict with success/failure counts.
    """
    conn = psycopg2.connect(...)  # your connection params
    results = {"loaded": 0, "failed": 0}

    INSERT_SQL = """
        INSERT INTO raw_staging (order_id, order_date, customer_name, sales, quantity)
        VALUES (%s, %s, %s, %s, %s)
    """

    with open(filepath, encoding="latin-1") as f:
        reader = csv.DictReader(f)

        with conn.cursor() as cur:
            for row_num, row in enumerate(reader, start=2):  # start=2 accounts for header
                try:
                    cur.execute(INSERT_SQL, (
                        row.get("Order ID"),
                        row.get("Order Date"),
                        row.get("Customer Name"),
                        row.get("Sales"),
                        row.get("Quantity"),
                    ))
                    results["loaded"] += 1

                except Exception as e:
                    conn.rollback()
                    logging.warning(f"Row {row_num} failed: {e} | Data: {dict(row)}")
                    results["failed"] += 1

            conn.commit()

    conn.close()
    return results
```

### 4.5 Choosing the Right Python Method

| Method | Speed | Control | Best For |
|--------|-------|---------|----------|
| `copy_expert` | ⚡ Fastest | Low | Large files, trusted sources |
| `pandas to_sql` | Medium | High | Pre-processing, column mapping |
| Row-by-row | Slowest | Maximum | Dirty data, per-row error logging |

---

## Part 5: Temporary Tables

Temporary tables exist **only for the duration of your session**. They are automatically dropped when you disconnect. This makes them ideal for intermediate work — no cleanup required.

### 5.1 Creating a Temp Table

```sql
-- Created in session memory — disappears on disconnect
CREATE TEMP TABLE temp_clean_orders AS
SELECT * FROM raw_staging WHERE FALSE;  -- Same structure, zero rows
```

Or create with an explicit structure:

```sql
CREATE TEMP TABLE temp_deduped (
    order_id     TEXT,
    order_date   DATE,
    customer_id  INTEGER,
    sales        NUMERIC(10,2),
    row_num      INTEGER
);
```

### 5.2 Populating a Temp Table from Staging

```sql
-- Cast and filter from staging into a typed temp table
INSERT INTO temp_clean_orders (order_id, order_date, sales, quantity, profit)
SELECT
    order_id,
    TO_DATE(order_date, 'MM/DD/YYYY'),   -- Cast text → date
    CAST(REPLACE(sales, ',', '') AS NUMERIC(10,2)),  -- Remove commas, cast
    CAST(quantity AS INTEGER),
    CAST(profit AS NUMERIC(10,2))
FROM raw_staging
WHERE
    order_id IS NOT NULL
    AND sales ~ '^\d+(\.\d+)?$';        -- Only rows where sales is a valid number
```

### 5.3 Using Temp Tables to Deduplicate

A common ETL task: the source file has duplicate rows. Use a temp table with a `ROW_NUMBER()` window function to isolate the first occurrence.

```sql
-- Step 1: Load all rows into temp, adding a row number per order_id
CREATE TEMP TABLE temp_ranked AS
SELECT
    *,
    ROW_NUMBER() OVER (
        PARTITION BY order_id
        ORDER BY order_date DESC  -- Keep the most recent version of each order
    ) AS rn
FROM raw_staging;

-- Step 2: Inspect what you're deduplicating
SELECT order_id, COUNT(*) AS occurrences
FROM raw_staging
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC
LIMIT 20;

-- Step 3: Pull only the "winning" row (rn = 1) into production
INSERT INTO orders_clean
SELECT order_id, order_date, customer_name, sales
FROM temp_ranked
WHERE rn = 1;
```

### 5.4 Temp Table Visibility

Temp tables are **session-scoped and schema-isolated**:

```sql
-- This works in your session
SELECT * FROM temp_clean_orders;

-- Another user's session cannot see your temp table
-- They would get: ERROR: relation "temp_clean_orders" does not exist

-- Temp tables live in the pg_temp schema
SELECT schemaname, tablename FROM pg_tables
WHERE schemaname LIKE 'pg_temp%';
```

---

## Part 6: CTEs — Transform Without Touching Disk

A **CTE** (Common Table Expression) is a named subquery defined with `WITH`. It exists only for the duration of the query. Think of it as a temp table that never gets written to disk — it is pure in-query logic.

### 6.1 Basic CTE Syntax

```sql
WITH cte_name AS (
    SELECT ...
    FROM   ...
    WHERE  ...
)
SELECT * FROM cte_name;
```

### 6.2 Multi-Step Transformation with Chained CTEs

CTEs shine when you need to apply transformations in logical stages, each building on the previous one:

```sql
WITH

-- Step 1: Cast and filter the raw data
casted AS (
    SELECT
        order_id,
        TO_DATE(order_date, 'MM/DD/YYYY')              AS order_date,
        CAST(REPLACE(sales, ',', '') AS NUMERIC(10,2)) AS sales,
        CAST(quantity AS INTEGER)                       AS quantity,
        UPPER(TRIM(customer_segment))                   AS customer_segment
    FROM raw_staging
    WHERE order_id IS NOT NULL
      AND order_date IS NOT NULL
),

-- Step 2: Deduplicate using a window function
deduped AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date DESC) AS rn
    FROM casted
),

-- Step 3: Classify customers by segment
enriched AS (
    SELECT
        order_id,
        order_date,
        sales,
        quantity,
        customer_segment,
        CASE
            WHEN customer_segment = 'CONSUMER'    THEN 'B2C'
            WHEN customer_segment = 'CORPORATE'   THEN 'B2B'
            WHEN customer_segment = 'HOME OFFICE' THEN 'B2B'
            ELSE 'UNKNOWN'
        END AS channel_type
    FROM deduped
    WHERE rn = 1  -- Only keep the first occurrence of each order
)

-- Final SELECT: insert into production
INSERT INTO orders_production (order_id, order_date, sales, quantity, channel_type)
SELECT order_id, order_date, sales, quantity, channel_type
FROM enriched;
```

> **CTEs vs. Temp Tables:** Use CTEs when the transformation is a single logical operation. Use temp tables when you need to run multiple queries against the intermediate result, or when you want to index the intermediate data.

### 6.3 CTEs for Data Quality Reporting

Before loading production, use a CTE to produce a quality summary:

```sql
WITH quality_check AS (
    SELECT
        COUNT(*)                                        AS total_rows,
        COUNT(*) FILTER (WHERE order_id IS NULL)        AS missing_order_id,
        COUNT(*) FILTER (WHERE sales IS NULL)           AS missing_sales,
        COUNT(*) FILTER (WHERE sales !~ '^\d+\.?\d*$') AS invalid_sales_format,
        COUNT(DISTINCT order_id)                        AS unique_orders,
        COUNT(*) - COUNT(DISTINCT order_id)             AS duplicate_orders
    FROM raw_staging
)
SELECT
    total_rows,
    missing_order_id,
    missing_sales,
    invalid_sales_format,
    unique_orders,
    duplicate_orders,
    ROUND(100.0 * duplicate_orders / NULLIF(total_rows, 0), 2) AS duplicate_pct
FROM quality_check;
```

---

## Part 7: Moving Data Between Tables

Once your data is clean, the final step is promotion — moving it from staging or temp tables into the production schema.

### 7.1 `INSERT INTO ... SELECT`

The workhorse of ETL. Reads from one table and writes to another in a single statement.

```sql
-- Basic promotion from staging to production
INSERT INTO orders (order_date, ship_date, sales, quantity, profit, shipping_mode)
SELECT
    TO_DATE(order_date, 'MM/DD/YYYY'),
    TO_DATE(ship_date,  'MM/DD/YYYY'),
    CAST(sales    AS NUMERIC(10,2)),
    CAST(quantity AS INTEGER),
    CAST(profit   AS NUMERIC(10,2)),
    TRIM(shipping_mode)
FROM raw_staging
WHERE order_id IS NOT NULL;
```

### 7.2 `INSERT ... ON CONFLICT` (Upsert)

What if you run the pipeline twice? You do not want duplicate rows in production. Use `ON CONFLICT` to update existing rows instead of erroring.

```sql
INSERT INTO orders (order_id, order_date, sales, quantity)
SELECT
    order_id,
    TO_DATE(order_date, 'MM/DD/YYYY'),
    CAST(sales    AS NUMERIC(10,2)),
    CAST(quantity AS INTEGER)
FROM raw_staging
ON CONFLICT (order_id) DO UPDATE
    SET
        order_date = EXCLUDED.order_date,
        sales      = EXCLUDED.sales,
        quantity   = EXCLUDED.quantity;
```

`EXCLUDED` refers to the row that *would have been inserted*. This pattern is called an **upsert** — update if exists, insert if not.

### 7.3 `CREATE TABLE AS SELECT` (CTAS)

Creates a brand-new table from a query result. Useful for snapshots, reporting tables, or archive copies.

```sql
-- Create a monthly summary table from production data
CREATE TABLE monthly_sales_summary AS
SELECT
    DATE_TRUNC('month', order_date)   AS month,
    shipping_mode,
    COUNT(*)                          AS order_count,
    SUM(sales)                        AS total_sales,
    AVG(profit)                       AS avg_profit
FROM orders
GROUP BY 1, 2
ORDER BY 1, 2;

-- Add an index to the new table
CREATE INDEX idx_monthly_month ON monthly_sales_summary(month);
```

### 7.4 Normalizing a Flat File into Multiple Tables

A staging table typically violates 3NF — it has repeated data everywhere. Your job is to split it into normalized tables.

```sql
-- Extract the customers dimension (distinct values only)
INSERT INTO customers (customer_name, customer_segment, country, city, state)
SELECT DISTINCT
    TRIM(customer_name),
    TRIM(customer_segment),
    TRIM(country),
    TRIM(city),
    TRIM(state)
FROM raw_staging
WHERE customer_name IS NOT NULL
ON CONFLICT (customer_name) DO NOTHING;

-- Extract the products dimension
INSERT INTO products (product_name, category)
SELECT DISTINCT
    TRIM(product_name),
    TRIM(category)
FROM raw_staging
WHERE product_name IS NOT NULL
ON CONFLICT (product_name) DO NOTHING;

-- Now load the fact table, joining back to get the generated IDs
INSERT INTO orders (order_date, ship_date, customer_id, product_id, sales, quantity)
SELECT
    TO_DATE(s.order_date, 'MM/DD/YYYY'),
    TO_DATE(s.ship_date,  'MM/DD/YYYY'),
    c.customer_id,
    p.product_id,
    CAST(s.sales    AS NUMERIC(10,2)),
    CAST(s.quantity AS INTEGER)
FROM raw_staging s
JOIN customers c ON TRIM(s.customer_name) = c.customer_name
JOIN products  p ON TRIM(s.product_name)  = p.product_name
WHERE s.order_id IS NOT NULL;
```

---

## Part 8: Full Python ETL Pipeline

Putting it all together: a Python script that runs the entire pipeline end-to-end.

```python
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )


# ─── Phase 1: Extract ────────────────────────────────────────────────────────

def extract(filepath: str) -> int:
    """Load raw CSV into the staging table."""
    log.info(f"EXTRACT: Loading {filepath} into raw_staging...")
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE raw_staging;")
            with open(filepath, encoding="latin-1") as f:
                cur.copy_expert(
                    "COPY raw_staging FROM STDIN WITH CSV HEADER ENCODING 'LATIN1'",
                    f
                )
            conn.commit()

            cur.execute("SELECT COUNT(*) FROM raw_staging;")
            count = cur.fetchone()[0]
            log.info(f"EXTRACT: {count:,} rows loaded.")
            return count

    except Exception as e:
        conn.rollback()
        log.error(f"EXTRACT failed: {e}")
        raise
    finally:
        conn.close()


# ─── Phase 2: Transform ───────────────────────────────────────────────────────

def transform() -> dict:
    """
    Run SQL-based transformations inside the database.
    Uses CTEs and temp tables — no data pulled into Python memory.
    """
    log.info("TRANSFORM: Running quality checks and transformations...")
    conn = get_connection()

    try:
        with conn.cursor() as cur:

            # Quality check
            cur.execute("""
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE order_id IS NULL)  AS missing_id,
                    COUNT(*) FILTER (WHERE sales IS NULL)     AS missing_sales,
                    COUNT(DISTINCT order_id)                  AS unique_orders
                FROM raw_staging;
            """)
            row = cur.fetchone()
            stats = {
                "total": row[0], "missing_id": row[1],
                "missing_sales": row[2], "unique_orders": row[3]
            }
            log.info(f"TRANSFORM quality stats: {stats}")

            # Create a temp table with cleaned, cast, deduplicated data
            cur.execute("""
                CREATE TEMP TABLE temp_transformed AS
                WITH casted AS (
                    SELECT
                        order_id,
                        TO_DATE(order_date, 'MM/DD/YYYY')               AS order_date,
                        TO_DATE(ship_date,  'MM/DD/YYYY')               AS ship_date,
                        TRIM(customer_name)                              AS customer_name,
                        UPPER(TRIM(customer_segment))                   AS customer_segment,
                        TRIM(product_name)                              AS product_name,
                        TRIM(category)                                  AS category,
                        CAST(REPLACE(sales, ',', '') AS NUMERIC(10,2))  AS sales,
                        CAST(quantity AS INTEGER)                       AS quantity,
                        CAST(profit AS NUMERIC(10,2))                   AS profit,
                        TRIM(shipping_mode)                             AS shipping_mode,
                        TRIM(country)                                   AS country,
                        TRIM(city)                                      AS city,
                        TRIM(state)                                     AS state,
                        ROW_NUMBER() OVER (
                            PARTITION BY order_id ORDER BY order_date DESC
                        ) AS rn
                    FROM raw_staging
                    WHERE order_id IS NOT NULL
                )
                SELECT * FROM casted WHERE rn = 1;
            """)

            cur.execute("SELECT COUNT(*) FROM temp_transformed;")
            clean_count = cur.fetchone()[0]
            stats["clean_rows"] = clean_count
            log.info(f"TRANSFORM: {clean_count:,} clean rows in temp table.")

            conn.commit()
            return stats

    except Exception as e:
        conn.rollback()
        log.error(f"TRANSFORM failed: {e}")
        raise
    finally:
        conn.close()


# ─── Phase 3: Load ────────────────────────────────────────────────────────────

def load() -> int:
    """Promote transformed data from temp table into production tables."""
    log.info("LOAD: Promoting data to production schema...")
    conn = get_connection()

    try:
        with conn.cursor() as cur:

            # Load customers dimension
            cur.execute("""
                INSERT INTO customers (customer_name, customer_segment, country, city, state)
                SELECT DISTINCT customer_name, customer_segment, country, city, state
                FROM temp_transformed
                ON CONFLICT (customer_name) DO NOTHING;
            """)
            log.info(f"LOAD: customers → {cur.rowcount} rows inserted.")

            # Load products dimension
            cur.execute("""
                INSERT INTO products (product_name, category)
                SELECT DISTINCT product_name, category
                FROM temp_transformed
                ON CONFLICT (product_name) DO NOTHING;
            """)
            log.info(f"LOAD: products → {cur.rowcount} rows inserted.")

            # Load orders fact table
            cur.execute("""
                INSERT INTO orders (order_date, ship_date, customer_id, product_id,
                                    sales, quantity, profit, shipping_mode)
                SELECT
                    t.order_date,
                    t.ship_date,
                    c.customer_id,
                    p.product_id,
                    t.sales,
                    t.quantity,
                    t.profit,
                    t.shipping_mode
                FROM temp_transformed t
                JOIN customers c ON t.customer_name = c.customer_name
                JOIN products  p ON t.product_name  = p.product_name
                ON CONFLICT (order_id) DO NOTHING;
            """)
            orders_loaded = cur.rowcount
            log.info(f"LOAD: orders → {orders_loaded} rows inserted.")

            conn.commit()
            return orders_loaded

    except Exception as e:
        conn.rollback()
        log.error(f"LOAD failed: {e}")
        raise
    finally:
        conn.close()


# ─── Orchestrator ─────────────────────────────────────────────────────────────

def run_pipeline(filepath: str):
    log.info("=" * 60)
    log.info("ETL PIPELINE STARTING")
    log.info("=" * 60)

    try:
        raw_count   = extract(filepath)
        stats       = transform()
        final_count = load()

        log.info("=" * 60)
        log.info("PIPELINE COMPLETE")
        log.info(f"  Raw rows extracted : {raw_count:,}")
        log.info(f"  Clean rows after QC: {stats['clean_rows']:,}")
        log.info(f"  Orders loaded      : {final_count:,}")
        log.info(f"  Duplicates dropped : {raw_count - stats['clean_rows']:,}")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"PIPELINE FAILED: {e}")
        raise


if __name__ == "__main__":
    run_pipeline("data/DataCoSupplyChainDataset.csv")
```

---

## Part 9: Inspecting and Debugging Your Pipeline

### Check what tables exist

```sql
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

### Check row counts across all tables

```sql
SELECT
    relname                          AS table_name,
    n_live_tup                       AS estimated_rows
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

### Use `EXPLAIN ANALYZE` to verify query performance

```sql
EXPLAIN ANALYZE
SELECT o.order_date, c.customer_name, p.product_name, o.sales
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
WHERE o.order_date >= '2023-01-01';
```

Look for **Seq Scan** (bad on large tables — add an index) vs **Index Scan** (good).

### Rollback safely during development

```sql
BEGIN;

-- Try your transformation
INSERT INTO orders SELECT ... FROM raw_staging;

-- Check results before committing
SELECT COUNT(*) FROM orders;

-- If something looks wrong:
ROLLBACK;

-- If everything looks right:
COMMIT;
```

---

## Summary: ETL Decision Map

```
Does the source data need encoding handling?
  └─ Yes → Add ENCODING 'LATIN1' to \copy or read_csv()

Do you need to pre-process before inserting?
  ├─ No  → Use \copy or copy_expert (fastest)
  └─ Yes → Use pandas to_sql or row-by-row

Is the transformation a single logical operation?
  ├─ Yes → Use a CTE
  └─ No  → Use a TEMP TABLE (allows multiple queries, indexing)

Will you run the pipeline more than once?
  ├─ No  → INSERT INTO ... SELECT
  └─ Yes → INSERT ... ON CONFLICT (upsert)

Is the file too large for memory?
  └─ Yes → Use chunksize in pandas, or copy_expert (streams the file)
```

---

*Next up: Building analytical views with Window Functions, aggregations, and JOIN strategies across your normalized schema.*
