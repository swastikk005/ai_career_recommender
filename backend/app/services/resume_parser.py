import pdfplumber
import docx2txt
import io

class ResumeParser:
    @staticmethod
    def extract_text_from_pdf(file_bytes):
        """Extract text from a PDF file."""
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return ""

    @staticmethod
    def extract_text_from_docx(file_bytes):
        """Extract text from a DOCX file."""
        try:
            text = docx2txt.process(io.BytesIO(file_bytes))
            return text
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return ""

    @staticmethod
    def extract_text(file_bytes, filename):
        """Detect file type and extract text."""
        if filename.lower().endswith('.pdf'):
            return ResumeParser.extract_text_from_pdf(file_bytes)
        elif filename.lower().endswith('.docx'):
            return ResumeParser.extract_text_from_docx(file_bytes)
        else:
            try:
                return file_bytes.decode('utf-8', errors='ignore')
            except:
                return ""
