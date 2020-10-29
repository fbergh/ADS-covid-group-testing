import input_output as io
import math


def zero_point_solution(graph):
    # First test everything, then read everything (faster than having to wait for output each time)
    for node in range(graph.n_nodes):
        io.send_test(node)

    positive_result_idcs = [node for node in range(graph.n_nodes) if io.get_test_result()]
    io.send_answer(positive_result_idcs)

    is_success = io.get_problem_result()
    n_tests = graph.n_nodes
    return is_success, n_tests


def divide_and_conquer(graph, n):
    positive_result_idcs, n_tests = dc_helper(n, 0, graph.n_nodes - 1, 0)

    io.send_answer(positive_result_idcs)
    is_success = io.get_problem_result()
    return is_success, n_tests


def dc_helper(n, p, r, n_tests):
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
                _positive_result_idcs, _n_tests = dc_helper(n, node, end_node - 1, 0)
                positive_result_idcs.extend(_positive_result_idcs)
                n_tests += _n_tests

    n_tests += n

    return positive_result_idcs, n_tests


def dorfman_test(graph):
    # NOTE: p_infection is not the right probability to choose, we can refine t
    n = _get_optimal_group_size(graph.p_infection)

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


def _get_optimal_group_size(p_infection):
    """
    Based on https://blogs.sas.com/content/iml/2020/07/06/pool-testing-covid19.html
    """
    max_test_reduction, best_k = math.inf, 0
    for k in range(1, 20):
        test_reduction = test_reduction_proportion(p_infection, k)
        if test_reduction < max_test_reduction:
            max_test_reduction = test_reduction
            best_k = k
    return best_k


def test_reduction_proportion(p, k):
    return 1 / k + 1 - (1 - p) ** k


if __name__ == "__main__":
    ps = [0.01, 0.025, 0.05, 0.1, 0.15]
    for p in ps:
        print(_get_optimal_group_size(p))
