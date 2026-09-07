from pathlib import Path

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import MediaUploadForm
from .models import MediaFile, ProcessingJob


def dashboard(request):
    """
    Display the main media processing dashboard.
    """

    total_files = MediaFile.objects.count()

    total_jobs = ProcessingJob.objects.count()

    pending_jobs = ProcessingJob.objects.filter(
        status="PENDING"
    ).count()

    processing_jobs = ProcessingJob.objects.filter(
        status="PROCESSING"
    ).count()

    completed_jobs = ProcessingJob.objects.filter(
        status="COMPLETED"
    ).count()

    failed_jobs = ProcessingJob.objects.filter(
        status="FAILED"
    ).count()

    recent_jobs = (
        ProcessingJob.objects
        .select_related("media")
        .order_by("-created_at")[:10]
    )

    context = {
        "total_files": total_files,
        "total_jobs": total_jobs,
        "pending_jobs": pending_jobs,
        "processing_jobs": processing_jobs,
        "completed_jobs": completed_jobs,
        "failed_jobs": failed_jobs,
        "recent_jobs": recent_jobs,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


def upload_media(request):
    """
    Handle image/video upload and create a processing job.
    """

    if request.method == "POST":

        form = MediaUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            # --------------------------------------------
            # Get uploaded file
            # --------------------------------------------

            uploaded_file = form.cleaned_data["file"]

            # --------------------------------------------
            # Create MediaFile object
            # --------------------------------------------

            media_file = form.save(commit=False)

            # Store only the filename
            media_file.original_name = Path(
                uploaded_file.name
            ).name

            # --------------------------------------------
            # Detect media type
            # --------------------------------------------

            if uploaded_file.content_type.startswith("image/"):

                media_file.media_type = "IMAGE"

            elif uploaded_file.content_type.startswith("video/"):

                media_file.media_type = "VIDEO"

            else:

                form.add_error(
                    "file",
                    "Unsupported media type."
                )

                return render(
                    request,
                    "upload.html",
                    {"form": form}
                )

            # --------------------------------------------
            # Store file size
            # --------------------------------------------

            media_file.file_size = uploaded_file.size

            # --------------------------------------------
            # Save file
            # --------------------------------------------

            media_file.save()

            # --------------------------------------------
            # Create processing job
            # --------------------------------------------

            ProcessingJob.objects.create(
                media=media_file,
                operation=form.cleaned_data["operation"],
                status="PENDING",
            )

            # --------------------------------------------
            # Success message
            # --------------------------------------------

            messages.success(
                request,
                "Media uploaded successfully. "
                "Processing job created."
            )

            return redirect("dashboard")

    else:

        form = MediaUploadForm()

    return render(
        request,
        "upload.html",
        {
            "form": form
        }
    )