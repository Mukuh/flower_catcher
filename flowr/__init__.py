# standard imports
from os import path

# flask imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# global variables
db = SQLAlchemy()
DB_NAME = "users.db"


def create_app() -> Flask:
    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY']='dev' # TODO: CHANGE THIS LATER!
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # surpress warning by disabling the SQLAlchemy's built-in event system
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
 
    # import blueprints
    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.sign_in"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app: Flask):
    if not path.exists(path.join("flowr", DB_NAME)):
        db.create_all(app=app)
        print("* Created database")
    else:
        print(" * Database already created")

