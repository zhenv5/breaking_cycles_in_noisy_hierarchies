import networkx as nx
from s_c_c import filter_big_scc
from s_c_c import get_big_sccs
from file_io import write_pairs_to_file
from file_io import read_dict_from_file
import os.path
import sys
sys.setrecursionlimit(5500000)


def get_agony(edge,players):
	u,v = edge 
	return max(players[u]-players[v],0)

def get_agonies(edges,players):
	edges_agony_dict = {}
	for edge in edges:
		edges_agony_dict[edge] = get_agony(edge,players)
	return edges_agony_dict

def remove_cycle_edges_by_agony(graph,players,edges_to_be_removed):
	
	pair_agony_dict = {}
	for pair in graph.edges():
		u,v = pair
		agony = max(players[u]-players[v],0)
		pair_agony_dict[pair] = agony
	from helper_funs import pick_from_dict
	pair_max_agony,agony = pick_from_dict(pair_agony_dict)

	edges_to_be_removed.append(pair_max_agony)
	#print("edge to be removed: %s, agony: %0.4f" % (pair_max_agony,max_agony))
	sub_graphs = filter_big_scc(graph,[pair_max_agony])
	if sub_graphs:
		num_subs = len(sub_graphs)
		for index,sub in enumerate(sub_graphs):
			#print("%d / %d scc: (%d,%d)" % (index+1,num_subs,sub.number_of_nodes(),sub.number_of_edges()))
			remove_cycle_edges_by_agony(sub,players,edges_to_be_removed)
	else:
		return None


def remove_cycle_edges_by_agony_iterately(sccs,players,edges_to_be_removed):
	while True:
		graph = sccs.pop()
		pair_max_agony = None
		max_agony = -1
		for pair in graph.edges():
			u,v = pair
			agony = max(players[u]-players[v],0)
			if agony >= max_agony:
				pair_max_agony = (u,v)
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

def scores_of_nodes_in_scc(sccs,players):
	from s_c_c import nodes_in_scc
	scc_nodes = nodes_in_scc(sccs)
	scc_nodes_score_dict = {}
	for node in scc_nodes:
		scc_nodes_score_dict[node] = players[node]
	#print("# scores of nodes in scc: %d" % (len(scc_nodes_score_dict)))
	return scc_nodes_score_dict

def scc_based_to_remove_cycle_edges_recursilvely(g,nodes_score):
	big_sccs = get_big_sccs(g)
	scc_nodes_score_dict = scores_of_nodes_in_scc(big_sccs,nodes_score)

	edges_to_be_removed = []
	for sub in big_sccs:
		scc_edges_to_be_removed = []
		remove_cycle_edges_by_agony(sub,scc_nodes_score_dict,scc_edges_to_be_removed)
		edges_to_be_removed += scc_edges_to_be_removed
	#print(" # edges to be removed: %d" % len(edges_to_be_removed))
	return edges_to_be_removed


def scc_based_to_remove_cycle_edges_iterately(g,nodes_score):
	from remove_self_loops import remove_self_loops_from_graph
	self_loops = remove_self_loops_from_graph(g)
	big_sccs = get_big_sccs(g)
	scc_nodes_score_dict = scores_of_nodes_in_scc(big_sccs,nodes_score)
	edges_to_be_removed = []
	if len(big_sccs) == 0:
		print("After removal of self loop edgs: %s" % nx.is_directed_acyclic_graph(g))
		return self_loops
	
	remove_cycle_edges_by_agony_iterately(big_sccs,scc_nodes_score_dict,edges_to_be_removed)
	#print(" # edges to be removed: %d" % len(edges_to_be_removed))
	return edges_to_be_removed+self_loops

def remove_cycle_edges(graph_file,players_score):
	return remove_cycle_edges_by_agony(graph_file,players_score)
