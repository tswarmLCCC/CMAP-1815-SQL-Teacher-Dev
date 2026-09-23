# Unit 2: Lab Evaluation Rubric (100 Points)

## Overview
This rubric is used to evaluate student submissions for the **Unit 2 Practical Lab: Targeted Retrieval & Precision Filtering**.

---

## Detailed Scoring Criteria

| Criteria | Exemplary (Full Points) | Competent (Partial Points) | Developing (Needs Revision) | Points |
| :--- | :--- | :--- | :--- | :---: |
| **1. Filtering Accuracy & Correct Logic** | All WHERE conditions accurately restrict rows per the prompt. Correct operators (`IN`, `BETWEEN`, `LIKE`, `IS NULL`) used throughout. | 1–2 minor filtering bugs (e.g. exclusive range instead of `BETWEEN`, minor condition omission). | Frequent logic errors; returned incorrect row sets. | **40** |
| **2. Boolean Precedence & Parentheses** | Parentheses correctly placed to disambiguate chained `AND` and `OR` logic; zero logical data leakage. | Query produces correct output, but relies on default precedence without defensive parentheses. | Omitted parentheses leading to incorrect records in the result set. | **20** |
| **3. Three-Valued Logic & NULL Handling** | Correct usage of `IS NULL` / `IS NOT NULL`. Zero instances of `= NULL` or `!= NULL`. | Minor misunderstanding of how NULL impacts aggregate/math expressions. | Used `= NULL`; failed to retrieve unpopulated records. | **15** |
| **4. Wildcards & Text Search Integrity** | Correct use of `%` and `_` wildcards; proper application of single quotes for literals and `ILIKE` for case-insensitivity. | Minor wildcard placement error (e.g. `%` missing at start or end). | Syntax errors in string matching or used double quotes for text literals. | **15** |
| **5. Formatting, Aliasing & Pagination** | Uppercase keywords, clean indentation, explicit column naming, and correct `LIMIT`/`OFFSET` pagination. | Inconsistent keyword casing or unformatted single-line queries. | Monolithic unformatted code; missing semicolons; unaliased calculated columns. | **10** |
| **Total** | | | | **100** |
