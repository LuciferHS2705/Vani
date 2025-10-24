import os
from fastapi import UploadFile
from uuid import uuid4

async def save_upload_file(upload_file: UploadFile, upload_dir: str) -> str:
    os.makedirs(upload_dir, exist_ok=True)
    ext = upload_file.filename.split('.')[-1]
    fname = f"{uuid4().hex}.{ext}"
    fpath = os.path.join(upload_dir, fname)
    with open(fpath, 'wb') as f:
        contents = await upload_file.read()
        f.write(contents)
    return fpath
