def compute_risk_score(schema_result, quality_result):
    score = 0.0

    # Schema violations are critical
    if not schema_result["schema_valid"]:
        score += 40

    summary = quality_result["summary_percentages"]

    score += summary.get("duplicates_pct", 0) * 0.3
    score += summary.get("negative_amount_pct", 0) * 0.3
    score += summary.get("future_date_pct", 0) * 0.2
    score += summary.get("empty_rows_pct", 0) * 0.2

    return min(round(score, 2), 100.0)


def verdict_from_score(score):
    if score == 0:
        return "HEALTHY"
    elif score <= 25:
        return "NEEDS_REVIEW"
    else:
        return "UNSAFE"


def prioritize_issues(schema_result, quality_result):
    issues = []

    if not schema_result["schema_valid"]:
        if schema_result["missing_columns"]:
            issues.append({
                "category": "SCHEMA",
                "severity": "HIGH",
                "message": f"Missing required columns: {schema_result['missing_columns']}",
            })

        if schema_result["unexpected_columns"]:
            issues.append({
                "category": "SCHEMA",
                "severity": "LOW",
                "message": f"Unexpected columns present: {schema_result['unexpected_columns']}",
            })

    if quality_result["duplicate_rows"] > 0:
        issues.append({
            "category": "INTEGRITY",
            "severity": "MEDIUM",
            "message": f"{quality_result['duplicate_rows']} duplicate rows detected",
        })

    if quality_result["future_date_rows"] > 0:
        issues.append({
            "category": "VALIDITY",
            "severity": "MEDIUM",
            "message": f"{quality_result['future_date_rows']} future-dated records found",
        })

    if quality_result["empty_rows"] > 0:
        issues.append({
            "category": "COMPLETENESS",
            "severity": "LOW",
            "message": f"{quality_result['empty_rows']} empty rows detected",
        })

    return issues