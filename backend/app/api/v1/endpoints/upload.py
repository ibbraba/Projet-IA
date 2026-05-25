from fastapi import APIRouter, UploadFile, File, Depends

from app.dependencies import get_app_settings
from app.models.schemas import UploadResponse
from app.utils.file_handler import save_upload

router = APIRouter()


@router.post("/", response_model=UploadResponse)
def upload_cv(
	file: UploadFile = File(...),
	settings=Depends(get_app_settings),
) -> UploadResponse:
	file_path = save_upload(file, settings.upload_dir)
	return UploadResponse(upload_id=file_path)
