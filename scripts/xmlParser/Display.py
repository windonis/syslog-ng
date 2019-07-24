import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

graph.EdgeAdder()


def Nameless (ruleNumber):
    for i in (parser.G.edges.data('Nweight')):
        if ( i[0] == ruleNumber and i[2] is not None):
            lst = list(i)
            lst[0] = parser.G.node[ruleNumber]['lhs']
            print(lst)

Nameless(7)

'''
--- stdout ---

['http_option', 'KW_URL', 1]
['http_option', "'('", 2]
['http_option', 'string_list', 3]
['http_option', "')'", 4]

'''