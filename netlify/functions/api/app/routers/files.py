from fastapi import APIRouter, UploadFile, File
from ..utils import save_upload_file
from ..core import settings

router = APIRouter()

@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    path = await save_upload_file(file, settings.UPLOAD_DIR)
    return {"path": path}
