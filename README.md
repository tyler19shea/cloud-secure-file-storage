# secure-file-storage
A secure file storage system built with Flask that allows users to upload and download encrypted files. 
# features
- User Registration
- User Login
- File Upload with Encryption
- File Download with Decryption
- Loggin of Access and Errors

# Requirements
- Python 3.7+ 
- Flask
- Flask-Login
- Cryptography

# Installation
1. Clone the repository
2. ```cd secure-file-storage```
3. Create a virtual environemnt and activate it
```
python -m venv env
source env/bin/activate # On windows use 'env'Scripts/activate'
```
4. Install the required packages
```
pip install -r requirements.txt
```
# Usage
1. Run the application
```python run.py```
2. Open your web browser and navigate to http://127.0.0.1:5000/
3. Login: with your credentials
4. Register a new user: http://127.0.0:5000/auth/register
5. Use the file upload form to select a file and upload. The file will be encrypted and stored securely.
6. Use the file Download: enter the filename in the download form and submit it to the download the file. The file will be decrypted before downloading
# Configuration
Configuration setting are managed in the 'config.py' file. Adjust the settings as needed for the environment
# Logging
User authentication, File upload and download activities are lgoged in the 'access.log' file. Errors are logged as well.
