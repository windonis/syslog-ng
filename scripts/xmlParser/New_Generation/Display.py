import networkx as nx
import GraphCreator as graph

graph.TerminalAdder()
graph.EdgeAdder()

print(graph.G.edges(61))
#stdout --> [(61, 'KW_BATCH_TIMEOUT'), (61, "'('"), (61, 50), (61, "')'")]

T = nx.dfs_edges(graph.G, source=61)
print(list(T))

##stdout --> [(61, 'KW_BATCH_TIMEOUT'), (61, "'('"), (61, 50), (50, 49), (49, 'LL_NUMBER'), (61, "')'")]