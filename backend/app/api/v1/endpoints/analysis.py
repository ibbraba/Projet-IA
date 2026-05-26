from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.llm_suggestions import generate_suggestions
from app.services.nlp_processor import process_cv_text
from app.services.scoring import compute_score
from app.services.semantic_matcher import match_semantic
from app.services.visualization import build_visualization_data

router = APIRouter()

CURRENT_CV_TXT = Path("uploads/current_cv.txt")


@router.post("/", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:

    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="job_description is required")

    # check CV exists
    if not CURRENT_CV_TXT.exists():
        raise HTTPException(
            status_code=404,
            detail="No CV uploaded. Please upload a CV first."
        )

    # read stored CV
    cv_text = CURRENT_CV_TXT.read_text(encoding="utf-8")

    # pipeline
    _ = process_cv_text(cv_text)
    match_result = match_semantic(cv_text, request.job_description)
    score = compute_score(match_result)
    visualization = build_visualization_data(score)
    suggestions = generate_suggestions(cv_text, request.job_description)

    details = match_result.get("details", {})
    strengths = details.get("matched_terms", [])
    weaknesses = details.get("missing_terms", [])



    return AnalyzeResponse(
        score=score,
        message="analysis complete",
        visualization=visualization,
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions
    )
