from wsgiref.simple_server import make_server

from lo_framework.lo_main import FrameWork, FakeFrameWork, DebugFrameWork
from urls import fronts
from views import routes

# application = FrameWork(routes, fronts)
application = DebugFrameWork(routes, fronts)
# application = FakeFrameWork(routes, fronts)

with make_server('', 8080, application) as http:
    http.serve_forever()
