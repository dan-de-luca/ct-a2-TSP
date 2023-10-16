import os.path
# from tqdm import tqdm
import time
from helpers import data_handler, timing_handler
from algorithms import held_karp_exact_tsp, christofides_approx_tsp, lin_kernighan_heuristic_tsp

def run_tsp_simulation(data_file_path, num_cities, algorithms):
    """
    Runs the TSP simulation
    :param data_file_path: path to the data file
    :return: None
    """
    # Get the list of cities
    cities_exact = cities_approx = cities_heuristic = data_handler.handle_csv_file(data_file_path, num_cities)
    
    # Run given TSP algorithms
    
    if "exact" in algorithms:
        # Run Held-Karp (exact) TSP
        exact_start_time = time.perf_counter()
        exact_results = held_karp_exact_tsp.run(cities_exact)
        exact_tour, exact_distance = exact_results[0], exact_results[1]
        exact_end_time = time.perf_counter()
        exact_duration_hms = timing_handler.duration_hms(exact_start_time, exact_end_time)
        print("Exact Algorithm: Held-Karp")
        print("Optimal Tour:", exact_tour)
        print("Optimal Distance:", exact_distance, "km")
        print("Runtime:", exact_duration_hms, "\n")
    
    if "approx" in algorithms:
        # Run Christofides (approximation) TSP
        approx_start_time = time.perf_counter()
        approx_results = christofides_approx_tsp.run(cities_approx)
        approx_tour, approx_distance = approx_results[0], approx_results[1]
        approx_end_time = time.perf_counter()
        approx_duration_hms = timing_handler.duration_hms(approx_start_time, approx_end_time)
        print("Approximation Algorithm: Christofides")
        print("Approximate Best Tour:", approx_tour)
        print("Approximate Best Distance:", approx_distance, "km")
        print("Runtime:", approx_duration_hms, "\n")
    
    if "heuristic" in algorithms:
        # Run Lin-Kernighan (heuristic) TSP
        heuristic_start_time = time.perf_counter()
        heuristic_results = lin_kernighan_heuristic_tsp.run(cities_heuristic)
        heuristic_tour, heuristic_distance = heuristic_results[0], heuristic_results[1]
        heuristic_end_time = time.perf_counter()
        heuristic_duration_hms = timing_handler.duration_hms(heuristic_start_time, heuristic_end_time)
        print("Heuristic Best Tour:", heuristic_tour)
        print("Heuristic Best Distance:", heuristic_distance, "km")
        print("Runtime:", heuristic_duration_hms, "\n")


if __name__ == "__main__":
    # Get the number of cities to visit as user input
    num_cities = input("Enter the number of cities to visit: ")
    
    # Validate the input
    if num_cities.isdigit(): num_cities = int(num_cities)
    else: num_cities = 0 # invalid input to be handled next
    if num_cities < 2: num_cities = 5 # if input invalid, set to default number of cities
    
    # Get the path to the data file as user input
    data_file_path = input("Enter the path to the data file: ")
    
    # Convert the path to an absolute path
    if data_file_path: data_file_path = os.path.abspath(data_file_path)
    
    # Check if the file exists, using the default file if input was empty or the file does not exist
    if not os.path.exists(data_file_path):
        print("File does not exist, using default file instead: world.csv")
        
        # Get the path to the default data file
        data_file_path = os.path.join(os.path.dirname(__file__), "data", "world.csv")
        # print(data_file_path)
    
    # Set up the algorithms to run
    exact_algorithm = input("Run Held-Karp (exact) algorithm? (y/n): ")
    approx_algorithm = input("Run Christofides (approximation) algorithm? (y/n): ")
    heuristic_algorithm = input("Run Lin-Kernighan (heuristic) algorithm? (y/n): ")
    algorithms = []
    if exact_algorithm.lower() == "y": algorithms.append("exact")
    if approx_algorithm.lower() == "y": algorithms.append("approx")
    if heuristic_algorithm.lower() == "y": algorithms.append("heuristic")
    
    # Run the TSP simulation
    print("Running simulation: \nData file:", data_file_path, "\nNumber of cities:", num_cities, "\nAlgorithms:", algorithms, "\n")
    run_tsp_simulation(data_file_path, num_cities, algorithms)