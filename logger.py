########## IMPORTS ##########

# Standard libary imports
import os
import datetime
import json


########## LOGGER CLASS ##########

class Logger:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            os.mkdir(path)
        self.date = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.filename = ""
        self.log = {'problems': [], 'results': {}}

    def log_problem(self, problem_params, is_success, n_tests):
        """ Log a given problem, whether the algorithm succeeded in solving it and the number of tests used """
        # We do not log edges, to avoid clutter
        del problem_params["idcs_connected_nodes"]

        # Create dicitonary to store problem and corresponding results
        problem_dict = {}
        problem_dict.update(problem_params)
        problem_dict["is_success"] = is_success
        problem_dict["n_tests"] = n_tests

        # Log the problem
        self.log["problems"].append(problem_dict)

    def log_algorithm_with_results(self, algorithm, total_time, approx_score, n_correct):
        """ Log the result of an algorithm after running it on all problems on the server """
        # Set filename of the log file
        self.filename = f"{approx_score}_{n_correct}_{total_time:.2f}_{algorithm}_{self.date}.json"

        # Store overall results in a dictionary
        results = {"algorithm": algorithm, 
                   "total_time": total_time, 
                   "approx_score": approx_score,
                   "n_correct": n_correct}

        # Log results
        self.log["results"].update(results)

    def close(self):
        """ Store everything that was logged as a json file """
        with open(os.path.join(self.path, self.filename), 'w') as outfile:
            json.dump(self.log, outfile, indent="  ")