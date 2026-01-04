# DataLens QA — Data Quality & Risk Analyzer

DataLens QA is a backend system that checks whether tabular data (CSV / Excel) is **safe to ingest into analytics or production systems**.

Instead of failing jobs or silently accepting bad data, it **analyzes data quality and returns a clear decision with reasons**.

---

## What problem it solves

In real projects, bad data causes:
- Incorrect reports
- Broken dashboards
- Silent data corruption

Most systems don’t explain *why* data is unsafe.  
DataLens QA does.

---

## Key features

- **File validation**
  - Accepts CSV / Excel only
  - Detects empty or invalid files

- **Schema validation**
  - Missing or extra columns
  - Wrong data types
  - Null value violations

- **Data quality checks**
  - Duplicate rows
  - Negative or extreme numeric values
  - Invalid or future dates
  - Empty rows
  - Percentage-based summaries

- **Decision engine**
  - Risk score (0–100)
  - Verdict: `SAFE`, `REVIEW`, `UNSAFE`
  - Clear ingestion recommendation

- **Explainability**
  - Step-by-step execution log
  - No silent failures
  - Debuggable results

---

## Example outcome

Instead of raw errors, the system returns:

- Verdict: `REVIEW`
- Risk score: `37`
- Main issues:
  - 12% duplicate rows
  - 5 negative values
  - 2 future dates
- Recommendation:
  > Review issues before ingestion

---

## Tech stack

- Python
- Django (API-first)
- Pandas / NumPy
- SQLite
- GitHub Actions (CI)

---

## Why this project

Built to practice **real-world data engineering problems**:
- Defensive ingestion
- Data quality gating
- Explainable backend systems

This reflects how internal data platforms are designed in production.

---

## Author

Independently built as a learning and portfolio project by Shreyas GN
