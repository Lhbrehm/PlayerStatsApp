from . import db
from flask_login import UserMixin
from sqlalchemy import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    notes = db.relationship('Note')


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    name = db.Column(db.String(100))
    yards = db.Column(db.Integer)
    years = db.Column(db.String(100))
    team = db.Column(db.String(100))