from cryptography.fernet import Fernet
import boto3
import os
from encryptStorageApp.utils.logging import log_error
from config import Config

s3_client = boto3.client('s3')
fernet = Fernet(Config.ENCRYPTION_KEY)

def encrypt_file(username, file_path, filename):
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    
    s3_client.upload_file(file_path, Config.S3_BUCKET_NAME, f'{username}/{filename}')
    log_error(f'File uploaded to S3: {file_path} {filename}')

def decrypt_file(user, file_path, filename):
    s3_client.download_file(Config.S3_BUCKET_NAME, f'{user}/{filename}', file_path)
    log_error(f'file downloaded from S3: {file_path} {filename}')

    with open(file_path, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, 'wb') as dec_file:
        dec_file.write(decrypted)
    log_error(f'File decrypted: {file_path}')

def list_files(user):
    response = s3_client.list_objects_v2(Bucket=Config.S3_BUCKET_NAME, Prefix=f'{user}/')
    if 'Contents' in response:
        return [item['Key'] for item in response['Contents']]
    return []