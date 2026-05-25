from typing import Any


def compute_score(match_result: dict[str, Any]) -> float:
	return float(match_result.get("score", 0.0))
