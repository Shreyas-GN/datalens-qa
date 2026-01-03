SCHEMA_DEFINITION = {
    "id": {
        "type": "string",
        "required": True,
        "nullable": False,
    },
    "date": {
        "type": "date",
        "required": True,
        "nullable": False,
    },
    "amount": {
        "type": "number",
        "required": True,
        "nullable": False,
    },
    "category": {
        "type": "string",
        "required": False,
        "nullable": True,
    },
    "status": {
        "type": "enum",
        "required": False,
        "nullable": True,
        "allowed_values": ["SUCCESS", "FAILED", "PENDING"],
    }
}