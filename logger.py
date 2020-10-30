import os
import datetime
import json


class Logger:
    def __init__(self, path):
        super().__init__()
        self.path = path
        if not os.path.exists(path):
            os.mkdir(path)
        self.date = str(datetime.datetime.now()).replace(" ", "-").replace(":","-")
        self.filename = ""
        self.log = {'problems': [], 'results': {}}

    def log_problem(self, problem_params, is_success, n_tests):
        # Delete specific connections to avoid clutter
        del problem_params["idcs_connected_nodes"]

        problem_dict = {}
        problem_dict.update(problem_params)
        problem_dict["is_success"] = is_success
        problem_dict["n_tests"] = n_tests

        self.log["problems"].append(problem_dict)

    def log_algorithm_with_results(self, algorithm, total_time, proportion_test, proportion_correct):
        self.filename = f"{proportion_test:.3f}_{algorithm}_{self.date}.json"

        results = {"algorithm": algorithm, "total_time": total_time, "test_proportion": proportion_test,
                   "total_correct": proportion_correct}

        self.log["results"].update(results)

    def close(self):
        with open(os.path.join(self.path, self.filename), 'w') as outfile:
            json.dump(self.log, outfile, indent="  ")
