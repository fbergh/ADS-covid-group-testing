########## IMPORTS ##########

# Standard libary imports
import math


########## UTILITY FUNCTIONS ##########

def calculate_p_infection(graph):
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


def get_optimal_group_size(p_infection, upper_bound):
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


########## RUN FILE (BUGFIXING) ##########

if __name__ == "__main__":
    ps = [0.01, 0.025, 0.05, 0.1, 0.15]
    for p in ps:
        print(get_optimal_group_size(p))