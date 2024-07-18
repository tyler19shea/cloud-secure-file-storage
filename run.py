from encryptStorageApp import create_app, db
from encryptStorageApp.auth import bcrypt
from encryptStorageApp.auth.models import User


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
