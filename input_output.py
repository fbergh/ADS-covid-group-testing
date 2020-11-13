########## IMPORTS ##########

# Standard libary imports
import sys


########## PROBLEM PARSING ##########

def parse_number_of_problems():
    """ Parse the number of problems from server input """
    n_problems = int(input())
    eprint(f"Number of problems: {n_problems}")
    return n_problems

def get_values_from_input():
    """
    From the assignment: each problem consists of
        (a) A line with the number of nodes n
        (b) A line with the number of edges
        (c) A line with the number of initially infected people
        (d) A line with the chance p that people infect a close contact with 0 < p < 1
            and formatted as 0. followed by decimals
        (e) A line with a lower bound l and upper bound u on the number of total infections,
            with 0 < l <= i <= u <= 0.7n, with i the number of infections (just like in the real world,
            you already have an indication of how many people are infectious)
        (f) For each edge, a line with the two indices of the connected nodes
    
    :return: the parsed values
    """
    # Try to parse and initialise all values and conditions of variables
    try:
        # (a) number of nodes
        n_nodes = int(input())

        # (b) number of edges
        n_edges = int(input())
        max_edges = n_nodes * (n_nodes - 1) // 2
        n_edges = max_edges if n_edges > max_edges else n_edges # For robustness

        # (c) number of initially infected people
        n_initially_infected = int(input())
        n_initially_infected = int(0.7 * n_nodes) if n_initially_infected > int(0.7 * n_nodes) else n_initially_infected # For robustness

        # (d) probability of infecting others
        p_infection = float(input())
        assert 0 < p_infection < 1, "Infection probability should be greater than 0 and smaller than 1"

        # (e) lower and upper bounds
        lower_bound, upper_bound = input().strip().split(" ")
        lower_bound = int(lower_bound)
        upper_bound = int(upper_bound)
        assert 0 < lower_bound <= upper_bound, "Lower bound should be greater than 0 and smaller than or equal to the upper bound"
        assert lower_bound <= upper_bound <= 0.7 * n_nodes, "Upper bound should be greater than or equal to the lower bound and " \
                                                            "smaller than or equal to 0.7 * number of nodes "

        # (f) connected nodes
        idcs_connected_nodes = []
        for _ in range(n_edges):
            node1, node2 = input().strip().split(" ")
            node1 = int(node1)
            assert 0 <= node1 < n_nodes, "The index of the left node is out of bounds"
            node2 = int(node2)
            assert 0 <= node2 < n_nodes, "The index of the right node is out of bounds"
            idcs_connected_nodes.append((int(node1), int(node2)))
    
    # Throw and error if parsing failed
    except ValueError:
        print("Input values could not be parsed as integer/float")
        raise SystemExit

    # Return parsed variables
    return {"n_nodes": n_nodes, "n_edges": n_edges, "n_initially_infected": n_initially_infected,
            "p_infection": p_infection, "lower_bound": lower_bound, "upper_bound": upper_bound,
            "idcs_connected_nodes": idcs_connected_nodes}


########## SERVER INTERACTION ##########

def send_test(nodes):
    """ Send a test to the server for the given list of nodes """
    if type(nodes) == int:
        print("test", nodes, flush=True)
    else:
        print("test", *nodes, flush=True)

def send_answer(nodes):
    """ Send the given list of nodes as an answer to the server """
    if type(nodes) == int:
        print("answer", nodes, flush=True)
    else:
        print("answer", *nodes, flush=True)

def get_test_result():
    """ Get the result of a test """
    return input() == "true"

def get_problem_result():
    """ Get the result of the problem """
    return input() == "success"


########## PRINTING ##########

def pretty_print_input_params(input_params):
    """ Print all input parameters (except edges) in a neat way """
    for k, v in input_params.items():
        if k == "idcs_connected_nodes":
            continue
        eprint(f"{k:20} = {v}")

def eprint(*args, **kwargs):
    """ Print to stderror (which logs to console for group testing server) """
    print(*args, file=sys.stderr, **kwargs)