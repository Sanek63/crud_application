from app.api.api_v1.endpoints import MsgView, StatisticView # noqa
from app.api.base import MethodAndPathMatch # noqa

handlers = [
    (MethodAndPathMatch('POST', '/api/add'), MsgView),
    (MethodAndPathMatch('GET', '/api/get'), MsgView),
    (MethodAndPathMatch('DELETE', '/api/remove'), MsgView),
    (MethodAndPathMatch('PUT', '/api/update'), MsgView),
    (MethodAndPathMatch('GET', '/api/statistic'), StatisticView)
]
