from starlette.responses import HTMLResponse
from . import app

@app.route('/')
async def home(request):
    return HTMLResponse('<html><body><h1>Demo!</h1></body></html>')
