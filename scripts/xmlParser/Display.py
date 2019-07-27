import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

graph.EdgeAdder()


def Nameless (ruleNumber):
    store = []
    for i in (parser.G.edges.data('Nweight')):
        if ( i[0] == ruleNumber and i[2] is not None):
            lst = list(i)
            lst[0] = parser.G.node[ruleNumber]['lhs']
            store.append(lst)
    return(store)

beginNode = []

for i in parser.G.nodes.data('lhs'):
    if(i[1] == 'start'):
        count = i[0]

for x in list(nx.dfs_edges(parser.G, source=count)):
    if x[1] == "LL_CONTEXT_DESTINATION":
        for i in Nameless(x[0]):
            if i[1] != "LL_CONTEXT_DESTINATION":
                beginNode.append(i[1])
    elif x[1] == "LL_CONTEXT_SOURCE":
        for i in Nameless(x[0]):
            if i[1] != "LL_CONTEXT_SOURCE":
                beginNode.append(i[1])
'''
for i in beginNode:
    #print(i) ---> http_destination
    for x in parser.G.nodes.data('lhs'):
        if x[1] == i:
            #print(x[0]) ---> 4
            for part in (list(nx.dfs_edges(parser.G, source=x[0], depth_limit=0))):
                if isinstance(part[1], int) is True:
                    if part[1] > x[0]:
                        print(list(nx.dfs_tree(parser.G, source=part[1], depth_limit=0)))
'''
'''
                            if isinstance(z[1], int) is True:
                                returnValue = Nameless(z[1])
                                print("{}:{}".format(returnValue[0][1],returnValue[2][1]))
'''


test = parser.xmltoobject()
for i in test:
    if i.number == 61:
        print(i.rhs)