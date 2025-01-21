from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    SubmitField,
    EmailField
)
from wtforms.validators import (
    DataRequired,
)


class LoginForm(FlaskForm):
    email = EmailField(
        validators=[
            DataRequired(),
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField("Log In")
