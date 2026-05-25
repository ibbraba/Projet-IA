from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
	app_name: str
	environment: str
	log_level: str
	database_url: str
	redis_url: str
	upload_dir: str
	models_cache_dir: str
	spacy_model_fr: str
	spacy_model_en: str
	sentence_transformer_model: str
	anthropic_api_key: str
	openai_api_key: str


def get_settings() -> Settings:
	return Settings(
		app_name=os.getenv("APP_NAME", "CV Analyzer API"),
		environment=os.getenv("ENVIRONMENT", "development"),
		log_level=os.getenv("LOG_LEVEL", "info"),
		database_url=os.getenv("DATABASE_URL", ""),
		redis_url=os.getenv("REDIS_URL", ""),
		upload_dir=os.getenv("UPLOAD_DIR", "./uploads"),
		models_cache_dir=os.getenv("MODELS_CACHE_DIR", "./models_cache"),
		spacy_model_fr=os.getenv("SPACY_MODEL_FR", "fr_core_news_lg"),
		spacy_model_en=os.getenv("SPACY_MODEL_EN", "en_core_web_lg"),
		sentence_transformer_model=os.getenv(
			"SENTENCE_TRANSFORMER_MODEL", "paraphrase-multilingual-mpnet-base-v2"
		),
		anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
		openai_api_key=os.getenv("OPENAI_API_KEY", ""),
	)
