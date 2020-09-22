from flask.cli import FlaskGroup
from app import create_app
from flask import current_app
import os

from app.key import cred_json

app = create_app()
cli = FlaskGroup(create_app=create_app)

from seed_db import seed_users
from recreate_db import empty_db

#Can add cli commands for web app here
@cli.command()
def test():
    """ Runs the tests without code coverage"""
    os.system("python -m pytest -x --disable-warnings --cache-clear app/tests/")

@cli.command()
def recreate_db():
    if cred_json.get("project_id") == "pixel-editor-test":
        empty_db()
    else:
        print("Can only perform tests on Testing DB")

@cli.command()
def seed_db():
    if cred_json.get("project_id") == "pixel-editor-test":
        seed_users()
    else:
        print("Can only perform tests on Testing DB")

if __name__ == '__main__':
    cli()
