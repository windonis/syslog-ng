import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

graph.EdgeAdder()

### PREVIOS VERSION ###
print(parser.G.edges(61))  #stdout --> [(61, 'KW_BATCH_TIMEOUT'), (61, "'('"), (61, 50), (61, "')'")]

T = nx.dfs_edges(parser.G, source=61)
print(list(T))  ##stdout --> [(61, 'KW_BATCH_TIMEOUT'), (61, "'('"), (61, 50), (50, 49), (49, 'LL_NUMBER'), (61, "')'")]

### NEW VERSION ###
print(parser.G.edges(61))  #stdout --> []
T = nx.dfs_edges(parser.G, source=61)
print(list(T))  ##stdout --> []


### __STR__ FUNCTION OUTPUT ###
tester = list(parser.G.nodes())
print(tester[1])
'''
 number: 0
 usefulness: useful
 lhs: $accept
 rhs:
    1 : start
    2 : $end
'''
    