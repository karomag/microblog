# -*- coding:utf-8 -*-

"""Main module of blog."""

from app import app, db
from app.models import Post, User


@app.shell_context_processor
def make_shell_context():
    """Add objects DB to shell.

    Returns:
        dict: dict with objects.
    """
    return {'db': db, 'User': User, 'Post': Post}
