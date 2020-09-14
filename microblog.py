# -*- coding:utf-8 -*-

"""Main module of blog."""

from app import app, cli, db, mail
from app.models import Post, User


@app.shell_context_processor
def make_shell_context():
    """Add objects to shell.

    Returns:
        dict: dict with objects.
    """
    return {'db': db, 'User': User, 'Post': Post, 'mail': mail}
