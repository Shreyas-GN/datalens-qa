from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def root(request):
    return JsonResponse({
        "service": "DataLens QA Backend",
        "status": "running"
    })

urlpatterns = [
    path('', root),                 # GET-friendly root
    path('admin/', admin.site.urls),
    path('api/', include('uploads.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )