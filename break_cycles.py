import networkx as nx
import argparse

def evaluation(graph_file,gt_edges_file,method):
	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = int)
	if method == "dfs":
		from remove_cycle_edges_by_dfs import dfs_performance
		edges_to_be_removed = dfs_performance(graph_file,gt_edges_file)
	elif method == "mfas":
		from remove_cycle_edges_by_minimum_feedback_arc_set_greedy import mfas_performance
		mfas_performance(graph_file,gt_edges_file)
	elif method == "pagerank" or method == "ensembling" or method == "trueskill" or method == "socialagony":
		from remove_cycle_edges_by_hierarchy import breaking_cycles_by_hierarchy_performance
		breaking_cycles_by_hierarchy_performance(graph_file,gt_edges_file,method)
	
def break_cycles(graph_file,extra_edges_file = None):
	methods = ["dfs","pagerank","mfas","ensembling"]
	for method in methods:
		evaluation(graph_file,extra_edges_file,method)


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("-g","--graph_file",default= " ", help = "graph file to break cycles ")
	parser.add_argument("-t","--gt_edges_file",default= None, help = "ground truth of edges to be removed")

	args = parser.parse_args()

	break_cycles(args.graph_file,args.gt_edges_file)