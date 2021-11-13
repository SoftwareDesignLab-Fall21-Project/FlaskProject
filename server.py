from app import app_factory
from werkzeug.serving import run_simple
import os
application = None

if __name__ == '__main__':
    # from flask_cors import cross_origin, CORS
    # from flask import send_from_directory, request
    #
    # application = app_factory.create_app(debug=True)
    # application.secret_key = "fadsfji-j32kjnm89adn;2+jow"
    # CORS(application)
    #
    # # application.secret_key = os.urandom(32)
    #
    # @application.route("/datasets/dump.json", methods=["GET"])
    # @cross_origin()
    # def get_json_debug():
    #     return send_from_directory(application.static_folder, request.path[:-1])

    application = app_factory.create_app()
    application.secret_key = os.urandom(32)

    @application.route('/')
    def index():
        return application.send_static_file('index.html')

    run_simple(
        '0.0.0.0', 8080,
        application,
        use_reloader=True, threaded=True
    )
else:
    application = app_factory.create_app()
    application.secret_key = os.urandom(32)

    @application.route('/')
    def index():
        return application.send_static_file('index.html')
