# -*- coding:utf-8 -*-

"""Forms auth."""

from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
)

from app.models import User


class LoginForm(FlaskForm):
    """Login form.

    Args:
        FlaskForm (class): Flask-specific subclass of WTForms
    """

    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Sigh In'))


class RegistrationForm(FlaskForm):
    """Registration form.

    Args:
        FlaskForm (class): Flask-specific subclass of WTForms
    """

    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField(_l('Register'))

    # TODO: Method 'validate_username' may be 'static'
    def validate_username(self, username):
        """Checks the username field's data for uniqueness.

        Args:
            username: Username field data

        Raises:
            ValidationError, if the username is not unique
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    # TODO: Fix function.
    def validate_email(self, email):
        """Checks the email field's data for uniqueness.

        Args:
            email: Email field data

        Raises:
            ValidationError, if an email is not unique
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'),
        validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField(_l('Request Password Reset'))
