from flask import Flask
import os
from firebase_admin import credentials, initialize_app
from app.key import cred_json
import firebase_admin

def create_app(script_info=None):
    #app settings
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_json)
        default_app = initialize_app(cred)

    #registering blueprints
    #View
    from app.views.contributor import contributor
    app.register_blueprint(contributor)
    from app.views.admin import admin
    app.register_blueprint(admin)
    from app.views.graphics import graphics
    app.register_blueprint(graphics)
    from app.views.super_admin import super_admin
    app.register_blueprint(super_admin)

    #API
    from app.api.contributor import contributor_api
    app.register_blueprint(contributor_api)
    from app.api.reviewer import reviewer_api
    app.register_blueprint(reviewer_api)
    from app.api.admin import admin_api
    app.register_blueprint(admin_api)
    from app.api.graphics import graphics_api
    app.register_blueprint(graphics_api)
    from app.api.super_admin import super_admin_api
    app.register_blueprint(super_admin_api)

    @app.shell_context_processor
    def ctx():
        return {'app': app}
    return app
