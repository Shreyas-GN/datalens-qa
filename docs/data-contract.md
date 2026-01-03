# DataLens QA — Data Contract

## Purpose

This document defines the **input, processing, and output contract** for DataLens QA.
It exists to eliminate ambiguity, enforce consistency, and reduce data-related errors
before they reach the processing pipeline.

Any dataset that violates this contract will be **rejected early** with a clear error message.

---

## 1. Accepted Input Formats

The system accepts the following file types:

- CSV (`.csv`)
- Excel (`.xls`, `.xlsx`)

Unsupported file types (e.g., PDF, JSON, TXT) are rejected at upload time.

---

## 2. File Size Limits

- Maximum file size: **10 MB**
- Empty files are not allowed

Files exceeding size limits or containing no data will be rejected.

---

## 3. Dataset Structure Requirements

### 3.1 Required Columns

Each uploaded dataset **must** contain the following columns:

| Column Name | Description                        | Required |
|------------|------------------------------------|----------|
| `id`       | Unique record identifier           | Yes      |
| `date`     | Business or transaction date       | Yes      |
| `amount`   | Numeric value associated with row  | Yes      |

Column names are **case-sensitive**.

---

### 3.2 Data Type Expectations

| Column  | Expected Type | Notes |
|--------|---------------|-------|
| `id`   | String / Int  | Must be non-null and unique |
| `date` | Date / String | Must be parseable as a date |
| `amount` | Number      | Must be a valid numeric value |

Rows with invalid data types are flagged during validation.

---

## 4. Data Quality Assumptions

The following quality checks are applied:

- Missing value detection
- Duplicate record detection (based on `id`)
- Basic range validation on numeric fields

These checks **do not modify** the original data.
They only report findings.

---

## 5. Processing Behavior

- Files that violate schema requirements are rejected before processing.
- Data quality checks are deterministic and repeatable.
- No automatic data correction is performed in the MVP.

All processing steps are recorded in an explainable processing log.

---

## 6. Output Artifacts

For each successfully processed dataset, the system generates:

1. **Data Quality Report**
   - Validation errors
   - Warnings
   - Completeness metrics

2. **Summary Report**
   - Record counts
   - Aggregated statistics

3. **Processing Explanation Log**
   - Step-by-step description of validation and processing actions

Reports are generated in standard, downloadable formats.

---

## 7. Failure Handling

If a dataset violates this contract:
- Processing is stopped
- A clear error message is returned
- No partial or silent failures occur

This ensures predictable and auditable behavior.

---

## 8. Contract Evolution

This contract is expected to evolve as the system grows.
Any changes must be documented and versioned.

Breaking changes should be avoided in production environments.