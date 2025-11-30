from flask import Flask, render_template, request, send_file
import pdfplumber
from docx import Document
import io

app = Flask(__name__)

# Home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Convert PDF to Word
@app.route("/convert", methods=["POST"])
def convert():
    pdf_file = request.files.get('pdf_file')
    if not pdf_file:
        return "No file uploaded", 400

    # Create Word document
    doc = Document()
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)

    # Prepare file for download
    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return send_file(output, download_name="converted.docx", as_attachment=True)

# Render health check
@app.route("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    # Make sure to use the port Render expects
    app.run(host="0.0.0.0", port=10000)
