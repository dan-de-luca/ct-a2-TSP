import subprocess
import time
import os.path

from helpers import data_handler
import simulator

MAX_EXECUTION_TIME = 1800 # 30 minutes in seconds


def generate_tsp_instance(data_file_path, num_cities):
    """
    Generates the TSP instance to simulate
    :param data_file: path to the data file
    :param num_cities: number of cities to visit
    :return: A list of cities of size num_cities
    """
    return data_handler.handle_csv_file(data_file_path, num_cities)


def run_tsp_simulations(data_file_path, output_file_path, num_cities, tsp_size_increment):
    # Initial set-up
    exact_algorithm = True
    approx_algorithm = True
    heuristic_algorithm = True
    simulation_num = 1
    
    # Run the TSP simulation    
    while True:
        # Set up the algorithms to run
        algorithms = []
        if exact_algorithm: algorithms.append("exact")
        if approx_algorithm: algorithms.append("approx")
        if heuristic_algorithm: algorithms.append("heuristic")
        
        # Generate the TSP instance
        cities = generate_tsp_instance(data_file_path, num_cities)
        
        # Run the TSP simulation
        f = open(output_file_path, "a")
        arg = "Running simulation: " + str(simulation_num) + "\nNumber of cities: " + str(num_cities) +  "\nAlgorithms: " + str(algorithms) + "\n"
        f.write(arg)
        f.close()
        tsp_runtimes = simulator.run_tsp_simulation(cities, algorithms, output_file_path)
        
        # Check runtimes are within the maximum execution time
        exact_runtime, approx_runtime, heuristic_runtime = tsp_runtimes[0], tsp_runtimes[1], tsp_runtimes[2]
        if exact_runtime > MAX_EXECUTION_TIME: exact_algorithm = False
        if approx_runtime > MAX_EXECUTION_TIME: approx_algorithm = False
        if heuristic_runtime > MAX_EXECUTION_TIME: heuristic_algorithm = False
        
        # If all algorithms have been disabled, exit the program
        if not exact_algorithm and not approx_algorithm and not heuristic_algorithm: break
        else: 
            num_cities += tsp_size_increment
            simulation_num += 1


if __name__ == "__main__":
    # Get the number of cities to visit as user input
    num_cities = input("Enter the starting number of cities to visit: ")
    tsp_size_increment = input("Enter the increment size for the TSP instances in number of cities to visit: ")
    
    # Get the path to the data file as user input
    data_file_path = input("Enter the path to the data file: ")
    
    # Get the path to the output file as user input
    output_file_path = input("Enter the path to the output file: ")
    
    # Validate the inputs
    # Validate the initial TSP size
    if num_cities.isdigit(): num_cities = int(num_cities)
    else: num_cities = 0 # invalid input to be handled next
    if num_cities < 20: num_cities = 20 # if input invalid, set to default number of cities
    
    # Validate the TSP size increment
    if tsp_size_increment.isdigit(): tsp_size_increment = int(tsp_size_increment)
    else: tsp_size_increment = 5 # invalid input to be handled next
    
    # Validate the file paths
    # Convert the paths to absolute paths
    if data_file_path: data_file_path = os.path.abspath(data_file_path)
    if output_file_path: output_file_path = os.path.abspath(output_file_path)
    
    # Check if the file exists, using the default file if input was empty or the file does not exist
    if not os.path.exists(data_file_path):
        print("File does not exist, using default file instead: it16862.csv")
        
        # Get the path to the default data file
        data_file_path = os.path.join(os.path.dirname(__file__), "data", "it16862.csv")
    
    if not os.path.exists(output_file_path):
        print("File does not exist, using default file instead: test_results.txt")
        
        # Get the path to the default output file
        output_file_path = os.path.join(os.path.dirname(__file__), "results", "test_results.txt")
    
    run_tsp_simulations(data_file_path, output_file_path, num_cities, tsp_size_increment)
    
    print("\nTSP simulation complete!")
