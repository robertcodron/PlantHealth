import os
from flask import Flask
from dotenv import load_dotenv
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import json
from flaskr.auth import login_required
from flaskr.models import User
from influxdb import InfluxDBClient
client = InfluxDBClient(host='192.168.80.1', port=8086)

load_dotenv()

bp = Blueprint('plant', __name__)
from flaskr.database import db_session

@bp.route('/')
def index():
    #db = get_db()
    posts = User.query.all()
    print(client.get_list_database())
    client.switch_database('plant_metric')
    """
    room_pourcent_humidity_air': 33.0, 
        'status_moisture': 0.0, 'topic': 'stats/'}, 
        {'time': '2021-06-13T13:31:05.183513Z', 
        'UUID': 1458415.0, 
        'host': 'raspberrypi', 
        'moisture_pourcent': 54.0, 
        'room-temperature': 25.0
    """

    res = client.query('SELECT time, room_pourcent_humidity_air, moisture_pourcent, room-temperature, UUID  FROM mqtt_consumer where time < now() + 1d limit 10')
    #print(dir(res))
    to_posts = list(res.get_points())
    #print(to_posts)
    return render_template('plant/index.html', posts=to_posts[0])

