from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .tasks import process_image_task, process_video_task

app = FastAPI(title="Media Processing Microservice")

class JobRequest(BaseModel):
    file_key: str
    output_key: str
    file_type: str  

@app.post("/api/v1/process")
def create_processing_job(job: JobRequest):
    if job.file_type == 'image':
        task = process_image_task.delay(job.file_key, job.output_key)
    elif job.file_type == 'video':
        task = process_video_task.delay(job.file_key, job.output_key)
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Use 'image' or 'video'.")
        
    return {"job_id": task.id, "status": "QUEUED"}