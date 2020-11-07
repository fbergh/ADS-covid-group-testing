########## IMPORTS ##########

# Standard libary imports
import time
import sys

# Self-defined imports
import input_output as io
from social_graph import SocialGraph
from logger import Logger
from algorithms import ZeroPointSolution, DivideAndConquerBasic, DivideAndConquerBFS, DorfmanTest
from algorithms.algorithm_utils import connected_compoment_analysis



########## CONSTANTS ##########

logs_dir = "./logs"


########## RUNNING ALGORITHMS ##########

def test_server():
    """
    Run an algorithm on all problems on the server

    Run this in the terminal with: ncat -c 'python3 ./main.py' group-testing.maarse.xyz 6525
    NOTE: Add a credentials file in the repository
    """
    # Set recursion limit higher (default: 1000), otherwise connected_component_analysis might now run
    sys.setrecursionlimit(2000)
    io.give_credentials()
    n_problems = io.parse_number_of_problems()
    n_correct, total_n_tests, total_n_nodes = 0, 0, 0
    start_time = time.time()
    l = Logger(logs_dir)
    algorithm = ContactGroupTesting()

    for problem in range(n_problems):
        input_parameters = io.get_values_from_input()
        io.pretty_print_input_params(input_parameters) # FOR TESTING PURPOSES
        g = SocialGraph(None, input_parameters)
        is_success, n_tests = algorithm.run(g)
        io.eprint(f"Problem {(problem + 1):<12} = {is_success}")
        io.eprint(f"Tests/nodes{' ':9} = {n_tests}/{g.n_nodes}")
        io.pretty_print_input_params(input_parameters)
        io.eprint("")
        n_correct += is_success
        total_n_tests += n_tests
        total_n_nodes += g.n_nodes
        l.log_problem(input_parameters, is_success, n_tests)

    total_time = time.time() - start_time
    proportion_test = total_n_tests / total_n_nodes
    proportion_correct = n_correct / n_problems
    io.eprint(f"Time elapsed      = {total_time} sec")
    io.eprint(f"Test proportion   = {proportion_test}")
    io.eprint(f"Problems correct  = {proportion_correct}")
    l.log_algorithm_with_results(algorithm.name, total_time, proportion_test, proportion_correct)
    l.close()

def test_random_graph():
    """
    Run an algorithm on a random test graph (useful for debugging)
    """
    start_time = time.time()
    algorithm = ZeroPointSolution()
    n_tests = 0
    g = io.get_random_graph_with_parameters(n_nodes=10)
    is_success, n_tests = algorithm.run(g)
    io.eprint(f"Time elapsed      = {time.time() - start_time} sec")
    io.eprint(f"Total tests/nodes = {n_tests}/{g.n_nodes}")


########## RUN FILE ##########

if __name__ == '__main__':
    test_server()