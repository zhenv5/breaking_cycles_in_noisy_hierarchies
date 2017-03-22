import networkx as nx
import argparse
import os.path

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
	
def performance(graph_file,extra_edges_file):
	methods = ["dfs","pagerank","mfas","ensembling"]
	for method in methods:
		evaluation(graph_file,extra_edges_file,method)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--dir",default= " ", help = "directory to save files, such as data/ ")
	parser.add_argument("-n","--num_nodes",default= 300, type = int, help = "number of nodes")
	parser.add_argument("-m","--num_edges",default = 2500, type = int, help = "number of edges")
	parser.add_argument("-k","--num_extra_edges",default = 300, type = int, help = "# extra edges added to the DAG")
	parser.add_argument("-l","--path_length",default = 0, type = int, help = "thresold d to control path length (<=0: no constraints on path length, otherwise less than this threshold)")
	
	args = parser.parse_args()
	

	m = args.num_nodes 
	n = args.num_edges 
	k = args.num_extra_edges
	l = args.path_length

	graph_file = args.dir + "gnm_" + str(n) + "_" + str(m)+".edges"

	if not os.path.isfile(graph_file):
		from generate_random_dag import gnm_random_graph
		g = gnm_random_graph(n,m)
		from file_io import write_pairs_to_file
		write_pairs_to_file(g.edges(),graph_file)

	from introduce_cycles_to_DAG import introduce_cycles_2_DAG
	extra_edges_file,graph_with_extra_edges_file = introduce_cycles_2_DAG(graph_file,k,l)

	performance(graph_with_extra_edges_file,extra_edges_file)


