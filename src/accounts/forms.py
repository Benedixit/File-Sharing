from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from src.accounts.models import User


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True
    
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class GroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create Group')

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField('Create Project') 
