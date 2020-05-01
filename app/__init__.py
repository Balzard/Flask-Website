from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from app import routes