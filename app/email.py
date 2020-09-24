# -*- coding:utf-8 -*-

"""Email Framework."""

from threading import Thread

from flask_mail import Message

from app import current_app, mail


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
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg),
    ).start()
