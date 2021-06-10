from .app import app
from .config import Config
from .models import User

@app.route('/')
@app.route('/index')
def index():
    secret_key = app.config.get("SECRET_KEY")
    return f"The configured secret key is {secret_key}."