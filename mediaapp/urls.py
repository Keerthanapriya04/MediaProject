from django.urls import path
from . import views


urlpatterns = [
    # Upload page
    path('', views.upload_view, name='upload'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Job monitoring
    path(
        'monitoring/<int:job_id>/',
        views.job_monitoring_view,
        name='job_monitoring'
    ),

    # Job status API
    path(
        'api/status/<int:job_id>/',
        views.api_job_status,
        name='api_job_status'
    ),

    # Delete a job
    path(
        'delete/<int:job_id>/',
        views.delete_job_view,
        name='delete_job'
    ),
]