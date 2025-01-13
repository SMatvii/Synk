from os import getenv
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
BACKEND_URL = getenv("BACKEND_URL")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


from . import routes
