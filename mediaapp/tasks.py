import os
from celery import shared_task
from django.conf import settings
from PIL import Image
from .models import MediaJob

@shared_task
def process_media_task(job_id):
    try:
        job = MediaJob.objects.get(id=job_id)
        job.status = 'PROCESSING'
        job.save()

        file_path = job.original_file.path
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        output_dir = os.path.join(settings.MEDIA_ROOT, 'processed')
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f"processed_{filename}"
        output_path = os.path.join(output_dir, output_filename)

        # Image processing using Pillow
        if ext in ['.jpg', '.jpeg', '.png', '.webp']:
            with Image.open(file_path) as img:
                img.thumbnail((800, 800))
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(output_path, optimize=True, quality=80)

        # Video processing using FFmpeg
        elif ext in ['.mp4', '.mov', '.avi', '.mkv']:
            output_filename = f"processed_{os.path.splitext(filename)[0]}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            os.system(f'ffmpeg -y -i "{file_path}" -vcodec libx264 -crf 28 "{output_path}"')

        # Update database on completion
        job.processed_file = f"processed/{output_filename}"
        job.status = 'COMPLETED'
        job.save()

    except Exception as e:
        job.status = 'FAILED'
        job.error_message = str(e)
        job.save()
        raise e