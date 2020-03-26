import os

from flask import Flask

from src.models import migrate, db
from src.command import data_load_command
from src.api import api


config_variable_name = 'FLASK_CONFIG_PATH'
default_config_path = os.path.join(os.path.dirname(__file__), 'config/local.py')
os.environ.setdefault(config_variable_name, default_config_path)

def create_app(config_file=None, settings_override=None):
    app = Flask(__name__)

    if config_file:
        app.config.from_pyfile(config_file)
    else:
        app.config.from_envvar(config_variable_name)

    if settings_override:
        app.config.update(settings_override)

    @app.cli.command("load_docs")
    def load_docs():
        data_load_command()

    init_app(app)
    api.init_app(app)

    return app


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
    #api.init_app(app)
