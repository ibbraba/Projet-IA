from pydantic import BaseModel


class HealthResponse(BaseModel):
	status: str


class UploadResponse(BaseModel):
	upload_id: str
	extracted_text: str | None = None


class AnalyzeRequest(BaseModel):
	job_description: str
	cv_text: str | None = None


class AnalyzeResponse(BaseModel):
	score: float
	message: str
