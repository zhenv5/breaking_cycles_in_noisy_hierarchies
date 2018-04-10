import networkx as nx

def remove_self_loops_from_graph(g):
	self_loops = list(g.selfloop_edges())
	g.remove_edges_from(self_loops)
	return self_loops

def remove_self_loops_from_edges_file(graph_file):
	g = nx.read_edgelist(args.original_graph, nodetype = int, create_using = nx.DiGraph())
	return remove_self_loops_from_graph(g)
