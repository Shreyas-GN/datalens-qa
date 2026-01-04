import uuid
import hashlib
from pathlib import Path
from django.conf import settings


def compute_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def store_uploaded_file(uploaded_file):
    upload_dir = Path(settings.MEDIA_ROOT) / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid.uuid4()}_{uploaded_file.name}"
    file_path = upload_dir / stored_name

    with open(file_path, "wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    file_hash = compute_file_hash(file_path)

    return {
        "original_name": uploaded_file.name,
        "stored_name": stored_name,
        "path": str(file_path),
        "size": uploaded_file.size,
        "hash": file_hash,
    }