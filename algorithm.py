#!/usr/bin/env python

import csv
import networkx as nx

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
            predict_list[node] = list(missing_nodes[node])
        else:
            predict_list[node] = list()

    output_result(config.result_folder + "naive.csv", test_nodes, predict_list)


# Read a directed graph from training data
def read_network(fpath):
    graph = nx.DiGraph()
    fh = csv.reader( open(fpath, 'r') )
    fh.next()
    for edge in fh:
        node1 = edge[0]
        node2 = edge[1]
        graph.add_edges_from([(node1, node2)])

    return graph


# Read a list of source nodes from test data
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

    g = nx.Graph(train_network) # convert to undirected graph
    print len(nx.connected_components(g))

    #naive(train_network, test_nodes)

