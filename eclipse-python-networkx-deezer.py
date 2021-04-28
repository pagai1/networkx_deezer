#!/usr/bin/python
# This script reads a edgelist of a deezer-database-extract
# 
import csv
import networkx as nx
import matplotlib.pyplot as plt
import time
import sys
import json


from builtins import len
from networkx.algorithms.coloring.greedy_coloring_with_interchange import Node
from networkx.classes.function import get_node_attributes
from networkx.readwrite import json_graph;
from _operator import itemgetter
from matplotlib.pyplot import plot

def to_ms(time):
    return ("%.3f" % time)

def save(G, fname):
        for u,v in G.edges():
            print("EDGES: ")
        time.sleep(2) 
        print(str(edges))
        
              #open(fname, 'w'), indent=2)

def load(fname):
    G = nx.DiGraph()
    d = json.load(open(fname))
    G.add_nodes_from(d['nodes'])
    G.add_edges_from(d['edges'])
    return G

def get_column_names(filereader):
  headers = next(filereader, None)
  return headers

def draw_graph(Graph):
    nx.draw_kamada_kawai(Graph,with_labels=True)
    plt.plot()
    plt.show()

def all_pairs_shortest_path(G):
    numberOfUsers = len(G.nodes())
    user_list = list(G.nodes())
    numberOfUsers = len(user_list)
    algoTime=time.time()
    paths = nx.all_pairs_shortest_path(G)
    runTime=(time.time() - algoTime)
    print(paths["1"]["23250"])
    print("RUNTIME AllPairsShortestPath - " + str(_limit).split("_")[1] + " eges - " + str(numberOfUsers) + " users : " + str(runTime) )

def draw_all_shortest_path_for_single_node(G, source):
    pos = nx.spring_layout(G)
    nx.draw(G,pos,node_color='k')
    paths_single = nx.single_source_shortest_path(G, source)
    path_edges = zip(paths_single,paths_single[1:])
    for path in paths_single:
        nx.draw_networkx_nodes(G,pos,nodelist=paths,node_color='r')
    nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color='r',width=10)
    plt.axis('equal')
    plt.show()
    runTime=(time.time() - algoTime)
    #print(paths_single)

def all_shortest_path_for_single_node(G, source):
    numberOfUsers = len(G.nodes())
    #print("NUMBER1 nodes: " + str(numberOfUsers))
    user_list = list(G.nodes())
#===============================================================================
# subgraph Returns a SubGraph view of the subgraph induced on nodes.
# The induced subgraph of the graph contains the nodes in nodes and the edges between those nodes.
#===============================================================================
    numberOfUsers = len(user_list)
    #print("NUMBER2 List: " + str(numberOfUsers))
    algoTime=time.time()
    #paths = nx.all_pairs_shortest_path(G)
    paths_single = nx.single_source_shortest_path(G, source)
    runTime=(time.time() - algoTime)
    #print(paths_single)
    print("RUNTIME ShortestPathsSingleNode for node " + source + " - " + str(_limit).split("_")[1] + " edges - " + str(numberOfUsers) + " other users : " + str(runTime) )

def algo_shortest_path(G):
    #user_list=[x for x,y in G.nodes(data=True)]
#===============================================================================
# subgraph Returns a SubGraph view of the subgraph induced on nodes.
# The induced subgraph of the graph contains the nodes in nodes and the edges between those nodes.
#===============================================================================
#    subG = G.subgraph(user_list)
#    for user1 in user_list:
#        print(user1)
    numberOfUsers = len(G.nodes())
    user_list = list(G.nodes())
    algoTime=time.time()
    #Lahm
#    for user1 in user_list:
#       #print("Example: Calculating shortest paths from " + user1 + " to anyone...\r")
#        for user2 in user_list:
#            if (user1 != user2):
#                try:
#                    path = nx.shortest_path(subG, source=(user1), target=user2)
#                except nx.NetworkXNoPath as e:
#                    path = e
#                except nx.NodeNotFound as e:
#                    path = e
    ### schnell
    i = 0
    pathcount = 0
    while i < numberOfUsers:
        user1 = user_list[i]
        #print("STARTNODE: " + user1)
        j = i + 1
        while j < numberOfUsers:
            pathcount = pathcount + 1
            user2 = user_list[j]
            
         #   print(user2)
            try:
                path = nx.shortest_path(G, source=(user1), target=user2)
            except nx.NetworkXNoPath as e:
                path = e
            except nx.NodeNotFound as e:
                path = e
            #print(path)
            j = j + 1 
    #print("RUNTIME : " + str(time.time() - start_time) )
            #print("PATH: " + str(path))
        i = i + 1
    print("RUNTIME ShortestPath - " + str(_limit).split("_")[1] + " entries - " + str(numberOfUsers) + " users : " + to_ms(time.time() - algoTime) + ". Checked " + str(pathcount) + " paths." )
        

limit = sys.argv[1]
if limit == None:
    print("GIVE AN ARGUMENT")
    sys.exit(1)
if limit != "all":
    _limit = "_" + str(limit)
    filepath='/home/pagai/graph-data/deezer_clean_data/RO_edges' + _limit + '.csv'
elif limit == "all":
# getting number of all entries in file
    filepath='/home/pagai/graph-data/deezer_clean_data/RO_edges.csv'
    _limit=0
    f = open(filepath, 'r')
    for line in f:
        _limit = _limit + 1
    _limit = "_" + str(_limit)         
    

# Loading headers

#header_reader = csv.reader(file)
#print(get_column_names(header_reader))

G = nx.Graph()
G = nx.read_edgelist(filepath, comments="no comments", delimiter=",", create_using=nx.Graph(), nodetype=str)
#draw_graph(G)

#edgelist = []
#nodelist = []
#edgelist = G.edges()
#nodelist = G.nodes()
#for edge in edgelist:
#    print(str(edge[0]) + " -- " + str(edge[1]))


############################# ALGOS




#algo_shortest_path(G)
#all_pairs_shortest_path(G)
draw_all_shortest_path_for_single_node(G,"1")
#all_shortest_path_for_single_node(G,"12")





