import os
from uuid import uuid4

from fastapi import UploadFile

from app.core.security import sanitize_filename


def save_upload(file: UploadFile, upload_dir: str) -> str:
	os.makedirs(upload_dir, exist_ok=True)
	safe_name = sanitize_filename(file.filename or "upload")
	file_id = f"{uuid4().hex}_{safe_name}"
	file_path = os.path.join(upload_dir, file_id)

	with open(file_path, "wb") as handle:
		handle.write(file.file.read())
	print(f"Saved file to {file_path}")
	return file_path
