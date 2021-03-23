from django.contrib import admin
from dashboard.admin import dashboard_admin_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path("dashboard/admin/", dashboard_admin_site.urls),
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("dashboard/", include("dashboard.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
