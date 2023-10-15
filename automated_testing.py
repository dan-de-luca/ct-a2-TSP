# import subprocess
# import time
import os.path

from helpers import data_handler
import simulator

MAX_EXECUTION_TIME = 1800 # 30 minutes in seconds
DEFAULT_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "it16862.csv"))
DEFAULT_OUTPUT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "results", "test_results.txt"))


def generate_tsp_instance(data_file_path, num_cities):
    """
    Generates the TSP instance to simulate
    :param data_file: path to the data file
    :param num_cities: number of cities to visit
    :return: A list of cities of size num_cities
    """
    return data_handler.handle_csv_file(data_file_path, num_cities)


def setup_file_paths(data_file_path, output_file_path):
    """
    Sets up the file paths for the data file and output file
    :param data_file_path: path to the data file
    :param output_file_path: path to the output file
    :return: None
    """
    # Convert the paths to absolute paths
    data_file_path = os.path.abspath(data_file_path) if data_file_path else DEFAULT_DATA_FILE
    output_file_path = os.path.abspath(output_file_path) if output_file_path else DEFAULT_OUTPUT_FILE
    
    # Check if the file exists, using the default file if input was empty or the file does not exist
    if not os.path.exists(data_file_path):
        print("File does not exist, using default file instead: it16862.csv")
        data_file_path = DEFAULT_DATA_FILE
    
    if not os.path.exists(output_file_path):
        print("File does not exist, using default file instead: test_results.txt")
        output_file_path = DEFAULT_OUTPUT_FILE
    
    return data_file_path, output_file_path


def get_user_input(prompt, default_value, input_type=int):
    """
    Get user input with a prompt and validate the input type.
    :param prompt: The message to display to the user.
    :param default_value: The default value if the user input is empty.
    :param input_type: The data type to validate the user input (default is int).
    :return: User input after validation.
    """
    while True:
        user_input = input(prompt)
        if not user_input:
            return default_value
        try:
            return input_type(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid value of type {}.".format(input_type.__name__))


def run_tsp_simulations(data_file_path, output_file_path, num_cities, tsp_size_increment):
    data_file_path, output_file_path = setup_file_paths(data_file_path, output_file_path)
    simulation_num = 1

    while True:
        algorithms = ["exact", "approx", "heuristic"]

        # Generate the TSP instance
        cities = generate_tsp_instance(data_file_path, num_cities)

        # Run the TSP simulation
        with open(output_file_path, "a") as f:
            arg = f"Running simulation: {simulation_num}\nNumber of cities: {num_cities}\nAlgorithms: {algorithms}\n"
            f.write(arg)

        tsp_runtimes = simulator.run_tsp_simulation(cities, algorithms, output_file_path)

        # Check runtimes are within the maximum execution time
        exact_runtime, approx_runtime, heuristic_runtime = tsp_runtimes + [float('inf')] * (3 - len(tsp_runtimes))

        exact_algorithm = exact_runtime < MAX_EXECUTION_TIME
        approx_algorithm = approx_runtime < MAX_EXECUTION_TIME
        heuristic_algorithm = heuristic_runtime < MAX_EXECUTION_TIME

        # If all algorithms have been disabled, exit the program
        if not (exact_algorithm or approx_algorithm or heuristic_algorithm):
            break
        else:
            num_cities += tsp_size_increment
            simulation_num += 1


def main():
    # Get the number of cities to visit as user input
    num_cities = get_user_input("Enter the starting number of cities to visit: ", 20)
    tsp_size_increment = get_user_input("Enter the increment size for the TSP instances in number of cities to visit: ", 5)
    
    # Get the path to the data file as user input
    data_file_path = input("Enter the path to the data file: ")
    
    # Get the path to the output file as user input
    output_file_path = input("Enter the path to the output file: ")
    
    # Validate the inputs
    # Validate the initial TSP size
    if num_cities < 10: num_cities = 10 # if input invalid, set to default number of cities
    # if num_cities < 20: num_cities = 20 # if input invalid, set to default number of cities
    
    # Validate the TSP size increment
    if tsp_size_increment < 5: tsp_size_increment = 5 # if input invalid, set to default increment size
    
    # Validate the file paths
    data_file_path, output_file_path = setup_file_paths(data_file_path, output_file_path)
    
    run_tsp_simulations(data_file_path, output_file_path, num_cities, tsp_size_increment)
    
    print("\nTSP simulation complete!")


if __name__ == "__main__":
    main()
    
    # # Get the number of cities to visit as user input
    # num_cities = input("Enter the starting number of cities to visit: ")
    # tsp_size_increment = input("Enter the increment size for the TSP instances in number of cities to visit: ")
    
    # # Get the path to the data file as user input
    # data_file_path = input("Enter the path to the data file: ")
    
    # # Get the path to the output file as user input
    # output_file_path = input("Enter the path to the output file: ")
    
    # # Validate the inputs
    # # Validate the initial TSP size
    # if num_cities.isdigit(): num_cities = int(num_cities)
    # else: num_cities = 0 # invalid input to be handled next
    # if num_cities < 20: num_cities = 20 # if input invalid, set to default number of cities
    
    # # Validate the TSP size increment
    # if tsp_size_increment.isdigit(): tsp_size_increment = int(tsp_size_increment)
    # else: tsp_size_increment = 5 # invalid input to be handled next
    
    # # Validate the file paths
    # # Convert the paths to absolute paths
    # if data_file_path: data_file_path = os.path.abspath(data_file_path)
    # if output_file_path: output_file_path = os.path.abspath(output_file_path)
    
    # # Check if the file exists, using the default file if input was empty or the file does not exist
    # if not os.path.exists(data_file_path):
    #     print("File does not exist, using default file instead: it16862.csv")
        
    #     # Get the path to the default data file
    #     data_file_path = os.path.join(os.path.dirname(__file__), "data", "it16862.csv")
    
    # if not os.path.exists(output_file_path):
    #     print("File does not exist, using default file instead: test_results.txt")
        
    #     # Get the path to the default output file
    #     output_file_path = os.path.join(os.path.dirname(__file__), "results", "test_results.txt")
    
    # run_tsp_simulations(data_file_path, output_file_path, num_cities, tsp_size_increment)
    
    # print("\nTSP simulation complete!")
