from typing import Any
import re


def _tokenize(text: str) -> set[str]:
	words = re.findall(r"[A-Za-zÀ-ÿ0-9+#.-]+", text.lower())
	return {word for word in words if len(word) > 2}


def generate_suggestions(cv_text: str, job_text: str) -> dict[str, Any]:
	job_tokens = _tokenize(job_text)
	cv_tokens = _tokenize(cv_text)

	missing = sorted(job_tokens.difference(cv_tokens))
	suggestions: list[dict[str, Any]] = []

	for term in missing[:5]:
		suggestions.append(
			{
				"title": f"Add {term}",
				"description": (
					f"The job description mentions '{term}'. Consider adding it if relevant."
				),
				"priority": "medium",
			}
		)

	if not suggestions:
		suggestions.append(
			{
				"title": "Highlight key achievements",
				"description": (
					"Emphasize measurable outcomes to strengthen alignment with the role."
				),
				"priority": "low",
			}
		)
	print(f"[LLM Suggestions] Generated {len(suggestions)} suggestions based on missing terms: {missing[:5]}")
	print(f"[LLM Suggestions] Suggestions: {suggestions}")
	return {"suggestions": suggestions}
