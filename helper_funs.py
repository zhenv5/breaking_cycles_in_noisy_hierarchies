import numpy as np
import subprocess
import os 


def dir_tail_name(file_name):
	import os.path
	dir_name = os.path.dirname(file_name)
	head, tail = os.path.split(file_name)
	print("dir name: %s, file_name: %s" % (dir_name,tail))
	return dir_name,tail


def run_command(command,is_print = False):
	print command
	p = subprocess.Popen(command,shell = True, stdout = subprocess.PIPE)
	o = p.communicate() 
	if is_print:
		print o[0]


def normalize_dict(d,method = "min_max"):
	values = d.values()
	if method == "min_max":
		min_v = min(values)
		max_v = max(values)
		return {key:(value - min_v)*1.0/(max_v - min_v) for key,value in d.iteritems()}
	elif method == "z_score":
		mean = np.mean(values)
		std = np.std(values)
		return {key:(value - mean)*1.0/(std) for key,value in d.iteritems()}



def pick_from_dict(d, order = "max"):
	min_k, min_v = 0, 10000

	min_items = []
	max_k, max_v=  0, -10000
	
	max_items = []
	for k,v in d.iteritems():
		if v > max_v:
			max_v = v
			max_items = [(k,max_v)] 
		elif v == max_v:
			max_items.append((k,v))

		if v < min_v:
			min_v = v
			min_items = [(k,min_v)]
		elif v == min_v:
			min_items.append((k,v))

	max_k,max_v = pick_randomly(max_items)
	min_k,min_v = pick_randomly(min_items)

	if order == "max":
		return max_k,max_v
	if order == "min":
		return min_k,min_v
	else:
		return max_k,max_v,min_k,min_v


def pick_randomly(source):
	np.random.shuffle(source)
	np.random.shuffle(source)
	np.random.shuffle(source)
	return source[0]
