from gevent import monkey; monkey.patch_all()
import gevent
from socketio import socketio_manage
from socketio.namespace import BaseNamespace

from flask import request, Flask, abort, render_template, Response


PORT = 8080
app = Flask(__name__)
app.debug = True


# ---------------------------------------------------------------------------
# Socket.IO Stuff

class HellowWorldNamespace(BaseNamespace):

    def on_message_from_client(self, message):
        print "Message: {}".format(message)
        return "Your message was: {}".format(message)


# ---------------------------------------------------------------------------
# Flask Stuff

@app.route('/socket.io/<path:remaining>')
def handle_websocket(remaining):
    try:
        socketio_manage(request.environ, {'/hello': HellowWorldNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection", exc_info=True)
    return Response()


@app.route('/')
def main():
    return render_template('index.html')


# ---------------------------------------------------------------------------


from socketio.server import SocketIOServer


if __name__ == '__main__':
    print "Flask-SockeetIO exmaple running on port {}".format(PORT)
    SocketIOServer(("0.0.0.0", PORT), app, resource="socket.io").serve_forever()
