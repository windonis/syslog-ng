import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

graph.EdgeAdder()


print(parser.G.nodes[61])


T = nx.dfs_edges(parser.G, source=61)
print(list(T))

nx.draw(parser.G, node_size=400, font_size=10, with_labels=True, font_color="red", node_color="black", edge_color="purple")
plt.show()

