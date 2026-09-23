# Unit 7: Formative Self-Check Drills & Solutions

Test your knowledge of schema normalization, DDL constraint declarations, and view creation. Test your code in `psql` before reviewing the solutions below.

---

## Drill 1: Identifying Normalization Violations
**Prompt:** Consider a table with columns `student_id (PK)`, `course_code (PK)`, `student_email`, `grade`.
Which Normal Form does this table violate, and why?

### Solution
*Answer:* It violates **Second Normal Form (2NF)**.  
*Explanation:* The primary key is composite (`student_id`, `course_code`). The column `student_email` depends solely on `student_id`, which is only part of the composite primary key. This is a **partial functional dependency**. To reach 2NF, `student_email` must be moved to a dedicated `students` table.

---

## Drill 2: Declaring Check Constraints
**Prompt:** Write a `CREATE TABLE` statement for `inventory_items` with:
* `item_id SERIAL PRIMARY KEY`
* `item_name VARCHAR(100) NOT NULL`
* `quantity INT NOT NULL`
* `unit_price NUMERIC(10,2) NOT NULL`
Include named `CHECK` constraints ensuring that `quantity >= 0` and `unit_price > 0.00`.

### Solution
```sql
CREATE TABLE inventory_items (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    CONSTRAINT chk_nonnegative_quantity CHECK (quantity >= 0),
    CONSTRAINT chk_positive_price CHECK (unit_price > 0.00)
);
```

---

## Drill 3: Declaring Foreign Keys with Referential Actions
**Prompt:** Write a `CREATE TABLE` statement for `item_orders` with:
* `order_id SERIAL PRIMARY KEY`
* `item_id INT NOT NULL`
* `order_date DATE DEFAULT CURRENT_DATE`
Include a Foreign Key referencing `inventory_items(item_id)` with `ON DELETE RESTRICT`.

### Solution
```sql
CREATE TABLE item_orders (
    order_id SERIAL PRIMARY KEY,
    item_id INT NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_orders_item 
        FOREIGN KEY (item_id) 
        REFERENCES inventory_items(item_id) 
        ON DELETE RESTRICT
);
```

---

## Drill 4: Testing Constraint Rejections
**Prompt:** Using the tables created in Drills 2 and 3:
1. Insert an item with `unit_price = -5.00`.
2. Observe and explain the error returned by PostgreSQL.

### Solution
```sql
INSERT INTO inventory_items (item_name, quantity, unit_price)
VALUES ('Defective Widget', 10, -5.00);
```
*Output:*
`ERROR: new row for relation "inventory_items" violates check constraint "chk_positive_price"`  
*Explanation:* PostgreSQL intercepts the row before writing to disk and rejects it because `-5.00` violates the condition `unit_price > 0.00`.

---

## Drill 5: Security View Masking
**Prompt:** Create a view named `v_safe_staff_directory` that projects `first_name`, `last_name`, `department`, and `job_title` from the `employees` table, completely omitting `salary` and `employee_id`.

### Solution
```sql
CREATE OR REPLACE VIEW v_safe_staff_directory AS
SELECT 
    first_name,
    last_name,
    department,
    job_title
FROM employees
WHERE is_active = TRUE;
```
*Takeaway:* Any user granted access to `v_safe_staff_directory` can view staff roles without gaining visibility into confidential compensation records.
