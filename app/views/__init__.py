from .default import bp


def register_blueprints(app):
    """
    :type app: flask.Flask
    :param app:
    :return:
    """
    app.register_blueprint(default.bp)