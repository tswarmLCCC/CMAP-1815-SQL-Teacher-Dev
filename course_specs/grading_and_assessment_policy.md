# CMAP 1815: Grading & Assessment Policy

## Grading Architecture
Final grades in CMAP 1815 are based on continuous active learning, conceptual mastery, and demonstrable database engineering ability:

| Assessment Category | Weight | Frequency | Description |
| :--- | :---: | :--- | :--- |
| **Weekly Practical Labs** | **40%** | Weekly (Units 1–7) | Hands-on SQL query scripts evaluated on query accuracy, formatting standards, and output verification. |
| **Weekly Unit Quizzes** | **20%** | Weekly (Units 1–8) | 15-question Canvas quizzes testing async concepts (30%), syntax error identification (30%), and query output prediction (40%). |
| **Asynchronous Self-Checks & Prep** | **10%** | Weekly (Units 1–8) | Formative low-stakes knowledge checks completed prior to synchronous class meetings. |
| **Comprehensive Capstone Project** | **30%** | Week 8 | End-to-end database architecture: 3NF design, DDL script, safe DML population, and complex analytics (CTEs + Window Functions). |
| **Total** | **100%** | | |

---

## Grading Scale
- **A**: 90.0% – 100%
- **B**: 80.0% – 89.9%
- **C**: 70.0% – 79.9%
- **D**: 60.0% – 69.9%
- **F**: Below 60.0%

---

## SQL Code Quality Standards (Deduction Criteria)
In professional data environments, syntactically working code that is unreadable or dangerous is unacceptable. All lab submissions are evaluated against the following standards:

1. **SQL Keyword Casing**: All standard SQL reserved keywords must be in **UPPERCASE** (`SELECT`, `FROM`, `WHERE`, `ORDER BY`, `JOIN`, `AS`).
2. **Clause Indentation & Line Breaks**: Each major clause must begin on a new line. Never submit monolithic single-line queries for multi-clause logic.
3. **Explicit Projection**: Use of `SELECT *` is prohibited in production lab submissions unless explicitly requested for exploratory table schema audits. Always project named columns.
4. **Column & Table Aliasing**: Whenever expressions, aggregations, or multi-table joins are used, meaningful aliases must be supplied (`AS total_compensation`, `FROM employees e`).
5. **DML Safety Protocols**: Any submission containing an `UPDATE` or `DELETE` statement must include the accompanying pre-execution `SELECT` verification query used to audit row targeting.

---

## AI Augmentation & Academic Integrity Policy
In alignment with the **AI Practitioner Model**:
- **Permitted AI Use**: Students are encouraged to use AI tools (ChatGPT, Gemini, Claude) as an interactive tutor—for example, asking *"Explain why this PostgreSQL error occurred"* or *"What is the difference between WHERE and HAVING?"*.
- **Prohibited AI Use**: Copy-pasting problem statements into an AI and blindly submitting the output without understanding or validation is strictly prohibited.
- **Verification Rule**: During synchronous in-class sessions, students will be asked to live-code or explain query mechanisms in real-time. Full credit requires being able to articulate *why* your query works.
