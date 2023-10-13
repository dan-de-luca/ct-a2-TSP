import itertools
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


def calculate_total_distance(tour, distances):
    total_distance = 0
    num_cities = len(tour)
    for i in range(num_cities):
        total_distance += distances[tour[i]][tour[(i + 1) % num_cities]]
    return total_distance


def find_best_k_opt(tour, distances):
    num_cities = len(tour)
    best_distance = calculate_total_distance(tour, distances)
    best_tour = tour
    
    for i in range(num_cities):
        for j in range(i + 2, num_cities - 1):
            if i == 0 and j == num_cities - 1:
                continue
            new_tour = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:] # 2-opt swap
            new_distance = calculate_total_distance(new_tour, distances)
            if new_distance < best_distance:
                best_distance = new_distance
                best_tour = new_tour
    return best_tour


def run(cities):
    distances = generate_distance_matrix(cities)
    num_cities = len(distances)
    initial_tour = list(range(num_cities))
    best_tour = initial_tour
    best_distance = calculate_total_distance(initial_tour, distances)
    
    for iteration in range(num_cities - 1):
        for subset in itertools.combinations(range(num_cities), iteration + 2):
            subset_tour = [initial_tour[i] for i in subset]
            subset_distance = calculate_total_distance(subset_tour, distances)
            for _ in range(num_cities - iteration):
                subset_tour = find_best_k_opt(subset_tour, distances)
                new_distance = calculate_total_distance(subset_tour, distances)
                if new_distance < subset_distance:
                    subset_distance = new_distance
                else:
                    break
            if subset_distance < best_distance:
                best_distance = subset_distance
                best_tour = subset_tour
    
    results = [best_tour, best_distance]
    
    return results