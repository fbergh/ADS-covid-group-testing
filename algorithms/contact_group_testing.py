import math

from algorithms import Algorithm
import input_output as io

class ContactGroupTesting(Algorithm):
    def __init(self):
        self.name = "countact_group_testing"

    ### RUNNING THE ALGORITHM ###
    
    def run(self, graph):
        # Set global variables
        self.database = {} # database for storing known positives & negatives
        self.n_found_clusters = 0 # number of found clusters
        self.n_known_positive = 0 # number of known positives
        self.graph = graph # graph on which the algorithm is called

        # Compute list of connected components
        self.connected_components = self.get_connected_components()

        # WTH IS GOING ON HERE???
        for i in self.connected_components:
            io.send_test(i)
        for i in self.connected_components:
            io.eprint(i)
            io.eprint(io.get_test_result())

        # Solve the problem for each component
        self.solve_all_components()

        error # I only want to test a single graph for now, so this is how I make the system crash
    

    ### SOLVING ALL COMPONENTS ###

    def solve_all_components(self):
        pass #TODO


    ### SOLVING A SINGLE COMPONENT (WITH AT LEAST 1 POSITIVE NODE) ###

    def solve_component(self, component):
        pass #TODO
        

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