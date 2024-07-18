from flask import Flask
from flask_login import LoginManager
from encryptStorageApp.auth import db, bcrypt, auth_blueprint
from encryptStorageApp.app import app_blueprint
from config import Config
from encryptStorageApp.auth.models import User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(app_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password=bcrypt.generate_password_hash('adminpass'), is_admin=True)
            db.session.add(admin_user)
            db.session.commit()

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))