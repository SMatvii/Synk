from os import getenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
BACKEND_URL = getenv("BACKEND_URL")

csrf = CSRFProtect()

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = SECRET_KEY
csrf.init_app(flask_app)


from . import routes
