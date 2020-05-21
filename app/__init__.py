from flask import Flask
import os

def create_app(script_info=None):
    #app settings
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    #registering blueprints
    from app.views.contributor import contributor
    app.register_blueprint(contributor)
    from app.api.contributor import contributor_api
    app.register_blueprint(contributor_api)

    @app.shell_context_processor
    def ctx():
        return {'app': app}
    return app
