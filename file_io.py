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