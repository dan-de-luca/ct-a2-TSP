import networkx as nx
import math
from tqdm import tqdm

#######################################################################################################################################################


def get_length(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1.0 / 2.0)


def build_graph(data):
    graph = {}
    for this in range(len(data)):
        for another_point in range(len(data)):
            if this != another_point:
                if this not in graph:
                    graph[this] = {}

                graph[this][another_point] = get_length(data[this][0], data[this][1], data[another_point][0],
                                                        data[another_point][1])

    return graph


class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def minimum_spanning_tree(G):
    tree = []
    subtrees = UnionFind()
    for W, u, v in sorted((G[u][v], u, v) for u in G for v in G[u]):
        if subtrees[u] != subtrees[v]:
            tree.append((u, v, W))
            subtrees.union(u, v)

    return tree


def find_odd_vertexes(MST):
    tmp_g = {}
    vertexes = []
    for edge in MST:
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0

        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0

        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1

    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)

    return vertexes


def minimum_weight_matching(MST, G, odd_vert):
    import random
    random.shuffle(odd_vert)

    while odd_vert:
        v = odd_vert.pop()
        length = float("inf")
        u = 1
        closest = 0
        for u in odd_vert:
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u

        MST.append((v, closest, length))
        odd_vert.remove(closest)


def find_eulerian_tour(MatchedMSTree, G):
    # find neigbours
    neighbours = {}
    for edge in MatchedMSTree:
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])

    # print("Neighbours: ", neighbours)

    # finds the hamiltonian circuit
    start_vertex = MatchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]

    while len(MatchedMSTree) > 0:
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            remove_edge_from_matchedMST(MatchedMSTree, v, w)

            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)

            v = w

    return EP


def remove_edge_from_matchedMST(MatchedMST, v1, v2):

    for i, item in enumerate(MatchedMST):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del MatchedMST[i]

    return MatchedMST


def tsp(data):
    # build a graph
    G = build_graph(data)
    # print("Graph: ", G)

    # build a minimum spanning tree
    MSTree = minimum_spanning_tree(G)
    # print("MSTree: ", MSTree)

    # find odd vertexes
    odd_vertexes = find_odd_vertexes(MSTree)
    # print("Odd vertexes in MSTree: ", odd_vertexes)

    # add minimum weight matching edges to MST
    minimum_weight_matching(MSTree, G, odd_vertexes)
    # print("Minimum weight matching: ", MSTree)

    # find an eulerian tour
    eulerian_tour = find_eulerian_tour(MSTree, G)

    # print("Eulerian tour: ", eulerian_tour)

    current = eulerian_tour[0]
    path = [current]
    visited = [False] * len(eulerian_tour)
    visited[eulerian_tour[0]] = True
    length = 0

    for v in eulerian_tour:
        if not visited[v]:
            path.append(v)
            visited[v] = True

            length += G[current][v]
            current = v

    length +=G[current][eulerian_tour[0]]
    path.append(eulerian_tour[0])

    # print("Result path: ", path)
    # print("Result length of the path: ", length)

    return length, path



#######################################################################################################################################################

def calculate_distance(coord1, coord2):
    """
    Calculates the distance between two cities (coordinates: latitude, longitude) using Haversine formula
    """
    lat1, lon1 = coord1.x, coord1.y
    lat2, lon2 = coord2.x, coord2.y
    radius = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance


def generate_distance_matrix(cities):
    num_cities = len(cities)
    distances = [[calculate_distance(cities[i], cities[j]) for j in range(num_cities)] for i in range(num_cities)]
    return distances


# def minimum_spanning_tree(graph):
#     """
#     Returns the minimum spanning tree of the graph
#     """
#     return nx.minimum_spanning_tree(graph)


# def find_eulerian_tour(graph, start_node):
#     """
#     Returns the Eulerian tour of the graph
#     """
#     return list(nx.eulerian_circuit(graph, source=start_node))


