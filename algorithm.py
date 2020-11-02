########## IMPORTS ##########

# Standard library imports
import math
import random as r

# Self-defined imports
import input_output as io


########## SUPERCLASS ##########

class Algorithm(object):
    def run(self, graph):
        raise NotImplementedError


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


########## BASIC DIVIDE-AND-CONQUER ##########

class DivideAndConquerBasic(Algorithm):
    def __init__(self, n_groups=None):
        self.n_groups = n_groups
        self.name = "basic_divide_and_conquer"

    def run(self, graph):
        if self.n_groups is None:
            p_infection = _calculate_p_infection(graph)
            group_size = _get_optimal_group_size(p_infection, graph.upper_bound)
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


########## BFS DIVIDE-AND-CONQUER ##########

class DivideAndConquerBFS(Algorithm):
    def __init__(self, min_groups=None):
        self.min_groups = min_groups
        self.name = "bfs_divide_and_conquer"
    
    def run(self, graph):
        # # If min_groups is undefined, set it to the "optimal" number
        # if self.min_groups is None:
        #     p_infection = _calculate_p_infection(graph)
        #     group_size = _get_optimal_group_size(p_infection, graph.upper_bound)
        #     min_groups = graph.n_nodes // group_size + 1
        # else:
        #     min_groups = self.min_groups
        min_groups = int(graph.n_nodes/10)
        
        # Run Divide-and-Conquer, using BFS to split the problem into subproblems
        positive_result_idcs, n_tests = self.dc_bfs_helper(graph, list(range(graph.n_nodes)), min_groups)

        # Check results
        io.send_answer(positive_result_idcs)
        is_success = io.get_problem_result()
        return is_success, n_tests

    def dc_bfs_helper(self, graph, v, k):
        # Base case: if dividing is useless, test everyone individually
        if len(v) <= k:
            positive_result_idcs = []
            for node in v:
                io.send_test(node)
                if io.get_test_result():
                    positive_result_idcs.append(node)
            return positive_result_idcs, len(v)
        
        # Recursive case: divide the problem into subgroups and recurse if necessary
        positive_result_idcs = []
        groups = self.bfs_divide(graph, v, k)
        n_tests = len(groups)
        for group in groups:
            io.send_test(group)
            if io.get_test_result():
                _positive_result_idcs, _n_tests = self.dc_bfs_helper(graph, group, k)
                positive_result_idcs.extend(_positive_result_idcs)
                n_tests += _n_tests
        return positive_result_idcs, n_tests

    def bfs_divide(self, graph, v, k):
        """
        Divide vertices v in a given graph into groups of size at most len(v)/k
        """
        # Set maximum group size and initialize list of groups
        max_group_size = int(len(v)/k)
        groups = []

        # Initialize list of unvisited and queued nodes
        unvisited = v
        queue = []
        
        # While there are still nodes to explore (queued or unvisited), do:
        while unvisited + queue:
            # Get a new source node (either the first element in the old queue, or a random unvisited node)
            s = queue.pop() if queue else unvisited.pop(r.randrange(len(unvisited)))
            # Add the remaining elements of the old queue back into the unvisited list
            unvisited.extend(queue)

            # Initialize group list and new queue
            group = []
            queue = [s]
            # While the queue is not empty and the group has not exceeded maximum capacity, explore vertices in a BFS manner
            while queue and len(group) < max_group_size:
                u = queue.pop()
                for v in graph.graph[u]:
                    if v in unvisited:
                        unvisited.remove(v)
                        queue.append(v)
                group.append(u)
            groups.append(group)
            
        # Return the created list of connected groups
        return groups

########## DORFMAN TEST ##########

class DorfmanTest(Algorithm):
    def __init__(self, group_size=None):
        self.group_size = group_size
        self.name = "dorfman_test"

    def run(self, graph):
        if self.group_size is None:
            p_infection = _calculate_p_infection(graph)
            n = _get_optimal_group_size(p_infection, graph.upper_bound)
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


def _calculate_p_infection(graph):
    n_nodes, n_edges, p_infect_neighbour = graph.n_nodes, graph.n_edges, graph.p_infection
    avg_n_edges_per_node = round(n_edges / (n_nodes - 1))
    if avg_n_edges_per_node <= 1:
        return p_infect_neighbour
    else:
        N = avg_n_edges_per_node
        p_infection = 0
        p_infected = (graph.lower_bound + graph.upper_bound) // 2 / n_nodes
        # i represents a hypothetical number of infections
        for i in range(1, N + 1):
            p_will_infect = p_infected * p_infect_neighbour
            p_infection += math.comb(math.floor(N), i) * p_will_infect ** i * (1 - p_will_infect) ** (N - i)
        return p_infection


def _get_optimal_group_size(p_infection, upper_bound):
    """
    Based on https://blogs.sas.com/content/iml/2020/07/06/pool-testing-covid19.html
    """
    max_test_reduction, best_k = math.inf, 0
    for k in range(1, upper_bound):
        test_reduction = test_reduction_proportion(p_infection, k)
        if test_reduction < max_test_reduction:
            max_test_reduction = test_reduction
            best_k = k
    return max(best_k, 2)


def test_reduction_proportion(p, k):
    return 1 / k + 1 - (1 - p) ** k


if __name__ == "__main__":
    ps = [0.01, 0.025, 0.05, 0.1, 0.15]
    for p in ps:
        print(_get_optimal_group_size(p))
