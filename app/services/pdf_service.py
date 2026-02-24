import io
from pypdf import PdfReader

class PDFService:
    @staticmethod
    def extract_text(file_content: bytes) -> str:
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    