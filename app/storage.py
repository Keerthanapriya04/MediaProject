import os
import shutil

UPLOAD_DIR = "media/uploads"
PROCESSED_DIR = "media/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def download_from_s3(file_key: str, download_path: str):
    
    if os.path.exists(file_key):
        shutil.copy(file_key, download_path)
    return download_path

def upload_to_s3(file_path: str, file_key: str):
    
    dest_path = os.path.join(PROCESSED_DIR, os.path.basename(file_path))
    shutil.copy(file_path, dest_path)
    return f"/media/processed/{os.path.basename(file_path)}"