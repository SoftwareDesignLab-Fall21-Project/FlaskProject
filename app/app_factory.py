from flask import Flask, url_for
from . import views
from werkzeug.middleware.shared_data import SharedDataMiddleware
import os
from flask_cors import CORS
from app.scripts import mongo


def create_app(test_config=None):
    """ Creates the Flask instance for the WSGI application.

    :param test_config: (optional) Any additional config options to pass to the app instance for debug purposes.
    :return: A Flask instance which can be used by a WSGI application.
    """
    app = Flask(__name__,
                instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/static': os.path.join(os.path.dirname(__file__), 'static')
    })

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    try:
        app.config['MONGO_URI'] = "mongodb+srv://tbertolino:softwarelabfall2021@cluster0.mphmj.mongodb.net" \
                                          "/SoftwareDesignLab-Fall21-Project?retryWrites=true&w=majority "
        mongo.init_app(app)
    except ValueError as ex:
        print("*****ERRROR DATABASE*****")
        print(ex)
        return None

    views.register_blueprints(app)

    return app
