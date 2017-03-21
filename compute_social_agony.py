from datetime import datetime

def compute_social_agony_script(graph_file,output,agony_path = "agony/agony "):
	#if is_local:
	#	command = "/home/sunjiank/Dropbox/Codes/agony/agony "
	#else:
	#	command = "~/Codes/agony/agony "
	command = agony_path + graph_file + " " + output
	from script import run_command
	print("running command: %s" % command)
	start = datetime.now()
	run_command(command)
	end = datetime.now()
	time_used = end - start
	print("time used in computing social agony: %0.4f s" % (time_used.seconds))
	print("====compute agony done=====")
def compute_social_agony(graph_file,agony_path = "agony/agony "):
	output = graph_file[:len(graph_file)-6] + "_rank.txt"
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
	compute_social_agony(graph_file,is_local = False)
	