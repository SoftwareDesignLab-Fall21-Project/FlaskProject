import logging

from flask import Flask, url_for
from . import views
from werkzeug.middleware.shared_data import SharedDataMiddleware
import os
from flask_cors import CORS
from app.scripts import mongo


def create_app(debug=False):
    """ Creates the Flask instance for the WSGI application.

    :return: A Flask instance which can be used by a WSGI application.
    """
    app = Flask(__name__,
                instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
