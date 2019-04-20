from starlette.responses import JSONResponse
from . import app

@app.route('/api/v1/topology')
async def topology(request):
    return JSONResponse({'demo': 'demo'})
