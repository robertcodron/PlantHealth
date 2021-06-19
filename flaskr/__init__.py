import os
from flask import Flask

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr import auth
from flaskr import plant
from dotenv import load_dotenv
from flaskr.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
load_dotenv()
from flaskr.models import *
from flaskr.database import db_session, init_db


#db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(Config)

    # we register blueprint
    app.register_blueprint(auth.bp)
    app.register_blueprint(plant.bp)
    app.add_url_rule('/', endpoint='index')

    db.init_app(app)
    migrate = Migrate(app, db)

    if test_config is None:
        # load the instance config, if it exists, when not testing
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

    return app

