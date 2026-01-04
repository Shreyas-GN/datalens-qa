from datetime import datetime

QUALITY_RULES = {
    "amount": {
        "min": 0,
        "max": 1_000_000,   # extreme value threshold
    },
    "date": {
        "max_date": datetime.utcnow().date(),
    }
}