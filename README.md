# File Compressor

A simple web application built with Flask for compressing image and PDF files. Upload your files, specify the desired size, and download the compressed version.

## Features

- **Image Compression**: Compress PNG, JPEG, and JPG images.
- **PDF Compression**: Compress PDF files with optimized version settings.
- **File Size Control**: Specify target size in KB or MB for compression.
- **User-Friendly Interface**: Upload and compress files through an intuitive web interface.

## Getting Started

To get started with this project, follow these steps:

### Prerequisites

- **Python**: Make sure you have Python 3.6+ installed.
- **Flask**: Web framework for building the application.
- **Pillow**: Python Imaging Library for image manipulation.
- **pikepdf**: Library for handling PDF files.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository-URL>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:

   - **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **MacOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Create a `requirements.txt` file with the following content:

   ```plaintext
   Flask
   Pillow
   pikepdf
   ```

5. **Run the Application**:

   ```bash
   python app.py
   ```

   By default, the application will run on `http://127.0.0.1:5000/`.

### Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Use the upload form to select and upload a file.
3. Specify the desired target size for compression.
4. Click the "Compress" button to process the file.
5. Download the compressed file from the provided download link.

### Contributing

Contributions are welcome! If you have suggestions or improvements, please:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.


### Acknowledgements

- **Flask**: A micro web framework for Python.
- **Pillow**: A Python Imaging Library (PIL) fork.
- **pikepdf**: A Python library for PDF manipulation.
