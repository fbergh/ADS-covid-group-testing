import input_output as io
from social_graph import SocialGraph
import pprint

if __name__ == '__main__':
    # input_values = io.get_values_from_input()
    # g = SocialGraph(input_values)
    g = io.get_random_graph_with_parameters()
    pprint.pprint(g.graph)
