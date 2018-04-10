import networkx as nx
from s_c_c import filter_big_scc
from s_c_c import get_big_sccs
from file_io import write_pairs_to_file
from file_io import read_dict_from_file
#from network_functions import analysis_graph

def remove_cycle_edges_by_ranking_score_iterately(sccs,players,edges_to_be_removed,is_Forward):
	while True:
		graph = sccs.pop()
		node_scores_dict = {}
		for node in graph.nodes():
			node_scores_dict[node] = players[node]
		from helper_funs import pick_from_dict
		max_k,max_v,min_k,min_v = pick_from_dict(node_scores_dict,"both")

		#node_scores = [(node,players[node]) for node in graph.nodes_iter()]
		#sorted_node_scores = sorted(node_scores,key = lambda x: x[1])
	
		if is_Forward:
			node,score = max_k,max_v
			target_edges = [(node,v) for v in graph.successors(node)]
			#target_edges = [(v,node) for v in graph.predecessors_iter(node)]
		else:
			node,score = min_k,min_v
			#node,score = sorted_node_scores.pop()
			target_edges = [(v,node) for v in graph.predecessors(node)]
		
		'''
		from remove_cycle_edges_by_agony import get_agonies
		pair_agony_dict = get_agonies(target_edges,players)
		from helper_funs import pick_from_dict
		pair_max_agony,agony = pick_from_dict(pair_agony_dict)
		print("edge with max agony: %s, max agony: %0.4f" % (pair_max_agony,agony))
		target_edges = [pair_max_agony]
		'''

		edges_to_be_removed += target_edges
		graph.remove_edges_from(target_edges)

		sub_graphs = filter_big_scc(graph,target_edges)
		if sub_graphs:
			sccs += sub_graphs
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


def scc_based_to_remove_cycle_edges_iterately(g,nodes_score,is_Forward):
	big_sccs = get_big_sccs(g)
	if len(big_sccs) == 0:
		print("After removal of self loop edgs: %s" % nx.is_directed_acyclic_graph(g))
		return []
	scc_nodes_score_dict = scores_of_nodes_in_scc(big_sccs,nodes_score)
	edges_to_be_removed = []
	remove_cycle_edges_by_ranking_score_iterately(big_sccs,scc_nodes_score_dict,edges_to_be_removed,is_Forward)
	#print(" # edges to be removed: %d" % len(edges_to_be_removed))
	return edges_to_be_removed

def remove_cycle_edges_BF_iterately(g,players,is_Forward = True,score_name = "socialagony"):
	from remove_self_loops import remove_self_loops_from_graph
	self_loops = remove_self_loops_from_graph(g)
	edges_to_be_removed = scc_based_to_remove_cycle_edges_iterately(g,players,is_Forward)
	edges_to_be_removed = list(set(edges_to_be_removed))
	return edges_to_be_removed+self_loops

