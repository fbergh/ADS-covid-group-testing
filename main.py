import input_output as io
import algorithm as a
from social_graph import SocialGraph


"""
Run this in the terminal with: ncat -c 'python3 ./main.py' group-testing.maarse.xyz 6525
NOTE: Add a credentials file in the repository
"""
if __name__ == '__main__':
    io.give_credentials()
    n_problems = io.parse_number_of_problems()
    n_correct = 0
    for problem in range(n_problems):
        input_parameters = io.get_values_from_input()
        g = SocialGraph(None, input_parameters)
        is_success = a.zero_point_solution(g)
        io.eprint(f"Problem {problem}: {is_success}")
        n_correct += is_success
    io.eprint(f"Problems correct: {n_correct}/{n_problems}")
