import pdfplumber
from docx import Document

def pdf_to_word(pdf_file, word_path):
    document = Document()

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text and text.strip():
                document.add_paragraph(text)
                document.add_page_break()

    document.save(word_path)
