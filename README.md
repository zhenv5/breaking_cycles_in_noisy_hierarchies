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

```
method: dfs, # edges to be removed: 1357
method: dfs, accu: 0.0722, recall: 0.3267, f1: 0.1183
```
#### Breaking Cycles by MFAS

Local greedy implementation of Minimum feedback arc set problem.

```
python remove_cycle_edges_by_minimum_feedback_arc_set_greedy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges
```

You can specificity a edges list of file as ground truth (edges should be removed to break cycles)  by using '-t'. It will report precision, recall and F-1 score.

```
python remove_cycle_edges_by_minimum_feedback_arc_set_greedy.py -g data/gnm_300_2500_graph_w_extra_300_path_len_0.edges -t data/gnm_300_2500_extra_300_path_len_0.edges
```

Performance will be:

```
method: mfas, # edges to be removed: 459
method: mfas, accu: 0.5730, recall: 0.8767, f1: 0.6930
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

The performance will be:

```
method: pagerank Hiearchy_Greedy (H_G), # edges to be removed: 548
method: pagerank Hiearchy_Greedy (H_G), accu: 0.3759, recall: 0.6867, f1: 0.4858
method: pagerank Hiearchy_Forward(H_F), # edges to be removed: 606
method: pagerank Hiearchy_Forward(H_F), accu: 0.3597, recall: 0.7267, f1: 0.4812
method: pagerank Hiearchy_Backward (H_B), # edges to be removed: 767
method: pagerank Hiearchy_Backward (H_B), accu: 0.2816, recall: 0.7200, f1: 0.4049
method: pagerank Hiearchy_Voting (H_Voting), # edges to be removed: 573
method: pagerank Hiearchy_Voting (H_Voting), accu: 0.3647, recall: 0.6967, f1: 0.4788
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

```
method:  TrueSkill, Hiearchy_Greedy (H_G), # edges to be removed: 370
method:  TrueSkill, Hiearchy_Greedy (H_G), accu: 0.7054, recall: 0.8700, f1: 0.7791
method:  TrueSkill, Hiearchy_Forward(H_F), # edges to be removed: 448
method:  TrueSkill, Hiearchy_Forward(H_F), accu: 0.6049, recall: 0.9033, f1: 0.7246
method:  TrueSkill, Hiearchy_Backward (H_B), # edges to be removed: 452
method:  TrueSkill, Hiearchy_Backward (H_B), accu: 0.6040, recall: 0.9100, f1: 0.7261
method:  TrueSkill, Hiearchy_Voting (H_Voting:[TS_G,TS_F,TS_B]), # edges to be removed: 342
method:  TrueSkill, Hiearchy_Voting (H_Voting:[TS_G,TS_F,TS_B]), accu: 0.7485, recall: 0.8533, f1: 0.7975
```

##### Breaking Cycles via Hierarchy, inferred by SocialAgony

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

```
method:  SocialAgony, Hiearchy_Greedy (H_G), # edges to be removed: 337
method:  SocialAgony, Hiearchy_Greedy (H_G), accu: 0.7715, recall: 0.8667, f1: 0.8163
method:  SocialAgony, Hiearchy_Forward(H_F), # edges to be removed: 450
method:  SocialAgony, Hiearchy_Forward(H_F), accu: 0.5978, recall: 0.8967, f1: 0.7173
method:  SocialAgony, Hiearchy_Backward (H_B), # edges to be removed: 448
method:  SocialAgony, Hiearchy_Backward (H_B), accu: 0.6049, recall: 0.9033, f1: 0.7246
method:  SocialAgony, Hiearchy_Voting (H_Voting:[SA_G,SA_B,SA_F]), # edges to be removed: 327
method:  SocialAgony, Hiearchy_Voting (H_Voting:[SA_G,SA_B,SA_F]), accu: 0.7829, recall: 0.8533, f1: 0.8166
```

##### Breaking Cycles via Hierarchy, Ensembling

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

```
method:  SocialAgony, Hiearchy_Greedy (H_G), # edges to be removed: 337
method:  SocialAgony, Hiearchy_Greedy (H_G), accu: 0.7715, recall: 0.8667, f1: 0.8163
method:  SocialAgony, Hiearchy_Forward(H_F), # edges to be removed: 467
method:  SocialAgony, Hiearchy_Forward(H_F), accu: 0.5675, recall: 0.8833, f1: 0.6910
method:  SocialAgony, Hiearchy_Backward (H_B), # edges to be removed: 463
method:  SocialAgony, Hiearchy_Backward (H_B), accu: 0.5875, recall: 0.9067, f1: 0.7130
method:  SocialAgony, Hiearchy_Voting (H_Voting:[SA_G,SA_B,SA_F]), # edges to be removed: 332
method:  SocialAgony, Hiearchy_Voting (H_Voting:[SA_G,SA_B,SA_F]), accu: 0.7831, recall: 0.8667, f1: 0.8228


method:  TrueSkill, Hiearchy_Greedy (H_G), # edges to be removed: 370
method:  TrueSkill, Hiearchy_Greedy (H_G), accu: 0.7054, recall: 0.8700, f1: 0.7791
method:  TrueSkill, Hiearchy_Forward(H_F), # edges to be removed: 448
method:  TrueSkill, Hiearchy_Forward(H_F), accu: 0.6049, recall: 0.9033, f1: 0.7246
method:  TrueSkill, Hiearchy_Backward (H_B), # edges to be removed: 452
method:  TrueSkill, Hiearchy_Backward (H_B), accu: 0.6040, recall: 0.9100, f1: 0.7261
method:  TrueSkill, Hiearchy_Voting (H_Voting:[TS_G,TS_F,TS_B]), # edges to be removed: 342
method:  TrueSkill, Hiearchy_Voting (H_Voting:[TS_G,TS_F,TS_B]), accu: 0.7485, recall: 0.8533, f1: 0.7975


method: ensembling SocialAgony and TrueSkill (H_Voting:[SA_G,SA_B,SA_F,TS_G,TS_F,TS_B]), # edges to be removed: 335
method: ensembling SocialAgony and TrueSkill (H_Voting:[SA_G,SA_B,SA_F,TS_G,TS_F,TS_B]), accu: 0.7821, recall: 0.8733, f1: 0.8252
```