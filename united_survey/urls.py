
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("organization.urls")),
    path("", include("info_pages.urls")),
    path("users/", include("users.urls")),
    path("surveys/", include("djf_surveys.urls"))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
