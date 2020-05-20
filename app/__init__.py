from flask import Flask
from flask_login import LoginManager
from firebase_admin import credentials, initialize_app
from app.key import cred_json
import os

# instantiate the extensions
login_manager = LoginManager()

def create_app(script_info=None):
    #app settings
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    login_manager.init_app(app)
    cred = credentials.Certificate(cred_json)
    db = initialize_app(cred)

    #registering blueprints
    from app.views.contributor import contributor
    app.register_blueprint(contributor)
    from app.api.contributor import contributor_api
    app.register_blueprint(contributor_api)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
