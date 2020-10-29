import input_output as io
import algorithm as a
from social_graph import SocialGraph
import time
import random as r


def test_server():
    """
    Run this in the terminal with: ncat -c 'python3 ./main.py' group-testing.maarse.xyz 6525
    NOTE: Add a credentials file in the repository
    """
    io.give_credentials()
    n_problems = io.parse_number_of_problems()
    n_correct = 0
    start_time = time.time()
    total_n_tests = 0
    total_n_nodes = 0
    for problem in range(n_problems):
        input_parameters = io.get_values_from_input()
        g = SocialGraph(None, input_parameters)
        is_success, n_tests = a.dorfman_test(g)
        io.eprint(f"Problem {(problem + 1):<12} = {is_success}")
        io.eprint(f"Tests/nodes{' ':9} = {n_tests}/{g.n_nodes}")
        io.pretty_print_input_params(input_parameters)
        io.eprint("")
        n_correct += is_success
        total_n_tests += n_tests
        total_n_nodes += g.n_nodes
    io.eprint(f"Time elapsed      = {time.time() - start_time} sec")
    io.eprint(f"Total tests/nodes = {total_n_tests}/{total_n_nodes}")
    io.eprint(f"Problems correct  = {n_correct}/{n_problems}")


def test_random_graph():
    """
    Useful for debugging
    """
    start_time = time.time()
    total_n_tests = 0
    total_n_nodes = 0
    g = io.get_random_graph_with_parameters(n_nodes=10, seed=r.seed(0))
    is_success, n_tests = a.dorfman_test(g, 3)
    io.eprint(f"Tests/nodes{' ':9} = {n_tests}/{g.n_nodes}")
    io.eprint("")
    total_n_tests += n_tests
    total_n_nodes += g.n_nodes
    io.eprint(f"Time elapsed      = {time.time() - start_time} sec")
    io.eprint(f"Total tests/nodes = {total_n_tests}/{total_n_nodes}")


if __name__ == '__main__':
    test_server()
