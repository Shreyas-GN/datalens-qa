from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from uploads.services.file_validation import (
    validate_uploaded_file,
    FileValidationError,
)
from uploads.services.file_storage import store_uploaded_file
from uploads.services.schema_validation import validate_schema


@csrf_exempt
@require_POST
def upload_file(request):
    uploaded_file = request.FILES.get("file")

    try:
        validate_uploaded_file(uploaded_file)
    except FileValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)

    # Store the file
    file_info = store_uploaded_file(uploaded_file)

    # Validate schema
    schema_result = validate_schema(file_info["path"])

    return JsonResponse(
        {
            "message": "File uploaded and validated",
            "file": file_info,
            "schema_validation": schema_result,
        },
        status=200
    )


def health_check(request):
    return JsonResponse({"status": "ok"})