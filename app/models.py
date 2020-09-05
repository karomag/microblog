# -*- coding:utf-8 -*-

"""Models module for DB."""

from datetime import datetime

from flask_login import UserMixin
from libgravatar import Gravatar
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

USERNAME_LENGTH = 64
EMAIL_LENGTH = 120
PASSWORD_HASH_LENGTH = 128
POST_BODY_LENGTH = 140


class User(UserMixin, db.Model):
    """Class User.

    Args:
        UserMixin (class): This provides default implementations for the
            methods that Flask-Login expects user objects to have.
        db (class): Database class SQLAlchemi
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_LENGTH), index=True, unique=True)
    email = db.Column(db.String(EMAIL_LENGTH), index=True, unique=True)
    password_hash = db.Column(db.String(PASSWORD_HASH_LENGTH))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        """Print users info.

        Returns:
            str: Users info.
        """
        return '<User {0}>'.format(self.username)

    def set_password(self, password):
        """Set user's password.

        Args:
            password (str): user's password
        """
        # TODO: resolve error WPS601 Found shadowed class attribute
        self.password_hash = generate_password_hash(password)  # noqa: WPS601

    def check_password(self, password):
        """Check user's password.

        Args:
            password (str): user's password

        Returns:
            bool: returns True, if password is correct
        """
        return check_password_hash(self.password_hash, password)

    def get_avatar(self, size):
        """Returns an URL to the user profile image.

        Args:
            size: a specific image size

        Returns:
            (str): an URL gravatar image
        """
        avatar = Gravatar(self.email.lower())
        return avatar.get_image(size=size, default='monsterid')


class Post(db.Model):
    """Class Post.

    Args:
        db (class): Base class SQLAlchemi

    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(POST_BODY_LENGTH))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Print post's text.

        Returns:
            str: Post's text.
        """
        return '<Post {0}>'.format(self.body)


@login.user_loader
def load_user(id):  # noqa: A002=
    """Load user function.

    Args:
        id (str): user's id

    Returns:
        User from db.
    """
    return User.query.get(int(id))
