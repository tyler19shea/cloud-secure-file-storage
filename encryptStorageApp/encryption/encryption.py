from cryptography.fernet import Fernet
import os

KEY_FILE = '/Users/tylershea/repos/secure-file-storage/encryption_key.key'

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
    
ENCRYPTION_KEY = load_key()
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, 'wb') as dec_file:
        dec_file.write(decrypted)
