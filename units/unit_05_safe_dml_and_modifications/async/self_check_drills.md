# Unit 5: Formative Self-Check Drills & Solutions

Test your mastery of safe data manipulation, transaction handling, and staging workflows. Test your answers in `psql` before checking the solution below.

---

## Drill 1: Explicit Column INSERT
**Prompt:** Write an `INSERT` statement that adds a new employee to the `employees` table:
* `first_name`: `'Elena'`
* `last_name`: `'Rostova'`
* `department`: `'Research'`
* `job_title`: `'Data Engineer'`
* `salary`: `88500.00`
* `is_active`: `TRUE`
* `hire_date`: Current date (`CURRENT_DATE`)
Include an explicit column list.

### Solution
```sql
INSERT INTO employees (
    first_name, 
    last_name, 
    department, 
    job_title, 
    salary, 
    is_active, 
    hire_date
) VALUES (
    'Elena', 
    'Rostova', 
    'Research', 
    'Data Engineer', 
    88500.00, 
    TRUE, 
    CURRENT_DATE
);
```

---

## Drill 2: Atomic Upsert with ON CONFLICT
**Prompt:** Write an `INSERT` statement for a product with `product_id = 15`, `product_name = 'Wireless Precision Mouse'`, and `retail_price = 45.99`. If `product_id = 15` already exists, update its `retail_price` to `45.99` and `product_name` to the new name using `EXCLUDED`.

### Solution
```sql
INSERT INTO products (product_id, product_name, retail_price)
VALUES (15, 'Wireless Precision Mouse', 45.99)
ON CONFLICT (product_id) 
DO UPDATE SET 
    product_name = EXCLUDED.product_name,
    retail_price = EXCLUDED.retail_price;
```

---

## Drill 3: Safe UPDATE with RETURNING
**Prompt:** Management decides that all active employees in the `'Sales'` department with a current salary under `$55,000` will receive a 7% raise. Write an `UPDATE` statement that applies this raise and uses the `RETURNING` clause to display: `employee_id`, `first_name`, `last_name`, old salary, and new salary rounded to 2 decimal places.

### Solution
```sql
UPDATE employees
SET salary = ROUND(salary * 1.07, 2)
WHERE department = 'Sales' 
  AND is_active = TRUE 
  AND salary < 55000.00
RETURNING 
    employee_id, 
    first_name, 
    last_name, 
    ROUND(salary / 1.07, 2) AS old_salary, 
    salary AS new_salary;
```

---

## Drill 4: Transaction Sandbox with ROLLBACK
**Prompt:** Write a transaction block that begins a transaction, deletes all records from `products` where `stock_quantity = 0`, inspects the remaining product count, and then immediately aborts the transaction using `ROLLBACK` so no data is actually deleted.

### Solution
```sql
BEGIN;

DELETE FROM products
WHERE stock_quantity = 0;

-- Inspect remaining count inside the transaction
SELECT COUNT(*) FROM products;

-- Safely abort all changes
ROLLBACK;
```

---

## Drill 5: Temporary Staging Table Creation & Ingestion
**Prompt:** Create a temporary table named `stage_new_hires` with columns `emp_name VARCHAR(100)` and `raw_salary VARCHAR(50)`. Insert two rows with messy salary strings (`'$65,000'` and `'$72,500'`). Then write a `SELECT` statement that cleans and converts the salary into a numeric decimal.

### Solution
```sql
CREATE TEMPORARY TABLE stage_new_hires (
    emp_name VARCHAR(100),
    raw_salary VARCHAR(50)
);

INSERT INTO stage_new_hires (emp_name, raw_salary)
VALUES 
    ('Alice Smith', '$65,000'),
    ('Bob Jones', '$72,500');

SELECT 
    emp_name,
    CAST(REPLACE(REPLACE(raw_salary, '$', ''), ',', '') AS NUMERIC(10,2)) AS clean_salary
FROM stage_new_hires;
```
