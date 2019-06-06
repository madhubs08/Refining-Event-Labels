# -*- coding: utf-8 -*-
"""
Created on Sat May 25 12:26:38 2019

@author: Nicole
"""

#from graph import *
#from mappings import *
#from cost import *
import numpy as np
import networkx as nx
import itertools as it

def clusterDetection(threshold):
    """
    clusters the variants based on a given threshold; to do so, edges with a weight above the threshold are deleted from the given graph respresenting the optimal mappings

    :param threshold: the variant threshold the algorithm should use
    :return: list of subgraphs where each subgraph represents a cluster of variants

    """

    edges = list(G.edges(data=True))

    # remove the edges above the threshold (and equal to 0 -> default value)
    for node1, node2, weight in edges:
        if weight['weight'] > threshold or weight['weight'] == 0:
            G.remove_edge(node1, node2)

    # get the subgraphs of the graph created this way
    subgraphNodes = nx.k_edge_subgraphs(G, k=1)
    subgraphs = [G.subgraph(nodes) for nodes in subgraphNodes]
    return subgraphs


def horizontalRefinement(candidateLabels, graphList):
    """
    Performs horizontal relabelling of event labels within a cluster; each event that belongs to the candidate labels will get a unique new label per cluster

    :param candidateLabels: a list of labels that should be refined
    :param graphList: a list of subgraphs where each subgraph represents a cluster of variants
    :return: a list of refined subgraphs, where the attribute 'newLabel' is changed for each candidate label, such that the event labels are unique per cluster
    """

    counter=1
    for subgraph in graphList:
        for label in candidateLabels:
            for node, dict in list(subgraph.nodes(data=True)):
                if dict['curLabel'] == label:
                    dict['newLabel'] += str(counter)
        counter += 1

    return graphList






    
    
    
    
