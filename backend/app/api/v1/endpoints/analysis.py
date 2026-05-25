from fastapi import APIRouter

from app.models.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter()


@router.post("/", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
	return AnalyzeResponse(score=0.0, message="analysis placeholder")
