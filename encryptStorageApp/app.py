from flask import Blueprint, request, jsonify, json, send_file, render_template, flash, Response, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from .encryption import encrypt_file, decrypt_file
from .utils import log_access, log_error
from .auth import bcrypt
from .auth.models import User
from config import Config
import traceback
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

app_blueprint = Blueprint('app', __name__)

@app_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')

@app_blueprint.route('/change-pass', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        username = current_user.username
        password1 = request.form['password1']
        password2 = request.form['password2']
        password3 = request.form['password3']

        # #fetch the user from database
        user = User.query.filter_by(username=username).first()
        if not bcrypt.check_password_hash(user.password, password1):
            flash('Incorrect original password entered')
            log_error(f'{username} password change attempt fail due to incorrect original password')
        elif password2 != password3:
            flash('Passwords do not match')
        else:
            try:
                current_user.password = bcrypt.generate_password_hash(password2)
                flash('Password has been changed!')
                log_error(f'{username} password changed')
                return redirect(url_for('app.index'))
            except Exception as e:
                log_error(f'{username} fail to change password due to {e}')
                flash('Password change failed due to {e}')

    return render_template('changePass.html')

@app_blueprint.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files.get('file')
    if not file: 
        log_error('No file part')
        flash("Invalid file name!")
        return jsonify({'message': 'No file part'}), 400
    
    user = current_user.username
    filename = secure_filename(file.filename)
    
    try:
        log_error(f'Received file: {filename} from user: {user}')
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)

        # create the downloads directory if it doesn't exist
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)

        file.save(file_path)
        log_error(f'Saved file locally: {file_path}')
        encrypt_file(file_path, filename)
        log_error(f'Encrypted file and upload to S3: {file_path}')
        log_access(user, filename)
        os.remove(file_path)
        flash('File uploaded and encrypted successfully!')
        return jsonify({'message': 'File uploaded and encrypted successful!'})
    except (NoCredentialsError, PartialCredentialsError) as e:
        log_error(f'Credentials error: {str(e)}')
        return jsonify({'message': 'File upload failed due to credential error'})
    except ClientError as e: 
        log_error(f'Client error: {str(e)}')
        return jsonify({'message': 'File upload filed due to client error'})
    except Exception as e:
        log_error(f'File upload failed for user: {user}: {traceback.format_exc()}')
        return jsonify({'message': 'File upload failed!', 'error': str(e)}), 500

@app_blueprint.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    user = current_user.username
    if not filename:
        return flash('Filename not provided'), 400
    file_path = os.path.join(Config.DOWNLOAD_FOLDER, secure_filename(filename))

    # create the downloads directory if it doesn't exist
    if not os.path.exists(Config.DOWNLOAD_FOLDER):
        os.makedirs(Config.DOWNLOAD_FOLDER)

    try: 
        decrypt_file(file_path, secure_filename(filename))

        if not os.path.exists(file_path):
            log_error(f'File not found after decryption: {file_path}')
            return jsonify({'message': 'File not found after decryption'})

        file_size = os.path.getsize(file_path)
        log_error(f'File size: {file_size} bytes')

        response = send_file(file_path, as_attachment=True)
        log_error(f'File {filename} sent as attachement')
        os.remove(file_path)
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            log_error(f'File not found in S3 bucket: {filename}')
            return Response(json.dumps({'message': 'File not found in S3 bucket'}), status=404, mimetype='application/json')
        else:
            log_error(f'Client error: {str(e)}')
            return Response(json.dumps({'message': 'File download filed due to client error'}), status=500, mimetype='application/json')
    except FileNotFoundError as e:
        log_error(f'File not found: {str(e)}')
        flash('File not found')
        return Response(json.dumps({'message': 'File not found'}), status=404, mimetype='application/json')
    except Exception as e:
        log_error(f'File download failed for user {user}: {traceback.format_exc()}')
        return Response(json.dumps({'message': 'An Unexpected error occurred'}), status=500, mimetype='application/json')