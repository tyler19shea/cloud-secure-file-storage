import os 
from cryptography.fernet import Fernet
from encryptStorageApp.auth.models import User

KEY_FILE = os.path.join(os.getcwd(), 'encryption_key.key')

def generate_key():
    return Fernet.generate_key()

def save_key(key):
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = generate_key()
        save_key(key)
        return key

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENCRYPTION_KEY = load_key()
    S3_BUCKET_NAME = ''
    UPLOAD_FOLDER = 'uploads'
    DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
