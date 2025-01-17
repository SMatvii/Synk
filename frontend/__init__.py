from os import getenv
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
BACKEND_URL = getenv("BACKEND_URL")

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = SECRET_KEY


from . import routes