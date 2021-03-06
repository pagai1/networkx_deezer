#!/usr/bin/python
# This script reads a edgelist of a deezer-database-extract
# 
import csv
import networkx as nx
import matplotlib.pyplot as plt
import time
import json
import signal

# import own helper-modules
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),"../../networkx_modules")))
from helpers.generalStuff import *
from helpers.networkx_load_n_save import *
from helpers.search_functions import *
from algoPackage.pageRank import *
from algoPackage.simRank import *
from algoPackage.hits import *
from algoPackage.shortestPath import *
from algoPackage.jaccard_coefficient import *
from algoPackage.degree_centrality import *

from builtins import len
from networkx.algorithms.coloring.greedy_coloring_with_interchange import Node
from networkx.classes.function import get_node_attributes
from networkx.readwrite import json_graph;
from _operator import itemgetter
from matplotlib.pyplot import plot

#def to_ms(time):
#    return ("%.3f" % time)

def cleanupAll(tmpfilepath):
    print("CLEANING UP.")
    os.remove(tmpfilepath)

def get_column_names(filereader):
  headers = next(filereader, None)
  return headers

def draw_graph(Graph):
    nx.draw_kamada_kawai(Graph,with_labels=True)
    plt.plot()
    plt.show()

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


#
# MAIN
#
#
#filepath='/home/pagai/graph-data/deezer_clean_data/both.csv'    
filepath='/home/pagai/graph-data/pokec/soc-pokec-relationships_weighted.txt'
tmpfilepath = "/tmp/tmpfile.csv" # Limiting the lines is not possible with read_weighted_edgelist. So introduced tempfile with line-extract to use read_weighted_edgelist for that file. 
limit = 0
seclimit=1
operatorFunction="eq"
verbose=False
doExport=False
createByImport=False
importExportFileName = "/tmp/node_link_data_export_Kantenliste.json"

doAlgo=True
doAlgoPageRankTest=False
doAlgoShortestPath=True
doDegreeCentrality=False
doSimRank=False
doHITS=False
algoVerbose=False

operatorFunction="eq"
drawit=False

deleteTest=False
testGetAll=False
testSearch=False



#catchable_sigs = set(signal.Signals) - {signal.SIGKILL, signal.SIGSTOP}
#for sig in catchable_sigs:
#    signal.signal(sig, tmpfilepath)  # Substitute handler of choice for `print`


if (len(sys.argv) == 1):
    if (verbose):
        print("NOTHING WAS GIVEN")
    limit = "all"
elif (len(sys.argv) == 2):
    limit = sys.argv[1]
    if (verbose):
        print("LOADING " + str(limit) + " LINES ")
elif (len(sys.argv) == 3):
    limit = sys.argv[1] 
    seclimit = sys.argv[2]
    if (verbose):
        print("LOADING " + str(limit) + " LINES AND " + str(seclimit) + " DEGREE.")
elif (len(sys.argv) == 4):    
    limit = sys.argv[1] 
    seclimit = int(sys.argv[2])
    operatorFunction=sys.argv[3]
    if (verbose):
        print("LOADING " + str(limit) + " LINES AND DEGREE " + operatorFunction + " " + str(seclimit))    

if limit != "all":
    cleanup = True
# get number of lines of file
    with open(filepath) as f:
        allLines = [next(f) for x in range(int(limit))]
        tmpFile = open(tmpfilepath, 'w+')
        for line in allLines:
            tmpFile.write(line)
    tmpFile.close()
    filepath = tmpfilepath

if not createByImport:    
    start_time = time.time()
    G = nx.read_weighted_edgelist(filepath, comments="no comments", delimiter=",", create_using=nx.DiGraph(), nodetype=str)
    for node in (G.nodes()):
        G.nodes[node]['name'] = str(node)

    if (verbose):
        print("Load of " + limit + " finished in: " + to_ms(time.time() - start_time) + " s.")
        print(nx.info(G))
        print("########################")

startTime=time.time()
#nodes = G.nodes(data=True)
#edges = G.edges(data=True)
endTime=time.time()

