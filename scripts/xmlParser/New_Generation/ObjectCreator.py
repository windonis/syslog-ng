#XML to Python Array

import xml.etree.ElementTree as syslog

tree = syslog.parse("gsoc.xml")
root = tree.getroot()

class RULE:
    def __init__(self, number, usefulness, lhs):
        self.number = number
        self.usefulness = usefulness
        self.lhs = lhs
        self.rhs = []

def xmltoobject():
    collector = []
    for rule in root.iter('rule'):
        number = rule.get('number')
        usefulness = rule.get('usefulness')
        #print(type(usefulness))
        lhs = rule.find('lhs').text
        g_rule = RULE(int (number),usefulness,lhs)
        for rhs in rule.iter('rhs'):
            symbol = rhs.findall('symbol')
            for x in symbol:
                #print(type(x.text))
                g_rule.rhs.append(x.text)
        collector.append(g_rule)
        del g_rule 
    return collector

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

