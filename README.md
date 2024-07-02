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