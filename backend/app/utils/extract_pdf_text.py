import pdfplumber

def extract_pdf_text(file_path: str) -> str:
    text_parts = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")

    return "\n".join(text_parts).strip() 
##