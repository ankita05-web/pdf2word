# converters.py - helper file for PDF to Word conversion

import pdfplumber
from docx import Document

def pdf_to_word(pdf_file):
    doc = Document()
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
    return doc
