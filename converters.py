# converters.py
import pdfplumber
from docx import Document

def pdf_to_word(pdf_file, word_path):
    document = Document()
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                document.add_paragraph(text)
                if i < len(pdf.pages) - 1:
                    document.add_page_break()
    document.save(word_path)
