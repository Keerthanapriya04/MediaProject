from django.contrib import admin
from .models import MediaJob

@admin.register(MediaJob)
class MediaJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_file', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('original_file',)