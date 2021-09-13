# standard imports
import os

# external imports
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY']='dev' # TODO: CHANGE THIS LATER!

    # import blueprints
    from .view import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app

