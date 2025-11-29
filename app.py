@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return "No file uploaded"

        pdf = request.files["pdf_file"]
        if pdf.filename == "":
            return "No file selected"

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        pdf.save(pdf_path)

        word_filename = pdf.filename.rsplit(".", 1)[0] + ".docx"
        word_path = os.path.join(OUTPUT_FOLDER, word_filename)

        pdf_to_word(pdf_path, word_path)

        return send_file(word_path, as_attachment=True)

    return render_template("index.html")
