from pypdf import PdfReader
from pypdf.errors import PdfReadError
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        pdf_stream = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)

        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()
    except PdfReadError:
        raise ValueError("The uploaded file is not a valid PDF or is corrupted.")