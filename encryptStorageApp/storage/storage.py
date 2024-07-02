import os
from encryptStorageApp.utils.logging import log_error
import uuid

def save_file(file, storage_path):
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
        log_error(f'Created storage path: {storage_path}')

    unique_filename = f'{uuid.uuid4().hex}_{file.filename}'
    file_path = os.path.join(storage_path, file.filename)
    file.save(file_path)

    if os.path.exists(file_path):
        log_error(f'File saved successfully at: {file_path}')
        return file_path
    else:
        raise Exception(f'Failed to save file to {file_path}')

def retrieve_file(file_path):
    if os.path.exists(file_path):
        log_error(f'File exists at: {file_path}')
        return open(file_path, 'rb')
    else:
        log_error(f'File not found at: {file_path}')
        return None
