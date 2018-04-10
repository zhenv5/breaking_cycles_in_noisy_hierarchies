import networkx as nx
from remove_cycle_edges_by_hierarchy_greedy import scc_based_to_remove_cycle_edges_iterately
from remove_cycle_edges_by_hierarchy_BF import remove_cycle_edges_BF_iterately
from remove_cycle_edges_by_hierarchy_voting import remove_cycle_edges_heuristic
from measures import F1
from file_io import read_dict_from_file
from file_io import write_pairs_to_file
	
def get_edges_voting_scores(set_edges_list):
	total_edges = set()
	for edges in set_edges_list:
		total_edges = total_edges | edges
	edges_score = {}
	for e in total_edges:
		edges_score[e] = len(filter(lambda x: e in x, set_edges_list))
	return edges_score


def remove_cycle_edges_strategies(graph_file,nodes_score_dict,score_name = "socialagony", nodetype = int):


	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = nodetype)
	# greedy
	e1 = scc_based_to_remove_cycle_edges_iterately(g,nodes_score_dict)
	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = nodetype)
	# forward
	e2 = remove_cycle_edges_BF_iterately(g,nodes_score_dict,is_Forward = True,score_name = score_name)
	# backward
	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = nodetype)
	e3 = remove_cycle_edges_BF_iterately(g,nodes_score_dict,is_Forward = False,score_name = score_name)
	return e1,e2,e3

def remove_cycle_edges_by_voting(graph_file,set_edges_list,nodetype = int):
	edges_score = get_edges_voting_scores(set_edges_list)
	e = remove_cycle_edges_heuristic(graph_file,edges_score,nodetype = nodetype)
	return e 

def remove_cycle_edges_by_hierarchy(graph_file,nodes_score_dict,score_name = "socialagony",nodetype = int):
	e1,e2,e3 = remove_cycle_edges_strategies(graph_file,nodes_score_dict,score_name = score_name,nodetype = nodetype)
	e4 = remove_cycle_edges_by_voting(graph_file,[set(e1),set(e2),set(e3)],nodetype = nodetype)
	return e1,e2,e3,e4

def computing_hierarchy(graph_file,players_score_func_name, nodetype = int):
	import os.path
	if players_score_func_name == "socialagony":
		from helper_funs import dir_tail_name
		dir_name,tail = dir_tail_name(graph_file)
		agony_file = os.path.join(dir_name,tail.split(".")[0] + "_socialagony.txt")
		#agony_file = graph_file[:len(graph_file)-6] + "_socialagony.txt"
		#from compute_social_agony import compute_social_agony
		#players = compute_social_agony(graph_file,agony_path = "agony/agony ")		
		if False:
		#if os.path.isfile(agony_file):
			print("load pre-computed socialagony from: %s" % agony_file)
			players = read_dict_from_file(agony_file)
		else:
			print("start computing socialagony...")
			from compute_social_agony import compute_social_agony
			players = compute_social_agony(graph_file,agony_path = "agony/agony ")
			print("write socialagony to file: %s" % agony_file)
		return players
	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = nodetype)
	if players_score_func_name == "pagerank":
		#print("computing pagerank...")
		players = nx.pagerank(g, alpha = 0.85)
		return players
	elif players_score_func_name == "trueskill":
		output_file = graph_file[:len(graph_file)-6] + "_trueskill.txt"
		output_file_2 = graph_file[:len(graph_file)-6] + "_trueskill.pkl"
		#from true_skill import graphbased_trueskill
		#players = graphbased_trueskill(g)
		#from file_io import write_dict_to_file
		#write_dict_to_file(players,output_file)
		
		'''
		if os.path.isfile(output_file):
			print("load pre-computed trueskill from: %s" % output_file)
			players = read_dict_from_file(output_file,key_type = int, value_type = float)
		elif os.path.isfile(output_file_2):
			print("load pre-computed trueskill from: %s" % output_file_2)
			players = read_from_pickle(output_file_2)			
		'''
		if True:
			print("start computing trueskill...")
			from true_skill import graphbased_trueskill
			players = graphbased_trueskill(g)
			from file_io import write_dict_to_file
			print("write trueskill to file: %s" % output_file)
			write_dict_to_file(players,output_file)
		
		return players

