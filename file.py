from flask import Flask, request, send_file, jsonify, render_template_string, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os
import pikepdf

app = Flask(__name__)

MAX_FILE_SIZE_MB = 500

def compress_image(image_path, target_size_kb):
    """Compress the image to the target size in KB."""
    img = Image.open(image_path)
    quality = 95
    while True:
        img.save(image_path, quality=quality)
        final_size = os.path.getsize(image_path) / 1024  # Size in KB
        if final_size <= target_size_kb or quality <= 10:
            break
        quality -= 5

def compress_pdf(pdf_path, output_path, target_size_kb):
    """Compress the PDF to the target size in KB."""
    with pikepdf.open(pdf_path) as pdf:
        pdf.save(output_path, optimize_version=True)
    final_size = os.path.getsize(output_path) / 1024
    if final_size > target_size_kb:
        pass

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Compressor</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
                text-align: center;
            }
            h1 {
                color: #333;
            }
            form {
                margin-bottom: 20px;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }
            input[type="file"], input[type="number"], select {
                display: block;
                margin: 10px auto;
                padding: 10px;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .file-limit {
                color: red;
                font-weight: bold;
            }
            .results {
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                margin-top: 20px;
                display: none;
            }
            a {
                text-decoration: none;
                color: #007bff;
                font-weight: bold;
            }
            a:hover {
                color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>File Compressor</h1>
        <p class="file-limit">File Upload Size Limit: 500 MB</p>
        <form id="upload-form" enctype="multipart/form-data">
            <input type="file" id="file-input" name="file" required><br><br>
            <button type="button" onclick="uploadFile()">Upload</button>
        </form>

        <div id="results" class="results">
            <h2>Results:</h2>
            <p id="original-size"></p>
            <form id="compress-form">
                <label for="size">Specify required size:</label>
                <input type="number" id="size" name="size" required>
                <select id="unit" name="unit">
                    <option value="KB">KB</option>
                    <option value="MB">MB</option>
                </select><br><br>
                <button type="button" onclick="compressFile()">Compress</button>
            </form>
            <p id="final-size"></p>
            <a id="download-link" href="#" download>Download Compressed File</a>
        </div>

        <script>
            function uploadFile() {
                var formData = new FormData(document.getElementById('upload-form'));
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload', true);
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        document.getElementById('original-size').innerText = 'Original Size: ' + response.original_size + ' ' + response.size_unit;
                        document.getElementById('results').style.display = 'block';
                        document.getElementById('compress-form').dataset.filepath = response.filepath;
                    } else {
                        console.error('Upload failed. Status:', xhr.status);
                    }
                };
                xhr.onerror = function() {
                    console.error('An error occurred during the upload.');
                };
                xhr.send(formData);
            }

            function compressFile() {
                var formData = new FormData();
                formData.append('filepath', document.getElementById('compress-form').dataset.filepath);
                formData.append('size', document.getElementById('size').value);
                formData.append('unit', document.getElementById('unit').value);

                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/compress', true);
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        document.getElementById('final-size').innerText = 'Final Size: ' + response.final_size + ' ' + response.size_unit;
                        document.getElementById('download-link').href = response.download_link;
                        document.getElementById('download-link').style.display = 'inline';
                    } else {
                        console.error('Compression failed. Status:', xhr.status);
                    }
                };
                xhr.onerror = function() {
                    console.error('An error occurred during the compression.');
                };
                xhr.send(formData);
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(os.getcwd(), filename)
        file.save(filepath)

        original_size_bytes = os.path.getsize(filepath)
        original_size_kb = original_size_bytes / 1024
        original_size_mb = original_size_kb / 1024

        if original_size_mb > 1:
            original_size = f'{original_size_mb:.2f}'
            size_unit = 'MB'
        else:
            original_size = f'{original_size_kb:.2f}'
            size_unit = 'KB'

        return jsonify({
            'filepath': filename,
            'original_size': original_size,
            'size_unit': size_unit
        })

@app.route('/compress', methods=['POST'])
def compress():
    filepath = request.form['filepath']
    target_size = int(request.form['size'])
    unit = request.form['unit']

    if unit == 'MB':
        target_size_kb = target_size * 1024
    else:
        target_size_kb = target_size

    file_path = os.path.join(os.getcwd(), filepath)
    if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
        compress_image(file_path, target_size_kb)
    elif filepath.lower().endswith('.pdf'):
        output_path = os.path.join(os.getcwd(), f'compressed_{filepath}')
        compress_pdf(file_path, output_path, target_size_kb)
        file_path = output_path

    final_size_kb = os.path.getsize(file_path) / 1024  # Size in KB
    final_size_mb = final_size_kb / 1024
    final_size = f'{final_size_mb:.2f}' if unit == 'MB' else f'{final_size_kb:.2f}'

    return jsonify({
        'final_size': final_size,
        'size_unit': unit,
        'download_link': url_for('download', filepath=os.path.basename(file_path))
    })

@app.route('/download/<path:filepath>')
def download(filepath):
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
