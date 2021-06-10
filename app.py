import os
from flask import Flask
from dotenv import load_dotenv
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()


app = Flask(__name__)
#env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(Config)


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from . import routes, models


if __name__ == '__main__':
    app.run()
