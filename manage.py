from flask.cli import FlaskGroup
from app import create_app
from flask import current_app
import os

app = create_app()
cli = FlaskGroup(create_app=create_app)

#Can add cli commands for web app here
@cli.command()
def test():
  """ Runs the tests without code coverage"""
  os.system("python -m pytest -x --disable-warnings --cache-clear app/tests/")

if __name__ == '__main__':
    cli()
