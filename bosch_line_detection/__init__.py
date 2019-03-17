from flask import Flask
import os
from os.path import join, dirname, realpath


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'bosch_line_detection.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    upload_folder = join(dirname(realpath(__file__)), 'static/uploads/')
    try:
        os.makedirs(app.instance_path)
        os.makedirs(upload_folder)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # configure upload_folder to save all uploaded files
    app.config['UPLOAD_FOLDER'] = upload_folder       # todo: make this configurable

    # register the database commands
    from . import db
    db.init_app(app)

    # apply the blueprints to the app
    from . import server
    app.register_blueprint(server.bp)

    return app
