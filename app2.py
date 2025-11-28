from flask import Flask, request, send_file
import pdfplumber
from docx import Document
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "PDF to Word Converter is running!"

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400

    pdf_file = request.files['file']
    
    doc = Document()
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="output.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
