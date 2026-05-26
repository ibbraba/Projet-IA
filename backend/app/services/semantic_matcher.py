from typing import Any
import re


def _tokenize(text: str) -> set[str]:
	words = re.findall(r"[A-Za-zÀ-ÿ0-9+#.-]+", text.lower())
	return {word for word in words if len(word) > 2}


def match_semantic(cv_text: str, job_text: str) -> dict[str, Any]:
	job_tokens = _tokenize(job_text)
	cv_tokens = _tokenize(cv_text)

	if not job_tokens:
		return {
			"score": 0.0,
			"details": {"matched_terms": [], "missing_terms": [], "coverage": 0.0},
		}

	matched = sorted(job_tokens.intersection(cv_tokens))
	missing = sorted(job_tokens.difference(cv_tokens))
	coverage = len(matched) / len(job_tokens)
 
	print(f"[Semantic Matcher] Job tokens: {len(job_tokens)}, CV tokens: {len(cv_tokens)}")
	print(f"[Semantic Matcher] Matched tokens: {len(matched)}, Missing tokens: {len(missing)}, Coverage: {coverage:.2%}")
 
	return {
		"score": round(coverage * 100, 2),
		"details": {
			"matched_terms": matched,
			"missing_terms": missing,
			"coverage": round(coverage * 100, 2),
		},
	}
