from flask.cli import FlaskGroup
from decouple import config

from src import app


cli = FlaskGroup(app)


if __name__ == "__main__":
    
    cli()