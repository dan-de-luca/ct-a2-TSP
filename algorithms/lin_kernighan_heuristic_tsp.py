# import itertools
import math
from tqdm import tqdm


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
    threshold = 1e-10
    if -threshold <= a <= threshold:
        a = 0
        c = 0
    else:
        a = max(0, min(a, 1))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = radius * c
    return distance


def generate_distance_matrix(cities):
    num_cities = len(cities)
    distances = [[0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = calculate_distance(cities[i], cities[j])
            distances[i][j] = distances[j][i] = distance
    return distances


def two_opt_swap(tour, i, j):
    tour[i:j + 1] = reversed(tour[i:j + 1])


def calculate_total_distance(tour, distances):
    num_cities = len(tour)
    total_distance = sum(distances[tour[i - 1]][tour[i]] for i in range(num_cities))
    return total_distance


def run(cities):
    num_cities = len(cities)
    distances = generate_distance_matrix(cities)
    best_tour = list(range(num_cities))
    best_distance = calculate_total_distance(best_tour, distances)
    improvement = True
    
    print("Running heuristic algorithm TSP: Lin-Kernighan")
    print("Number of cities:", num_cities)
    
    while improvement:
        print("Iterating...")
        improvement = False
        with tqdm(total=num_cities, desc="Lin-Kernighan TSP Iteration") as pbar:
            for iteration in range(num_cities - 1):
                for subset in range(iteration + 1, num_cities):
                    new_tour = best_tour.copy()
                    two_opt_swap(new_tour, iteration, subset)
                    new_distance = calculate_total_distance(new_tour, distances)
                    
                    if new_distance < best_distance:
                        best_distance = new_distance
                        best_tour = new_tour
                        improvement = True
                pbar.update(1)
            pbar.update(1)
    
    best_distance += distances[best_tour[-1]][best_tour[0]]
    best_tour.append(best_tour[0])
    
    results = [best_tour, best_distance]
    return results