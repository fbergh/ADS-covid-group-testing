########## IMPORTS ##########

# Self-defined imports
import input_output as io
from algorithms import Algorithm, calculate_p_infection, get_optimal_group_size


########## DORFMAN TEST ##########

class DorfmanTest(Algorithm):
    def __init__(self, group_size=None):
        self.group_size = group_size
        self.name = "dorfman_test"

    def run(self, graph):
        if self.group_size is None:
            p_infection = calculate_p_infection(graph)
            n = get_optimal_group_size(p_infection, graph.upper_bound)
        else:
            n = self.group_size

        n_groups = graph.n_nodes // n
        if not graph.n_nodes % n == 0:
            n_groups += 1
        n_tests = n_groups
        nodes = list(range(graph.n_nodes))
        # Test groups of size n
        for g_idx in range(0, graph.n_nodes, n):
            io.send_test(nodes[g_idx:min(g_idx + n, graph.n_nodes)])
        group_results = [io.get_test_result() for _ in range(n_groups)]

        # For all positively tested groups, test individuals
        for g_idx, is_positive in enumerate(group_results):
            if not is_positive:
                pass
            for node in range(g_idx * n, min((g_idx + 1) * n, graph.n_nodes)):
                io.send_test(node)
                n_tests += 1

        # Get individual results
        positive_result_idcs = []
        for g_idx, is_positive in enumerate(group_results):
            if not is_positive:
                pass
            for node in range(g_idx * n, min((g_idx + 1) * n, graph.n_nodes)):
                if io.get_test_result():
                    positive_result_idcs.append(node)

        io.send_answer(positive_result_idcs)
        is_success = io.get_problem_result()
        return is_success, n_tests