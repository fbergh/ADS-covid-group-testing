import input_output as io


def zero_point_solution(graph):
    # First test everything, then read everything (faster than having to wait for output each time)
    for node in range(graph.n_nodes):
        io.send_test(node)

    positive_result_idcs = [node for node in range(graph.n_nodes) if io.get_test_result()]
    io.send_answer(positive_result_idcs)

    is_success = io.get_problem_result()
    return is_success


def basic_divide_and_conquer(graph):
    positive_result_idcs = basic_dc_helper(0,graph.n_nodes)

    io.send_answer(positive_result_idcs)
    is_success = io.get_problem_result()
    return is_success

def basic_dc_helper(p,r):
    # Base case: test one person and return their index if positive
    if p + 1 == r:
        io.send_test(p)
        if io.get_test_result():
            return [p]
        else:
            return []
    # Recursive case: test two halves and recurse if either half is positive
    positive_result_idcs = []
    q = int((p + r)/2)

    io.send_test(range(p,q))
    if io.get_test_result():
        positive_result_idcs.extend(basic_dc_helper(p,q))
        
    io.send_test(range(q,r))
    if io.get_test_result():
        positive_result_idcs.extend(basic_dc_helper(p,q))
        
    return positive_result_idcs
        
        