def run(cities):
    distances = generate_distance_matrix(cities)
    num_cities = len(cities)
    
    # Run Christofides (approximation) TSP with progress bar
    print("Running approximation algorithm TSP: Christofides")
    print("Number of cities:", num_cities)
    
    with tqdm(total=1, desc="Christofides TSP") as pbar:
        results = tsp(distances)
        pbar.update(1)
    
    # with tqdm(total=9, desc="Christofides TSP") as pbar:
    #     # Step 0: Create a complete graph with the cities as nodes
    #     graph = nx.Graph()
    #     for i in range(num_cities):
    #         for j in range(i + 1, num_cities):
    #             graph.add_edge(i, j, weight=distances[i][j])
    #     pbar.update(1)
        
    #     # Step 1: Compute minimum spanning tree
    #     mst = minimum_spanning_tree(graph)
    #     pbar.update(1)
        
    #     # Step 2: Find the set of odd-degree nodes in the minimum spanning tree
    #     odd_degree_nodes = [node for node, degree in dict(mst.degree()).items() if degree % 2 != 0]
    #     odd_degree_subgraph = graph.subgraph(odd_degree_nodes)
    #     pbar.update(1)
        
    #     # Step 3: Compute minimum weight perfect matching on odd-degree nodes
    #     matching = nx.max_weight_matching(odd_degree_subgraph, maxcardinality=True)
    #     pbar.update(1)

    #     # Step 4: Combine minimum spanning tree and minimum weight perfect matching to form a connected multigraph
    #     multigraph = nx.MultiGraph(mst)
    #     for edge in matching:
    #         multigraph.add_edge(*edge)
    #     pbar.update(1)

    #     # Step 5: Find an Eulerian tour in the multigraph
    #     eulerian_tour = find_eulerian_tour(multigraph, start_node=0)
    #     pbar.update(1)

    #     # Step 6: Shortcut the Eulerian tour to get the TSP tour
    #     tsp_tour = []
    #     visited = set()
    #     for edge in eulerian_tour:
    #         if edge[1] not in visited:
    #             tsp_tour.append(edge[1])
    #             visited.add(edge[1])
    #     pbar.update(1)

    #     # Step 7: Complete the tour by returning to the starting city
    #     tsp_tour.append(tsp_tour[0])
    #     pbar.update(1)

    #     # Step 8: Calculate the total distance of the tour
    #     total_distance = sum(distances[tsp_tour[i]][tsp_tour[i + 1]] for i in range(num_cities))
    #     results = [tsp_tour, total_distance]
    #     pbar.update(1)
    
    
    
    return results


# def run(cities):
#     distances = generate_distance_matrix(cities)
#     num_cities = len(cities)
    
#     # Run Christofides (approximation) TSP with progress bar
#     print("Running approximation algorithm TSP: Christofides")
#     print("Number of cities:", num_cities)
#     with tqdm(total=9, desc="Christofides TSP") as pbar:
#         # Step 0: Create a complete graph with the cities as nodes
#         graph = nx.Graph()
#         graph.add_nodes_from(range(num_cities))
#         for i in range(num_cities):
#             for j in range(i + 1, num_cities):
#                 graph.add_edge(i, j, weight=distances[i][j])
#         pbar.update(1)
        
#         # Step 1: Compute minimum spanning tree
#         mst = nx.minimum_spanning_tree(graph)
#         pbar.update(1)
        
#         # Step 2: Find the set of odd-degree nodes in the minimum spanning tree
#         odd_degree_nodes = [node for node, degree in mst.degree() if degree % 2 != 0]
#         pbar.update(1)
        
#         # Step 3: Compute minimum weight perfect matching on odd-degree nodes
#         matching_edges = nx.max_weight_matching(mst, maxcardinality=True)
#         matching_graph = nx.Graph(list(matching_edges))
#         pbar.update(1)

#         # Step 4: Combine minimum spanning tree and minimum weight perfect matching to form a connected multigraph
#         multigraph = nx.MultiGraph(mst)
#         multigraph.add_edges_from(matching_graph.edges())
#         pbar.update(1)

#         # Step 5: Find an Eulerian tour in the multigraph
#         eulerian_tour_edges = nx.eulerian_circuit(multigraph)
        
#         # Extract the nodes from the Eulerian tour
#         eulerian_tour_nodes = [edge[0] for edge in eulerian_tour_edges]
#         eulerian_tour_nodes.append(eulerian_tour_edges[-1][1]) # Add the last node of the last edge
#         pbar.update(1)

#         # Step 6: Shortcut the Eulerian tour to get the TSP tour
#         visited = set()
#         tsp_tour = []
#         for node in eulerian_tour_nodes:
#             if node not in visited:
#                 tsp_tour.append(node)
#                 visited.add(node)
#         pbar.update(1)

#         # Step 7: Complete the tour by returning to the starting city
#         tsp_tour.append(tsp_tour[0])
#         pbar.update(1)

#         # Step 8: Calculate the total distance of the tour
#         total_distance = sum(distances[tsp_tour[i]][tsp_tour[i + 1]] for i in range(num_cities))
#         results = [tsp_tour, total_distance]
#         pbar.update(1)
    
#     return results
