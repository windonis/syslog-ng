import xml.etree.ElementTree as ElementTree
import networkx as nx
import matplotlib.pyplot as plt

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):

    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                else:
                    aDict = {element[0].tag: XmlListConfig(element)}
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            elif element.items():
                self.update({element.tag: dict(element.items())})
            else:
                self.update({element.tag: element.text})

filePath = input('Please specify file path.(Full path):')
tree = ElementTree.parse(filePath)
root = tree.getroot()
xmldict = XmlDictConfig(root)
G = nx.Graph()
for x in xmldict:
    G.add_nodes_from([x])
for y in xmldict["grammar"]:
    G.add_edges_from([("grammar", y)])
for z in (xmldict["grammar"]["rules"]["rule"]):
    G.add_edges_from([("rules", z["number"])])
    G.add_edges_from([(z["number"], z["usefulness"])])

nx.draw(G, node_size=1000, font_size=10, with_labels=True, font_color="red", node_color="black", edge_color="purple")
plt.show()

