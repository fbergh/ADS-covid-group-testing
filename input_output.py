########## IMPORTS ##########

# Standard libary imports
import random as r
from collections import defaultdict
import pprint
import sys

# Self-defined imports
from social_graph import SocialGraph


########## PROBLEM PARSING ##########

def parse_number_of_problems():
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
        n_edges = max_edges if n_edges > max_edges else n_edges # ???

        # (c) number of initially infected people
        n_initially_infected = int(input())
        n_initially_infected = int(0.7 * n_nodes) if n_initially_infected > int(0.7 * n_nodes) else n_initially_infected # ???

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

def give_credentials():
    with open('credentials') as c:
        username, password = c.readline().split(" ")
    print(username)
    print(password)

def send_test(nodes):
    if type(nodes) == int:
        print("test", nodes, flush=True)
    else:
        print("test", *nodes, flush=True)

def send_answer(nodes):
    if type(nodes) == int:
        print("answer", nodes, flush=True)
    else:
        print("answer", *nodes, flush=True)

def get_test_result():
    return input() == "true"

def get_problem_result():
    return input() == "success"


########## PRINTING ##########

def pretty_print_input_params(input_params):
    for k, v in input_params.items():
        if k == "idcs_connected_nodes":
            continue
        eprint(f"{k:20} = {v}")

def eprint(*args, **kwargs):
    """
    Print to stderror (which logs to console for group testing server)
    """
    print(*args, file=sys.stderr, **kwargs)


########## DEBUGGING & TESTING ##########

def get_random_graph_with_parameters(n_nodes=None, n_edges=None, seed=r.random(), is_connected=True):
    print(f"Constructing random graph for seed {seed}")
    r.seed(seed)

    if n_nodes is None:
        n_nodes = r.randint(2, 10)

    if n_edges is None:
        max_edges = n_nodes * (n_nodes - 1) // 2
        n_edges = r.randint(n_nodes - 1, max_edges)

    n_initially_infected = r.randint(1, int(0.7 * n_nodes))
    p_infection = r.random()
    lower_bound = 1 if n_initially_infected == 1 else r.randint(1, n_initially_infected)
    upper_bound = n_initially_infected if n_initially_infected == int(0.7 * n_nodes) \
        else r.randint(n_initially_infected, int(0.7 * n_nodes))
    parameters = {"n_nodes": n_nodes, "n_edges": n_edges, "n_initially_infected": n_initially_infected,
                  "p_infection": p_infection, "lower_bound": lower_bound, "upper_bound": upper_bound}
    print("The graph has the following parameters:")
    pprint.pprint(parameters)
    random_graph = _build_random_graph(n_nodes, n_edges, is_connected)
    return SocialGraph(random_graph, parameters)

def _build_random_graph(n_nodes, n_edges, is_connected=True):
    if is_connected:
        graph = SocialGraph(_generate_connected_base_graph(n_nodes), {})
    else:
        graph = SocialGraph(defaultdict(set), {})
    lower_bound = n_nodes - 1 if is_connected else 0

    for _ in range(lower_bound, n_edges):
        node1 = r.randrange(0, n_nodes)
        # If node1 is already fully connected
        while len(graph.graph[node1]) == n_nodes - 1:
            node1 = r.randrange(0, n_nodes)
        possible_connections = set(range(n_nodes)) - {node1} - graph.graph[node1]
        node2 = r.sample(possible_connections, 1)[0]
        graph.add(node1, node2)
    return graph

def _generate_connected_base_graph(n_nodes):
    base_graph = defaultdict(set)
    connected = set()
    for _ in range(n_nodes - 1):
        node1 = r.sample(set(range(n_nodes)) - connected, 1)[0]
        # Take set difference
        possible_connections = set(range(n_nodes)) - {node1} - connected
        # random.sample returns a list
        node2 = r.sample(possible_connections, 1)[0]

        base_graph[node1].add(node2)
        base_graph[node2].add(node1)
        connected.update([node1])
    return base_graph


########## RUN FILE (TESTING) ##########

if __name__ == "__main__":
    seed = r.random()
    print(seed)
    r.seed(seed)
    g = _generate_base_graph(5)
    pprint.pprint(g)