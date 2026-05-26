from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
import shutil

from app.dependencies import get_app_settings
from app.models.schemas import UploadResponse
from app.utils.extract_pdf_text import extract_pdf_text

router = APIRouter()

UPLOAD_DIR = Path("uploads")
CURRENT_CV_TXT = UPLOAD_DIR / "current_cv.txt"
CURRENT_CV_PDF = UPLOAD_DIR / "current_cv.pdf"


@router.post("/", response_model=UploadResponse)
def upload_cv(
    file: UploadFile = File(...),
    settings=Depends(get_app_settings),
) -> UploadResponse:

    UPLOAD_DIR.mkdir(exist_ok=True)

    # overwrite previous CV
    with open(CURRENT_CV_PDF, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # extract text
    cv_text = extract_pdf_text(str(CURRENT_CV_PDF))

    # save text
    CURRENT_CV_TXT.write_text(cv_text, encoding="utf-8")

    return UploadResponse(
        upload_id="current_cv",
        extracted_text=cv_text[:1000],
    )