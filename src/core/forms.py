from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FileUploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField('Create Project') 