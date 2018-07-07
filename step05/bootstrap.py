from flask import Flask
from ddtrace import tracer, patch
patch(sqlalchemy=True,sqlite3=True)
from models import Thought, db


# configure the tracer so that it reaches the Datadog Agent
# available in another container
tracer.configure(hostname='localhost')


def create_app():
    """Create a Flask application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    initialize_database(app, db)
    return app


def initialize_database(app, db):
    """Drop and restore database in a consistent state"""
    with app.app_context():
        db.drop_all()
        db.create_all()

        db.session.add(Thought(quote='My religion consists of a humble admiration of the illimitable superior spirit who reveals himself in the slight details we are able to perceive with our frail and feeble mind.',
                               author='Albert Einstein',
                               subject='religion'))

        db.session.add(Thought(quote='For a successful technology, reality must take precedence over public relations, for Nature cannot be fooled.',
                               author='Richard Feynman',
                               subject='technology'))
        db.session.add(Thought(quote='One is left with the horrible feeling now that war settles nothing; that to win a war is as disastrous as to lose one.',
                               author='Agatha Christie',
                               subject='war'))
        db.session.add(Thought(quote='Life grants nothing to us mortals without hard work.',
                               author='Horace',
                               subject='work'))
        db.session.add(Thought(quote='Ah, music. A magic beyond all we do here!',
                               author='J. K. Rowling',
                               subject='music'))
        db.session.add(Thought(quote='I think that God in creating Man somewhat overestimated his ability.',
                               author='Oscar Wilde',
                               subject='mankind'))
        db.session.commit()
