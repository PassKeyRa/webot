from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_pymongo import PyMongo
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get('MONGODB_URL')
mongo = PyMongo(app)


from app import routes
