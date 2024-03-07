from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        label="Enter your Userame:", validators=[Length(min=3, max=30), DataRequired()]
    )
    email = StringField(
        label="Enter your Email Address:", validators=[DataRequired(), Email()]
    )
    password1 = PasswordField(
        label="Enter your Password:",
        validators=[
            DataRequired(),
            Length(min=10, message="The password must be at least 10 characters long"),
        ],
    )
    password2 = PasswordField(
        label="Confirm your Password:",
        validators=[EqualTo("password1", message="The passwords do not match.")],
    )
    submit = SubmitField("Create Account")

    def validate_username(self, field):
        user_to_add = User.query.filter_by(username=field.data).first()
        if user_to_add:
            raise ValidationError("The username is already in use.")

    def validate_email(self, field):
        email_to_add = User.query.filter_by(email=field.data).first()
        if email_to_add:
            raise ValidationError("The email is already in use.")
