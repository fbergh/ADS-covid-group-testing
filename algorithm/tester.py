########## IMPORTS ##########

# Self-defined imports
import input_output as io


########## TESTER ##########

class Tester():

    ### INITIALIZATION ###

    def __init__(self, max_n_infections):
        # Set maximum number of infections (for intelligent termination)
        self._max_n_infections = max_n_infections

        # Initialize 
        self._database = {}
        self._performed_tests = {}
    

    ### TESTING ###

    def test(self, nodes):
        # Make sure the test is not redundant
        assert not self.reached_max_infections(), "Attempted to test while maximum number of infections already reached"

        # If the input is not a flat list of nodes, convert it to one
        nodes = self._convert_to_flat_list(nodes)

        # Make sure the list is not empty
        assert nodes, "Attempted to test empty list"

        # Sort the list of nodes
        nodes = sorted(nodes)
        test_key = tuple(nodes)

        # If the solution to the test is already known, return the result
        if test_key in self._performed_tests:
            return self._performed_tests[test_key]

        # Otherwise, if all nodes in the test are already in the database, return the corresponding result
        elif all(node in self._database for node in nodes):
            return any(self._database[node] for node in nodes)

        # Otherwise, if at least one node in the test is a known positive, return positive/True
        elif any(node in self._database and self._database[node] for node in nodes):
            return True
        
        # Otherwise, actually perform the test
        else:
            # Test the list of nodes and store the result
            io.send_test(nodes)
            result = io.get_test_result()
            self._performed_tests[test_key] = result

            # If the result was negative or only a single node was tested, update the database (if a single node is tested, that node always solved afterwards)
            if not result or len(nodes) == 1:
                self._database.update({node : result for node in nodes})
            
            # Return the result
            return result
    

    def test_unknown_only(self, nodes):
        # If the input is not a flat list of nodes, convert it to one
        nodes = self._convert_to_flat_list(nodes)
        
        # Remove nodes that are already in the database
        to_test = [node for node in nodes if not node in self._database]

        # If there are any unknown nodes, return the result of testing only those nodes
        if to_test:
            return self.test(to_test)
        
        # Otherwise, return None (indicating that nothing was tested)
        else:
            return None

    
    ### EXTRACTING POSITIVE INDICES AND NUMBER OF TESTS ###

    def get_positive_indices(self):
        return [n for n in self._database if self._database[n]]

    def get_n_tests(self):
        return len(self._performed_tests)


    ### FILLING IN VALUES ###

    def fill_remaining(self, nodes, result):
        self._database.update({node : result for node in nodes if node not in self._database})


    ### CHECKING IF SINGLE NODE IS IN DATABASE ###

    def in_database(self, node):
        return node in self._database


    ### CHECKING IF DONE ###

    def reached_max_infections(self):
        return sum(self._database.values()) >= self._max_n_infections

    def done(self, nodes):
        return all(node in self._database for node in nodes)

    
    ### UTILITY FUNCTIONS ###

    def _convert_to_flat_list(self, element):
        # Convert an integer or a 2d list to a 1d list
        if type(element) == int:
            output = [element]
        elif all(isinstance(i, list) for i in element):
            output = [el for l in element for el in l]
        else:
            output = element
        return output