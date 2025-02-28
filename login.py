from flask_login import LoginManager, flask
from flask_sqlalchemy import SQLAlchemy-login
from main import app

login_manager = LoginManager()

login_manager.init_app(app)

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    name = db.Column(db.String(80))
