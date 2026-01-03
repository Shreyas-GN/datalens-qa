from django.urls import path
from .views import upload_file, health_check

urlpatterns = [
    path('upload/', upload_file, name='upload-file'),
    path('health/', health_check, name='health-check'),
]