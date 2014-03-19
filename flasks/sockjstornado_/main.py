import os
from flask import Flask, render_template
import tornado, tornado.httpserver
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop

import sockjs.tornado


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
    import logging
    logging.getLogger().setLevel(logging.DEBUG)


    http_server = tornado.httpserver.HTTPServer(http_app)
    http_server.listen(8080)

    sock_app.listen(8081)

    IOLoop.instance().start()
