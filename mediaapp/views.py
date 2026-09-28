from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import MediaJob
from .forms import MediaUploadForm
from .tasks import process_media_task

def upload_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()
            process_media_task(job.id)
            return redirect('job_monitoring', job_id=job.id)
        else:
            print("Form Errors:", form.errors)
    else:
        form = MediaUploadForm()
    return render(request, 'upload.html', {'form': form})

def dashboard_view(request):
    all_jobs = MediaJob.objects.all().order_by('-created_at')
    
    context = {
        'recent_jobs': all_jobs[:15],
        'total_files': all_jobs.count(),
        'total_jobs': all_jobs.count(),
        'pending_jobs': all_jobs.filter(status='PENDING').count(),
        'processing_jobs': all_jobs.filter(status='PROCESSING').count(),
        'completed_jobs': all_jobs.filter(status='COMPLETED').count(),
        'failed_jobs': all_jobs.filter(status='FAILED').count(),
    }
    return render(request, 'dashboard.html', context)

def job_monitoring_view(request, job_id):
    job = get_object_or_404(MediaJob, id=job_id)
    
    five_minutes_ago = timezone.now() - timedelta(minutes=5)
    stuck_jobs = MediaJob.objects.filter(
        created_at__lte=five_minutes_ago,
        status__in=['PENDING', 'PROCESSING']
    )
    failed_jobs = MediaJob.objects.filter(status='FAILED').order_by('-created_at')[:5]

    context = {
        'job': job,
        'stuck_jobs': stuck_jobs,
        'failed_jobs': failed_jobs,
    }
    return render(request, 'job_monitoring.html', context)

def api_job_status(request, job_id):
    job = get_object_or_404(MediaJob, id=job_id)
    return JsonResponse({
        'status': job.status,
        'processed_url': job.processed_file.url if job.processed_file else None,
        'error': job.error_message
    })

def delete_job_view(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(MediaJob, id=job_id)
        if job.original_file:
            job.original_file.delete(save=False)
        if job.processed_file:
            job.processed_file.delete(save=False)
        job.delete()
    return redirect('dashboard')