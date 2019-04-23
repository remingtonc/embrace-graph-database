from starlette.applications import Starlette
from . import settings

app = Starlette()
app.debug = settings.DEBUG

from . import api
from . import views
