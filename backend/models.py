import enum
import networkx as nx
from backend.utils import multi_dict
from backend.tsp import christofides
from networkx.algorithms.shortest_paths.generic import shortest_path 
import json
from collections import namedtuple
from json import JSONEncoder

class Warehouse(object):
    dimensions = None
    grid = None
    graph = None

    def __init__(self, dimensions, grid):
        self.dimensions = dimensions
        self.grid = grid
        self.graph = self.create_graph()


    def init_graph(self):
        G = nx.Graph()
        n, m = self.dimensions
        for i in range(n):
            for j in range(m):
                G.add_node((i,j))

        return G


    def check(self, v):
        n, m = self.dimensions
        x, y = v
        if x>=0 and x<n and y>=0 and y<m:
            if self.grid[x][y] == WarehouseCell.Navigable:
                return True
            else:
                return False
        else:
            return False


    def add_neighbour(self, G, u, v):
        if self.check(v) is True and G.has_edge(u,v) is False:
            G.add_edge(u, v, weight = 1)


    def create_graph(self):
        n, m = self.dimensions
        offsets = [(1,0), (-1,0), (0,1), (0,-1)]
        G = self.init_graph()
        for i in range(n):
            for j in range(m):
                if self.grid[i][j] == WarehouseCell.Navigable:
                    for offset in offsets:
                        x, y = offset
                        u = (i, j)
                        v = (i+x, j+y)
                        self.add_neighbour(G, u, v)
                    
        return G

    
    def _get_complete_path_and_cost(self, tour):
        complete_path = [tour[0]]
        cost = 0
        for i, u in enumerate(tour[:len(tour)-1]):
            v = tour[i+1]
            cells_in_path = shortest_path(self.graph, source = u, target = v)
            cost += len(cells_in_path)
            for cell in cells_in_path[1:]:
                complete_path.append(cell)
        return complete_path, cost


    def find_optimal_path(self, pick_points, source):
        tour = christofides(self.graph, pick_points, source)
        complete_path, cost = self._get_complete_path_and_cost(tour)
        # cost for comparing if more algorithms used 
        return complete_path

    def _build_response(self, cells):
        response = {
            'path': []
        }
        for cell in cells:
            response['path'].append({
                'x': cell[0], 'y': cell[1]
            })
        return response

class WarehouseCell(enum.Enum):
    Navigable = 1
    Shelving = 2
    