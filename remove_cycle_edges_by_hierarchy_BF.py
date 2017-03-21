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
		for node in graph.nodes_iter():
			node_scores_dict[node] = players[node]
		from helper_funs import pick_from_dict
		max_k,max_v,min_k,min_v = pick_from_dict(node_scores_dict,"both")

		#node_scores = [(node,players[node]) for node in graph.nodes_iter()]
		#sorted_node_scores = sorted(node_scores,key = lambda x: x[1])
	
		if is_Forward:
			node,score = max_k,max_v
			target_edges = [(node,v) for v in graph.successors_iter(node)]
			#target_edges = [(v,node) for v in graph.predecessors_iter(node)]
		else:
			node,score = min_k,min_v
			#node,score = sorted_node_scores.pop()
			target_edges = [(v,node) for v in graph.predecessors_iter(node)]
		
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
	scc_nodes_score_dict = scores_of_nodes_in_scc(big_sccs,nodes_score)
	edges_to_be_removed = []
	remove_cycle_edges_by_ranking_score_iterately(big_sccs,scc_nodes_score_dict,edges_to_be_removed,is_Forward)
	#print(" # edges to be removed: %d" % len(edges_to_be_removed))
	return edges_to_be_removed

def remove_cycle_edges_BF_iterately(g,players,is_Forward = True,score_name = "socialagony"):
	edges_to_be_removed = scc_based_to_remove_cycle_edges_iterately(g,players,is_Forward)
	edges_to_be_removed = list(set(edges_to_be_removed))
	return edges_to_be_removed

'''
def remove_cycle_edges_BF(graph_file,players_score_file,is_Forward = True,score_name = "socialagony"):
	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = int)
	players = read_dict_from_file(players_score_file,key_type = int, value_type = float)
	edges_to_be_removed = remove_cycle_edges_BF_iterately(g,players,is_Forward = is_Forward,score_name = score_name)
	g.remove_edges_from(edges_to_be_removed)
	edges_to_be_removed_file = graph_file[:len(graph_file)-6] + "_removed_by_" + score_name + "_is_forward_" + str(is_Forward) + "_greedy.edges"
	write_pairs_to_file(edges_to_be_removed,edges_to_be_removed_file)
	print("after removal of cycle edges: %d" % len(edges_to_be_removed))
	analysis_graph(g)
	import random 
	index = random.randint(0, len(edges_to_be_removed)-1)
	g.add_edges_from([edges_to_be_removed[index]])
	print("analysis of graph after adding an edge back")
	analysis_graph(g)
	g.remove_edges_from([edges_to_be_removed[index]])
	#print edges_to_be_removed
	return edges_to_be_removed

import argparse
if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("-g","--graph_file",default= "data/dbpedia/dbpedia_2014_c_2_p_edges.edges", help = "input graph file name (edges list)")
	parser.add_argument("-s","--score",default = "data/dbpedia/dbpedia_2014_c_2_p_edges_rank.txt",help = "nodes score file")
	parser.add_argument("-n","--name",default = "socialagony",help = "score function name")
	args = parser.parse_args()
	graph_file = args.graph_file
	players_score = args.score
	score_name = args.name
	print("graph_file %s " % graph_file)
	print("score funtion: %s" % players_score)
	print("score function name: %s" % score_name)
	#remove_cycle_edges_BF(graph_file,players_score,is_Forward = True,score_name = score_name)
	remove_cycle_edges_BF(graph_file,players_score,is_Forward = False,score_name = score_name)

'''