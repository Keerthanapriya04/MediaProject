from django.contrib import admin

from .models import MediaFile, ProcessingJob


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):

    list_display = (
        "original_name",
        "media_type",
        "file_size",
        "uploaded_at",
    )

    list_filter = (
        "media_type",
        "uploaded_at",
    )

    search_fields = (
        "original_name",
    )

    ordering = (
        "-uploaded_at",
    )


@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):

    list_display = (
        "media",
        "operation",
        "status",
        "retry_count",
        "created_at",
        "started_at",
        "completed_at",
    )

    list_filter = (
        "status",
        "operation",
        "created_at",
    )

    search_fields = (
        "media__original_name",
        "operation",
        "error_message",
    )

    ordering = (
        "-created_at",
    )