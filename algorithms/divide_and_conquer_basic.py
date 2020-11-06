########## IMPORTS ##########

# Standard libary imports
import math

# Self-defined imports
import input_output as io
from algorithms import Algorithm, calculate_p_infection, get_optimal_group_size


########## BASIC DIVIDE-AND-CONQUER ##########

class DivideAndConquerBasic(Algorithm):
    def __init__(self, n_groups=None):
        self.n_groups = n_groups
        self.name = "basic_divide_and_conquer"

    def run(self, graph):
        if self.n_groups is None:
            p_infection = calculate_p_infection(graph)
            group_size = get_optimal_group_size(p_infection, graph.upper_bound)
            n_groups = graph.n_nodes // group_size + 1
        else:
            n_groups = self.n_groups

        positive_result_idcs, n_tests = self.dc_helper(n_groups, 0, graph.n_nodes - 1, 0)

        io.send_answer(positive_result_idcs)
        is_success = io.get_problem_result()
        return is_success, n_tests

    def dc_helper(self, n, p, r, n_tests):
        # Base case: if the group size is smaller than or equal to the number of groups to be tested, test everyone
        if r - p + 1 <= n:
            tested_positive = []
            for node in range(p, r + 1):
                io.send_test(node)
                if io.get_test_result():
                    tested_positive.append(node)
                n_tests += 1
            return tested_positive, n_tests

        # Recursive case: test n groups and recurse on group if that group is positive
        positive_result_idcs = []
        # NOTE: determining q like this is not guaranteed to be correct (e.g. take n=4, p=0, and q=5)
        q = math.ceil((r - p + 1) / n)

        for node in range(p, r + 1, q):
            end_node = min(r + 1, node + q)
            io.send_test(range(node, end_node))
            if io.get_test_result():
                # If the group consists of a single note, do base case here
                if node + 1 == end_node:
                    positive_result_idcs.append(node)
                    n_tests += 1
                else:
                    _positive_result_idcs, _n_tests = self.dc_helper(n, node, end_node - 1, 0)
                    positive_result_idcs.extend(_positive_result_idcs)
                    n_tests += _n_tests

        n_tests += n

        return positive_result_idcs, n_tests