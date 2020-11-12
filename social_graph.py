########## IMPORTS ##########

# Standard libary imports
from collections import defaultdict


########## GRAPH CLASS ##########

class SocialGraph:
    """ Undirected graph data structure for a social graph """

    def __init__(self, graph, input_values):
        # Initialize all parameters in input_values as class parameters
        self.__dict__.update(input_values)
        # Constructor overloading is not supported in Python, so do it like this
        if type(graph) == SocialGraph:
            self.__graph = graph.graph
        elif graph is None:
            self.__graph = defaultdict(set)
            self.add_connections()
        else:
            self.__graph = graph

    def add_connections(self):
        """ Add connections (list of tuple pairs) to graph """
        for node1, node2 in self.idcs_connected_nodes:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """
        self.__graph[node1].add(node2)
        self.__graph[node2].add(node1)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

    @property
    def graph(self):
        return self.__graph