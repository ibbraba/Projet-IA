from typing import Any


def process_cv_text(text: str, language: str = "fr") -> dict[str, Any]:
	return {"entities": {}, "metadata": {"language": language}}
