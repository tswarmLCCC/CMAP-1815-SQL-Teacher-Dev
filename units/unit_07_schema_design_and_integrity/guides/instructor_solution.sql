-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 7: Schema Design, DDL & Data Integrity
-- Instructor Master Solution
-- ============================================================================

-- Clean environment
DROP VIEW IF EXISTS v_active_trial_roster CASCADE;
DROP TABLE IF EXISTS trial_medications CASCADE;
DROP TABLE IF EXISTS clinical_trials CASCADE;
DROP TABLE IF EXISTS physicians CASCADE;
DROP TABLE IF EXISTS patients CASCADE;

-- ----------------------------------------------------------------------------
-- TASKS 1 & 2 & 3: 3NF Table Architecture & Constraints
-- ----------------------------------------------------------------------------

-- Entity 1: Patients
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    patient_email VARCHAR(255) NOT NULL,
    patient_dob DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_patients_email 
        UNIQUE (patient_email)
);

-- Entity 2: Physicians
CREATE TABLE physicians (
    physician_id SERIAL PRIMARY KEY,
    physician_name VARCHAR(100) NOT NULL,
    physician_pager VARCHAR(20) NOT NULL,
    hospital_wing VARCHAR(50) NOT NULL
);

-- Entity 3: Clinical Trials (Core Association)
CREATE TABLE clinical_trials (
    trial_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    physician_id INT NOT NULL,
    start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    trial_status VARCHAR(20) NOT NULL DEFAULT 'Enrolled',
    
    CONSTRAINT fk_trials_patient
        FOREIGN KEY (patient_id) 
        REFERENCES patients(patient_id)
        ON DELETE RESTRICT,
        
    CONSTRAINT fk_trials_physician
        FOREIGN KEY (physician_id) 
        REFERENCES physicians(physician_id)
        ON DELETE RESTRICT,
        
    CONSTRAINT chk_trials_status
        CHECK (trial_status IN ('Enrolled', 'Active', 'Completed', 'Withdrawn'))
);

-- Entity 4: Trial Medications (Junction Table)
CREATE TABLE trial_medications (
    trial_med_id SERIAL PRIMARY KEY,
    trial_id INT NOT NULL,
    drug_code VARCHAR(50) NOT NULL,
    drug_dosage VARCHAR(50) NOT NULL,
    
    CONSTRAINT fk_meds_trial
        FOREIGN KEY (trial_id) 
        REFERENCES clinical_trials(trial_id)
        ON DELETE CASCADE,
        
    CONSTRAINT chk_meds_dosage_not_empty
        CHECK (LENGTH(TRIM(drug_dosage)) > 0)
);

-- ----------------------------------------------------------------------------
-- SAMPLE DATA INSERTION (Verification State)
-- ----------------------------------------------------------------------------
INSERT INTO patients (patient_name, patient_email, patient_dob)
VALUES 
    ('Sarah Connor', 'sconnor@cyberdyne.org', '1985-05-12'),
    ('Kyle Reese', 'kreese@resistance.net', '1990-11-23');

INSERT INTO physicians (physician_name, physician_pager, hospital_wing)
VALUES 
    ('Dr. Peter Silberman', 'PAGER-801', 'Psychiatry Wing B'),
    ('Dr. Miles Dyson', 'PAGER-404', 'Advanced Technology Wing');

INSERT INTO clinical_trials (patient_id, physician_id, trial_status)
VALUES 
    (1, 1, 'Active'),
    (2, 2, 'Enrolled');

INSERT INTO trial_medications (trial_id, drug_code, drug_dosage)
VALUES 
    (1, 'MED-902', '50mg daily'),
    (1, 'MED-104', '10mg as needed'),
    (2, 'MED-330', '100mg twice daily');

-- ----------------------------------------------------------------------------
-- TASK 4: Constraint Stress Testing & Proof
-- ----------------------------------------------------------------------------

-- Test 1: Invalid trial status
-- INSERT INTO clinical_trials (patient_id, physician_id, trial_status)
-- VALUES (1, 1, 'Terminated');
-- EXPECTED ERROR: violates check constraint "chk_trials_status"

-- Test 2: Duplicate email address
-- INSERT INTO patients (patient_name, patient_email, patient_dob)
-- VALUES ('Sarah Imposter', 'sconnor@cyberdyne.org', '1992-01-01');
-- EXPECTED ERROR: duplicate key value violates unique constraint "uq_patients_email"

-- ----------------------------------------------------------------------------
-- TASK 5: Security & Executive Reporting View
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_active_trial_roster AS
SELECT 
    t.trial_id,
    p.patient_name,
    doc.physician_name,
    doc.hospital_wing,
    m.drug_code,
    m.drug_dosage
FROM clinical_trials t
JOIN patients p ON t.patient_id = p.patient_id
JOIN physicians doc ON t.physician_id = doc.physician_id
JOIN trial_medications m ON t.trial_id = m.trial_id
WHERE t.trial_status = 'Active';

-- Verify the view:
SELECT * FROM v_active_trial_roster;
