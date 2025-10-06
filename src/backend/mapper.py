from flask import Flask, render_template, request, jsonify
import os
import sys

# Add the parent directory of `backend/` (which is `src/`) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import entry
from main import entry_manual_process

# Set the template folder to the UI path
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ui'))

# set the path for uploaded files
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploaded'))
# create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.json'):
        return jsonify({'error': 'Only .json files are allowed'}), 400

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)

    return jsonify({'message': f'File {file.filename} uploaded successfully!'})


@app.route('/process', methods=['POST'])
def process_file():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'message': 'File is not found. Please upload a JSON file.'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({'message': 'File is not found. Please upload a JSON file.'}), 404

    errorList = entry(filepath)

    print("No of errors: ", len(errorList))


    return jsonify({'errorList': [e.to_dict() for e in errorList]})


@app.route('/manualprocess', methods=['POST'])
def process_error_entry():
    data = request.get_json()
    
    errorType = data.get('errorType')
    if not errorType:
        return jsonify({'message': 'Error occured.'}), 400

    originalText = data.get('originalText')
    if not originalText:
        return jsonify({'message': 'Error occured.'}), 400

    correctedText = data.get('correctedText')
    if not correctedText:
        return jsonify({'message': 'Error occured.'}), 400

    res = entry_manual_process(errorType, originalText, correctedText)
    
    return jsonify(res.to_dict())

if __name__ == '__main__':
    app.run(debug=True)