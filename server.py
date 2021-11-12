from app import app_factory
from werkzeug.serving import run_simple
from flask_cors import CORS
from app.scripts import mongo

application = app_factory.create_app()
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

try:
    application.config['MONGO_URI'] = "mongodb+srv://tbertolino:softwarelabfall2021@cluster0.mphmj.mongodb.net/SoftwareDesignLab-Fall21-Project?retryWrites=true&w=majority"
    mongo.init_app(application)
except Exception as ex:
    print("*****ERRROR DATABASE*****")
    print(ex)

if __name__ == '__main__':
    run_simple(
        '127.0.0.1', 5000,
        application,
        # static_files=get_static_files(),
        use_reloader=True, use_debugger=True, threaded=True
    )
