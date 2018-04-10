import networkx as nx
import argparse

def evaluation(graph_file,gt_edges_file,method,nodetype = int):
	g = nx.read_edgelist(graph_file,create_using = nx.DiGraph(),nodetype = nodetype)
	if method == "dfs":
		from remove_cycle_edges_by_dfs import dfs_performance
		edges_to_be_removed = dfs_performance(graph_file,gt_edges_file,nodetype = nodetype)
	elif method == "mfas":
		from remove_cycle_edges_by_minimum_feedback_arc_set_greedy import mfas_performance
		mfas_performance(graph_file,gt_edges_file,nodetype = nodetype)
	elif method == "pagerank" or method == "ensembling" or method == "trueskill" or method == "socialagony":
		from remove_cycle_edges_by_hierarchy import breaking_cycles_by_hierarchy_performance
		breaking_cycles_by_hierarchy_performance(graph_file,gt_edges_file,method,nodetype = nodetype)
	
def break_cycles(graph_file,extra_edges_file = None,algorithm = "ensembling",nodetype = int):
	methods = ["dfs","pagerank","mfas","ensembling"]

	if algorithm == "all":
		for method in methods:
			evaluation(graph_file,extra_edges_file,method,nodetype = nodetype)
	else:
		evaluation(graph_file,extra_edges_file,algorithm,nodetype = nodetype)
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("-g","--graph_file",default= " ", help = "graph file to break cycles ")
	parser.add_argument("-t","--gt_edges_file",default= None, help = "ground truth of edges to be removed")
	parser.add_argument("-m","--method",default = "ensembling", help = "method to break cycles")
	parser.add_argument("-n","--node_type",default = "int", help = "graph node type")
	args = parser.parse_args()

	if args.node_type == "int":
		break_cycles(args.graph_file,args.gt_edges_file,args.method,nodetype = int)
	else:
		break_cycles(args.graph_file,args.gt_edges_file,args.method,nodetype = str)
