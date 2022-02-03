from tornado.web import RequestHandler


__all__ = ['BaseHandler', ]


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._set_header()
        self._set_ssl()

    def _set_header(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.set_header("Expires", "0")
        self.set_header("Pragma", "no-cache")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, PATCH, DELETE, HEAD, OPTIONS")
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin", ""))

    def _set_ssl(self):
        if self.request.headers.get("Ssl") == "on":
            self.https = True
            self.scheme = "https://"
        else:
            self.https = False
            self.scheme = "http://"
