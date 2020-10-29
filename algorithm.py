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


def basic_divide_and_conquer(graph):
    positive_result_idcs, n_tests = basic_dc_helper(0, graph.n_nodes - 1, 0)

    io.send_answer(positive_result_idcs)
    is_success = io.get_problem_result()
    return is_success, n_tests


def basic_dc_helper(p, r, n_tests):
    # Base case: test one person and return their index if positive
    if p == r:
        io.send_test(p)
        if io.get_test_result():
            return [p], 1
    # Other base case: test two persons and return their index if positive
    if p + 1 == r:
        tested_positive = []
        io.send_test(p)
        if io.get_test_result():
            tested_positive.append(p)
        io.send_test(r)
        if io.get_test_result():
            tested_positive.append(r)
        return tested_positive, 2
    # Recursive case: test two halves and recurse if either half is positive
    positive_result_idcs = []
    q = int((p + r) / 2)

    io.send_test(range(p, q + 1))
    if io.get_test_result():
        _positive_result_idcs, _n_tests = basic_dc_helper(p, q, 0)
        positive_result_idcs.extend(_positive_result_idcs)
        n_tests += _n_tests

    io.send_test(range(q + 1, r + 1))
    if io.get_test_result():
        _positive_result_idcs, _n_tests = basic_dc_helper(q + 1, r, 0)
        positive_result_idcs.extend(_positive_result_idcs)
        n_tests += _n_tests

    n_tests += 2

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
