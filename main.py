import os.path
import time
from data import data_handler
from results import results_handler
from algorithms import exact_held_karp_tsp, approx_christofides_tsp, heuristic_lin_kernighan_tsp

def run_tsp_simulation(data_file_path, num_cities):
    """
    Runs the TSP simulation
    :param data_file_path: path to the data file
    :return: None
    """
    # Get the list of cities
    cities = data_handler.handle_csv_file(data_file_path, num_cities)
    
    # Run the algorithms
    # Exact algorithm
    exact_start_time = time.time()
    exact_results = exact_held_karp_tsp.run(cities)
    exact_tour, exact_distance = exact_results[0], exact_results[1]
    exact_end_time = time.time()
    exact_duration_hms = results_handler.duration_hms(exact_start_time, exact_end_time)
    print("Exact Algorithm: Held-Karp")
    print("Optimal Tour:", exact_tour)
    print("Optimal Distance:", exact_distance)
    print("Runtime:", exact_duration_hms, "\n")
    
    # Approximation algorithm
    approx_start_time = time.time()
    approx_tour, approx_distance = approx_christofides_tsp.run(cities)
    approx_end_time = time.time()
    approx_duration_hms = results_handler.duration_hms(approx_start_time, approx_end_time)
    print("Approximation Algorithm: Christofides")
    print("Approximate Tour:", approx_tour)
    print("Approximate Distance:", approx_distance)
    print("Runtime:", approx_duration_hms, "\n")
    
    # Heuristic algorithm
    heuristic_start_time = time.time()
    heuristic_tour, heuristic_distance = heuristic_lin_kernighan_tsp.run(cities)
    heuristic_end_time = time.time()
    heuristic_duration_hms = results_handler.duration_hms(heuristic_start_time, heuristic_end_time)
    print("Heuristic Algorithm: Lin-Kernighan")
    print("Approximate Tour:", heuristic_tour)
    print("Approximate Distance:", heuristic_distance)
    print("Runtime:", heuristic_duration_hms, "\n")


if __name__ == "__main__":
    # Get the number of cities to visit as user input
    num_cities = input("Enter the number of cities to visit: ")
    
    if num_cities.isdigit(): num_cities = int(num_cities)
    else: num_cities = 0
    
    if num_cities < 2: num_cities = 5 # default number of cities
    # print(num_cities)
    
    # Get the path to the data file as user input
    data_file_path = input("Enter the path to the data file: ")
    
    # Check if the file exists, using the default file if input was empty or the file does not exist
    if not os.path.exists(data_file_path):
        print("File does not exist, using default file instead.")
        
        # Get the path to the default data file
        data_file_path = os.path.join(os.path.dirname(__file__), "data", "wi29.csv")
    
    run_tsp_simulation(data_file_path, num_cities)