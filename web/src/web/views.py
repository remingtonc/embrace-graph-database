from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from . import app

app.mount('/static', StaticFiles(directory='web/static'), name='static')

templates = Jinja2Templates(directory='web/templates')

@app.route('/')
async def home(request):
    return templates.TemplateResponse('index.html', {'request': request})
