########## SUPERCLASS ##########

class Algorithm(object):
    """ Base class for algorithms """
    def run(self, graph):
        raise NotImplementedError