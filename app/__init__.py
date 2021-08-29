from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_pymongo import PyMongo
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
                           'Testing_Secret_Key'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
#                                        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config["MONGO_URI"] = os.environ.get('MONGODB_URL')  # "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from app import routes
