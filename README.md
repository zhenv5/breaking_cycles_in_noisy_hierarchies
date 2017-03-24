#### Remove Cycle Edges  - Description

##### Requirements

* Python 2.7
* Lib: networkx
* Lib: TrueSkill

#### Generate Random Graphs (DAGs)

```
python generate_random_dag.py -n 300 -m 2500 -g data/gnm_300_2500.edges
```

* n: number of nodes
* m: number of edges 
* g: file path used to save the generated random graph

#### Introduce Cycles to DAG

```
python introduce_cycles_to_DAG.py -g data/gnm_300_2500.edges -k 300 -l 0
```
* -g:  target DAG edges list file 
* -k: number of extra edges introduced to make DAG have cycles 
* -l: threshold to control path length, if l <=0, no constraints on path length, else: path length < l (cycle length <= l)

output:
 
*  extra_edges_file (**Ground Truth Edges**): gnm_300_2500_extra_300_path_len_0.edges
*  graph_with_extra_edges_file : gnm_300_2500_graph_w_extra_300_path_len_0.edges

#### Breaking Cycles by DFS

```
python remove_cycle_edges_by_dfs.py -g gnm_300_2500_graph_w_extra_300_path_len_0.edges 
```

You can specificity a edges list of file as ground truth (edges should be removed to break cycles)  by using '-t'. It will report precision, recall and F-1 score.

```
python remove_cycle_edges_by_dfs.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -t data/gnm_300_2500_extra_300_path_len_0.edges
``` 

Performance will be:


#### Breaking Cycles by MFAS

Local greedy implementation of Minimum feedback arc set problem.

```
python remove_cycle_edges_by_minimum_feedback_arc_set_greedy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges
```

You can specificity a edges list of file as ground truth (edges should be removed to break cycles)  by using '-t'. It will report precision, recall and F-1 score.

```
python remove_cycle_edges_by_minimum_feedback_arc_set_greedy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -t data/gnm_300_2500_extra_300_path_len_0.edges
```

#### Breaking Cycles via Hierarchy, inferred by PageRank

Graph hierarchy is inferred from PageRank.

```
python remove_cycle_edges_by_hierarchy.py -s pagerank -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges
```

* -s pagerank: use pagerank to infer graph hierarchy

You can also specify the ground truth file path as ground_truth_edges_file by using '-t'

```
python remove_cycle_edges_by_hierarchy.py -s pagerank -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -t data/gnm_300_2500_extra_300_path_len_0.edges
```


#### Breaking Cycles via Hierarchy, inferred by TrueSkill

