# -*- coding:utf-8 -*-

"""Forms module."""

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    """Login form.

    Args:
        FlaskForm (class): Flask-specific subclass of WTForms
    """

    username = StringField('Пользователь', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    """Registration form.

    Args:
        FlaskForm (class): Flask-specific subclass of WTForms
    """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField('Register')

    # TODO: Method 'validate_username' may be 'static'
    def validate_username(self, username):
        """Checks the username field's data for uniqueness.

        Args:
            username: Username field data

        Returns:
            True, if the username is unique
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # TODO: Method 'validate_email' may be 'static'
    def validate_email(self, email):
        """Checks the email field's data for uniqueness.

        Args:
            email: Email field data

        Returns:
            True, if an email is unique
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
