from typing import Any
import re


def process_cv_text(text: str, language: str = "fr") -> dict[str, Any]:
	clean_text = text.strip()
	text_lower = clean_text.lower()

	skill_catalog: dict[str, list[str]] = {
		"languages": [
			"Python",
			"JavaScript",
			"TypeScript",
			"Java",
			"C++",
			"C#",
			"Go",
			"Rust",
			"PHP",
			"Ruby",
			"Swift",
			"Kotlin",
			"Scala",
		],
		"frameworks": [
			"React",
			"Vue",
			"Angular",
			"Django",
			"Flask",
			"FastAPI",
			"Express",
			"NestJS",
			"Spring",
			"Laravel",
			"Rails",
		],
		"databases": [
			"PostgreSQL",
			"MySQL",
			"MongoDB",
			"Redis",
			"Elasticsearch",
			"Oracle",
			"SQL Server",
			"Cassandra",
			"DynamoDB",
		],
		"devops": [
			"Docker",
			"Kubernetes",
			"Jenkins",
			"GitLab CI",
			"GitHub Actions",
			"Terraform",
			"Ansible",
			"AWS",
			"Azure",
			"GCP",
		],
		"tools": [
			"Git",
			"Jira",
			"Confluence",
			"Slack",
			"VS Code",
			"IntelliJ",
			"Postman",
			"Figma",
			"Tableau",
			"Power BI",
		],
	}

	skills: list[dict[str, Any]] = []
	for category, items in skill_catalog.items():
		for skill in items:
			if skill.lower() in text_lower:
				skills.append({"name": skill, "category": category, "mentioned": True})

	metadata: dict[str, str] = {"language": language}
	email_match = re.search(
		r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", clean_text
	)
	if email_match:
		metadata["email"] = email_match.group(0)

	phone_match = re.search(
		r"(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}", clean_text
	)
	if phone_match:
		metadata["phone"] = phone_match.group(0)

	linkedin_match = re.search(r"linkedin\.com/in/[\w-]+", clean_text, re.IGNORECASE)
	if linkedin_match:
		metadata["linkedin"] = linkedin_match.group(0)

	experience_keywords = [
	"experience",
	"worked",
	"developed",
	"engineer",
	"developer",
	"intern",
	"freelance",
	]

	experiences = [
		sentence.strip()
		for sentence in clean_text.split(".")
		if any(k in sentence.lower() for k in experience_keywords)
	]


	CERT_KEYWORDS = [
	"aws certified",
	"azure certified",
	"google cloud certified",
	"pmp",
	"scrum master",
	"oracle certified",
	]

	certifications = [
		cert for cert in CERT_KEYWORDS
		if cert in text_lower
	]

	LANGUAGE_MAP = {
	"français": "French",
	"french": "French",
	"anglais": "English",
	"english": "English",
	"espagnol": "Spanish",
	"spanish": "Spanish",
	"allemand": "German",
	}

	languages = list({
		LANGUAGE_MAP[k]
		for k in LANGUAGE_MAP
		if k in text_lower
	})
  
  
  	
	print(f"[NLP Processor] Extracted skills: {skills}")
	print(f"[NLP Processor] Extracted metadata: {metadata}")
	print(f"[NLP Processor] Extracted languages: {languages}")	
 #	print(f"[NLP Processor] Extracted certifications: {certifications}")
 

	return {
		"entities": {
			"skills": skills,
			"experiences": [],
			"education": [],
			"languages": languages,
			"certifications": certifications,
		},
		"metadata": metadata,
	}
