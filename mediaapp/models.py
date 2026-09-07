from django.db import models


class MediaFile(models.Model):

    MEDIA_TYPES = [
        ("IMAGE", "Image"),
        ("VIDEO", "Video"),
    ]

    file = models.FileField(upload_to="uploads/")

    original_name = models.CharField(
        max_length=255
    )

    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_TYPES
    )

    file_size = models.BigIntegerField(
        default=0
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.original_name


class ProcessingJob(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    media = models.ForeignKey(
        MediaFile,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    operation = models.CharField(
        max_length=100
    )

    output_file = models.FileField(
        upload_to="processed/",
        blank=True,
        null=True
    )

    error_message = models.TextField(
        blank=True,
        null=True
    )

    retry_count = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    started_at = models.DateTimeField(
        blank=True,
        null=True
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.media.original_name} - {self.status}"