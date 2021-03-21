import os
from flask import Flask
from shorty.api import api
from dotenv import load_dotenv

def create_app(settings_overrides=None):
    app = Flask(__name__)
    configure_settings(app, settings_overrides)
    configure_blueprints(app)
    return app


def configure_settings(app, settings_override):
    load_dotenv()
    app.config.from_object(os.environ['APP_SETTINGS'])
    if settings_override:
        app.config.update(settings_override)


def configure_blueprints(app):
    app.register_blueprint(api)