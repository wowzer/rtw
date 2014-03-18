from flask import request, Flask, abort, render_template
app = Flask(__name__)


@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            print message
            wsock.send("Your message was: {}".format(message)):
            break


@app.route('/')
def main():
    return render_template('index.html')


# ---------------------------------------------------------------------------


from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

WSGIServer(("0.0.0.0", 8080), app, handler_class=WebSocketHandler).serve_forever()
