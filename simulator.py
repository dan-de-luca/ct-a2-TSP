import os.path
# from tqdm import tqdm
import time
from helpers import timing_handler
from algorithms import held_karp_exact_tsp, christofides_approx_tsp, lin_kernighan_heuristic_tsp

def run_tsp_simulation(cities, algorithms, output_file_path):
    """
    Runs the TSP simulation
    :param data_file_path: path to the data file
    :return: None
    """
    # Create copies of the list of cities
    cities_exact = cities_approx = cities_heuristic = cities.copy()
    
    # Run given TSP algorithms
    tsp_runtimes = []
    
    if "exact" in algorithms:
        # Run Held-Karp (exact) TSP
        exact_start_time = time.perf_counter()
        exact_results = held_karp_exact_tsp.run(cities_exact)
        exact_tour, exact_distance = exact_results[0], exact_results[1]
        exact_end_time = time.perf_counter()
        exact_duration_hms = timing_handler.duration_hms(exact_start_time, exact_end_time)
        f = open(output_file_path, "a")
        f.write("Exact Algorithm: Held-Karp\n")
        tour_exact = "Optimal Tour: " +  str(exact_tour) + "\n"
        f.write(tour_exact)
        dist_exact = "Optimal Distance: " + str(exact_distance) + " km" + "\n"
        f.write(dist_exact)
        runtime_exact = "Runtime: " + exact_duration_hms + "\n"
        f.write(runtime_exact)
        f.close()
        tsp_runtimes.append(timing_handler.duration_s(exact_start_time, exact_end_time))
    
    if "approx" in algorithms:
        # Run Christofides (approximation) TSP
        approx_start_time = time.perf_counter()
        approx_results = christofides_approx_tsp.run(cities_approx)
        approx_tour, approx_distance = approx_results[0], approx_results[1]
        approx_end_time = time.perf_counter()
        approx_duration_hms = timing_handler.duration_hms(approx_start_time, approx_end_time)
        f = open(output_file_path, "a")
        f.write("Approximation Algorithm: Christofides\n")
        tour_approx = "Approximate Best Tour: " + str(approx_tour) + "\n"
        f.write(tour_approx)
        dist_approx = "Approximate Best Distance: " + str(approx_distance) + " km" + "\n"
        f.write(dist_approx)
        runtime_approx = "Runtime: " + approx_duration_hms + "\n"
        f.write(runtime_approx)
        f.close()
        tsp_runtimes.append(timing_handler.duration_s(approx_start_time, approx_end_time))
    
    if "heuristic" in algorithms:
        # Run Lin-Kernighan (heuristic) TSP
        heuristic_start_time = time.perf_counter()
        heuristic_results = lin_kernighan_heuristic_tsp.run(cities_heuristic)
        heuristic_tour, heuristic_distance = heuristic_results[0], heuristic_results[1]
        heuristic_end_time = time.perf_counter()
        heuristic_duration_hms = timing_handler.duration_hms(heuristic_start_time, heuristic_end_time)
        f = open(output_file_path, "a")
        f.write("Heuristic Algorithm: Lin-Kernighan\n")
        tour_heuristic = "Heuristic Best Tour: " + str(heuristic_tour) + "\n"
        f.write(tour_heuristic)
        dist_heuristic = "Heuristic Best Distance: " + str(heuristic_distance) + " km" + "\n"
        f.write(dist_heuristic)
        runtime_heuristic = "Runtime: " + heuristic_duration_hms + "\n\n"
        f.write(runtime_heuristic)
        f.close()
        tsp_runtimes.append(timing_handler.duration_s(heuristic_start_time, heuristic_end_time))
    
    return tsp_runtimes