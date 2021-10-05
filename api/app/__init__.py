from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
import atexit

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get('MONGODB_URL')
mongo = PyMongo(app)

from app import routes

atexit.register(routes.QueueHandler.delete_queues)
