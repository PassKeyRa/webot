from app import app
from app import mongo
from flask import render_template
from app.utils import *


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/show_chat/<token>')
def show_chat(token):
    chat = mongo.db.chats.find_one_or_404({"chat_token": token})
    return render_template("show_chat.html", chat=chat)


@app.errorhandler(404)
def err_404(_):
    return render_template('index.html')
