########## IMPORTS ##########

# Standard libary imports
import random

# Self-defined imports
import input_output as io
from algorithms import Algorithm, calculate_p_infection, get_optimal_group_size


########## DIVIDE-AND-CONQUER USING BFS TO SPLIT GROUPS ##########

class DivideAndConquerBFS(Algorithm):
    def __init__(self, min_groups=None):
        self.min_groups = min_groups
        self.name = "bfs_divide_and_conquer"
    
    def run(self, graph):
        # If min_groups is undefined, set it to the "optimal" number
        if self.min_groups is None:
            p_infection = calculate_p_infection(graph)
            group_size = get_optimal_group_size(p_infection, graph.upper_bound)
            min_groups = graph.n_nodes // group_size + 1
        else:
            min_groups = self.min_groups
        
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

    def bfs_divide(self, graph, vertices, k):
        """
        Divide vertices v in a given graph into groups of size at most len(v)/k
        """
        # Set maximum group size and initialize list of groups
        max_group_size = int(len(vertices)/k)
        groups = []

        # Initialize list of unvisited and queued nodes
        unvisited = vertices
        queue = []
        
        # While there are still nodes to explore (queued or unvisited), do:
        while unvisited + queue:
            # Get a new source node (either the first element in the old queue, or a random unvisited node)
            s = queue.pop() if queue else unvisited.pop(random.randrange(len(unvisited)))
            # Add the remaining elements of the old queue back into the unvisited list
            unvisited.extend(queue)

            # Initialize group list and new queue
            group = []
            queue = [s]
            # While the queue is not empty and the group has not exceeded maximum capacity, explore vertices in a BFS manner
            while queue and len(group) < max_group_size:
                u = queue.pop()
                for v in graph.graph[u]:
                    if v in unvisited and v in vertices:
                        unvisited.remove(v)
                        queue.append(v)
                group.append(u)
            groups.append(group)
            
        # Return the created list of connected groups
        return groups