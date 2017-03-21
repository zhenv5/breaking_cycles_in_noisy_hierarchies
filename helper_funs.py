import numpy as np

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