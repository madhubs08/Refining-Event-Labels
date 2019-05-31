
import networkx as nx
import itertools  as it 



class graphTool:
    
    
    def __init__(self):
        self.G = nx.Graph()
        

    def createEdgeList(self, edges = [], weight = -1):
        """
        creates a list of tuples of edges with the corresponding weights given a list of edges and weights
    
        :param edges: edges given as a list of tuples (eventID1,eventID2)
        :param weight: a weight
        :return: a list of tuples (eventID1, eventID2, weight) of edges together with their weight
        """
        return [(a,b,{'weight': weight}) for (a,b) in edges]
    
    
#    def __pairwise(self, iterable):
#        """ auxiliary function to create pairs"""
#        a, b = it.tee(iterable)
#        next(b, None)
#        return zip(a, b)
    
    #Auxiliary function
    def pairwise(variant_nodes):
        """ auxiliary function to create pairs"""
        list_pairs = []
        l = len(variant_nodes)
        for i in range(l-1):
            list_pairs.append((variant_nodes[i],variant_nodes[i+1]))
        return list_pairs

    def __createNodeListFromVariant(self, variant = []):
        """
        assigns the current label ('curLabel') and an empty placeholder for the new label ('newLabel') as attributes to the events of a given variant
    
        :param variant: variant given as a list of tuples (eventID, event label)
        :return: list of variants with the attributes 'curLabel' (current event label) and 'newLabel' (initialized as event label)
        """
    
        return [(a,{'curLabel':b, 'newLabel':b}) for (a,b) in variant]
    
        
    def __createEdgeListFromVariant(self, variant = [], weight = -1):
        """
        creates a list of edges together with their weight for a given variant and weight
    
        :param variant: variant given as a list of tuples (eventID, event label)
        :param weight: a weight
        :return: a list of edges together with their weight
        """
        nodes,_ = zip(*variant)
        return self.createEdgeList(self.__pairwise(nodes), weight)
    
    
    def createGraphFromVariants(self, variants = []):
        """
        updates an empty graph, such that it becomes a weighted graph containing vertices of the form (eventID, event label) and edges of the form (eventID1, eventID2, weight) based on a given list of variants
    
        :param variants: list of variants, where a variant is given as a list of tuples (eventID, event label), i.e., a list of lists of tuples
        """
        for variant in variants:
            self.G.add_nodes_from(self.__createNodeListFromVariant(variant))
            self.G.add_edges_from(self.__createEdgeListFromVariant(variant))
    


#    def addOptimalMapping(self, optimalMapping = [], normalizedCost = -1):
#        """
#        updates the graph using a given optimal mapping between two variants and the normalized cost for this mapping
#    
#        :param optimalMapping: a mapping as a set of matched pairs (ID1,ID2), where the event label corresponding to ID1 is the same as that corresponding to ID2; ID1 is from the first variant and ID2 from the second variant
#        :param normalizedCost: the cost of the mapping
#        """
#        self.G.add_edges_from(self.createEdgeList(optimalMapping , normalizedCost))
    
    #Args: list containing all best mappings, maximalCost for normalization
    #Returns: updates the graph by adding edges between mapped pairs with corresponding cost
    

    def addOptimalMapping(self, bestMappingsList, maxCost, candidate_positions):
        """
        updates the graph using a given optimal mapping between two variants and the normalized cost for this mapping
        
        :param bestMappingsList:  list containing all best mappings, list has length number of (unordered) pairs of variants 
        :param normalizedCost: the maximal cost out of all best mappings which we use for normalization of the costs
        :param: candidate_positions: the list of all positions referring to some candidate label
        """ 
        for mapp in bestMappingsList:
            normalized_cost = mapp[1]/maxCost
            mapped_pairs = mapp[0]
            candidate_pairs = []
            non_candidate_pairs = []
            for (x,y) in mapped_pairs:
                if x in candidate_positions:
                    candidate_pairs.append((x,y))
                else:
                    non_candidate_pairs.append((x,y))
            self.G.add_edges_from(self.createEdgeList(candidate_pairs, normalized_cost))
            self.G.add_edges_from(self.createEdgeList(non_candidate_pairs, -1)) #cost -1 for pairs of non candidate labels

        
    def clusterDetection(self, customParams):
        """
        clusters the variants based on a given threshold; to do so, edges with a weight above the threshold are deleted from the given graph respresenting the optimal mappings
    
        :param threshold: the variant threshold the algorithm should use
        :return: list of subgraphs where each subgraph represents a cluster of variants
    
        """
        
        horizontalTreshold = customParams.getHorizontalTreshold()

        edges = list(self.G.edges(data=True))
        # remove the edges above the threshold (and below 0)
        for node1, node2, weight in edges:
            if weight['weight'] > horizontalTreshold or weight['weight'] < 0:
                self.G.remove_edge(node1, node2)
    
        # get the subgraphs of the graph created this way
        subgraphNodes = nx.k_edge_subgraphs(self.G, k=1)
        subgraphs = [self.G.subgraph(nodes) for nodes in subgraphNodes]
        return subgraphs



    

    

