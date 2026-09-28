import os
from PIL import Image
import ffmpeg
from .celery_app import celery_app
from .storage import download_from_s3, upload_to_s3

@celery_app.task(bind=True, name="process_image_task")
def process_image_task(self, file_key: str, output_key: str):
    local_input = f"/tmp/{os.path.basename(file_key)}"
    local_output = f"/tmp/processed_{os.path.basename(output_key)}"
    
    try:
        
        download_from_s3(file_key, local_input)
        
       
        with Image.open(local_input) as img:
            img.thumbnail((800, 800))
            img.save(local_output, optimize=True, quality=85)
            
        
        cdn_url = upload_to_s3(local_output, output_key)
        return {"status": "SUCCESS", "url": cdn_url}
        
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5, max_retries=3)
        
    finally:
       
        if os.path.exists(local_input): os.remove(local_input)
        if os.path.exists(local_output): os.remove(local_output)


@celery_app.task(bind=True, name="process_video_task")
def process_video_task(self, file_key: str, output_key: str):
    local_input = f"/tmp/{os.path.basename(file_key)}"
    local_output = f"/tmp/compressed_{os.path.basename(output_key)}"
    
    try:
        download_from_s3(file_key, local_input)
        
        
        (
            ffmpeg
            .input(local_input)
            .output(local_output, vcodec='libx264', crf=28, acodec='aac')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        
        cdn_url = upload_to_s3(local_output, output_key)
        return {"status": "SUCCESS", "url": cdn_url}
        
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10, max_retries=3)
        
    finally:
        if os.path.exists(local_input): os.remove(local_input)
        if os.path.exists(local_output): os.remove(local_output)