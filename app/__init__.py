# -*- coding:utf-8 -*-

"""Package app (Flask)."""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
boostrap = Bootstrap(app)
moment = Moment(app)

from app import errors, models, routes  # noqa: F401 It is ok in flask
