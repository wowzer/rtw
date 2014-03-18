import os
from flask import request, Flask, abort, render_template, Response
import tornado
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop

import sockjs.tornado


ROOT = os.path.normpath(os.path.dirname(__file__))
wsgi_app = Flask(__name__)


# ---------------------------------------------------------------------------
# Tornadio Stuff

class ExampleConnection(sockjs.tornado.SockJSConnection):

   @event
   def message_from_client(self, message):
       print "Message: {}".format(message)
       return "Your message was: {}".format(message)


def example_router(prefix):
   return sockjs.tornado.SockJSRouter(ExampleConnection, prefix).urls)


# ---------------------------------------------------------------------------
# Flask Stuff

@wsgi_app.route('/')
def main():
    return render_template('index.html')


# ---------------------------------------------------------------------------


sock_app = tornado.web.Application(
    handlers=example_router.urls,
    socket_io_port=8081,
    debug=True
)

http_app = tornado.web.Application(
    [
        (r".*", tornado.web.FallbackHandler, {'fallback': WSGIContainer(wsgi_app)})
    ],
    debug=True
)


if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)


    http_server = tornado.httpserver.HTTPServer(http_app)
    http_server.listen(8080)

    socket_server = SocketServer(sock_app, auto_start=False)

    IOLoop.instance().start()
