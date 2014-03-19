import os
from flask import request, Flask, abort, render_template, Response
import tornado
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornadio2 import SocketConnection, TornadioRouter, SocketServer, event


APP_PORT = 8080
SOCKET_IO_PORT = 8081
ROOT = os.path.normpath(os.path.dirname(__file__))
wsgi_app = Flask(__name__)


# ---------------------------------------------------------------------------
# Tornadio Stuff

class ExampleConnection(SocketConnection):

   @event
   def message_from_client(self, message):
       print "Message: {}".format(message)
       return "Your message was: {}".format(message)


example_router = TornadioRouter(ExampleConnection, {
    'enabled_protocols': [
        'websocket',
        'xhr-polling',
        'jsonp-polling',
        'htmlfile'
    ]
})


# ---------------------------------------------------------------------------
# Flask Stuff

@wsgi_app.route('/')
def main():
    return render_template('index.html')


# ---------------------------------------------------------------------------


sock_app = tornado.web.Application(
    handlers=example_router.urls,
    socket_io_port=SOCKET_IO_PORT,
    debug=True
)

http_app = tornado.web.Application(
    [
        (r".*", tornado.web.FallbackHandler, {'fallback': WSGIContainer(wsgi_app)})
    ],
    debug=True
)


if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(http_app)
    http_server.listen(APP_PORT)

    socket_server = SocketServer(sock_app, auto_start=False)

    IOLoop.instance().start()
