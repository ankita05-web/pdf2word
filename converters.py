import pdfplumber
from docx import Document
import os

def pdf_to_word(pdf_path, pages=None, output_path=None):
    """
    Converts a PDF file to Word document.
    """
    if not output_path:
        output_path = os.path.splitext(pdf_path)[0] + ".docx"
    
    doc = Document()
    with pdfplumber.open(pdf_path) as pdf:
        if pages:
            pages_to_extract = [p-1 for p in pages if 0 < p <= len(pdf.pages)]
        else:
            pages_to_extract = range(len(pdf.pages))
        for i in pages_to_extract:
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                for line in text.split('\n'):
                    doc.add_paragraph(line)
                doc.add_paragraph("\n")  # page break

    doc.save(output_path)
    return output_path
