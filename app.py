from flask import Flask, request, jsonify, render_template, send_from_directory
from backend.warehouse_layout import get_simple_warehouse_layout, get_large_warehouse_layout
import json
from backend.models import WarehouseCell
import networkx as nx
import os

app = Flask(__name__)

WAREHOUSE = {
    'simple-warehouse': get_simple_warehouse_layout(), 
    'large-warehouse': get_large_warehouse_layout()
}

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/') 
def homepage():
    return app.send_static_file('index.html')

@app.route('/warehouse/<warehouse_id>')
def get_warehouse(warehouse_id):
    warehouse = WAREHOUSE[warehouse_id]
    # blocked_nodes = warehouse
    return json.dumps({
        'dimensions': warehouse.dimensions, 
        'valid_nodes': get_all_valid_nodes(warehouse)
    })

# find pick path from respective warehouse
@app.route('/<warehouse_id>/find-pick-path', methods = ['POST'])
def find_pick_path(warehouse_id):
    data = request.get_json()
    source = (data['source']['x'], data['source']['y'])
    items = [(item['x'], item['y']) for item in data['items']]
    warehouse = WAREHOUSE[warehouse_id]
    path = warehouse.find_optimal_path(pick_points = items, source = source)
    return json.dumps({
        'path': path
    })

def get_all_valid_nodes(G):
    valid_nodes = []
    for i in range(G.dimensions[0]):
        for j in range(G.dimensions[1]):
            if G.grid[i][j] == WarehouseCell.Navigable:
                valid_nodes.append((i,j))
    return valid_nodes


if __name__ == "__main__":
    app.run(debug = True)