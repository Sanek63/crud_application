import tornado.ioloop
from tornado.web import Application

from app.api.handlers import handlers # noqa


def make_app():
    app = Application(
        handlers=handlers
    )

    return app

def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
