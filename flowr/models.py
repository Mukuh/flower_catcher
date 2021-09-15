# flask imports
from flask_login import UserMixin
from sqlalchemy.sql import func

# local imports
from . import db


class User(db.Model, UserMixin):
    # every table needs a primary key (identifier)
    id = db.Column(db.Integer, primary_key=True)
    # (150) is the max length of the string and it is unique in the tabel
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    # sets the creation time automatically
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())