import uuid
from pathlib import Path
from django.conf import settings

def store_uploaded_file(file) -> dict:
    """
    Stores an uploaded file in a controlled location and returns metadata.
    """

    uploads_dir = Path(settings.MEDIA_ROOT) / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    unique_name = f"{uuid.uuid4()}_{file.name}"
    file_path = uploads_dir / unique_name

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return {
        "original_name": file.name,
        "stored_name": unique_name,
        "path": str(file_path),
        "size": file.size,
    }