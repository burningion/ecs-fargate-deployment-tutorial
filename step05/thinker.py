import requests

from flask import Flask, Response, jsonify
from flask import request as flask_request

from flask_caching import Cache

from ddtrace import tracer, patch
from ddtrace.contrib.flask import TraceMiddleware

from bootstrap import create_app
from models import Thought

from time import sleep

patch(redis=True)
app = create_app()
cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST': 'localhost'})
cache.init_app(app)

traced_app = TraceMiddleware(app, tracer, service='thinker-microservice', distributed_tracing=True)

# Tracer configuration
# TODO: make this DAEMON
tracer.configure(hostname='localhost')

@tracer.wrap(name='think')
@cache.memoize(30)
def think(subject):
    tracer.current_span().set_tag('subject', subject)

    sleep(0.5)
    quote = Thought.query.filter_by(subject=subject).first()

    if quote is None:
        return Thought(quote='Hmmm, that\'s something I\'ll need to think about.',
                       author='The Machine',
                       subject=subject)
    return quote

@app.route('/')
def think_microservice():
    # because we have distributed tracing, don't need to manually grab headers
    subject = flask_request.args.get('subject')
    thoughts = think(subject)
    return jsonify(thoughts.serialize())
