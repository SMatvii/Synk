from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=20)])
    bio = TextAreaField("Bio", validators=[Length(max=500)])
