import os
from flask import Flask, render_template
import tornado, tornado.httpserver
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop

import sockjs.tornado


HTTP_PORT = 8080
SOCKJS_PORT = 8081
ROOT = os.path.normpath(os.path.dirname(__file__))
wsgi_app = Flask(__name__)


# ---------------------------------------------------------------------------
# SockJS Tornado Stuff

class ExampleConnection(sockjs.tornado.SockJSConnection):

    def on_message(self, message):
        print "Message: {}".format(message)
        self.send("Your message was: {}".format(message))


def example_router(prefix):
    return sockjs.tornado.SockJSRouter(ExampleConnection, prefix)


# ---------------------------------------------------------------------------
# Flask Stuff

@wsgi_app.route('/')
def main():
    return render_template('index.html')


# ---------------------------------------------------------------------------


sock_app = tornado.web.Application(
    handlers=example_router('/info').urls,
    debug=True
)

http_app = tornado.web.Application(
    [
        (r".*", tornado.web.FallbackHandler, {'fallback': WSGIContainer(wsgi_app)})
    ],
    debug=True
)


if __name__ == '__main__':
    print "sockjs-tornado version running on port {}".format(HTTP_PORT)

    http_server = tornado.httpserver.HTTPServer(http_app)
    http_server.listen(HTTP_PORT)

    sock_app.listen(SOCKJS_PORT)

    IOLoop.instance().start()
