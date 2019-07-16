import pytest
from xml.dom.minidom import parse
import xml.dom.minidom
from ObjectCreator import xmltoobject
import random

Ruleobject = xmltoobject()

class parseRULE:
    def __init__(self, number, usefulness, lhs):
        self.number = number
        self.usefulness = usefulness
        self.lhs = lhs
        self.rhs = []

def parserXML(getNumber):
    DOMTree = xml.dom.minidom.parse("gsoc.xml")
    collection = DOMTree.documentElement
    rules = collection.getElementsByTagName("rule")
    for rule in rules:
        if rule.getAttribute("number") == str(getNumber):
            n = rule.getAttribute("number")
            u = rule.getAttribute("usefulness")
            lhs = rule.getElementsByTagName('lhs')[0]
            l = lhs.childNodes[0].data
            parsed = parseRULE(n,u,l)
            rhs = rule.getElementsByTagName("symbol")
            for symbol in rhs:
                parsed.rhs.append(symbol.childNodes[0].data)
    return parsed

def childxmltoobject(xmltoobject,getNumber):
    data = xmltoobject
    for i in data:
        if i.number == getNumber:
            return i


def test_array():
    print("\n")
    for x in range(10):
        selectedValue = random.randrange(0,235)
        print("{}.test, trying for rule {}".format(x,selectedValue))
        data = childxmltoobject(xmltoobject=xmltoobject(), getNumber=selectedValue)
        assert parserXML(selectedValue).lhs == data.lhs
        assert parserXML(selectedValue).usefulness == data.usefulness
        assert parserXML(selectedValue).rhs == data.rhs
   

## pytest test.py -s