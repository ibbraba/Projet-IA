import logging


def configure_logging(level: str = "info") -> None:
	logging.basicConfig(level=level.upper())
