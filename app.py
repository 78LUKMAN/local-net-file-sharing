import os
from flask import Flask, request, send_from_directory, render_template, jsonify

# Inisialisasi Flask
app = Flask(__name__)

# Direktori untuk menyimpan file yang diunggah
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rute untuk halaman utama
@app.route('/')
def home():
    return render_template('index.html')

# Rute untuk mengunggah file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Simpan file di direktori server
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return f"File {file.filename} uploaded successfully!"

# Rute untuk mengunduh file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Rute untuk mendapatkan daftar file
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2024)
