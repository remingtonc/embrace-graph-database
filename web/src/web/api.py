from starlette.responses import JSONResponse
from arango import ArangoClient
from . import app, settings

arangodb_client = None

@app.on_event('startup')
def startup():
    global arangodb_client
    arangodb_client = ArangoClient(host=settings.ARANGODB_HOST)
    arangodb_client = arangodb_client.db(
        settings.ARANGODB_DATABASE,
        username=settings.ARANGODB_USERNAME,
        password=str(settings.ARANGODB_PASSWORD)
    )

@app.route('/api/v1/topology/el_grapho')
async def topology(request):
    node_aql = """
    FOR node IN Nodes
        RETURN node._id
    """
    nodes = [
        node for node
        in arangodb_client.aql.execute(node_aql)
    ]
    node_indices = {}
    for index, node in enumerate(nodes):
        node_indices[node] = index
    edge_aql = """
    FOR connection IN Connections
        RETURN connection
    """
    edges = [
        (edge['_from'], edge['_to']) for edge
        in arangodb_client.aql.execute(edge_aql)
    ]
    return JSONResponse(
        {
            'nodes': [
                {'group': 0} for node in nodes
            ],
            'edges': [
                {
                    'from': node_indices[edge[0]],
                    'to': node_indices[edge[1]]
                } for edge in edges
            ]
        }
    )
