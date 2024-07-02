from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class AccessToken(db.Model):
    # 2048 bytes should be large enough for a Plaid access token 
    # and a Plaid item id. I was unable to find any documentation
    # on their length.
    # I am also assuming access tokens are globally unique.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    access_token = db.Column(db.String(2048), primary_key=True)
    item_id = db.Column(db.String(2048))