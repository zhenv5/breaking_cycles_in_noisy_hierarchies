import networkx as nx
import argparse
import numpy as np

def add_cycle_edges_by_path(g,number_of_edges,path_length = 5):
	number = 0
	num_nodes = g.number_of_nodes()
	nodes = g.nodes()
	extra_edges = []
	while number < number_of_edges:
		u,v = np.random.randint(0,num_nodes,2)
		u = nodes[u]
		v = nodes[v]
		if nx.has_path(g,u,v):
			length = nx.shortest_path_length(g,source = u,target = v)
			if length <= path_length:
				extra_edges.append((v,u))
				number += 1
		if nx.has_path(g,v,u):
			length = nx.shortest_path_length(g,source = v,target = u)
			if length <= path_length:
				extra_edges.append((u,v))
				number += 1
	print("# extra edges added with path length <= %d: %d" % (path_length,len(extra_edges)))
	return extra_edges

def add_extra_edges(g,number_of_edges):
	number = 0
	num_nodes = g.number_of_nodes()
	nodes = g.nodes()
	extra_edges = set()
	while len(extra_edges) < number_of_edges:
		u,v = np.random.randint(0,num_nodes,2)
		u = nodes[u]
		v = nodes[v]
		if nx.has_path(g,u,v):
			if (v,u) not in extra_edges:
				extra_edges.add((v,u))	
		if nx.has_path(g,v,u):
			if (u,v) not in extra_edges:
				extra_edges.add((u,v))
	extra_edges = list(extra_edges)
	print("# extra edges added (path lenght unconstrainted): %d" % (len(extra_edges)))
	return extra_edges	



def add_cycle_edges(g,num_extra_edges,path_length = 1):
	if path_length == 1:
		edges = list(g.edges_iter())
		extra_edges_index = np.random.choice(len(edges),num_extra_edges)
		extra_edges = [(edges[index][1],edges[index][0]) for index in extra_edges_index]
		extra_edges = list(set(extra_edges))
		print("# extra edges added by length = %d: %d" % (path_length,len(extra_edges)))
		return extra_edges
	else:
		return add_cycle_edges_by_path(g,num_extra_edges,path_length = path_length)

def introduce_cycles(g,num_extra_edges,path_length):
	if path_length <= 0:
		# no constraints on path length 
		return add_extra_edges(g,num_extra_edges)
	else:
		# path length >= 1
		return add_cycle_edges(g,num_extra_edges,path_length)

def introduce_cycles_2_DAG(graph_file,num_extra_edges,path_length):

	if path_length <= 0:
		print("no constraints on path length")
	else:
		print("path length: %d" % path_length)

	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = int)
	extra_edges = introduce_cycles(g,num_extra_edges,path_length = path_length)

	extra_edges_file = graph_file[:len(graph_file)-6] + "_extra_" + str(num_extra_edges) + "_path_len_" + str(path_length) + ".edges"
	graph_with_extra_edges_file = graph_file[:len(graph_file)-6] + "_graph_w_extra_" + str(num_extra_edges) + "_path_len_" + str(path_length) + ".edges"

	print("extra edges saved in: %s" % extra_edges_file)
	print("graph with extra edges saved in: %s" % graph_with_extra_edges_file)
	from file_io import write_pairs_to_file

	write_pairs_to_file(extra_edges,extra_edges_file)
	write_pairs_to_file(extra_edges + g.edges(),graph_with_extra_edges_file)	

	return (extra_edges_file,graph_with_extra_edges_file)
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-g","--graph_file",default= " ", help = "input graph file name (edges list) DAG")
	parser.add_argument("-k","--number",default = 100, type = int, help = "# extra edges added to the DAG")
	parser.add_argument("-l","--length",default = 0, type = int, help = "thresold d to control path length (<=0: no constraints on path length, otherwise less than this threshold)")
	args = parser.parse_args()
	
	graph_file = args.graph_file
	k = int(args.number)
	l = args.length

	print("graph_file %s " % graph_file)
	print("# extra edges: %d" % k)
	introduce_cycles_2_DAG(graph_file,k,l)