############ Export/Import ##########
if createByImport:
    importFile='/tmp/node_link_data_export_edgelist_'+str(limit)+'.json'
    print("IMPORTING " + importFile)
    start_time = time.time()
    G = import_node_link_data_to_graph(importFile, verbose=verbose)
    if (verbose): 
        print("IMPORTED FILE: " + importFile)
        print(nx.info(G))

if doExport:
    export_graph_to_node_link_data(G, '/tmp/node_link_data_export_edgelist_'+str(limit)+'.json', verbose=verbose)



########## DELETE-test Clear ################
if deleteTest:
    numberOfNodes = G.number_of_nodes()
    numberOfEdges = G.number_of_edges()
    export_graph_to_node_link_data(G, importExportFileName+"_full", verbose=verbose)
    
    start_time_clear=time.time()
    G.clear()
    export_graph_to_node_link_data(G, importExportFileName, verbose=verbose)
    end_time_clear=time.time()
    print(numberOfNodes, numberOfEdges, to_ms(end_time_clear - start_time_clear), sep=",")

   
########### ALGO TESTS ################
if doAlgo:
    #### SHORTEST PATH
    if doAlgoShortestPath:
        startTime=time.time()
        #nodeList=[x for x,y in G.nodes(data=True) if (y.get('ACTOR') == True)]
        #subG = G.subgraph(nodeList)
        #algo_shortest_path(G,verbose=algoVerbose)
        #algo_all_pairs_shortest_path_regular(G,nodeTypeForSubGraph=None,verbose=False)
        
        algo_all_pairs_dijkstra(G,nodeTypeForSubGraph=None,verbose=True,inputWeight='weight')
        #algo_all_pairs_bellman_ford_path(G,verbose=True,inputWeight='weight')
        
        #all_pairs_shortest_path(G)
        
        #algo_all_pairs_shortest_path(G,verbose=False,inputWeight='weight')
        #draw_all_shortest_path_for_single_node(G,"1")
        #all_shortest_path_for_single_node(G,"12")
        
        
        #### SHORTESTPATH ASTAR
        #algo_all_pairs_shortest_path_astar(G,verbose=verbose)
        endTime=time.time()
        print(((G.number_of_nodes()**2)-G.number_of_nodes()),G.number_of_nodes(), G.number_of_edges(), to_ms(endTime - startTime), sep=",")
        
    #### PAGERANK    
    if doAlgoPageRankTest:       
        #### PAGERANK
        weightInputForAlgos="weight"
        #weightInputForAlgos=None
        
        print("==============================")
        #algo_pagerank(G, "default",  weightInput=weightInputForAlgos, verbose=algoVerbose, maxLineOutput=15)
        # NUMPY IS OBSOLETE
        #algo_pagerank(G, "numpy", weightInput=weightInputForAlgos, verbose=algoVerbose, maxLineOutput=10)
        algo_pagerank(G, "scipy", weightInput=weightInputForAlgos, verbose=algoVerbose, maxLineOutput=0)
        print("==============================")
        print("EXECUTION TOOK: " + to_ms(time.time() - start_time))
    
    #### SIMRANK    
    if doSimRank:    #### SIMRANK
        algo_simRank(G,verbose=True,max_iterations=1)

    #### DEGREE CENTRALITY
    if doDegreeCentrality:
        verbose=True
        #algo_degree_centrality(G, verbose=True)
        #### OWN DEGREE CENTRALITY
        #peng = sorted(G.degree, key=lambda x: x[1], reverse=True)
        #if (verbose):
        #    for bums in peng:
        #        print(bums)
    
    
        #algo_degree_centrality(G, verbose=False)
    
    
    #print("TIME: " + to_ms(end_time - start_time))
    
        
    #print(str(G.number_of_nodes()) + "," + str(G.number_of_edges()) + "," + to_ms(end_time-start_time))
    #algo_jaccard_coefficient(G,G.edges(),verbose=True) 
    #### HITS
    if doHITS:#get_hits(G)
        get_hits(G)#draw_all_shortest_path_for_single_node(G,"1")
        #all_shortest_path_for_single_node(G,"12")





