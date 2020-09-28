# -*- coding:utf-8 -*-

"""Models module for DB."""

from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from libgravatar import Gravatar
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from app.search import add_to_index, remove_from_index, query_index

USERNAME_LENGTH = 64
EMAIL_LENGTH = 120
PASSWORD_HASH_LENGTH = 128
POST_BODY_LENGTH = 140
ABOUT_ME_LENGTH = 140

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)


class User(UserMixin, db.Model):  # noqa: WPS214 Found too many methods
    """Class User.

    Args:
        UserMixin (class): This provides default implementations for the
            methods that Flask-Login expects user objects to have.

        db.Model (class): Database class SQLAlchemi.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_LENGTH), index=True, unique=True)
    email = db.Column(db.String(EMAIL_LENGTH), index=True, unique=True)
    password_hash = db.Column(db.String(PASSWORD_HASH_LENGTH))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(ABOUT_ME_LENGTH))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic',
    )

    def __repr__(self):
        """Print users info.

        Returns:
            str: Users info.
        """
        return '<User {0} email:{1}>'.format(self.username, self.email)

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
        return avatar.get_image(size=size, default='robohash')

    def follow(self, user):
        """Adds the user as a follower.

        Args:
            user: a follower.
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """Deletes the user as a follower.

        Args:
            user: a follower.
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """Checks the user is follower.

        Args:
            user: a user.

        Returns:
            True, if user is a follower.
        """
        return self.followed.filter(
            followers.c.followed_id == user.id,
        ).count() > 0

    def followed_posts(self):
        """Selects all posts written by users that you follow and own posts.

        Returns:
            (list): Posts.
        """
        followed = Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id),
        ).filter(
            followers.c.follower_id == self.id,
        )
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        """Generates JWT token.

        Args:
            expires_in: Expiration time of token.

        Returns:
            JWT token for a reset password message.
        """
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256',
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        """Checks the token.

        Args:
            token: JWT token.

        Returns:
            The User.
        """
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'],
            )['reset_password']
        except:
            return
        return User.query.get(id)


class SearchableMixin(object):
    """SearchableMixin class."""
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class Post(SearchableMixin, db.Model):
    """Class Post.

    Args:
        db.Model (class): Base class SQLAlchemi

    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(POST_BODY_LENGTH))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))
    # Add a __searchable__ attribute to the Post model.
    __searchable__ = ['body']

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


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
