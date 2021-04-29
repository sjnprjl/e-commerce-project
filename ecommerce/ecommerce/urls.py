from pathlib import Path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


urlpatterns = [
    path("dashboard/", admin.site.urls),
    path("", include("main.urls")),
    path("accounts/", include("allauth.urls")),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
