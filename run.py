from wsgiref.simple_server import make_server

from lo_framework.lo_main import FrameWork
from urls import routes, fronts

application = FrameWork(routes, fronts)

with make_server('', 8080, application) as http:
    http.serve_forever()
