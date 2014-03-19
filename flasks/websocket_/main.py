from flask import request, Flask, abort, render_template


PORT = 8080
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
            wsock.send("Your message was: {}".format(message))
        except:
            pass

@app.route('/')
def main():
    return render_template('index.html')


# ---------------------------------------------------------------------------


from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


if __name__ == '__main__':
    print "Flask-websocket version running on port {}".format(PORT)
    WSGIServer(("0.0.0.0", PORT), app, handler_class=WebSocketHandler).serve_forever()
