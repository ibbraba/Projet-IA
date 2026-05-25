from typing import Any


def build_visualization_data(score: float) -> dict[str, Any]:
	return {"score": score, "radar": {}, "breakdown": {}}
