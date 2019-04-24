from collections import ChainMap
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

@app.route('/api/v1/collection_counts', methods=['POST'])
async def api_collection_counts(request):
    requested_collections = await request.json()
    collection_count_query = """
    LET given_collections = @given_collections
    FOR collection IN given_collections
        RETURN {
            [ collection ]: COLLECTION_COUNT(collection)
        }
    """
    bind_vars = {'given_collections': requested_collections}
    collection_counts = arangodb_client.aql.execute(collection_count_query, bind_vars=bind_vars)
    return JSONResponse(
        {
            collection: count for collection_count in collection_counts
            for collection, count in collection_count.items()
        }
    )

@app.route('/api/v1/nodes')
async def api_nodes(request):
    nodes_aql = """
    FOR node IN Nodes
        RETURN node
    """
    nodes = arangodb_client.aql.execute(nodes_aql)
    return JSONResponse([node for node in nodes])

@app.route('/api/v1/weights')
async def api_weights(request):
    return JSONResponse(["distance"])

@app.route('/api/v1/topology/shortest_path')
async def api_topology_shortest_path(request):
    shortest_path_aql = """
    FOR vertex, edge
        IN ANY SHORTEST_PATH
        @from_node TO @to_node
        GRAPH "Topology"
        OPTIONS {
            weightAttribute: @weight_attribute
        }
        RETURN {
            "node": vertex,
            "connection": edge
        }
    """
    bind_vars = {
        'from_node': request.query_params['fromNode'],
        'to_node': request.query_params['toNode'],
        'weight_attribute': request.query_params['weightAttribute']
    }
    shortest_path = arangodb_client.aql.execute(shortest_path_aql, bind_vars=bind_vars)
    return JSONResponse([element for element in shortest_path])

@app.route('/api/v1/topology/d3')
async def api_topology_d3(request):
    node_aql = """
    FOR node IN Nodes
        RETURN {
            "id": node._id,
            "label": node._key,
            "value": node.temperature
        }
    """
    nodes = [
        node for node
        in arangodb_client.aql.execute(node_aql)
    ]
    edge_aql = """
    FOR connection IN Connections
        RETURN {
            "source": connection._from,
            "target": connection._to,
            "value": connection.distance
        }
    """
    edges = [
        edge for edge
        in arangodb_client.aql.execute(edge_aql)
    ]
    return JSONResponse(
        {
            'nodes': nodes,
            'links': edges
        }
    )

@app.route('/api/v1/topology/el_grapho')
async def api_topology_el_grapho(request):
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
                {'group': index} for index, node in enumerate(nodes)
            ],
            'edges': [
                {
                    'from': node_indices[edge[0]],
                    'to': node_indices[edge[1]]
                } for edge in edges
            ]
        }
    )
