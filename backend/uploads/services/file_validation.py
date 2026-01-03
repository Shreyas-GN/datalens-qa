from uploads.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB, get_extension

class FileValidationError(Exception):
    pass

def validate_uploaded_file(file):
    if not file:
        raise FileValidationError("No file provided")

    ext = get_extension(file.name)
    if ext not in ALLOWED_EXTENSIONS:
        raise FileValidationError(f"Unsupported file type: {ext}")

    if file.size == 0:
        raise FileValidationError("Empty file is not allowed")

    size_mb = file.size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise FileValidationError("File size exceeds limit")
