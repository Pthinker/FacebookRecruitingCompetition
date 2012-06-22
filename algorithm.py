#!/usr/bin/env python

import csv
import networkx as nx
from operator import *
import heapq

import config


# Naive method: to predict links for node A, if B->A exists in training data,
# then predict A->B.
def naive(train_network, test_nodes):
    missing_nodes = dict()
    for node in train_network.nodes():
        for neighbor in train_network.neighbors(node):
            if not node in train_network.neighbors(neighbor):
                missing_nodes.setdefault(neighbor, set()).add(node)

    predict_list = dict()
    for node in test_nodes:
        if node in missing_nodes:
            predict_list[node] = missing_nodes[node]
        else:
            predict_list[node] = set()

    for node in test_nodes:
        candidates = set()
        for neighbour in train_network.neighbors(node):
            for n in train_network.neighbors(neighbour):
                if n != node:
                    candidates.add(n)
        for n in list(candidates):
            if (n not in train_network.neighbors(node)):
                predict_list.setdefault(node, set()).add(n)
    
    for node in predict_list:
        neighbor_set = set(train_network.neighbors(node))
        candidates = list(predict_list[node])
        similarity = dict()
        for candidate in candidates:
            candidate_neighbor_set = set(train_network.neighbors(candidate))
            similarity[candidate] = neighbor_set.union(candidate_neighbor_set)
        records = heapq.nlargest(10, similarity.iteritems(), itemgetter(1))
        ranked_list = []
        for rec in records:
            ranked_list.append(rec[0])
        predict_list[node] = ranked_list

    output_result(config.result_folder + "naive_nc_rank.csv", test_nodes, predict_list)


def neighbour_counting(train_network, test_nodes):
    predict_list = dict()

    for node in test_nodes:
        predict_list[node] = list()
        candidates = set()
        for neighbour in train_network.neighbors(node):
            for n in train_network.neighbors(neighbour):
                candidates.add(n)
        for n in list(candidates):
            if n not in train_network.neighbors(node):
                predict_list[node].append(n)

    output_result(config.result_folder + "nc.csv", test_nodes, predict_list)


# Read a directed graph from training data, return a networkx graph
def read_network(fpath):
    graph = nx.DiGraph()
    fh = csv.reader( open(fpath, 'r') )
    fh.next()
    for edge in fh:
        node1 = edge[0]
        node2 = edge[1]
        graph.add_edges_from([(node1, node2)])

    return graph


# Read a list of source nodes from test data and return the list
def read_test(fpath):
    nodes = []
    fh = open(fpath, 'r')
    fh.readline()
    for line in fh:
        line = line.strip()
        nodes.append(line)

    return nodes


def output_result(fpath, test_nodes, predict_list):
    fh = csv.writer( open(fpath, "w") )
    fh.writerow( ['source_node', 'destination_nodes'] )
    for node in test_nodes:
        fh.writerow([node, " ".join(predict_list[node][0:9])])


if __name__ == "__main__":
    train_network = read_network(config.train_fpath)
    test_nodes = read_test(config.test_fpath)

    #g = nx.Graph(train_network) # convert to undirected graph
    #print train_network.number_of_nodes()


    naive(train_network, test_nodes)

    #neighbour_counting(train_network, test_nodes)
