from datetime import datetime
import os.path
from helper_funs import dir_tail_name

def compute_social_agony_script(graph_file,output,agony_path = "agony/agony "):
	command = agony_path + graph_file + " " + output
	from helper_funs import run_command
	print("running command: %s" % command)
	start = datetime.now()
	run_command(command)
	end = datetime.now()
	time_used = end - start
	print("time used in computing social agony: %0.4f s" % (time_used.seconds))
	print("====compute agony done=====")

def compute_social_agony(graph_file,agony_path = "agony/agony "):
	
	dir_name,tail = dir_tail_name(graph_file)
	output = os.path.join(dir_name,tail.split(".")[0] + "_socialagony.txt")
	
	compute_social_agony_script(graph_file,output,agony_path = agony_path)
	from file_io import read_dict_from_file
	agony_score = read_dict_from_file(output)
	return agony_score

import argparse
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-g","--graph_file",default= " ", help = "input graph file name (edges list)")
	args = parser.parse_args()
	graph_file = args.graph_file
	compute_social_agony(graph_file)
	