import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from recallPrecision import plotPrecisionRecallDiagram

def load_points(file_name):
	f = open(file_name,"r")
	points = []
	for l in f.readlines()[1:]:
		p = float(l.split()[2])
		r = float(l.split()[3])
		points.append((p,r))
	f.close()
	return points 


def draw_dbp_performance():
	labels = ["DFS","PR","MFAS","TS_G","TS_B","TS_F","SA_G","SA_B","SA_F","H_Voting"]
	title = "DBP-2014"
	data_file_name = ["dbpedia"]
	titles = ["DBP_2014","DBP_2014"]
	file_paths = []
	for d in data_file_name:
		file_paths.append("data/" + d + "/performance1.txt")
		file_paths.append("data/" + d + "/performance2.txt")
	for i,p in enumerate(file_paths):
		points = load_points(p)
		plotPrecisionRecallDiagram(title = titles[i],points = points,labels = labels, loc = "best" ,xy_ranges = [0,0.2,0,0.25], save_file = p[:len(p)-4] + "_" + titles[i]+".pdf")	

#draw_dbp_performance()
def draw_recall_precision():
	
	labels = ["DFS","PR","MFAS","TS_G","TS_B","TS_F","SA_G","SA_B","SA_F","H_Voting"]
	data_file_name = ["dbpedia/2014","dbpedia/201510","dbpedia/201604","web_google","wiki_vote","cit-Patents","arXiv","eu_email","taxonomy","gnu","wiki_talk","sx_stackoverflow"]
	titles = ["DBP_2014","DBP_2015","DBP_2016","Web_Google","Wiki_Vote","Cit-Patents","arXiv","EU-Email","NCBI-Taxo","Gnutella","Wiki_Talk","Stackoverflow_Q2A"]
	ranges_dict = {"dbp_2014":[0.7,0.9,0.8,0.9],"dbp_2015":[0.7,0.9,0.8,0.9],"dbp_2016":[0.7,0.9,0.8,0.9],
				"web_google":[0.62,0.72,0.6,0.8],"wiki_vote":[0.92,1,0.94,1],
				"cit-Patents":[0.4,0.95,0.55,0.95],"arXiv":[0.1,0.9,0.6,0.95],
				"EU-Email":[0.75,0.9,0.75,0.9],"NCBI-Taxo":[0.5,0.95,0.35,0.8]}
	legend_location_dict = {"NCBI-Taxo":"lower right","cit-Patents":"lower right","arXiv":"lower right","wiki_vote":"lower right"}
	file_paths = []
	for d in data_file_name:
		file_paths.append("data/" + d + "/performance.txt")
	for i,p in enumerate(file_paths):
		points = load_points(p)
		plotPrecisionRecallDiagram(title = titles[i],points = points,labels = labels, loc = legend_location_dict.get(titles[i],"lower right") ,xy_ranges = [0.2,1,0.2,1], save_file = p[:len(p)-4] + "_" + titles[i]+".pdf")

#draw_recall_precision()

def draw_recall_precision_core(data_file_names,titles):
	
	labels = ["DFS","PR","MFAS","TS_G","TS_B","TS_F","SA_G","SA_B","SA_F","H_Voting"]

	'''
	data_file_name = ["dbpedia/2014","dbpedia/201510","dbpedia/201604","web_google","wiki_vote","cit-Patents","arXiv","eu_email","taxonomy","gnu","wiki_talk","sx_stackoverflow"]
	titles = ["DBP_2014","DBP_2015","DBP_2016","Web_Google","Wiki_Vote","Cit-Patents","arXiv","EU-Email","NCBI-Taxo","Gnutella","Wiki_Talk","Stackoverflow_Q2A"]
	'''
	ranges_dict = {"dbp_2014":[0.7,0.9,0.8,0.9],"dbp_2015":[0.7,0.9,0.8,0.9],"dbp_2016":[0.7,0.9,0.8,0.9],
				"web_google":[0.62,0.72,0.6,0.8],"wiki_vote":[0.92,1,0.94,1],
				"cit-Patents":[0.4,0.95,0.55,0.95],"arXiv":[0.1,0.9,0.6,0.95],
				"EU-Email":[0.75,0.9,0.75,0.9],"NCBI-Taxo":[0.5,0.95,0.35,0.8]}
	
	legend_location_dict = {"NCBI-Taxo":"lower right","cit-Patents":"lower right","arXiv":"lower right","wiki_vote":"lower right"}
	
	'''
	file_paths = []
	for d in data_file_name:
		file_paths.append("data/" + d + "/performance.txt")
	'''
	for i,p in enumerate(data_file_names):
		points = load_points(p)
		plotPrecisionRecallDiagram(title = titles[i],points = points,labels = labels, loc = legend_location_dict.get(titles[i],"lower right") ,xy_ranges = [0.1,1,0.1,1], save_file = p[:len(p)-4] + "_" + titles[i]+".pdf")

def random_graphs():

	data_file_name = ["3K_15K","3K_30K","3K_45K","5K_25K","10K_50K","15K_75K","20K_100K","30K_150K","5K_50K","5K_75K","10K_100K","10K_150K"]
	file_paths = []
	for d in data_file_name:
		file_paths.append("data/random/" + d + "/performance.txt")
	titles = ["RG(3K,15K)","RG(3K,30K)","RG(3K,45K)","RG(5K,25K)","RG(10K,50K)","RG(15K,75K)","RG(20K,100K)","RG(30K,150K)","RG(5K,50K)","RG(5K,75K)","RG(10K,100K)","RG(10K,150K)"]
	draw_recall_precision_core(file_paths,titles)

random_graphs()
