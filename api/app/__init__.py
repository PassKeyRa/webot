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

from app import QueueHandler, routes

atexit.register(QueueHandler.QueueHandler.delete_queues)
