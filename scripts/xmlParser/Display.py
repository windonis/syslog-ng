import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

graph.EdgeAdder()


def Nameless (ruleNumber):
    store = []
    for i in parser.xmltoobject():
        if ( i.number == ruleNumber):
            store.append(i.lhs)
            store.append(i.rhs)
    return(store)


beginNode = []

for i in parser.G.nodes.data('lhs'):
    if(i[1] == 'start'):
        count = i[0]

for x in list(nx.dfs_edges(parser.G, source=count)):
    if x[1] == 'LL_CONTEXT_DESTINATION':
        for i in Nameless(x[0]):
            if i[1] != 'LL_CONTEXT_DESTINATION':
                beginNode.append(i[1])
    elif x[1] == 'LL_CONTEXT_SOURCE':
        if i[1] != 'LL_CONTEXT_SOURCE':
            beginNode.append(i[1])

for i in beginNode:
    for x in parser.G.nodes.data('lhs'):
        if x[1] == i:
            for part in (list(nx.dfs_edges(parser.G, source=x[0], depth_limit=0))):
                if isinstance(part[1], int) is True:
                    if part[1] > x[0]: 
                        if len(list(nx.dfs_edges(parser.G, source=part[1], depth_limit=0))) != 0:
                            for f in (list(nx.dfs_edges(parser.G, source=part[1], depth_limit=0))):
                                returnValue = Nameless(f[1])
                                print("{}:{}".format(returnValue[1][0], returnValue[1][2]))


#abbas = Nameless(61)
#print(abbas)

'''
for a in (list(nx.dfs_edges(parser.G, source=8, depth_limit=0))):
    print(a)
'''