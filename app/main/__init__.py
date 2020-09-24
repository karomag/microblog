# -*- coding:utf-8 -*-

"""Main module."""

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
