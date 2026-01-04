import pandas as pd
from dateutil.parser import parse as parse_date
from uploads.quality_rules import QUALITY_RULES


def run_data_quality_checks(file_path: str) -> dict:
    # Load data
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    total_rows = len(df)

    report = {
        "total_rows": total_rows,
        "duplicate_rows": 0,
        "negative_amount_rows": 0,
        "extreme_amount_rows": 0,
        "future_date_rows": 0,
        "invalid_date_rows": 0,
        "empty_rows": 0,
        "row_quality_flags": {},
        "summary_percentages": {},
    }

    # --- Empty row detection ---
    empty_rows = df.isnull().all(axis=1)
    report["empty_rows"] = int(empty_rows.sum())

    # --- Duplicate detection (id) ---
    if "id" in df.columns:
        duplicates = df.duplicated(subset=["id"], keep=False)
        report["duplicate_rows"] = int(duplicates.sum())

    # --- Amount checks ---
    if "amount" in df.columns:
        amount_series = pd.to_numeric(df["amount"], errors="coerce")

        negative_amounts = amount_series < QUALITY_RULES["amount"]["min"]
        extreme_amounts = amount_series > QUALITY_RULES["amount"]["max"]

        report["negative_amount_rows"] = int(negative_amounts.sum())
        report["extreme_amount_rows"] = int(extreme_amounts.sum())

    # --- Date checks ---
    if "date" in df.columns:
        invalid_dates = 0
        future_dates = 0

        for value in df["date"]:
            try:
                parsed = parse_date(str(value)).date()
                if parsed > QUALITY_RULES["date"]["max_date"]:
                    future_dates += 1
            except Exception:
                invalid_dates += 1

        report["invalid_date_rows"] = invalid_dates
        report["future_date_rows"] = future_dates

    # --- Row-level flags (explainability) ---
    for idx, row in df.iterrows():
        flags = []

        if "id" in df.columns and duplicates.iloc[idx]:
            flags.append("DUPLICATE_ID")

        if "amount" in df.columns:
            amt = pd.to_numeric(row.get("amount"), errors="coerce")
            if pd.notnull(amt):
                if amt < QUALITY_RULES["amount"]["min"]:
                    flags.append("NEGATIVE_AMOUNT")
                if amt > QUALITY_RULES["amount"]["max"]:
                    flags.append("EXTREME_AMOUNT")

        if "date" in df.columns:
            try:
                parsed = parse_date(str(row.get("date"))).date()
                if parsed > QUALITY_RULES["date"]["max_date"]:
                    flags.append("FUTURE_DATE")
            except Exception:
                flags.append("INVALID_DATE")

        if row.isnull().all():
            flags.append("EMPTY_ROW")

        if flags:
            report["row_quality_flags"][int(idx)] = flags

    # --- Summary percentages ---
    def pct(count):
        return round((count / total_rows) * 100, 2) if total_rows else 0

    report["summary_percentages"] = {
        "duplicates_pct": pct(report["duplicate_rows"]),
        "negative_amount_pct": pct(report["negative_amount_rows"]),
        "extreme_amount_pct": pct(report["extreme_amount_rows"]),
        "future_date_pct": pct(report["future_date_rows"]),
        "empty_rows_pct": pct(report["empty_rows"]),
    }

    return report
