# import sys
import time
import math
import threading
import itertools
from tqdm import tqdm


#######################################################################################################################################################

def timer():
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        print(f'\rElapsed Time: {elapsed_time:.2f} seconds', end='')
        time.sleep(1)

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
    distances = [[calculate_distance(cities[i], cities[j]) for j in range(num_cities)] for i in range(num_cities)]
    return distances


def calculate_tour_distance(tour, distances):
    total_distance = 0
    num_cities = len(tour)
    for i in range(num_cities - 1):
        total_distance += distances[tour[i]][tour[i + 1]]
    total_distance += distances[tour[-1]][tour[0]]  # Return to the starting city
    return total_distance


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
#             if (new_mask, city) not in memo:
#                 memo[(new_mask, city)] = tsp_helper(distances, num_cities, memo, new_mask, city)
#             new_distance = distances[last_city][city] + memo[(new_mask, city)]
#             min_distance = min(min_distance, new_distance)
    
#     memo[(mask, last_city)] = min_distance
    
#     return min_distance


# def run(cities):
#     num_cities = len(cities)    
#     distances = generate_distance_matrix(cities)
#     memo = {} # Memoization dictionary to store subproblem solutions
    
#     # Start from city 0
#     mask = 1 # City 0 is visited initially
#     min_distance = tsp_helper(distances, num_cities, memo, mask, 0)
#     optimal_tour = []
#     last_city = 0
    
#     # Run Held-Karp (exact) TSP with progress bar
#     print("Running exact algorithm TSP: Held-Karp")
#     print("Number of cities:", num_cities)
#     with tqdm(total=num_cities, desc="Held-Karp TSP") as pbar:
#         # Reconstruct the optimal tour
#         while True:
#             optimal_tour.append(last_city)
#             if len(optimal_tour) == num_cities:
#                 break
            
#             next_city = None
#             min_distance = float('inf')
#             for city in range(num_cities):
#                 if mask & (1 << city) == 0: # If city not visited
#                     new_distance = distances[last_city][city] + memo[(mask | (1 << city), city)]
#                     if new_distance < min_distance:
#                         min_distance = new_distance
#                         next_city = city
#             mask |= (1 << next_city)
#             last_city = next_city
#             pbar.update(1)
#         pbar.update(1)
    
#     optimal_tour.append(0) # Return to the starting city (0)
#     results = [optimal_tour, min_distance]
    
#     return results

def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the TSP using dynamic programming with memoization.

    Parameters:
        dists: distance matrix

    Returns:
        A tuple, (cost, path).
    """
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return list(reversed(path)), opt


def run(cities):
    num_cities = len(cities)
    distances = generate_distance_matrix(cities)

    # Run Held-Karp (exact) TSP
    print("\nRunning exact algorithm TSP: Held-Karp")
    print("Number of cities:", num_cities)
    
    # Start the timer in a separate thread
    timer_thread = threading.Thread(target=timer)
    timer_thread.daemon = True  # Set the thread as a daemon to exit with the main program
    timer_thread.start()
    
    try:
        results = held_karp(distances)
        
    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt detected. Exiting...")
    
    return results
