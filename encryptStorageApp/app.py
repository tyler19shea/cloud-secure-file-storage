from flask import Blueprint, request, jsonify, send_file, render_template
from .encryption import ENCRYPTION_KEY, generate_key, encrypt_file, decrypt_file
from .storage import save_file, retrieve_file
from .utils import log_access, log_error
import traceback
import os

app_blueprint = Blueprint('app', __name__)

STORAGE_PATH = '/Users/tylershea/repos/secure-file-storage/secure_storage/'

@app_blueprint.route('/')
def index():
    return render_template('index.html')

@app_blueprint.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    user = request.form['username']
    try:
        log_error(f'Received file: {file.filename} from user: {user}')
        file_path = save_file(file, STORAGE_PATH)
        log_error(f'Saved file path: {file_path}')
        encrypt_file(file_path, ENCRYPTION_KEY)
        log_error(f'Encrypted file: {file_path}')
        log_access(user, file.filename)
        return jsonify({'message': 'File uploaded and encrypted successful!'})
    except Exception as e:
        log_error(f'File upload failed for user: {user}: {str(e)}')
        return jsonify({'message': 'File upload failed!', 'error': str(e)}), 500

@app_blueprint.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    user = request.args.get('username')
    file_path = os.path.join(STORAGE_PATH, filename)
    try: 
        decrypt_file(file_path, ENCRYPTION_KEY)
        file = retrieve_file(file_path)
        if file:
            log_access(user, filename)
            log_error(f'File ready to be sent: {file_path}')
            return send_file(
                file, 
                as_attachment=True, 
                download_name=filename, 
                mimetype='application/octet-stream')
        else: 
            log_error(f'File not found: {file_path}')
            return jsonify({'message': 'File not found'}), 404
    except Exception as e:
        log_error(f'File download failed for user {user}: {traceback.format_exc()}')
        return jsonify({'message': 'File download failed!', 'error': str(e)}), 500