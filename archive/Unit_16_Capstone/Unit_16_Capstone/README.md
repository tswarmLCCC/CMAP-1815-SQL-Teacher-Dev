# Capstone Project: DataCo Global Logistics Engine

## Mission

You are the lead Data Architect for DataCo Global Logistics. The organization is currently suffering from operational paralysis due to a massive, redundant flat-file data dump. Your task is to transform this raw chaos into a high-speed, secure, and predictive intelligence engine.

---

## Environment & Data Ingestion

The raw dataset contains over 180,000 rows. Because it contains Spanish accent marks, you must specify the correct encoding during import to avoid UTF-8 translation errors.

1. Create the staging table using `sql/Setup_Staging.sql`.
2. Run this command in your terminal from the project root to import the data:

```bash
PGPASSWORD=postgres psql -U postgres -h db -d mydb -c "\copy raw_staging FROM 'Unit_16_Capstone/data/DataCoSupplyChainDataset.csv' WITH CSV HEADER ENCODING 'LATIN1';"
```

---

## Architectural Requirements

You are not just writing queries; you are building an engine. Your work will be evaluated on:

1. **Relational Integrity (3NF):** Eliminate all data redundancies. If a table contains repeating groups, your schema is flawed.
2. **Performance Optimization:** Use `EXPLAIN ANALYZE` to verify your query paths. Implement B-Tree indexes on high-traffic foreign keys and lookup columns.
3. **Advanced Analytical Logic:** Your `v_supply_chain_intelligence` view must utilize CTEs, Window Functions, and `CASE` statements.
4. **AI Grounding:** Integrate MindsDB to provide predictive insights. You must document the `_confidence` score of your predictions.

---

## Deliverables

- `init_schema.sql`: The complete architectural script.
- `Data_Dictionary.md`: The technical blueprint of your system.