########## IMPORTS ##########

# Standard library imports
import random

# Self-defined imports
from algorithm import Algorithm, Tester
import input_output as io


########### CLUSTER GROUP TESTING ALGORITHM ##########

class ClusterGroupTesting(Algorithm):
    """ Class containing code for the cluster group testing algorithm """

    def __init__(self):
        self.name = "cluster_group_testing"


    ### RUNNING THE ALGORITHM ###
    
    def run(self, graph):
        """ 
        Run the algorithm on a given graph 
        
        :return: whether the result was correct and the number of tests required
        """
        # Set variables
        self.graph = graph # Graph on which the algorithm is called
        self.tester = Tester(self.graph.upper_bound) # Tester that will perform all tests
        self.found_clusters = [] # List of encountered clusters 

        # Compute list of connected components
        io.eprint("Retrieving connected components...")
        self.connected_components = self.get_connected_components()
        io.eprint(f"Encountered {len(self.connected_components)} connected components.")

        # Solve the problem for each component
        io.eprint("Solving each component...")
        self.solve_all_components()
        io.eprint("All components solved.")

        # If the maximum number of clusters or the upper bound was reached, fill in the rest of the database
        if self.__reached_thresholds():
            io.eprint("Algorithm was intelligently terminated. Setting all remaining nodes to negative.")
            self.tester.fill_remaining(range(self.graph.n_nodes), False)

        # Verify we are done testing and extract the positive nodes 
        assert self.tester.done(range(self.graph.n_nodes)), "The algorithm has not finished testing"
        io.eprint("Extracting positive indices...")
        positive_indices = self.tester.get_positive_indices()
        io.eprint(f"Extracted {len(positive_indices)} positive indices.")

        # Send answer and check result
        io.eprint("Sending answer...")
        io.send_answer(positive_indices)
        is_success = io.get_problem_result()
        io.eprint("Result obtained.")

        # Return result and number of tests used
        return is_success, self.tester.get_n_tests()
    

    ### SOLVING ALL COMPONENTS ###

    def solve_all_components(self):
        """ Solve the problem separately for all positive connected components """
        # Set the correct number of groups, the test type in the base case and how to process a component
        p_group_infected = self.graph.n_initially_infected/len(self.connected_components)
        n_groups = max(2, round(p_group_infected*75)) # Number of groups depends on probability that a group is infected
        process_item = self.solve_component

        # Recursively search for positive components
        self.recursive_search(self.connected_components, n_groups, process_item)


    ### SOLVING A SINGLE COMPONENT ###

    def solve_component(self, component):
        """ Solve the problem for a single connected component that tested positive as a whole """
        # Check that the function was called on a positive component
        assert self.tester.known_positive(component), "Attempted to solve a component that is now known to be positive"

        # If the length of the component is 1, store it as a cluster (since the one node is necessarily positive)
        if len(component) == 1:
            assert self.tester.in_database(component[0]), "Solving component with single element, but element not stored in database"
            self.found_clusters.append(component)
            return
        
        # While the total problem is not solved and the component is not fully solved:
        while not self.__reached_thresholds() and not self.tester.done(component):
            # Sample some nodes from the component
            sample_size = max(5, 0.25*len(component))
            sample = self.sample(component, sample_size)
            assert sample, "Sample is empty"

            # Look for clusters in the sample by recursively searching for positive nodes
            p_node_infected = (self.graph.upper_bound + self.graph.lower_bound)/(2*self.graph.n_nodes) # Number of groups depends on probability that a node is infected
            n_groups = max(2, round(p_node_infected*75))
            process_item = lambda node: self.explore_cluster(node) if not node in [n for c in self.found_clusters for n in c] else None
            self.recursive_search(sample, n_groups, process_item)

            # Test the nodes that remain unknown once, to see if all clusters have been found
            if not self.__reached_thresholds():
                self.tester.test_unknown_only(component)


    ### RANDOM SAMPLING ###

    def sample(self, component, sample_size=5):
        """ 
        Randomly sample a given number of nodes from a component, avoiding sampling neighbors if possible
        
        component: connected component to sample from
        sample_size: number of nodes to sample
        :return: list of sampled nodes
        """
        # Convert component into a set (for computational purposes)
        component = set(component)
        # Create set that stores the sample
        sample = set()

        # Get all nodes from the component that have already been solved
        tested = set([v for v in component if self.tester.in_database(v)])
        # The initial set of nodes we can sample includes all untested nodes in the component
        set_to_sample = component - tested

        # Initialize a set of neighbors of sampled nodes (to avoid picking adjacent nodes if possible)
        neighbours = set()

        # While there are sample-able nodes and sample_size has not been reached:
        while set_to_sample and len(sample) != sample_size:
            # Sample a single node
            node = random.sample(set_to_sample, 1)[0]
            assert not self.tester.in_database(node), "Sampled node already present in database"
            sample.add(node)

            # Add the neighbors of the sampled node to the list of neighbors to avoid sampling them if possible
            neighbours.update([n for n in self.graph.graph[node] if n in set_to_sample])
            # Update the set of nodes that can be sampled by removing the sampled node and its neighbors
            set_to_sample = set_to_sample - sample - neighbours
        
        # If set_to_sample is empty, fill the remaining space with some neighbors of already-sampled nodes to reach sample_size
        if not set_to_sample:
            while len(neighbours) != 0 and len(sample) != sample_size:
                node = random.sample(neighbours, 1)[0]
                neighbours.remove(node)
                sample.add(node)
        
        # Return the sample
        return list(sample)


    ### CLUSTER EXPLORATION ###

    def explore_cluster(self, source):
        """ Fully explore the cluster of positive nodes that the source is part of """
        # Make sure the source is not already part of a cluster
        assert source not in [node for c in self.found_clusters for node in c], "Exploring cluster that has already been explored"

        # Initialize lists for cluster and frontier
        cluster = [source]
        frontier = [source]

        # While there are still nodes in the frontier:
        while frontier and not self.__reached_thresholds():
            # Get the unknown neighbors of the current frontier
            neighbors = list(set([n for node in frontier for n in self.graph.graph[node]]))
            new_neighbors = [n for n in neighbors if n not in cluster]
            assert not self.tester.known_positive(new_neighbors), "Encountered known positive while expanding cluster"
            unknown_neighbors = [n for n in neighbors if not self.tester.in_database(n)]
            
            # If there are any unknown neighbors, retrieve the ones that are positive
            positive_neighbors = []
            if unknown_neighbors:
                p_neighbor_infected = self.graph.p_infection
                n_groups = max(2, round(p_neighbor_infected*75))
                process_item = lambda node: node
                positive_neighbors = self.recursive_search(unknown_neighbors, n_groups, process_item, True)

            # Update the frontier and the cluster
            frontier = positive_neighbors
            cluster.extend(positive_neighbors)

        # After exploring the entire cluster, add it to the list of clusters
        self.found_clusters.append(cluster)


    ### CONNECTED COMPONENT ANALYSIS ###

    def get_connected_components(self):
        """ Perform connected component analysis using BFS """
        # Initialize visited list and list for storing connected components
        visited = {v: False for v in range(self.graph.n_nodes)}
        connected_components = []

        # While there are still unvisited nodes, perform BFS from the next unvisited node to get a new connected component
        for v in range(self.graph.n_nodes):
            if not visited[v]:
                cc = self.BFS(v, visited)
                connected_components.append(cc)
        
        # Return the found connected components
        return connected_components


    ### BASIC ALGORITHMS ###

    def BFS(self, source, visited):
        """ Breadth-first search implementation (using pre-initialized dictionary to keep track of visited nodes) """
        # Set the source node to visited and initialize a list for all nodes reachable from the source
        visited[source] = True
        connected_component = []
        
        # Perform BFS to get all nodes reachable from the source
        queue = [source]
        while queue:
            u = queue.pop()
            for v in self.graph.graph[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
            connected_component.append(u)

        # Return the list of all vertices reachable from the source
        return connected_component

    def recursive_search(self, items, n_groups, process_item, return_results=False):
        """ 
        Algorithm that recursively searches for positive elements:
        - if the number of items is less than or equal to n_groups, test every element sequentially and process the element if positive
        - if the number of items is bigger than n_groups, split into groups and recurse if a group tests positive 

        items: list of items to search for positives in
        n_groups: number of groups to split the list into in the recursive case
        process_item: function specifying what should happend to an element that tests positive
        return_results: whether to keep track of results and return them
        """
        # If results should be returned, initialize list that stores results
        if return_results:
            results = []

        # Base case: linearly process elements in items
        if len(items) <= n_groups:
            for item in items:
                if not self.__reached_thresholds():
                    if self.tester.test(item):
                        if return_results:
                            results.append(process_item(item))
                        else:
                            process_item(item)
        
        # Recursive case: split items into groups and recurse on groups
        else:
            # For all groups of nodes:
            for i in range(n_groups):
                if not self.__reached_thresholds():
                    # Compute start and end indices of the group
                    start, end = self.__get_split_indices(len(items), n_groups, i)

                    # If the group tests positive, recursively search the group
                    if self.tester.test(items[start:end]):
                        if return_results:
                            results.extend(self.recursive_search(items[start:end], n_groups, process_item, return_results))
                        else:
                            self.recursive_search(items[start:end], n_groups, process_item, return_results)
        
        # If the result should be returned, return it
        if return_results:
            return results


    ### UTILITY ###

    ## CHECKING THRESHOLDS ##
    def __reached_thresholds(self):
        """ Check if the maximum number of clusters or positives has been reached """
        reached_max_clusters = len(self.found_clusters) > self.graph.n_initially_infected
        return reached_max_clusters or self.tester.reached_max_infections()

    ## GETTING SPLIT INDICES ##
    def __get_split_indices(self, list_length, n_groups, group_index):
        """ 
        Compute indices of a given group while splitting a list into approximately equally-sized groups
        
        list_length: length of the list that is being split into groups
        n_groups: the number of groups that the list will be split into
        group_index: the index of the group to retrieve start and end indices for
        :return: start and end indices for the group corresponding to group_index
        """
        # Compute the size of a single group given the number of groups and the length of the total list
        group_size = list_length/n_groups

        # Compute the start and end indices corresponding to the given group index
        start = round(group_size*group_index)
        end = round(group_size*(group_index+1))

        # Return the computed indices
        return start, end