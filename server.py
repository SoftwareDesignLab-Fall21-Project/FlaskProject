from app import app_factory
from werkzeug.serving import run_simple
import os

application = app_factory.create_app()

#returns the capacity of the hardware sets
#using placeholder until DB is setup
@application.route('/hwcapacity')
def getHwCapacity():
    return{
        "Set 1": "5",
    }



if __name__ == '__main__':
    run_simple(
        '0.0.0.0', 8080,
        application,
        # static_files=get_static_files(),
        use_reloader=True, use_debugger=True, threaded=True
    )
