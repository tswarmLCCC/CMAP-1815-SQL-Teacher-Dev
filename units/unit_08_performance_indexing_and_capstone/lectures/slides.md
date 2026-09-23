---
marp: true
theme: default
paginate: true
header: "CMAP 1815: Introduction to Modern SQL"
footer: "Unit 8: Performance Tuning, Indexing & Capstone Defense"
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 40px;
    background-color: #fdfdfd;
  }
  h1 {
    color: #1a365d;
  }
  h2 {
    color: #2b6cb0;
  }
  .highlight {
    background-color: #ebf8ff;
    border-left: 5px solid #3182ce;
    padding: 10px;
    border-radius: 4px;
  }
  .danger {
    background-color: #fff5f5;
    border-left: 5px solid #e53e3e;
    padding: 10px;
    border-radius: 4px;
  }
  code {
    background-color: #edf2f7;
    color: #c53030;
    padding: 2px 6px;
    border-radius: 4px;
  }
---

# CMAP 1815: Introduction to Modern SQL
## Unit 8: Query Performance, Indexing & Capstone Defense

**Instructor:** Department of Computer Applications  
**Environment:** PostgreSQL 16 & GitHub Codespaces  
**Focus:** Query Execution Plans (`EXPLAIN ANALYZE`), B-Tree Indexes, The Write Penalty, Audit Tracking & Capstone Defense

---

## The Culmination: From Correctness to Performance

Up until now, our primary question was:  
*"Does the query produce the correct answer?"*

In enterprise systems with 50 million rows, a query that takes 45 seconds is **broken**, even if its output is mathematically correct.

Today's question:  
*"How does the database engine execute this query, and how do we make it 1,000 times faster?"*

---

## Video 8.1: Reading the Database Mind: EXPLAIN & EXPLAIN ANALYZE

PostgreSQL has an internal **Cost-Based Query Planner**:

```sql
EXPLAIN ANALYZE
SELECT * FROM employees WHERE salary > 90000;
```

```
Execution Output:
Seq Scan on employees  (cost=0.00..18.50 rows=10 width=128) 
                       (actual time=0.015..0.028 rows=8 loops=1)
  Filter: (salary > 90000)
  Rows Removed by Filter: 42
Planning Time: 0.082 ms
Execution Time: 0.045 ms
```

* **`Seq Scan` (Sequential Scan):** Reads every single block of the table from start to finish. Inefficient for selective queries!
* **`Cost`:** Unitless measure of disk I/O and CPU effort.

---

## Video 8.2: How Indexes Work (B-Trees)

An **Index** is like the index at the back of a textbook:  
A separate, sorted data structure that points directly to the physical storage location (`ctid`) of each row on disk.

```
                  [ Root Node (B-Tree) ]
                         /      \
             [ Branch < 50k ]   [ Branch >= 50k ]
                  /     \            /     \
             [ Leaf ] [ Leaf ]   [ Leaf ] [ Leaf ]
                |        |          |        |
         [ Physical Table Heap Pages on Disk ]
```

```sql
-- Creating a B-Tree Index:
CREATE INDEX idx_employees_department ON employees(department);
```

After indexing: `Seq Scan` transforms into an ultra-fast **`Index Scan`** ($O(\log N)$ search time)!

---

## The Write Penalty: Why NOT Index Everything?

<div class="danger">
<b>The Engineering Tradeoff:</b><br>
Every index makes read queries (<code>SELECT</code>) faster, but makes write operations (<code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>) slower!
</div>

```
Single INSERT without indexes:
1. Write row to table heap. (Done!)

Single INSERT with 8 indexes:
1. Write row to table heap.
2. Update B-Tree 1.
3. Update B-Tree 2.
...
9. Update B-Tree 8. (Severe Write Penalty!)
```

**Rule of Thumb:** Index columns used heavily in `WHERE`, `JOIN ON`, and `ORDER BY`. Avoid indexing high-churn, write-heavy columns.

---

## Video 8.3: Change Tracking & The Comprehensive Capstone

### Audit Logging: Who Changed What and When?
Enterprise databases require historical compliance:

```sql
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    action VARCHAR(20),
    record_id INT,
    changed_by VARCHAR(50) DEFAULT CURRENT_USER,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## The CMAP 1815 Capstone Architecture

Your Capstone unites all 8 weeks of engineering:
1. **Schema Design (3NF):** Tables, PKs, FKs with referential actions.
2. **Data Integrity:** `CHECK`, `UNIQUE`, `NOT NULL`.
3. **Data Ingestion:** Batch `INSERT` & safe staging pipelines.
4. **Analytical Reporting:** CTEs, Window Functions, and Matrix Pivots.
5. **Performance Tuning:** `EXPLAIN ANALYZE` profiling and targeted B-Tree Indexing.

*Congratulations on reaching the final milestone of Modern SQL!*
