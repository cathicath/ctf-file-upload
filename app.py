from flask import Flask, request, render_template, send_from_directory, jsonify
import os
import urllib.parse
import re
import subprocess
from translator import text_to_hieroglyphs, hieroglyphs_to_text  # Import translation functions

app = Flask(__name__)
UPLOAD_FOLDER = "/app/uploads/"
FLAG_FILE = "/flag.txt"
PHP_EXECUTABLE = "/usr/local/bin/php"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Validate file type while allowing null-byte bypass"""
    decoded_filename = urllib.parse.unquote(filename)
    clean_filename = re.split(r'[\x00%00]', decoded_filename, maxsplit=1)[0]

    if clean_filename.count('.') > 1:
        return False  # Reject double extensions

    ext = clean_filename.rsplit('.', 1)[-1].lower()

    # Allow PHP only if null-byte trick is used
    if ext == "php":
        return "%00" in decoded_filename or "\x00" in decoded_filename

    return ext in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    message = None

    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            message = "No file selected."
        elif allowed_file(file.filename):
            real_filename = re.split(r'[\x00%00]', urllib.parse.unquote(file.filename), maxsplit=1)[0]
            filepath = os.path.join(UPLOAD_FOLDER, real_filename)
            file.save(filepath)
            message = f"Offering recieved: {real_filename}. Available at: <a href='http://localhost:8000/{real_filename}' target='_blank'>http://localhost:8000/{real_filename}</a>"
        else:
            message = "Invalid file type. The Gods only accept images."

    return render_template("index.html", message=message)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """If a PHP file is uploaded and executed, it must fetch the flag manually."""
    real_filename = re.split(r'[\x00%00]', urllib.parse.unquote(filename), maxsplit=1)[0]
    file_path = os.path.join(UPLOAD_FOLDER, real_filename)

    # If the uploaded file is a PHP script, execute it and return output
    if file_path.endswith(".php") and os.path.exists(file_path):
        try:
            result = subprocess.run([PHP_EXECUTABLE, file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if "flag.txt" in result.stdout:
                with open(FLAG_FILE, "r") as f:
                    return f.read()

            return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"

        except Exception as e:
            return f"Execution error: {str(e)}"

    return send_from_directory(UPLOAD_FOLDER, real_filename)

@app.route("/translate", methods=["POST"])
def translate():
    """API endpoint for translating hieroglyphs to text."""
    data = request.json
    hieroglyphs = data.get("hieroglyphs", "")
    translated_text = hieroglyphs_to_text(hieroglyphs)
    return jsonify({"translation": translated_text})

@app.route("/translate_to_hieroglyphs", methods=["POST"])
def translate_to_hieroglyphs():
    """API endpoint for translating text to hieroglyphs."""
    data = request.json
    text = data.get("text", "")
    translated_hieroglyphs = text_to_hieroglyphs(text)
    return jsonify({"translation": translated_hieroglyphs})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
