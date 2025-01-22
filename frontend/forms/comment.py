from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import (
    DataRequired,
    Length
)

class CommentForm(FlaskForm):
    content = StringField("Comment", validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField("Submit")