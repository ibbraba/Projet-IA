from pydantic import BaseModel


class HealthResponse(BaseModel):
	status: str


class UploadResponse(BaseModel):
	upload_id: str


class AnalyzeRequest(BaseModel):
	job_description: str
	cv_text: str | None = None


class AnalyzeResponse(BaseModel):
	score: float
	message: str
