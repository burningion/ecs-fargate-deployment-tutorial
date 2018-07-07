from flask_sqlalchemy import SQLAlchemy


# don't initialize the SQLAlchemy immediately
db = SQLAlchemy()


class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(128), unique=True)
    author = db.Column(db.String(32))

    subject = db.Column(db.String(32))

    def __init__(self, quote, author, subject):
        self.quote = quote
        self.author = author
        self.subject = subject

    def serialize(self):
        return {
            'id': self.id,
            'quote': self.quote,
            'author': self.author,
            'subject': self.subject
        }
