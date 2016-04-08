from flask import Flask
import sys, requests, json, urllib.request, os

import sys

app = Flask(__name__)

# Setup the app with the config.py file
app.config.from_object('config')

# Setup the database
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the mail server
from flask.ext.mail import Mail
mail = Mail(app)

# Setup the password crypting
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import the views
from app.views import lobby, setup, user, wager, filters
app.register_blueprint(setup.setupbp)
app.register_blueprint(user.userbp)
app.register_blueprint(wager.wagerbp)

# Setup the user login process
from flask.ext.login import LoginManager
from app.models import User, MLBWager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'

@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()
