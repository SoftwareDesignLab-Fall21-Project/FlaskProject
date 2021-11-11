from app import app_factory
from werkzeug.serving import run_simple

application = app_factory.create_app()

if __name__ == '__main__':
    run_simple(
        '0.0.0.0', 8080,
        application,
        # static_files=get_static_files(),
        use_reloader=True, use_debugger=True, threaded=True
    )
