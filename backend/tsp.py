import networkx as nx
import matplotlib.pyplot as plt 
from backend.utils import multi_dict

def get_distance_matrix(graph, points):
        distance = multi_dict(2, tuple)
        for u in points:
            for v in points:
                if u == v:
                    distance[u][v] = 0
                else:
                    distance[u][v] = nx.shortest_path_length(graph, source = u, target = v)
                    distance[v][u] = distance[u][v]
        return distance


def create_graph(points, distance):
    G = nx.MultiGraph()
    for u in points:
        for v in points:
            if u!=v and G.has_edge(u, v) is False:
                G.add_edge(u, v, weight = distance[u][v])
    
    return G


def get_nodes_with_odd_degree(G):
    odd_degree_nodes = []
    for node in G.nodes:
        if G.degree(node)%2 == 1:
            odd_degree_nodes.append(node)
    
    return odd_degree_nodes


def min_weight_perfect_matching(T, G):
    visited = {}
    nodes = list(G.nodes)
    for i in nodes:
        if visited.get(i) is None:
            min_dist = 1000000
            node = None
            for j in nodes:
                if i!=j and visited.get(j) is None:
                    if G.adj[i][j][0]['weight'] < min_dist:
                        min_dist = G.adj[i][j][0]['weight']
                        node = j
            visited[i] = True
            visited[node] = True
            T.add_edge(i, node, weight = min_dist)


def get_euler_tour(G, u, euler_tour):
    euler_tour.append(u)
    neighbours = list(G.adj[u])
    for v in neighbours:
        if len(G.adj[u])>0 and is_valid_edge(G, u, v):
            G.remove_edge(u, v)
            get_euler_tour(G, v, euler_tour)


def is_valid_edge(G, u, v):
    if len(G.adj[u]) == 1: 
        return True
    visited = {}
    count_before_removal = dfs_count(G, u, visited)
    edge_weight = G.adj[u][v][0]['weight']
    G.remove_edge(u, v)
    visited = {}
    count_after_removal = dfs_count(G, u, visited)
    G.add_edge(u, v, weight = edge_weight)   
    return False if count_after_removal<count_before_removal else True


def dfs_count(G, u, visited):
    visited[u] = True
    neighbours = list(G.adj[u])
    count = 1
    for v in neighbours:
        if visited.get(v) is None:
            count += dfs_count(G, v, visited)
    return count


def get_hamiltonian_circuit(euler_tour, num_of_nodes):
    visited = {}
    tour = []
    for node in euler_tour:
        if visited.get(node) is None:
            tour.append(node)
            visited[node] = True
    tour.append(euler_tour[0])
    return tour


def christofides(graph, pick_points, source):

    # create graph G
    points = [source] + pick_points
    distance = get_distance_matrix(graph, points)
    G = create_graph(points, distance)

    # create minimum spanning tree of G
    T = nx.minimum_spanning_tree(G)

    # get nodes with odd degree in T
    odd_degree_nodes = get_nodes_with_odd_degree(T)
    
    # create a subgraph S of odd degree nodes in T 
    S = G.subgraph(nodes=odd_degree_nodes)
    
    # perform min-weight perfect matching of the nodes in S
    min_weight_perfect_matching(T, S)

    # create euler circuit
    euler_tour = []
    get_euler_tour(T, source, euler_tour)

    # create hamiltonian circuit
    final_tour = get_hamiltonian_circuit(euler_tour, T.number_of_nodes())
    return final_tour