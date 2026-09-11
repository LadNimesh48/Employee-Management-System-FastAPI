import shutil

from fastapi import UploadFile
import os
import uuid

UPLOAD_DIC = "uploads/profile_images"

os.makedirs(UPLOAD_DIC, exist_ok=True)

def upload_file(file:UploadFile):
    
    extension = os.path.splitext(file.filename)[1]
    fileName = (f"{uuid.uuid4()}.{extension}")
    
    filePath = os.path.join(UPLOAD_DIC,fileName)
    
    with open(filePath, 'wb') as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    return f"{UPLOAD_DIC}/{fileName}"
    
    