import ObjectCreator as parser
import networkx as nx
#For testing
import matplotlib.pyplot as plt

data = parser.xmltoobject()
G = nx.DiGraph()

#add Terminals for Node
def TerminalAdder():
    for rule in data:
        for p in rule.rhs:
            if p is not None:
                terminalControl = parser.lhsfinder(p)
                if len(terminalControl) == 0:
                    G.add_node(p) 
def EdgeAdder():
    for i in data:
        count = 1
        G.add_node(i.number, data=i)
        for symbol in i.rhs:
            if symbol is not None:
                terminalCheck = parser.lhsfinder(symbol)
                if len(terminalCheck) == 0:
                    G.add_edge(i.number, symbol, weight=count )
                    count = count + 1
                else:
                    for d in terminalCheck:
                        G.add_edge(i.number , d , weight=count )
                        count = count + 1
