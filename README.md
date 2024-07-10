# secure-file-storage
A secure file storage system built with Flask that allows users to upload and download encrypted files. 
# features
- User Registration
- User Login
- File Upload with Encryption
- File Download with Decryption
- AWS S3 integration for file storage
- Loggin of Access and Errors

# Requirements
- Python 3.7+ 
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Boto3
- Cryptography

# Installation
1. Clone the repository
2. ```cd cloud-secure-file-storage```
3. Create a virtual environemnt and activate it
```
python -m venv env
source env/bin/activate # On windows use 'env'Scripts/activate'
```
4. Install the required packages
```
pip install -r requirements.txt
```
5. Configure AWS credentials ```aws configure``` with your access key and secret access key.
6. Add your S3 bucket name and other configurations in 'config.py'
# Usage
1. Run the application
```python run.py```
2. Open your web browser and navigate to http://127.0.0.1:5000/
3. Login: with your credentials
4. From Login page: a new user can be registered
5. Use the file upload form to select a file and upload. The file will be encrypted and stored securely.
6. Use the file Download: enter the filename in the download form and submit it to the download the file. The file will be decrypted before downloading.
# Configuration
Configuration setting are managed in the 'config.py' file. Adjust the settings as needed for the environment
# Logging
User authentication, File upload and download activities are lgoged in the 'access.log' file. Errors are logged as well.
