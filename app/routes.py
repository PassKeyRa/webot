from app import app
from app import mongo
from flask import render_template


def queue_handler():
    pass


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/show_chat/<token>')
def show_chat(token):
    chat = mongo.db.chats.find_one_or_404({"token": token})
    return render_template("show_chat.html", chat=chat)
