########## IMPORTS ##########

# Standard libary imports
import time

# Self-defined imports
import input_output as io
from social_graph import SocialGraph
from logger import Logger
from algorithm import ClusterGroupTesting


########## CONSTANTS ##########

logs_dir = "./logs"


########## RUNNING ALGORITHMS ##########

def test_server():
    """
    Run the algorithm on all problems on the server

    Run this in the terminal with: ncat -c 'echo 'USERNAME' && echo 'PASSWORD' && python3 ./main.py' group-testing.maarse.xyz 6525 (Mac)
                                   ncat -c "echo "USERNAME" && echo "PASSWORD" && python .\main.py" group-testing.maarse.xyz 6525 (Windows)
    """
    # Setup: parse number of problems, start counters for performance, start a timer, create a logger and choose an algorithm
    n_problems = io.parse_number_of_problems()
    n_correct, approx_score = 0, 0
    start_time = time.time()
    l = Logger(logs_dir)
    algorithm = ClusterGroupTesting()

    # For each problem:
    for problem in range(n_problems):
        # Parse the input parameters
        input_parameters = io.get_values_from_input()
        # Print the input parameters (except for edges)
        io.eprint(f"Problem {(problem + 1):<12}")
        io.pretty_print_input_params(input_parameters)
        # Create graph based on input parameters
        g = SocialGraph(None, input_parameters)
        # Run the algorithm
        io.eprint(f"Running algorithm: {algorithm.name}")
        is_success, n_tests = algorithm.run(g)
        # Print the result obtained by the algorithm (correctenss, number of tests)
        io.eprint(f"Result:")
        io.eprint(f"Correct solution{' ':4} = {is_success}")
        io.eprint(f"Tests/nodes{' ':9} = {n_tests}/{g.n_nodes}")
        io.eprint("")
        # Increment counters for performance
        n_correct += is_success
        if is_success:
            approx_score += (1 - n_tests/g.n_nodes)*1000000
        # Log the problem (for saving result later on)
        l.log_problem(input_parameters, is_success, n_tests)

    # Compute time required, proportion of tests used and proportion of correct results
    total_time = time.time() - start_time
    io.eprint(f"Time elapsed      = {total_time:.4f} sec")
    io.eprint(f"Problems correct  = {n_correct}/{n_problems}")
    io.eprint(f"Approximate score = {int(approx_score)}")
    # Save results to a log file
    l.log_algorithm_with_results(algorithm.name, total_time, int(approx_score), n_correct)
    l.close()


########## RUN FILE ##########

if __name__ == '__main__':
    test_server()