########## IMPORTS ##########

# Standard libary imports
from collections import defaultdict


########## GRAPH CLASS ##########

class SocialGraph:
    """
    Undirected graph data structure for a social graph
    """
    def __init__(self, graph, input_values):
        # Initialises all parameters in input_values as class parameters
        self.__dict__.update(input_values)
        # Constructor overloading is not supported in Python, so do it like this
        if type(graph) == SocialGraph:
            self._graph = graph.graph
        elif graph is None:
            self._graph = defaultdict(set)
            self.add_connections()
        else:
            self._graph = graph

    def add_connections(self):
        """ Add connections (list of tuple pairs) to graph """
        for node1, node2 in self.idcs_connected_nodes:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """
        self._graph[node1].add(node2)
        self._graph[node2].add(node1)

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """
        return node1 in self._graph and node2 in self._graph[node1]

    def n_edges_in_component(self, component):
        """ Compute the number of edges within a given component (correct only if the component is connected) """
        edges = []
        for node in component:
            edges.extend(self.graph[node])
        return len(edges) // 2

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

    @property
    def graph(self):
        return self._graph
