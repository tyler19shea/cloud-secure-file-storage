from flask import Flask
from encryptStorageApp.auth import db, bcrypt, auth_blueprint
from encryptStorageApp.app import app_blueprint
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(app_blueprint)

    return app