from pathlib import Path

ALLOWED_EXTENSIONS = {".csv", ".xls", ".xlsx"}
MAX_FILE_SIZE_MB = 10

def get_extension(filename):
    return Path(filename).suffix.lower()