import networkx as nx
import math


def calculate_distance(coord1, coord2):
    """
    Calculates the distance between two cities (coordinates: latitude, longitude) using Haversine formula
    """
    lat1, lon1 = coord1.x, coord1.y
    lat2, lon2 = coord2.x, coord2.y
    radius = 6371 # Radius of the Earth in km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c
    return distance


def generate_distance_matrix(cities):
    num_cities = len(cities)
    distances = [[0 for _ in range(num_cities)] for _ in range(num_cities)]
    
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = calculate_distance(cities[i], cities[j])
            distances[i][j] = distances[j][i] = distance
    
    return distances


def minimum_spanning_tree(graph):
    """
    Returns the minimum spanning tree of the graph
    """
    return nx.minimum_spanning_tree(graph)


# def adjust_weights_for_matching(graph, matching):
#     """
#     Adjusts the weights of the graph for the minimum weight matching
#     """
#     adjusted_graph = graph.copy()
#     for edge in matching:
#         adjusted_graph[edge[0]][edge[1]]['weight'] *= -1 # Negate the weight of the edges in the matching
    
#     return adjusted_graph


# def minimum_weight_matching(graph):
#     """
#     Returns the minimum weight matching of the graph
#     """
    
#     return nx.max_weight_matching(graph, maxcardinality=True)


def find_eulerian_tour(graph, start_node):
    """
    Returns the Eulerian tour of the graph
    """
    return list(nx.eulerian_circuit(graph, source=start_node))


def run(cities):
    distances = generate_distance_matrix(cities)
    num_cities = len(cities)
    
    # Create a complete graph with the cities as nodes
    graph = nx.Graph()
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            graph.add_edge(i, j, weight=distances[i][j])
    
    # Step 1: Compute minimum spanning tree
    mst = minimum_spanning_tree(graph)
    
    # Step 2: Find the set of odd-degree nodes in the minimum spanning tree
    odd_degree_nodes = [node for node, degree in dict(mst.degree()).items() if degree % 2 != 0]
    odd_degree_subgraph = graph.subgraph(odd_degree_nodes)
    
    # Step 3: Compute minimum weight perfect matching on odd-degree nodes
    matching = nx.max_weight_matching(odd_degree_subgraph, maxcardinality=True)
    
    # Step 4: Combine minimum spanning tree and minimum weight perfect matching to form a connected multigraph
    multigraph = nx.MultiGraph(mst)
    for edge in matching:
        multigraph.add_edge(*edge)
    
    # Step 5: Find an Eulerian tour in the multigraph
    eulerian_tour = find_eulerian_tour(multigraph, 0)
    
    # Step 6: Shortcut the Eulerian tour to get the TSP tour
    tsp_tour = []
    visited = set()
    for edge in eulerian_tour:
        if edge[1] not in visited:
            tsp_tour.append(edge[1])
            visited.add(edge[1])
    
    # Complete the tour by returning to the starting city
    tsp_tour.append(tsp_tour[0])
    
    # Calculate the total distance of the tour
    total_distance = sum(distances[tsp_tour[i]][tsp_tour[i + 1]] for i in range(num_cities))
    results = [tsp_tour, total_distance]
    
    return results