import networkx as nx
from s_c_c import filter_big_scc
from s_c_c import get_big_sccs
from file_io import write_pairs_to_file
from file_io import read_dict_from_file
import os.path

def remove_cycle_edges_by_agony_iterately(sccs,edges_score,edges_to_be_removed):
	while True:
		graph = sccs.pop()
		pair_max_agony = None
		max_agony = -1
		for pair in graph.edges():
			agony = edges_score.get(pair,0)
			if agony >= max_agony:
				pair_max_agony = pair
				max_agony = agony
		edges_to_be_removed.append(pair_max_agony)
		#print("graph: (%d,%d), edge to be removed: %s, agony: %0.4f" % (graph.number_of_nodes(),graph.number_of_edges(),pair_max_agony,max_agony))
		graph.remove_edges_from([pair_max_agony])
		#print("graph: (%d,%d), edge to be removed: %s" % (graph.number_of_nodes(),graph.number_of_edges(),pair_max_agony))
		sub_graphs = filter_big_scc(graph,[pair_max_agony])
		if sub_graphs:
			for index,sub in enumerate(sub_graphs):
				sccs.append(sub)
		if not sccs:
			return

def scc_based_to_remove_cycle_edges_iterately(g,edges_score):
	big_sccs = get_big_sccs(g)
	if len(big_sccs) == 0:
		print("After removal of self loop edgs: %s" % nx.is_directed_acyclic_graph(g))
		return []
	edges_to_be_removed = []
	remove_cycle_edges_by_agony_iterately(big_sccs,edges_score,edges_to_be_removed)
	#print(" # edges to be removed: %d" % len(edges_to_be_removed))
	return edges_to_be_removed

def remove_cycle_edges_heuristic(graph_file,edges_score,nodetype = int):
	
	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = nodetype)

	from remove_self_loops import remove_self_loops_from_graph
	self_loops = remove_self_loops_from_graph(g)

	edges_to_be_removed = scc_based_to_remove_cycle_edges_iterately(g,edges_score)
	edges_to_be_removed = list(set(edges_to_be_removed))
	return edges_to_be_removed+self_loops
