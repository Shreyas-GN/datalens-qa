import pandas as pd
from dateutil.parser import parse as parse_date
from uploads.schema import SCHEMA_DEFINITION


class SchemaValidationError(Exception):
    pass


def _load_dataframe(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith((".xls", ".xlsx")):
        return pd.read_excel(file_path)
    else:
        raise SchemaValidationError("Unsupported file format")


def _count_type_violations(series, rules):
    violations = 0

    for value in series.dropna():
        try:
            if rules["type"] == "number":
                float(value)

            elif rules["type"] == "string":
                str(value)

            elif rules["type"] == "date":
                parse_date(str(value))

            elif rules["type"] == "enum":
                if value not in rules["allowed_values"]:
                    raise ValueError()

        except Exception:
            violations += 1

    return violations


def validate_schema(file_path: str) -> dict:
    df = _load_dataframe(file_path)

    result = {
        "schema_valid": True,
        "total_rows": int(len(df)),
        "missing_columns": [],
        "unexpected_columns": [],
        "null_violations": {},
        "type_violations": {},
    }

    df_columns = set(df.columns)
    expected_columns = set(SCHEMA_DEFINITION.keys())

    # Missing required columns
    for column, rules in SCHEMA_DEFINITION.items():
        if rules["required"] and column not in df_columns:
            result["missing_columns"].append(column)
            result["schema_valid"] = False

    # Unexpected columns (allowed but flagged)
    result["unexpected_columns"] = list(df_columns - expected_columns)

    # Column-level validation
    for column, rules in SCHEMA_DEFINITION.items():
        if column not in df_columns:
            continue

        series = df[column]

        # Null checks
        if not rules["nullable"]:
            null_count = int(series.isnull().sum())
            if null_count > 0:
                result["null_violations"][column] = null_count
                result["schema_valid"] = False

        # Type checks
        type_errors = _count_type_violations(series, rules)
        if type_errors > 0:
            result["type_violations"][column] = type_errors
            result["schema_valid"] = False

    return result