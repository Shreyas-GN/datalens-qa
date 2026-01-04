from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from uploads.services.file_validation import (
    validate_uploaded_file,
    FileValidationError,
)
from uploads.services.file_storage import store_uploaded_file
from uploads.services.schema_validation import validate_schema
from uploads.services.data_quality import run_data_quality_checks
from uploads.services.execution_log import ExecutionLogger
import time


@csrf_exempt
@require_POST
def upload_file(request):
    logger = ExecutionLogger()
    uploaded_file = request.FILES.get("file")

    # Step 1: File validation
    start = time.time()
    try:
        validate_uploaded_file(uploaded_file)
        logger.log_step(
            "file_validation",
            "success",
            duration_ms=int((time.time() - start) * 1000),
        )
    except FileValidationError as e:
        logger.log_step(
            "file_validation",
            "failed",
            details={"error": str(e)},
        )
        return JsonResponse(
            {"error": str(e), "execution_log": logger.build_report()},
            status=400,
        )

    # Step 2: File storage
    start = time.time()
    file_info = store_uploaded_file(uploaded_file)
    logger.log_step(
        "file_storage",
        "success",
        details={"path": file_info["path"]},
        duration_ms=int((time.time() - start) * 1000),
    )

    # Step 3: Schema validation
    start = time.time()
    schema_result = validate_schema(file_info["path"])
    logger.log_step(
        "schema_validation",
        "warning" if not schema_result["schema_valid"] else "success",
        details=schema_result,
        duration_ms=int((time.time() - start) * 1000),
    )

    # Step 4: Data quality checks
    start = time.time()
    quality_report = run_data_quality_checks(file_info["path"])
    logger.log_step(
        "data_quality_checks",
        "success",
        details=quality_report,
        duration_ms=int((time.time() - start) * 1000),
    )

    return JsonResponse(
        {
            "message": "File processed successfully",
            "file": file_info,
            "schema_validation": schema_result,
            "data_quality": quality_report,
            "execution_log": logger.build_report(),
        },
        status=200,
    )


def health_check(request):
    return JsonResponse({"status": "ok"})