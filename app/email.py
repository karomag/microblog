# -*- coding:utf-8 -*-

"""Email Framework."""

from threading import Thread

from flask import render_template
from flask_babel import _
from flask_mail import Message

from app import app, mail


def send_async_email(app, msg):
    """Sends a message in a background thread.

    Args:
        app: app
        msg: message
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """Send an email.

    Args:
        subject: subject
        sender: sender
        recipients: recipients
        text_body: text body
        html_body: html body
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    """Generates the password reset email.

    Args:
        user: User.
    """
    token = user.get_reset_password_token()
    send_email(
        _('[Microblog] Reset Your Password'),
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt',
            user=user,
            token=token,
        ),
        html_body=render_template(
            'email/reset_password.html',
            user=user,
            token=token,
        ),
    )
