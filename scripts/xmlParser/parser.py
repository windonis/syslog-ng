import xml.etree.ElementTree as syslog
import networkx as nx
import matplotlib.pyplot as plt

tree = syslog.parse("gsoc.xml")
root = tree.getroot()


def lhsfinder(nameoflhs):
    lhslist = []
    for rule in root.iter('rule'):
        lhs = rule.find('lhs').text
        lhslist.append(lhs)
        res_list = []
        for i, value in enumerate(lhslist):
            if nameoflhs == value:
                res_list.append(i)
    return res_list


def xmlparser():
    rules = []
    for rule in root.iter('rule'):
        d_rule = {}

        number = rule.get('number')
        d_rule.update({'number' : number})

        usefulness = rule.get('usefulness')
        d_rule.update({'usefulness' : usefulness })

        lhs = rule.find('lhs').text
        d_rule.update({'lhs' : lhs})

        for rhs in rule.iter('rhs'):
            symbol = rhs.findall('symbol')
            d_symbol = {}
            for i in symbol:
                if i is not None:
                    returnable = lhsfinder(i.text)
                    if len(returnable) != 0:
                        for z in returnable:
                            d_symbol.update({ z : i.text})
                    else:
                        d_symbol.update( {'[x]' : i.text } )
            d_rule.update( { 'symbol' : d_symbol } )
            del d_symbol
        rules.append(d_rule)
        del d_rule
        #print(rules)
    return rules

rules = xmlparser()

#for x in rules:
#    print(x['number'])

G = nx.DiGraph()
for x in rules:
    G.add_node(x["number"])
    G.add_edge(x["number"], x["usefulness"])
    G.add_edge(x["number"], x["lhs"])
    for q in x["symbol"].keys():
        G.add_edge(x["number"], x["symbol"][q] )

print(G.edges)

#nx.draw(G, node_size=400, font_size=10, with_labels=True, font_color="red", node_color="black", edge_color="purple")
#plt.show()

