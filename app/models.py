from app import db


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_name = db.Column(db.String(256), nullable=False)
    chat_token = db.Column(db.String(128), nullable=False, unique=True)
    messages = db.relationship('Message', backref='chat', lazy=True)

    def __repr__(self):
        return '<Chat {}>'.format(self.chat_name)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    message = db.Column(db.String(4096))
