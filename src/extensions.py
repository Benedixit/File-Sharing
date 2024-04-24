from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES

db = SQLAlchemy()

photos = UploadSet("photos", IMAGES)


