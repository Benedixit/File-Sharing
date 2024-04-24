from flask import Blueprint, redirect, render_template, request, url_for, session, current_app
from flask_principal import Permission, RoleNeed, identity_changed, UserNeed, RoleNeed
from flask_login import login_user
from .forms import RegisterForm, LoginForm, GroupForm, ProjectForm
from src.accounts.models import User, Group, Project
from src.extensions import db, photos

accounts_bp = Blueprint("accounts", __name__)


admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))


@accounts_bp.route('/create_group', methods=['GET', 'POST'])
def create_group():
    form = GroupForm(request.form)
    if form.validate_on_submit():
        group = Group(name=form.name.data)
        db.session.add(group)
        db.session.commit()
        print(group.name)
        return redirect('/')
    return render_template('create_group.html', form=form)


@accounts_bp.route('/project/create', methods=['GET' , 'POST'])
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        filename = photos.save(form.image.data)
        project = Project(name=form.name.data, image=filename)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("core.home"))
    return render_template('project/create.html', form=form)



@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", form=form)



@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    from src import bcrypt
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user.email)
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            identity_changed.send(current_app, identity=UserNeed(user.email))
            email = user.email
            session['email'] = email
            return redirect(url_for("core.home"))
        else:
            return render_template("accounts/invalid.html", form=form)
    return render_template("accounts/login.html", form=form)




@accounts_bp.route('/logout')
def logout():
    session.pop('email', None)
    identity_changed.send(current_app, identity=UserNeed(None))
    return redirect('/login')