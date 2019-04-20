from starlette.applications import Starlette

app = Starlette(debug=True)

from . import api
from . import views
