import re
from pathlib import Path
import fitz


PDF_PATH = r"C:\Users\Veekshith Megari\Downloads\_Uploads_LawDepartment_pdf_Act 15 of 1960_13012023_125004.pdf"


def extract_text(pdf_path: Path) -> str:
    document = fitz.open(pdf_path)

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)


def create_chunks(text: str) -> list[dict]:
    pattern = r"(?m)^\s*(\d+)\.\s+(.+)$"

    matches = list(re.finditer(pattern, text))

    chunks = []

    for index, match in enumerate(matches):

        section_number = match.group(1)
        section_title = match.group(2).strip()

        start = match.start()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        content = text[start:end].strip()

        chunks.append({
            "section": section_number,
            "title": section_title,
            "content": content
        })

    return chunks