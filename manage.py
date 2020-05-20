from flask.cli import FlaskGroup
from app import create_app
from flask import current_app

app = create_app()
cli = FlaskGroup(create_app=create_app)

#Can add cli commands for web app here

if __name__ == '__main__':
    cli()
