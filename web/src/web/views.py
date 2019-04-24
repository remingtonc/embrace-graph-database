from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from . import app

app.mount('/static', StaticFiles(directory='web/static'), name='static')

templates = Jinja2Templates(directory='web/templates')

@app.route('/')
async def index(request):
    return templates.TemplateResponse('index.html.jinja2', {'request': request})

@app.route('/topology/d3')
async def topology_d3(request):
    return templates.TemplateResponse('d3.html.jinja2', {'request': request})

@app.route('/topology/el_grapho')
async def topology_el_grapho(request):
    return templates.TemplateResponse('el_grapho.html.jinja2', {'request': request})

@app.route('/shortest_path')
async def shortest_path(request):
    return templates.TemplateResponse('shortest_path.html.jinja2', {'request': request})
