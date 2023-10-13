import sys
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


# def tsp_helper(distances, num_cities, memo, mask, last_city):
#     """
#     Helper function to calculate the minimum distance for a subset of cities
#     """
#     if mask == (1 << num_cities) - 1:
#         return distances[last_city][0]
    
#     if (mask, last_city) in memo:
#         return memo[(mask, last_city)]
    
#     min_distance = float('inf')
#     for city in range(num_cities):
#         if mask & (1 << city) == 0: # If city not visited
#             new_mask = mask | (1 << city)
#             new_distance = distances[last_city][city] + tsp_helper(distances, num_cities, memo, new_mask, city)
#             min_distance = min(min_distance, new_distance)
    
#     memo[(mask, last_city)] = min_distance
    
#     return min_distance


def tsp_helper(distances, num_cities, memo, mask, last_city):
    """
    Helper function to calculate the minimum distance for a subset of cities
    """
    if mask == (1 << num_cities) - 1:
        return distances[last_city][0]
    
    if (mask, last_city) in memo:
        return memo[(mask, last_city)]
    
    min_distance = float('inf')
    for city in range(num_cities):
        if mask & (1 << city) == 0: # If city not visited
            new_mask = mask | (1 << city)
            if (new_mask, city) not in memo:
                memo[(new_mask, city)] = tsp_helper(distances, num_cities, memo, new_mask, city)
            new_distance = distances[last_city][city] + memo[(new_mask, city)]
            min_distance = min(min_distance, new_distance)
    
    memo[(mask, last_city)] = min_distance
    
    return min_distance


def run(cities):
    num_cities = len(cities)
    # print("Number of cities:", num_cities)
    
    distances = generate_distance_matrix(cities)
    memo = {} # Memoization dictionary to store subproblem solutions
    # print("Memo keys:", memo.keys())
    
    # Start from city 0
    mask = 1 # City 0 is visited initially
    min_distance = tsp_helper(distances, num_cities, memo, mask, 0)
    optimal_tour = []
    last_city = 0
    
    # print("Memo keys:", memo.keys())
    
    # Reconstruct the optimal tour
    while True:
        optimal_tour.append(last_city)
        if len(optimal_tour) == num_cities:
            break
        
        next_city = None
        min_distance = float('inf')
        for city in range(num_cities):
            if mask & (1 << city) == 0: # If city not visited
                new_distance = distances[last_city][city] + memo[(mask | (1 << city), city)]
                if new_distance < min_distance:
                    min_distance = new_distance
                    next_city = city
        mask |= (1 << next_city)
        last_city = next_city
    
    optimal_tour.append(0) # Return to the starting city (0)
    results = [optimal_tour, min_distance]
    
    return results


