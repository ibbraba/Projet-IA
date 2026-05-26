from pydantic import BaseModel
from typing import Any


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
    visualization: dict[str, Any]
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[dict[str, Any]]
