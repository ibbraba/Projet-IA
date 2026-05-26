from typing import Any


def compute_score(match_result: dict[str, Any]) -> float:
	score = match_result.get("score")
	if score is None:
		details = match_result.get("details", {})
		coverage = details.get("coverage", 0.0)
		return float(coverage)
	print(f"[Scoring] Raw score: {score}")

	try:
		return float(score)
	except (TypeError, ValueError):
		return 0.0
