# Unit 3 Student Lab Guide: Multi-Table Relational Integration & Anomaly Audits

## Lab Objective
In this lab, you will:
1. Connect multiple normalized tables using ANSI SQL `INNER JOIN` and table aliases.
2. Chain three and four tables together to reconstruct complex business transactions.
3. Apply `LEFT JOIN` to prevent silent data loss in catalog and directory reports.
4. Execute the **Anti-Join** pattern to isolate business anomalies (unsold products, unstaffed facilities, customers without orders).

---

## Submission Instructions
1. Open your personal GitHub Codespace.
2. Create a file named `lab3_yourname.sql`.
3. Ensure every query uses **UPPERCASE** keywords, places `JOIN` and `ON` clauses on separate lines, and qualifies every column with its table alias (e.g. `e.first_name`, `l.city`).
4. Test all queries against your PostgreSQL database to guarantee error-free execution.
5. Commit and push your code to your repository.

---

## Lab Challenges

### Part 1: Two-Table INNER JOINs & Disambiguation (25 Points)
1. **Staff Regional Roster:** Join `employees` and `locations`. Retrieve the employee's `first_name`, `last_name`, `title`, and the `city` and `state` of their assigned location. Sort by `state` ascending, then by `last_name` ascending.
2. **Headquarters Staff Directory:** Modify Challenge 1 to display only employees assigned to facilities in the state of `'WY'`. Project `full_name` (combined), `department`, `city`, and `facility_type`.
3. **Order Ownership Audit:** Join `orders` and `employees`. Retrieve `order_id`, `order_date`, `status`, and the full name of the employee who processed the order (`first_name || ' ' || last_name AS processed_by`). Sort by `order_date` descending.

---

### Part 2: Multi-Table Transaction Reconstructions (30 Points)
4. **Order Line Subtotals (3 Tables):** Join `orders`, `order_lines`, and `products`. Display:
   - `o.order_id`
   - `o.order_date`
   - `p.product_name`
   - `p.category`
   - `ol.quantity`
   - `ol.unit_price`
   - A calculated column `line_subtotal` (`ol.quantity * ol.unit_price`)  
   Sort by `order_id` ascending, then by `line_subtotal` descending.
5. **High-Value Item Sales:** Using the 3-table join from Challenge 4, filter for individual line items where the `line_subtotal` is strictly greater than `$150.00`. Order from highest subtotal to lowest.
6. **Full Operational Audit Trail (4 Tables):** Trace transactions from the sales rep's physical office all the way to the line item. Join `locations` $\rightarrow$ `employees` $\rightarrow$ `orders` $\rightarrow$ `order_lines`. Display:
   - `o.order_id`
   - `l.city AS sales_office_city`
   - `e.last_name AS employee_last_name`
   - `ol.quantity`
   - `ol.unit_price`
   Filter for orders with `status = 'Completed'`. Sort by `order_id` ascending.

---

### Part 3: Outer Joins & Data Loss Prevention (25 Points)
7. **Complete Inventory Visibility:** Write a query that lists **ALL products** in the database alongside any order line items, using a `LEFT JOIN` from `products` to `order_lines`. Display `p.product_id`, `p.product_name`, `p.stock_quantity`, `ol.order_id`, and `ol.quantity`. Notice the `NULL` values for products that have never been purchased!
8. **Locations Staffing Overview:** Write a query using a `LEFT JOIN` from `locations` to `employees` that shows every facility in the company and any employees assigned to it. Display `l.city`, `l.facility_type`, `e.first_name`, and `e.last_name`. Sort by `l.city` ascending.

---

### Part 4: Anomaly Audits via Anti-Joins (20 Points)
9. **Dead Inventory Detection (The Anti-Join):** Write an Anti-Join query to find all products that have **NEVER appeared in any customer order**. Display `p.product_id`, `p.sku`, `p.product_name`, `p.stock_quantity`, and `p.retail_price`. Order by `stock_quantity` descending to highlight tied-up warehouse capital.
10. **Unstaffed Facility Audit:** Write an Anti-Join query against `locations` and `employees` to find facilities that currently have **zero employees assigned**. Display `l.location_id`, `l.city`, `l.state`, and `l.facility_type`.
