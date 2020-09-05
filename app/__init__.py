# -*- coding:utf-8 -*-

"""Экземпляр класса Flask.

Сценарий выше просто создает объект приложения как экземпляр класса Flask,
импортированного из пакета flask. Переменная __name__, переданная в класс
Flask, является предопределенной переменной Python, которая задается именем
модуля, в котором она используется. Один из аспектов, который может показаться
запутанным вначале, состоит в том, что существуют два объекта с именем app.
Пакет приложения определяется каталогом приложения и сценарием __init__.py и
указан в инструкции routes импорта приложения. Переменная app определяется как
экземпляр класса Flask в сценарии __init__.py, что делает его частью пакета
приложения.
"""

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import models, routes  # noqa: F401 It is ok in flask
