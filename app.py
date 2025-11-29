from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# Ensure a folder exists to store uploads
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "No file uploaded"

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        return "No file selected"

    # Save the file
    save_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(save_path)

    # Here you can call your PDF-to-Word conversion function
    # For now, just return a success message
    return f"File received: {pdf_file.filename}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

