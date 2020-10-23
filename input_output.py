def get_values_from_input():
    """
    From the assignment:
        (a) A line with the number of nodes n
        (b) A line with the number of edges
        (c) A line with the number of initially infected people
        (d) A line with the chance p that people infect a close contact with 0 < p < 1
            and formatted as 0. followed by decimals
        (e) A line with a lower bound l and upper bound u on the number of total infections,
            with 0 < l <= i <= u <= 0.7n, with i the number of infections (just like in the real world,
            you already have an indication of how many people are infectious)
        (f) For each edge, a line with the two indices of the connected nodes
    :return: the variables received above
    """
    # Try to parse and initialise all values and conditions of variables
    try:
        n_nodes = int(input())

        n_edges = int(input())
        max_edges = n_nodes * (n_nodes - 1) // 2
        n_edges = max_edges if n_edges > max_edges else n_edges

        n_initially_infected = int(input())
        n_initially_infected = n_nodes if n_initially_infected > n_nodes else n_initially_infected

        p_infection = float(input())
        assert 0 < p_infection < 1, "Infection probability should be greater than 0 and smaller than 1"

        lower_bound, upper_bound = input().strip().split(" ")
        lower_bound = int(lower_bound)
        assert 0 < lower_bound <= n_initially_infected, "Lower bound should be greater than 0 and smaller than the " \
                                                        "number of initially infected people "
        upper_bound = int(upper_bound)
        assert n_initially_infected <= upper_bound <= 0.7 * n_nodes, "Upper bound should be greater than the number " \
                                                                     "of initially infected people and smaller than " \
                                                                     "0.7 * number of nodes "

        idcs_connected_nodes = []
        for _ in range(n_edges):
            node1, node2 = input().strip().split(" ")
            node1 = int(node1)
            assert 0 <= node1 < n_nodes, "The index of the left node is out of bounds"
            node2 = int(node2)
            assert 0 <= node2 < n_nodes, "The index of the right node is out of bounds"
            idcs_connected_nodes.append((int(node1), int(node2)))
    except ValueError:
        print("Input values could not be parsed as integer/float")
        raise SystemExit

    return {"n_nodes": n_nodes, "n_edges": n_edges, "n_initially_infected": n_initially_infected,
            "p_infection": p_infection, "lower_bound": lower_bound, "upper_bound": upper_bound,
            "idcs_connected_nodes": idcs_connected_nodes}


# Test function
if __name__ == "__main__":
    input_values = get_values_from_input()
    print(input_values)
