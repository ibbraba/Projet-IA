from typing import Any


def build_visualization_data(score: float) -> dict[str, Any]:
	safe_score = max(0.0, min(100.0, float(score)))

	labels = ["Technical Skills", "Soft Skills", "Experience", "Education", "ATS Keywords"]
	section_scores = [
		safe_score,
		max(0.0, safe_score - 10.0),
		max(0.0, safe_score - 5.0),
		max(0.0, safe_score - 15.0),
		max(0.0, safe_score - 8.0),
	]
	print(f"[Visualization] Computed radar data with score: {safe_score}")
	print(f"[Visualization] Section scores: {section_scores}")
	print(f"[Visualization] Labels: {labels}")

	return {
		"score": safe_score,
		"radar": {
			"labels": labels,
			"cv_data": section_scores,
			"job_data": [100.0] * len(labels),
			"max_value": 100.0,
		},
		"breakdown": {
			"technical_skills": section_scores[0],
			"soft_skills": section_scores[1],
			"experience": section_scores[2],
			"education": section_scores[3],
			"keywords_ats": section_scores[4],
		},
	}
