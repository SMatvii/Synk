from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Email,
)


class RegisterForm(FlaskForm):
    name = StringField(
        validators=[
            DataRequired(),
        ]
    )
    email = EmailField(
        validators=[
            DataRequired(),
            Email(),
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired(),
        ]
    )
    password_confirm = PasswordField(validators=[DataRequired(), EqualTo("password")])
    bio = StringField()
    submit = SubmitField("Register")
