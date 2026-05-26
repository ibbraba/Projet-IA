from typing import Any
import re


def _tokenize(text: str) -> set[str]:
	words = re.findall(r"[A-Za-zÀ-ÿ0-9+#.-]+", text.lower())
	return {word for word in words if len(word) > 2}

def generate_suggestions(cv_text: str, job_text: str) -> list[dict[str, Any]]:
	job_tokens = _tokenize(job_text)
	cv_tokens = _tokenize(cv_text)

	missing = sorted(job_tokens.difference(cv_tokens))

	suggestions: list[dict[str, Any]] = []

	for term in missing[:5]:
		suggestions.append(
			{
				"title": f"Ajouter {term}",
				"description": (
					f"Le poste indique la compétence « {term} ». "
					"Si vous la possédez, pensez à la mettre en avant dans votre CV."
				),
				"priority": "medium",
			}
		)

	if not suggestions:
		suggestions.append(
			{
				"title": "Valoriser vos réalisations",
				"description": (
					"Ajoutez des résultats chiffrés ou des impacts concrets "
					"pour renforcer la qualité de votre candidature."
				),
				"priority": "low",
			}
		)

	print(
		f"[LLM Suggestions] Generated {len(suggestions)} suggestions "
		f"based on missing terms: {missing[:5]}"
	)

	print(f"[LLM Suggestions] Suggestions: {suggestions}")

	return suggestions