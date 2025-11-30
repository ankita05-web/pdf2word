from flask import Flask, render_template, request, send_file
import pdfplumber
from docx import Document
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert_pdf_to_word():
    if "pdf_file" not in request.files:
        return "No file uploaded!"

    pdf_file = request.files["pdf_file"]
    filename = pdf_file.filename

    # Save PDF
    os.makedirs("uploads", exist_ok=True)
    pdf_path = os.path.join("uploads", filename)
    pdf_file.save(pdf_path)

    # Convert
    doc = Document()
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    doc.add_paragraph(text)
    except:
        return "Error while converting PDF"

    # Output file
    output_name = filename.replace(".pdf", ".docx")
    output_path = os.path.join("uploads", output_name)
    doc.save(output_path)

    return send_file(output_path, as_attachment=True)

@app.route("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run()
