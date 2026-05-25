def sanitize_filename(filename: str) -> str:
	return filename.replace("..", "").replace("/", "_").replace("\\", "_")
