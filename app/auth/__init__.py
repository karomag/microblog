# -*- coding:utf-8 -*-

"""Auth blueprint."""

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import email, forms, routes
