import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

graph.EdgeAdder()

print(parser.G.edges('yesno'))

data = parser.xmltoobject()
uniqueLHS = []
for i in data:
    if i.lhs not in uniqueLHS:
        uniqueLHS.append(i.lhs)

f = open('./scripts/xmlParser/GraphOutput', 'w')
for x in uniqueLHS:
    f.write("\n-----Searchig for '{}'-----\n\n".format(x))
    H = nx.dfs_edges(parser.G, source='{}'.format(x))
    for j in H:
        f.write("{}\n".format(j))
