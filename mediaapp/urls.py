from django.urls import path

from .views import dashboard, upload_media


urlpatterns = [
    path("", dashboard, name="dashboard"),

    path(
        "upload/",
        upload_media,
        name="upload_media"
    ),
]