def breaking_cycles_by_hierarchy_performance(graph_file,gt_file,players_score_name,nodetype = int):
	
	from measures import report_performance
	if players_score_name != "ensembling":
		players_score_dict  = computing_hierarchy(graph_file,players_score_name,nodetype = nodetype)
		e1,e2,e3,e4 = remove_cycle_edges_by_hierarchy(graph_file,players_score_dict,players_score_name,nodetype = nodetype)
		
		if players_score_name == "pagerank":
			report_performance(gt_file,e1,"PR")
			return

		if players_score_name == "socialagony":
			note = "SA_"
		elif players_score_name == "trueskill":
			note = "TS_"

		report_performance(gt_file,e1, note+"G")
		report_performance(gt_file,e2, note+"F")
		report_performance(gt_file,e3, note+"B")
		report_performance(gt_file,e4, note+"Voting")
	else:
		players_score_dict  = computing_hierarchy(graph_file,"socialagony",nodetype = nodetype)
		e1,e2,e3,e4 = remove_cycle_edges_by_hierarchy(graph_file,players_score_dict,"socialagony",nodetype = nodetype)
		report_performance(gt_file,e1,  "SA_G")
		write_pairs_to_file(e1,graph_file[:len(graph_file)-6] + "_removed_by_SA-G.edges")
		report_performance(gt_file,e2,  "SA_F")
		write_pairs_to_file(e2,graph_file[:len(graph_file)-6] + "_removed_by_SA-F.edges")
		report_performance(gt_file,e3,  "SA_B")
		write_pairs_to_file(e3,graph_file[:len(graph_file)-6] + "_removed_by_SA-B.edges")
		report_performance(gt_file,e4,  "SA_Voting")
		write_pairs_to_file(e4,graph_file[:len(graph_file)-6] + "_removed_by_SA-Voting.edges")

		players_score_dict  = computing_hierarchy(graph_file,"trueskill",nodetype = nodetype)
		e5,e6,e7,e8 = remove_cycle_edges_by_hierarchy(graph_file,players_score_dict,"trueskill",nodetype = nodetype)
		report_performance(gt_file,e5,  "TS_G")
		write_pairs_to_file(e5,graph_file[:len(graph_file)-6] + "_removed_by_TS-G.edges")
		report_performance(gt_file,e6,  "TS_F")
		write_pairs_to_file(e6,graph_file[:len(graph_file)-6] + "_removed_by_TS-F.edges")
		report_performance(gt_file,e7,  "TS_B")
		write_pairs_to_file(e7,graph_file[:len(graph_file)-6] + "_removed_by_TS-B.edges")
		report_performance(gt_file,e8,  "TS_Voting")
		write_pairs_to_file(e7,graph_file[:len(graph_file)-6] + "_removed_by_TS-Voting.edges")

		e9 = remove_cycle_edges_by_voting(graph_file,[set(e1),set(e2),set(e3),set(e5),set(e6),set(e7)],nodetype = nodetype)
		report_performance(gt_file,e9,"H_Voting")
		write_pairs_to_file(e9,graph_file[:len(graph_file)-6] + "_removed_by_H-Voting.edges")



import argparse
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-g","--graph_file",default= " ", help = "input graph file name (edges list)")
	parser.add_argument("-s","--score_name",default = "pagerank",help = "nodes score function: trueskill, socialagony, ensembling, pagerank...")
	parser.add_argument("-t","--gt_edges_file",default = None, help = "ground truth edges file")
	
	args = parser.parse_args()
	graph_file = args.graph_file
	players_score_name = args.score_name
	gt_file = args.gt_edges_file

	breaking_cycles_by_hierarchy_performance(graph_file,gt_file,players_score_name)
	
