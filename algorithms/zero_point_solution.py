########## IMPORTS ##########

# Self-defined imports
import input_output as io
from algorithms import Algorithm


########## TESTING EVERYONE INDIVIDUALLY (ZERO-POINT SOLUTION) ##########

class ZeroPointSolution(Algorithm):
    def __init__(self):
        super().__init__()
        self.name = "zero_point_solution"

    def run(self, graph):
        # First test everything, then read everything (faster than having to wait for output each time)
        for node in range(graph.n_nodes):
            io.send_test(node)

        positive_result_idcs = [node for node in range(graph.n_nodes) if io.get_test_result()]
        io.send_answer(positive_result_idcs)

        is_success = io.get_problem_result()
        n_tests = graph.n_nodes
        return is_success, n_tests