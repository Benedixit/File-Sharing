from flask_login import UserMixin
from datetime import datetime
from src.extensions import db
import os

class User(UserMixin, db.Model):
    __tablename__ = "user"


    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    groups = db.relationship('Group', secondary='user_groups', backref='users')
    projects = db.relationship('Project', secondary='user_projects', backref='users')
    files = db.relationship('File', backref='user', lazy=True)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        from src import bcrypt  # Import db and bcrypt here
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.create_folder()

    def __repr__(self):
        return f"<email {self.email}>"
    
    def create_folder(self):
        path = "C:/Users/dell/Documents/files/users"
        os.mkdir(f'{path}/{self.email}')
    

# Group model
class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
        self.create_folder()

    def create_folder(self):
        path = "C:/Users/dell/Documents/files/groups"
        os.mkdir(f'{path}/{self.name}')
        


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    image = db.Column(db.String(255))
    folders = db.relationship('Folder', backref='project', lazy=True, cascade='all, delete-orphan')


    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.create_folder()

    def create_folder(self):
        path = "C:/Users/dell/Documents/files/projects"
        os.mkdir(f'{path}/{self.name}')
    

class File(db.Model):
    __tablename__ = "file"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(64), nullable=False)


    def __init__(self, filename, project_id, user_id, file_size, file_type):
        self.filename = filename
        self.project_id = project_id
        self.user_id = user_id
        self.file_size = file_size
        self.file_type = file_type

    def __repr__(self):
        return f"<File {self.filename}>"


class Folder(db.Model):
    __tablename__ = "folder"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    files = db.relationship('File', backref='folder', lazy=True, cascade='all, delete-orphan')

    def __init__(self, name, project_id):
        self.name = name
        self.project_id = project_id
    
    def __repr__(self):
        return f"<name {self.name}>"
 
user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

user_projects = db.Table('user_projects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

