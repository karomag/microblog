# -*- coding:utf-8 -*-

"""Main module of blog."""

from app import cli, create_app, db, mail
from app.models import Post, User

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    """Add objects to shell.

    Returns:
        dict: dict with objects.
    """
    return {'db': db, 'User': User, 'Post': Post, 'mail': mail}
