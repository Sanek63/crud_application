from tornado.routing import PathMatches


__all__ = ['MethodAndPathMatch', ]

class MethodAndPathMatch(PathMatches):
    def __init__(self, method, path_pattern):
        super().__init__(path_pattern)
        self.method = method

    def match(self, request):
        if request.method != self.method:
            return None

        return super().match(request)