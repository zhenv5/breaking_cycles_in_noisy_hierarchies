import pickle
def read_from_pickle(pickle_file):
	try:
		with open(pickle_file,"rb") as f:
			print("File loaded from: %s" % pickle_file)
			output = pickle.load(f)
		return output
	except Exception as e:
		print("******Exception: %s" % e)
		return {}

def write_dict_to_file(data_dict,output_file):
	tuple_list = [(k,v) for k,v in data_dict.iteritems()]
	write_pairs_to_file(tuple_list,output_file)

def write_pairs_to_file(edges_list,edges_list_file):
	f = open(edges_list_file, 'w')
	for e in edges_list:
		u,v = e
		f.write(str(u) + " " + str(v) + " \n")
	f.close()
	
def write_edges_to_file(edges_list,edges_list_file):
	write_pairs_to_file(edges_list,edges_list_file)

def write_set_to_txt(output,output_file):
	with open(output_file,"w") as f:
		for k in output:
			f.write(str(k) + "\n")

def write_dict_to_txt(output,output_file):
	with open(output_file,"w") as f:
		for k,v in output.iteritems():
			f.write(str(k) + " " + str(v) + " \n")


def write_to_pickle(output_pickle,output_file):
	with open(output_file,"wb") as f:
		print("File saved to: %s" % output_file)
		pickle.dump(output_pickle,f)

def read_pairs_from_file(edges_list_file,first_type = int, second_type = int):
	try:
		edges = []
		f = open(edges_list_file, 'r')
		for line in f:
			elements = line.split()
			s = elements[0]
			t = elements[1]
			s = first_type(s)
			t = second_type(t)
			edges.append((s,t))
		return edges
	except Exception as e:
		return []

	
def read_edges_from_file(edges_list_file,first_type = int, second_type = int):
	return read_pairs_from_file(edges_list_file,first_type = int, second_type = int)


def reverse_edges(edges_list_file,output_file = None,first_type = int, second_type = int):
	edges = read_edges_from_file(edges_list_file,first_type = first_type,second_type = second_type)
	new_edges = [ (v,u) for (u,v) in edges]
	if output_file:
		write_edges_to_file(new_edges,output_file)
	return new_edges
#reverse_edges("data/sx_stackoverflow/sx_stackoverflow_a2q.edges",output_file = "data/sx_stackoverflow/sx_stackoverflow_q2a.edges")


def read_dict_from_file(file_name,key_type = int, value_type = int):
	input_file = open(file_name,"r")
	d = {}
	for line in input_file.readlines():
		k,v = line.split()
		if (key_type is not None) and (value_type is not None):
			try:
				k=key_type(k)
				v=value_type(v)
				d[k] = v
			except Exception as e:
				print e 
	return d


def read_dict_from_csv(file_name,key_type = int,value_type = int,key_index = 0, value_index = 1):
	import pandas as pd
	df = pd.read_csv(file_name,sep = ",")
	d = {}
	for k,v in zip(df.iloc[:,key_index],df.iloc[:,value_index]):
		try:
			k = key_type(k)
			v = key_type(v)
			d[k] = v
		except Exception as e:
			pass
	return d

def read_dict_list_from_csv(file_name,key_type = int, value_type = int, key_index = 0, value_index = 1):
	import pandas as pd
	df = pd.read_csv(file_name,sep = ",")
	d = {}
	for k,v in zip(df.iloc[:,key_index],df.iloc[:,value_index]):
		k = key_type(k)
		v = key_type(v)
		if k in d:
			d[k] = d[k] + [v]
		else:
			d[k] = [v]
	return d



def switch_key_value_dict_list(d):
	new_d = {}
	for k,v in d.iteritems():
		if v in new_d:
			new_d[v] += [k]
		else:
			new_d[v] = [k]
	return new_d

def switch_key_value_dict_value(d):
	new_d = {}
	for k,v in d.iteritems():
		new_d[v] = k
	return new_d



def read_dict_pair_from_csv(file_name,key_type = int, value_type = int):
	import pandas as pd
	df = pd.read_csv(file_name,sep = ",")
	d = {}
	for k,v,days in zip(df.iloc[:,1],df.iloc[:,0],df.iloc[:,2]):
		k = key_type(k)
		v = value_type(v)
		if k in d:
			d[k].append((v,days))
		else:
			d[k] = [(v,days)]
	for k,v in d.iteritems():
		v = sorted(v,key = lambda x: x[1])
		d[k] =v
	return d 

def read_dict_pair_from_csv_2(file_name,key_type = int, value_type = int):
	import pandas as pd
	df = pd.read_csv(file_name,delim_whitespace = True)
	d = {}
	for k,v,simi in zip(df.iloc[:,0],df.iloc[:,1],df.iloc[:,2]):
		k = key_type(k)
		v = value_type(v)
		if k in d:
			d[k] = d[k] + [(v,simi)]
		else:
			d[k] = [(v,simi)]
	for k,v in d.iteritems():
		v = sorted(v,key = lambda x: x[1],reverse = True)
		d[k] =v
	return d 