# -*- coding:utf-8 -*-

"""Forms module."""

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)

from app.models import User


class LoginForm(FlaskForm):
    """Login form.

    Args:
        FlaskForm (class): Flask-specific subclass of WTForms
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sigh In')


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

        Raises:
            ValidationError, if the username is not unique
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # TODO: Method 'validate_email' may be 'static'
    def validate_email(self, email):
        """Checks the email field's data for uniqueness.

        Args:
            email: Email field data

        Raises:
            ValidationError, if an email is not unique
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    """User profile editing form."""

    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post = TextAreaField(
        'Say something',
        validators=[DataRequired(), Length(min=1, max=140)],
    )
    submit = SubmitField('Submit')
