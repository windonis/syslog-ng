import xml.etree.ElementTree as syslog
import networkx as nx
import matplotlib.pyplot as plt

tree = syslog.parse("gsoc.xml")
root = tree.getroot()

class RULE:
    def __init__(self,number,usefulness,lhs):
        self.number = number
        self.usefulness = usefulness
        self.lhs = lhs

def xmlparser():
    collector = []
    for rule in root.iter('rule'):
        number = rule.get('number')
        usefulness = rule.get('usefulness')
        lhs = rule.find('lhs').text
        g_rule = RULE(int (number),usefulness,lhs)
        collector.append(g_rule)
        del g_rule

    return collector

c_array = xmlparser()
G = nx.Graph()
for i in c_array:
    G.add_node(i.number, data=i)

print(G.node[0]['data'].usefulness)
