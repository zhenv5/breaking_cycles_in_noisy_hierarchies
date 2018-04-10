import networkx as nx 
import argparse
import numpy as np
from measures import F1

import sys
sys.setrecursionlimit(5500000)

def dfs_visit_recursively(g,node,nodes_color,edges_to_be_removed):

	nodes_color[node] = 1
	nodes_order = list(g.successors_iter(node))
	nodes_order = np.random.permutation(nodes_order)
	for child in nodes_order:
		if nodes_color[child] == 0:
				dfs_visit_recursively(g,child,nodes_color,edges_to_be_removed)
		elif nodes_color[child] == 1:
			edges_to_be_removed.append((node,child))

	nodes_color[node] = 2

def dfs_remove_back_edges(graph_file,nodetype = int):
	'''
	0: white, not visited 
	1: grey, being visited
	2: black, already visited
	'''

	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = nodetype)
	nodes_color = {}
	edges_to_be_removed = []
	for node in g.nodes_iter():
		nodes_color[node] = 0

	nodes_order = list(g.nodes_iter())
	nodes_order = np.random.permutation(nodes_order)
	num_dfs = 0
	for node in nodes_order:

		if nodes_color[node] == 0:
			num_dfs += 1
			dfs_visit_recursively(g,node,nodes_color,edges_to_be_removed)

	#print("number of nodes to start dfs: %d" % num_dfs)
	#print("number of back edges: %d" % len(edges_to_be_removed))
	edges_to_be_removed_file = graph_file[:len(graph_file)-6] + "_removed_by_dfs.edges"
	print("edges to be removed, saved in file: %s" % edges_to_be_removed_file)
	from file_io import write_pairs_to_file
	write_pairs_to_file(edges_to_be_removed,edges_to_be_removed_file)
	return edges_to_be_removed

def dfs_performance(graph_file,gt_edges_file):
	edges_to_be_removed = dfs_remove_back_edges(graph_file)
	from measures import report_performance
	report_performance(gt_edges_file,edges_to_be_removed,"DFS")


if __name__ == "__main__":

	'''
	DFS Remove Back Edges
	'''

	parser = argparse.ArgumentParser()
	parser.add_argument("-g","--graph_file",default= " ", help = "input graph file name (edges list)")
	parser.add_argument("-t","--gt_edges_file",default = None, help = "ground truth edges file")
	args = parser.parse_args()
	graph_file = args.graph_file
	
	print("graph_file %s " % graph_file)	
	dfs_performance(graph_file,args.gt_edges_file)
