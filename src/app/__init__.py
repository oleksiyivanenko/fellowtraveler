from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

flask_bcrypt = Bcrypt(app)

from app.auth.views import auth
from app.auth.models import User
app.register_blueprint(auth)

from app.destinations.views import destinations
app.register_blueprint(destinations)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