* Requirement: TrueSkill [install](http://trueskill.org/)

```
python remove_cycle_edges_by_hierarchy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -s trueskill
```

* -s trueskill: use TrueSkill to infer graph hierarchy

You can also specify the ground truth file path as ground_truth_edges_file by using '-t'.

```
python remove_cycle_edges_by_hierarchy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -s trueskill -t data/gnm_300_2500_extra_300_path_len_0.edges
```

It will report performance of TS_G, TS_B, TS_F, and TS_Voting (ensembling of TS_G, TS_B and TS_F).



#### Breaking Cycles via Hierarchy, inferred by SocialAgony

Social Agony code is from [Tatti](http://users.ics.aalto.fi/ntatti/software.shtml)

The source code has been put in /agony. You have to compile it first. 

After that run:

```
python remove_cycle_edges_by_hierarchy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -s socialagony
```

* -s socialagony: use SocialAgony to infer graph hierarchy

You can also specify the ground truth file path as ground_truth_edges_file by using '-t'.

```
python remove_cycle_edges_by_hierarchy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -s socialagony -t data/gnm_300_2500_extra_300_path_len_0.edges
```

It will report performance of SA_G, SA_B, SA_F, and SA_Voting (ensembling of SA_G, SA_B and SA_F).


#### Breaking Cycles via Hierarchy, Ensembling

Ensembling TS_G, TS_B, TS_F, SA_G, SA_B and SA_F.

```
python remove_cycle_edges_by_hierarchy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -s ensembling
```

* -s ensembling: ensembling all 6 apprpaches

You can also specify the ground truth file path as ground_truth_edges_file by using '-t'. 


```
python remove_cycle_edges_by_hierarchy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -s ensembling -t data/gnm_300_2500_extra_300_path_len_0.edges
```

* **This can also report performances of TS_G, TS_B, TS_F, SA_G, SA_B and SA_F individually**, these performance may have slightly difference with running them individually. 
* It can report performance of H_Voting (ensembling of SA_G, SA_B, SA_F, TS_G, TS_B and TS_F)

#### Test on Synthetic Graphs

Instead of testing above methods individually, you can simply run below code to compare performance of all methods on Synthetic Graphs (random generated graphs).

```
python synthetic_performance.py --dir data/ -m 350 -n 5000 -k 500 -l 0

```

* --dir: directory to save all results, 'data/' is in current directory
* -n: number of nodes in the generated random graph
* -m: number of edges in the generated random graph 
* -k: number of extra edges to introduce cycles to the generated random graph 
* -l: control parameter of path length

It will do: 

* generate a random DAG with n nodes and m edges
* introduce k extra edges to this DAG to make it have cycles (l is used to control generated cycle size, if l == 0, it has no constraints on cycle size)
* run all methods to break cycles and report performance

It will output such as:


```
**********************
**********************
method: dfs, # edges to be removed: 2938
method: dfs, precision: 0.0514, recall: 0.3020, f1: 0.0878
**********************
**********************
method: pagerank Hiearchy_Greedy (H_G), # edges to be removed: 1153
method: pagerank Hiearchy_Greedy (H_G), precision: 0.3452, recall: 0.7960, f1: 0.4815
**********************
**********************
method: pagerank Hiearchy_Forward(H_F), # edges to be removed: 1283
method: pagerank Hiearchy_Forward(H_F), precision: 0.3188, recall: 0.8180, f1: 0.4588
**********************
**********************
method: pagerank Hiearchy_Backward (H_B), # edges to be removed: 1386
method: pagerank Hiearchy_Backward (H_B), precision: 0.2929, recall: 0.8120, f1: 0.4305
**********************
**********************
method: pagerank Hiearchy_Voting (H_Voting), # edges to be removed: 1079
method: pagerank Hiearchy_Voting (H_Voting), precision: 0.3624, recall: 0.7820, f1: 0.4953
**********************
**********************
method: mfas, # edges to be removed: 774
method: mfas, precision: 0.6008, recall: 0.9300, f1: 0.7300
**********************
**********************
method:  SocialAgony, SA_G, # edges to be removed: 602
method:  SocialAgony, SA_G, precision: 0.7608, recall: 0.9160, f1: 0.8312
**********************
**********************
method:  SocialAgony, SA_F, # edges to be removed: 837
method:  SocialAgony, SA_F, precision: 0.5556, recall: 0.9300, f1: 0.6956
**********************
**********************
method:  SocialAgony, SA_B, # edges to be removed: 814
method:  SocialAgony, SA_B, precision: 0.5627, recall: 0.9160, f1: 0.6971
**********************
**********************
method:  SocialAgony, SA_Voting:([SA_G,SA_B,SA_F]), # edges to be removed: 594
method:  SocialAgony, SA_Voting:([SA_G,SA_B,SA_F]), precision: 0.7727, recall: 0.9180, f1: 0.8391
**********************
**********************
method:  TrueSkill,  TS_G, # edges to be removed: 587
method:  TrueSkill,  TS_G, precision: 0.7819, recall: 0.9180, f1: 0.8445
**********************
**********************
method:  TrueSkill, TS_F, # edges to be removed: 735
method:  TrueSkill, TS_F, precision: 0.6463, recall: 0.9500, f1: 0.7692
**********************
**********************
method:  TrueSkill, TS_B, # edges to be removed: 750
method:  TrueSkill, TS_B, precision: 0.6293, recall: 0.9440, f1: 0.7552
**********************
**********************
method:  TrueSkill, TS_Voting:([TS_G,TS_F,TS_B]), # edges to be removed: 579
method:  TrueSkill, TS_Voting:([TS_G,TS_F,TS_B]), precision: 0.8031, recall: 0.9300, f1: 0.8619
**********************
**********************
method: ensembling SocialAgony and TrueSkill (H_Voting:[SA_G,SA_B,SA_F,TS_G,TS_F,TS_B]), # edges to be removed: 565
method: ensembling SocialAgony and TrueSkill (H_Voting:[SA_G,SA_B,SA_F,TS_G,TS_F,TS_B]), precision: 0.8230, recall: 0.9300, f1: 0.8732
**********************
```

#### Test on Real Datasets

If you already have a graph with cycles, you can run:

```
python break_cycles.py -g data/test/gnm_300_1500_graph_w_extra_200_path_len_0.edges
```

* -g data/test/gnm_300_1500_graph_w_extra_200_path_len_0.edges : to specify edgeslist file

And if you have ground truth, you can run below commands to report performances:


```
python break_cycles.py -g data/test/gnm_300_1500_graph_w_extra_200_path_len_0.edges -t data/test/gnm_300_1500_extra_200_path_len_0.edges 
```

* -t data/test/gnm_300_1500_extra_200_path_len_0.edges   : to specify ground truth of edges to be removed
