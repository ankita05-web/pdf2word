from flask import Flask, render_template, request, send_file, flash, redirect
from converters import pdf_to_word
import os
import zipfile
import tempfile

app = Flask(__name__)
app.secret_key = "supersecretkey"

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

def parse_pages(pages_str):
    pages = []
    for part in pages_str.split(","):
        if "-" in part:
            start, end = part.split("-")
            pages.extend(range(int(start), int(end)+1))
        else:
            pages.append(int(part))
    return pages

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_files = request.files.getlist("pdfs")
        pages_input = request.form.get("pages")
        pages = parse_pages(pages_input) if pages_input else None

        converted_files = []
        temp_dir = tempfile.mkdtemp()

        for file in uploaded_files:
            if not file.filename.lower().endswith(".pdf"):
                flash(f"{file.filename} is not a PDF file, skipped.")
                continue

            file.seek(0, os.SEEK_END)
            if file.tell() > MAX_FILE_SIZE:
                flash(f"{file.filename} exceeds max size 20MB.")
                continue
            file.seek(0)

            pdf_path = os.path.join(temp_dir, file.filename)
            file.save(pdf_path)
            word_path = pdf_to_word(pdf_path, pages)
            converted_files.append(word_path)

        if not converted_files:
            flash("No valid PDFs converted.")
            return redirect("/")

        if len(converted_files) > 1:
            zip_path = os.path.join(temp_dir, "converted_files.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for file_path in converted_files:
                    zipf.write(file_path, os.path.basename(file_path))
            return send_file(zip_path, as_attachment=True)
        else:
            return send_file(converted_files[0], as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
