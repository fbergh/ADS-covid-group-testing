########## IMPORTS ##########

# Self-defined imports
import input_output as io


########## TESTER ##########

class Tester():
    """ 
    Tester class that contains all testing functions and keeps track of a database 
    of known positives and negatives as well as a list of performed tests 
    """

    def __init__(self, max_n_infections):
        self.__max_n_infections = max_n_infections
        self.__database = {}
        self.__performed_tests = {}
    

    ### TESTING ###

    def test(self, nodes):
        """ 
        Perform a test for the given input; actual tests are only performed if required (if result is not already known)

        nodes: integer, list of integers or list of listst of integers, representing node indices
        :return: result of testing nodes
        """
        # Make sure the test is not redundant
        assert not self.reached_max_infections(), "Attempted to test while maximum number of infections already reached"

        # If the input is not a flat list of nodes, convert it to one
        nodes = self.__convert_to_flat_list(nodes)

        # Make sure the list is not empty
        assert nodes, "Attempted to test empty list"

        # Sort the list of nodes
        nodes = sorted(nodes)
        test_key = tuple(nodes)

        # If the solution to the test is already known, return the result
        if test_key in self.__performed_tests:
            return self.__performed_tests[test_key]

        # Otherwise, if all nodes in the test are already in the database, return the corresponding result
        elif all(node in self.__database for node in nodes):
            return any(self.__database[node] for node in nodes)

        # Otherwise, if at least one node in the test is a known positive, return positive/True
        elif any(node in self.__database and self.__database[node] for node in nodes):
            return True
        
        # Otherwise, actually perform the test
        else:
            # Test the list of nodes and store the result
            io.send_test(nodes)
            result = io.get_test_result()
            self.__performed_tests[test_key] = result

            # If the result was negative or only a single node was tested, update the database (if a single node is tested, that node always solved afterwards)
            if not result or len(nodes) == 1:
                self.__database.update({node : result for node in nodes})
            
            # Return the result
            return result
    

    def test_unknown_only(self, nodes):
        """ 
        Perform a test for the given input after removing all already-known nodes

        nodes: integer, list of integers or list of listst of integers, representing node indices
        :return: result of testing nodes
        """
        # If the input is not a flat list of nodes, convert it to one
        nodes = self.__convert_to_flat_list(nodes)
        
        # Remove nodes that are already in the database
        to_test = [node for node in nodes if not node in self.__database]

        # If there are any unknown nodes, return the result of testing only those nodes
        if to_test:
            return self.test(to_test)
        
        # Otherwise, return None (indicating that nothing was tested)
        else:
            return None

    
    ### EXTRACTING POSITIVE INDICES AND NUMBER OF TESTS ###

    def get_positive_indices(self):
        """ Return indices of all known positives present in the database """
        return [n for n in self.__database if self.__database[n]]

    def get_n_tests(self):
        """ Return the number of tests performed by the tester"""
        return len(self.__performed_tests)


    ### FILLING IN VALUES ###

    def fill_remaining(self, nodes, result):
        """ 
        Update the database value of all not-already-known nodes in the input to the given result
        
        nodes: integer, list of integers or list of listst of integers, representing node indices
        result: Boolean value to to use as values in the database
        """
        self.__database.update({node : result for node in nodes if node not in self.__database})


    ### CHECKING IF LIST OF NODES IS IN DATABASE ###

    def in_database(self, nodes):
        """ Check if all nodes in the input (a single node or a list of nodes) are already in the database """
        # Convert input to a flat list of nodes
        nodes = self.__convert_to_flat_list(nodes)

        # Check if all nodes are in the database
        return all(node in self.__database for node in nodes)

    
    ### CHECKING FOR KNOWN POSITIVES ###

    def known_positive(self, nodes):
        """ Check if a list of nodes is known to test positive """
        # Convert input to a flat list of nodes
        nodes = self.__convert_to_flat_list(nodes)
        # Check if any of the nodes in the input are known positives in the database
        positive_in_database = any([node in self.__database and self.__database[node] for node in nodes])
        # Check if the list of nodes as a whole has been tested before
        test_key = tuple(sorted(nodes))
        positive_in_tests = test_key in self.__performed_tests and self.__performed_tests[test_key]
        # Return True if either of the above cases is true
        return positive_in_database or positive_in_tests


    ### CHECKING IF DONE ###

    def reached_max_infections(self):
        """ Check if the number of known positives has reached the maximum number of infections """
        return sum(self.__database.values()) >= self.__max_n_infections

    
    ### UTILITY FUNCTIONS ###

    def __convert_to_flat_list(self, element):
        """ Convert an integer or a 2D list of integers to a 1D list of integers """
        if type(element) == int:
            output = [element]
        elif all(isinstance(i, list) for i in element):
            output = [el for l in element for el in l]
        else:
            output = element
        return output