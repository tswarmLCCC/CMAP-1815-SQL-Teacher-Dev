# Unit 7 Student Lab Guide: Normalized Schema Design & Constraint Architecture

## Lab Overview
In this lab, you assume the role of Lead Database Architect for Global Logistics & Supply. You are presented with a broken, legacy "Denormalized Nightmare" spreadsheet tracking hospital clinical trials. Your task is to analyze its functional dependencies, decompose the flat file into a Third Normal Form (3NF) relational architecture, implement the schema using clean DDL scripts with ironclad constraints, stress-test your constraints, and build reporting views.

All work must be conducted in PostgreSQL 16.

---

## Deliverables & Submission Guidelines
1. Create a script named `lab7_submission.sql`.
2. Adhere strictly to the SQL Style Guide: UPPERCASE keywords, snake_case identifiers.
3. Every constraint must be explicitly named (e.g. `CONSTRAINT fk_...`, `CONSTRAINT chk_...`).
4. Test execution in `psql`:
   ```bash
   psql -U postgres -d postgres -f lab7_submission.sql
   ```

---

## The Legacy Spreadsheet Schema
The unnormalized spreadsheet contains the following 10 columns:
`trial_id`, `patient_name`, `patient_email`, `patient_dob`, `physician_name`, `physician_pager`, `hospital_wing`, `drug_code`, `drug_dosage`, `trial_status`.

---

## Lab Tasks

### Task 1: 3NF Relational Decomposition Plan
Decompose the flat spreadsheet into four normalized relational tables:
1. `patients`: Stores patient demographic information (`patient_id`, `patient_name`, `patient_email`, `patient_dob`).
2. `physicians`: Stores medical doctor records (`physician_id`, `physician_name`, `physician_pager`, `hospital_wing`).
3. `clinical_trials`: Stores overall study records (`trial_id`, `patient_id`, `physician_id`, `start_date`, `trial_status`).
4. `trial_medications`: Junction table tracking drugs administered in each trial (`trial_med_id`, `trial_id`, `drug_code`, `drug_dosage`).

### Task 2: DDL Scripting & Primary/Foreign Key Declarations
Write the complete DDL script to create the 4 tables in PostgreSQL:
* Use `SERIAL PRIMARY KEY` (or `IDENTITY`) on all entities.
* In `clinical_trials`, configure foreign keys to `patients` and `physicians` with `ON DELETE RESTRICT`.
* In `trial_medications`, configure foreign key to `clinical_trials` with `ON DELETE CASCADE`.

### Task 3: Enterprise Integrity & Domain Check Constraints
Add explicit constraints to enforce business rules:
* `patient_email` must be `UNIQUE` and `NOT NULL`.
* `trial_status` must be restricted via `CHECK` to one of: `'Enrolled'`, `'Active'`, `'Completed'`, `'Withdrawn'`.
* `drug_dosage` must be `NOT NULL` and checked to ensure it is not empty.

### Task 4: Constraint Stress Testing & Rejection Proof
Demonstrate that your database catches invalid data at the storage layer:
* Include an `INSERT` statement attempting to insert an invalid `trial_status` (e.g. `'Terminated'`). Comment out the statement and provide a 1-sentence explanation of the expected error.
* Include an `INSERT` statement attempting to insert a duplicate `patient_email`. Comment out and explain.

### Task 5: Security & Executive Reporting View
Create an analytical view named `v_active_trial_roster` that:
* Joins `clinical_trials`, `patients`, `physicians`, and `trial_medications`.
* Filters for `trial_status = 'Active'`.
* Displays `trial_id`, `patient_name`, `physician_name`, `hospital_wing`, `drug_code`, `drug_dosage`.
* Completely hides `patient_email` and `patient_dob` for HIPAA compliance.
