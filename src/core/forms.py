from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

class FileUploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])