from flask import Blueprint, request, redirect, render_template, url_for, flash
from src.accounts.models import Project, User, Group, File, Folder
from flask_login import current_user
from src.extensions import db
from werkzeug.utils import secure_filename
from .forms import FileUploadForm, ProjectForm, FolderForm
from src.extensions import db, photos
import os


core_bp = Blueprint("core", __name__)

@core_bp.route("/", methods=["GET", "POST"])
def home():
    form = ProjectForm()
    if form.validate_on_submit():
        filename = photos.save(form.image.data)
        project = Project(name=form.name.data, image=filename)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("core.home"))
    projects = Project.query.all()
    return render_template("index.html", projects=projects, form=form)


@core_bp.route('/project/<int:project_id>/delete', methods=['POST', 'DELETE'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        return redirect("/")
    else:
        return 'Project not found', 404


@core_bp.route('/project/<int:project_id>/', methods=['GET', 'POST'])
def project_view(project_id):
    folders = Folder.query.filter_by(project_id=project_id).all()
    return render_template("project/index.html", folders=folders, project_id=project_id)


@core_bp.route('/project/<int:project_id>/folder/create', methods=['GET', 'POST'])
def folder_view(project_id):
    form = FolderForm()
    if request.method == "POST" and form.validate_on_submit():
        folder = Folder(name=form.name.data, project_id=project_id)
        try:
            db.session.add(folder)
            db.session.commit()
            return redirect(url_for('core.project_view', project_id=project_id))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while creating the folder.", "error")
            print(e)
    return render_template("folder/index.html", form=form, project_id=project_id)

@core_bp.route("/users", methods=["GET", "POST"])
def all_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@core_bp.route("/project/<int:project_id>/add_user", methods=["GET", "POST"])
def add_user_to_project(project_id):
    users = User.query.all()
    if request.method == "POST":
        project = Project.query.get(project_id)
        user_ids = request.form.getlist('user_ids')
        if project:
            for user_id in user_ids:
                user = User.query.get(user_id)
                if user not in project.users:
                    project.users.append(user)
                else:
                    return redirect(f'/project/{project.id}/add_user')
            db.session.commit()
            return redirect('/')
    return render_template("projects/add_user.html", users=users)



@core_bp.route("/group/<int:group_id>/add_user", methods=["GET", "POST"])
def add_user_to_group(group_id):
    users = User.query.all()
    if request.method == "POST":
        group = Group.query.get(group_id)
        user_ids = request.form.getlist('user_ids')
        if group:
            for user_id in user_ids:
                user = User.query.get(user_id)
                if user not in group.users:
                    group.users.append(user)
                else:
                    return redirect(f'/project/{group.id}/add_user')
            db.session.commit()
            return redirect('/')
    return render_template("groups/add_user.html", users=users)


@core_bp.route('/project/<int:project_id>/upload', methods=['GET', 'POST'])
def upload_file_to_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = FileUploadForm(request.files)
    if request.method == "POST":
        if form.validate_on_submit():
            file = form.file.data
            filename = secure_filename(file.filename)
            file_size = len(file.read()) 
            file.seek(0)
            file_type = file.content_type
            path = f"C:/Users/dell/Documents/files/projects/{project.name}"
            file.save(os.path.join(path, filename))
            new_file = File(filename=filename, project_id=project.id, user_id=current_user.id, file_size=file_size, file_type=file_type)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('core.project_files', project_id=project_id))
    
    return render_template('projects/add_file.html', form=form)



@core_bp.route('/projects/<int:project_id>/files')
def project_files(project_id):
    project = Project.query.get_or_404(project_id)
    files = project.files
    return render_template('projects/files.html', project=project, files=files)
