import itertools
import random
import math
import networkx as nx
import numpy as np
from networkx.generators.classic import  complete_graph

def gnm_random_graph(n, m, seed=None, directed=True):
	"""Return the random graph G_{n,m}.

    Produces a graph picked randomly out of the set of all graphs
    with n nodes and m edges.

    Parameters
    ----------
    n : int
        The number of nodes.
    m : int
        The number of edges.
    seed : int, optional
        Seed for random number generator (default=None).
    directed : bool, optional (default=False)
        If True return a directed graph
    """
	if directed:
		G=nx.DiGraph()
		g = nx.DiGraph()
	else:
		G=nx.Graph()
		g = nx.Graph()

	G.add_nodes_from(range(n))
	G.name="gnm_random_graph(%s,%s)"%(n,m)

	if seed is not None:
		random.seed(seed)

	if n==1:
		return G

	max_edges=n*(n-1)
	
	if not directed:
		max_edges/=2.0
	if m>=max_edges:
		return nx.complete_graph(n,create_using=G)

	nlist=G.nodes()
	edge_count=0
	while edge_count < m:
		# generate random edge,u,v
		u = random.choice(nlist)
		v = random.choice(nlist)
		if u>=v or G.has_edge(u,v):
			continue
		else:
			G.add_edge(u,v)
			edge_count = edge_count+1

	permutation = np.random.permutation(n)
	#print permutation
	new_edges = []
	for e in G.edges():
		u,v = e 
		new_edges.append((permutation[u],permutation[v]))
	g.add_edges_from(new_edges)
	print("is_directed_acyclic_graph: %s" % nx.is_directed_acyclic_graph(g))
	return g

import argparse
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-n","--num_nodes",default= 300, help = "number of nodes")
	parser.add_argument("-m","--num_edges",default = 1000,help = "number of edges")
	parser.add_argument("-g","--graph_file",default = " ", help = "saved to graph file")
	args = parser.parse_args()

	n = int(args.num_nodes)
	m = int(args.num_edges)
	graph_file = args.graph_file
	g = gnm_random_graph(n, m, seed=None, directed=True)
	nx.write_edgelist(g,graph_file,data = False)


