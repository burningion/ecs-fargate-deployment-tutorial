import requests

from flask import Flask, Response, jsonify
from flask import request as flask_request

from ddtrace import tracer, patch, config
from ddtrace.contrib.flask import TraceMiddleware


# Tracer configuration
# TODO: get this hooked up as DAEMON
tracer.configure(hostname='localhost')
patch(requests=True)

# enable distributed tracing for requests
# to send headers (globally)
config.requests['distributed_tracing'] = True

app = Flask('api')
traced_app = TraceMiddleware(app, tracer, service='thinker-api')

@app.route('/')
def hello():
    return Response({'hello': 'world'}, mimetype='application/json')


@app.route('/think/')
def think_handler():
    thoughts = requests.get('http://localhost:5050/', params={
        'subject': flask_request.args.getlist('subject', str),
    }).text
    return Response(thoughts, mimetype='application/json')
