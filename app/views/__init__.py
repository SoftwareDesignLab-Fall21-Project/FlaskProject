from .default import bp
from flask_cors import CORS


def register_blueprints(app):
    """
    :type app: flask.Flask
    :param app:
    :return:
    """
    app.register_blueprint(default.bp)
