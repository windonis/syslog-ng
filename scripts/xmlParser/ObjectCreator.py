import xml.etree.ElementTree as syslog
import networkx as nx
import os
G = nx.DiGraph()

tree = syslog.parse("./scripts/xmlParser/http-grammar.xml")
root = tree.getroot()

def lhsfinder(symbolName):
    lhslist = []
    for rule in root.iter('rule'):
        lhs = rule.find('lhs').text
        lhslist.append(lhs)
        res_list = []
        for i, value in enumerate(lhslist):
            if symbolName == value:
                res_list.append(i)
    return res_list


class RULE:
    def __init__(self, number, usefulness, lhs):
        self.number = number
        self.usefulness = usefulness
        self.lhs = lhs
        self.rhs = []

    def __str__(self):
        data = " number: {} \n usefulness: {} \n lhs: {} \n rhs: \n".format(self.number,self.usefulness,self.lhs)
        x = 1
        for i in self.rhs:
            data = data + "    {} : {} \n".format(x, i)
            x = x + 1
        return data

    def add_terminal(self):
        for i in self.rhs:
            terminalcontrol = lhsfinder(i)
            if len(terminalcontrol) == 0:
                terminalNumber = ( -1 * self.number - 1 )
                G.add_node(terminalNumber, terminalName=i)

    def add_node(self):
        G.add_node(self.number, lhs=self.lhs)
        '''
        count = 1
        for i in self.rhs:
            G.add_edge(self.number, i, Nweight=count, rule=self.number)
            count = count + 1
        '''
        
def xmltoobject():
    collector = []
    for rule in root.iter('rule'):
        number = rule.get('number')
        usefulness = rule.get('usefulness')
        lhs = rule.find('lhs').text
        g_rule = RULE(int(number), usefulness, lhs)
        for rhs in rule.iter('rhs'):
            symbol = rhs.findall('symbol')
            for x in symbol:
                g_rule.rhs.append(x.text)
        collector.append(g_rule)
        g_rule.add_node()
        g_rule.add_terminal()
    return collector
