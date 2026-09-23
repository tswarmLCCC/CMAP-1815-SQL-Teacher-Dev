-- ============================================================================
-- CMAP 1815: Introduction to Modern SQL
-- Unit 7: Schema Design, DDL & Data Integrity
-- Script 1: Relational Normalization (1NF to 3NF Walkthrough)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEACHING CARD 1: The Denormalized Spreadsheet Nightmare (Un-normalized)
-- Note the severe anomalies: comma-separated items, repeated doctor data.
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS unnormalized_clinic_sheet (
    visit_id INT,
    patient_name VARCHAR(100),
    patient_phone VARCHAR(50),
    prescribed_medications VARCHAR(255), -- Violates 1NF! (Comma-separated list)
    doctor_name VARCHAR(100),
    doctor_specialty VARCHAR(100),       -- Violates 3NF! (Transitive dependency on doctor_name)
    doctor_clinic_room VARCHAR(20)
);

INSERT INTO unnormalized_clinic_sheet VALUES 
    (1, 'John Doe', '555-1111', 'Amoxicillin, Ibuprofen', 'Dr. Meredith Grey', 'General Surgery', 'Room 304'),
    (2, 'Jane Smith', '555-2222', 'Lisinopril', 'Dr. Derek Shepherd', 'Neurosurgery', 'Room 412'),
    (3, 'John Doe', '555-1111', 'Ibuprofen', 'Dr. Meredith Grey', 'General Surgery', 'Room 304');

-- ----------------------------------------------------------------------------
-- TEACHING CARD 2: Step 1 - Achieving First Normal Form (1NF)
-- Rule: Atomic values only. Every cell must contain a single value.
-- ----------------------------------------------------------------------------

-- In 1NF, we split comma-separated items into discrete rows:
CREATE TABLE IF NOT EXISTS clinic_1nf (
    visit_id INT,
    medication_name VARCHAR(100),
    patient_name VARCHAR(100),
    patient_phone VARCHAR(50),
    doctor_name VARCHAR(100),
    doctor_specialty VARCHAR(100),
    doctor_clinic_room VARCHAR(20),
    PRIMARY KEY (visit_id, medication_name) -- Composite Key
);

-- ----------------------------------------------------------------------------
-- TEACHING CARD 3: Step 2 & 3 - Decomposing to 3NF (Normalized Relations)
-- Eliminating Partial Dependencies (2NF) and Transitive Dependencies (3NF)
-- ----------------------------------------------------------------------------

-- Entity 1: Patients (Identified by patient_id)
CREATE TABLE IF NOT EXISTS clinic_patients (
    patient_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Entity 2: Doctors (Identified by doctor_id)
CREATE TABLE IF NOT EXISTS clinic_doctors (
    doctor_id SERIAL PRIMARY KEY,
    doctor_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    clinic_room VARCHAR(20) NOT NULL
);

-- Entity 3: Appointments/Visits (Junction linking Patient and Doctor)
CREATE TABLE IF NOT EXISTS clinic_visits (
    visit_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES clinic_patients(patient_id),
    doctor_id INT NOT NULL REFERENCES clinic_doctors(doctor_id),
    visit_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Entity 4: Prescriptions (Resolving Many-to-Many between Visits & Medications)
CREATE TABLE IF NOT EXISTS clinic_prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    visit_id INT NOT NULL REFERENCES clinic_visits(visit_id) ON DELETE CASCADE,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL
);

-- Verify: Zero redundancy, zero update/deletion anomalies!
