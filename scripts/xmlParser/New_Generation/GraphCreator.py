import ObjectCreator as parser
import networkx as nx
import matplotlib.pyplot as plt

data = parser.xmltoobject()

def EdgeAdder():
    for i in data:
        count = 1
        parser.G.add_node(i)
        for symbol in i.rhs:
            if symbol is not None:
                terminalCheck = parser.lhsfinder(symbol)
                if len(terminalCheck) == 0:
                    parser.G.add_edge(i, symbol, weight=count )
                    count = count + 1
                else:
                    for d in terminalCheck:
                        parser.G.add_edge(i , d , weight=count )
                        count = count + 1
