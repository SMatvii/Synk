from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length


class EditPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=20)])
    content = TextAreaField("Content", validators=[DataRequired()])


class PostForm(EditPostForm):
    image = FileField("Upload Image", validators=[DataRequired()])
