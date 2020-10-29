import input_output as io


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
