from pathlib import Path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    Path("accounts/", include('allauth.urls')),
    path("dashboard/", include("dashboard.urls")),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
