from flask import Flask, session
from flask_login import LoginManager
from flask_bcrypt import Bcrypt # type: ignore
from decouple import config
from flask_migrate import Migrate
from .accounts.views import accounts_bp
from .core.views import core_bp
from .extensions import db
from flask_principal import Principal, identity_loaded, RoleNeed
from flask_uploads import configure_uploads
from .extensions import photos


app = Flask(__name__)
 
app.config.from_object(config("APP_SETTINGS"))
app.config['UPLOADS_DEFAULT_DEST'] = "src/static/upload/"
app.config["UPLOADED_PHOTOS_DEST"] = "src/static/upload/"
configure_uploads(app, photos)

bcrypt = Bcrypt(app)

principal = Principal(app)
db.init_app(app)

with app.app_context():
    db.create_all()


migrate = Migrate(app, db)
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "accounts.login"


app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)


@login_manager.user_loader
def loader_user(user_id):
    from .accounts.models import User
    return User.query.get(user_id)



@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    from accounts.models import User
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            identity.user = user.email
            identity.provides.update([RoleNeed(role.name) for role in user.roles])
