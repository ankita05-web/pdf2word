from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# Folder to save uploaded PDFs
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route: Home page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Handle PDF upload
@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        return "No file selected", 400

    # Save uploaded PDF
    save_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(save_path)

    # Placeholder: Currently we just return the PDF name
    # Later, you can add PDF -> Word conversion logic here
    return f"File received: {pdf_file.filename}"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
