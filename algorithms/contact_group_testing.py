import math
import random

from algorithms import Algorithm
import input_output as io

class ContactGroupTesting(Algorithm):
    def __init(self):
        self.name = "countact_group_testing"

    ### RUNNING THE ALGORITHM ###
    
    def run(self, graph):
        # Set global variables
        self.database = {} # database for storing known positives & negatives
        self.n_known_positive = 0 # number of known positives
        self.n_tests = 0 # counter for the number of performed tests
        self.graph = graph # graph on which the algorithm is called

        # Compute list of connected components
        self.connected_components = self.get_connected_components()

        # Solve the problem for each component
        self.solve_all_components()

        # If the upper bound was reached, fill in the rest of the database
        if self._reached_upper_bound():
            for i in range(self.graph.n_nodes):
                if i not in self.database:
                    self.database[i] = False

        # Verify we are done testing and extract the positive nodes 
        assert len(self.database) == self.graph.n_nodes, "The algorithm has not finished testing"
        positive_result_idcs = [v for v in self.database if self.database[v]]

        # Send answer and check result
        io.send_answer(positive_result_idcs)
        is_success = io.get_problem_result()

        # Return result and number of tests used
        return is_success, self.n_tests
    

    ### SOLVING ALL COMPONENTS ###

    def solve_all_components(self):
        # Get the optimal number of groups for divide-and-conquer
        p_infection_component = self._calculate_p_infection_component()
        optimal_group_size = self._get_optimal_group_size(p_infection_component, len(self.connected_components))
        n_groups = round(self.graph.n_nodes / optimal_group_size) # Approximate n_groups to the closest integer resulting from n_nodes/optimal_group_size

        # Solve components via a divide-and-conquer-like strategy (split into groups, test, recurse if positive)
        self._solve_all_components_helper(self.connected_components, n_groups)

    def _solve_all_components_helper(self, components, n_groups):
        # Base case: check every group individually
        if len(components) < n_groups:
            for c in components:
                if not self._reached_upper_bound:
                    self.solve_component(c)
        # Recursive case: split components into groups and recurse if these groups test positive
        else:
            group_size = len(components)/n_groups
            split_indices = list(set([math.floor(group_size*i) for i in range(n_groups+1)]))

            for i in range(n_groups):
                if not self._reached_upper_bound():
                    start = split_indices[i]
                    end = split_indices[i+1]

                    union = [node for c in components[start:end] for node in c]

                    result, _, _ = self.test(union)
                    if result:
                        self._solve_all_components_helper(components[start:end], n_groups)



    ### SOLVING A SINGLE COMPONENT (WITH AT LEAST 1 POSITIVE NODE) ###

    def solve_component(self, component):
        if len(component) == 1:
            assert component[0] in self.database, "Lonely component, not stored"
        # while not self._solved(component):
        #     sample = self._get_sample(component)
            


    def _solved(self, nodes):
        for node in nodes:
            if node not in self.database:
                return False
        return True

    def _get_sample(self, component):
        fraction = 0.1 # Intermediate solution for computing how much to sample
        sample = []
        while len(sample) < fraction*len(component):
            # I did this instead of random.sample with k = ceil(fraction*length(component)) so that we can extend this with non-neighboring vertices
            sample.extend(random.sample([node for node in component if node not in sample], 1))
        return sample


    ### TESTING ###

    def test(self, nodes):
        # Create lists for already-solved nodes ([negative],[positive]) and for nodes that still need to be tested
        already_solved = [[],[]]
        to_test = []

        # Split nodes into already-solved nodes and nodes that still need to be tested
        for node in nodes:
            if node in self.database:
                already_solved[self.database[node]].append(node)
            else:
                to_test.append(node)
        
        # Set result to None (in case nothing needs to be tested)
        result = None

        # If any nodes need to be tested, test them
        if to_test:
            io.send_test(to_test)
            result = io.get_test_result()
            self.n_tests += 1

            # If the result was negative or only a single node was tested, update the database (if one node is tested, that node always solved afterwards)
            if not result or len(to_test) == 1:
                for node in to_test:
                    self.database[node] = result

            # Update the number of known positives
            self.n_known_positive = sum(self.database.values())

        # Return the result of the test (possibly None, if no nodes were tested), as well as the positives and negatives we knew beforehand
        return result, already_solved[1], already_solved[0]


    ### CONNECTED COMPONENT ANALYSIS ###

    def get_connected_components(self):
        # Initialize visited list and list for storing connected components
        visited = {v: False for v in range(self.graph.n_nodes)}
        connected_components = []

        # While there are still unvisited nodes, perform BFS from the next unvisited node to get a new connected component
        for v in range(self.graph.n_nodes):
            if not visited[v]:
                cc = self._BFS(v, visited)
                connected_components.append(cc)
        
        # Return the found connected components
        return connected_components

    def _BFS(self, source, visited):
        # Set the source node to visited and initialize a list for all nodes reachable from the source
        visited[source] = True
        connected_component = []
        
        # Perform BFS to get all nodes reachable from the source
        queue = [source]
        while queue:
            u = queue.pop()
            for v in self.graph.graph[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
            connected_component.append(u)

        # Return the list of all vertices reachable from the source
        return connected_component


    ### UTILITY ###

    # Checking for bounds
    def _reached_lower_bound(self):
        return sum(self.database.values()) >= self.graph.lower_bound

    def _reached_upper_bound(self):
        return sum(self.database.values()) >= self.graph.upper_bound # >= for robustness

    # Calculating optimal group sizes for splitting
    def _calculate_p_infection_node(self):
        # Too simple?
        return (self.graph.lower_bound + self.graph.upper_bound)/(2*self.graph.n_nodes)

    def _calculate_p_infection_component(self):
        # Best I could think of right now
        p_infection_node = self._calculate_p_infection_node()
        avg_component_size = len(self.connected_components)/self.graph.n_nodes
        p_infection_component = p_infection_node * avg_component_size
        return p_infection_component

    def _get_optimal_group_size(self, p_infection, upper_bound):
        # Based on https://blogs.sas.com/content/iml/2020/07/06/pool-testing-covid19.html
        max_test_reduction, best_k = float('inf'), 0
        for k in range(1, upper_bound):
            test_reduction = 1 / k + 1 - (1 - p_infection) ** k
            if test_reduction < max_test_reduction:
                max_test_reduction = test_reduction
                best_k = k
        return max(best_k, 2)
        