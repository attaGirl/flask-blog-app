import os
from flask import Flask


# __init__.py servers as: 
#              1. application factory 
#              2. indicate ./flaskr as package

def create_app(test_config=None):

    # create and configure the app
    # __name__ when run this file directly: '__main__'; 
    #          when import this file as module: module name
    # instance folder outside flaskr gives configuration and database files

    app = Flask(__name__, instance_relative_config=True)

    # config.from_mapping set default configuration
    # database file should be saved within instance folder

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:

        # config.from_pyfile set config from config.py within instance folder
        # when deployed, this can be used to set a real SECRET_KEY

        app.config.from_pyfile('config.py', silent=True)

    else:

        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app

