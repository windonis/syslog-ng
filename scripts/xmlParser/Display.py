import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt
import re
import time

alist = [] #using at agressiveRecursive()
blist = [] #using at passiveRecursive()
graph.EdgeAdder()


def getPureRule(ruleNumber):
    store = []
    for i in parser.xmltoobject():
        if ( i.number == ruleNumber):
            store.append(i.lhs)
            store.append(i.rhs)
    return(store)

def traversalUnlimeted(beginstate):
    return list(nx.dfs_edges(parser.G, source=beginstate))

def traversalLimited(beginstate):
    return list(nx.dfs_edges(parser.G, source=beginstate, depth_limit=0))

def findNode(lhs):
    for x in parser.G.nodes.data('lhs'):
        if x[1] == lhs:
            return(x[0])

def findNodeDetailed(lhs):
    listed = []
    for x in parser.G.nodes.data('lhs'):
        if x[1] is not None and x[1] == lhs:
            listed.append(x[0])
    for li in listed:
        stored = passiveRecursive(li)
    return(stored)
    
def terminalControl(name):
    stored = []
    for x in parser.G.node.data('terminalName'):
        try:
            if x[0] < 0:
                if x[1] not in stored:
                    stored.append(x[1])
        except:
            pass
    if name in stored:
        return(True)

def findBeginState():
    beginNode = []
    for i in parser.G.nodes.data('lhs'):
        if(i[1] == 'start'):
            for x in traversalUnlimeted(i[0]):
                if x[1] == 'LL_CONTEXT_DESTINATION':
                    source = getPureRule(x[0])
                    for i in source[1]:
                        if i != 'LL_CONTEXT_DESTINATION':
                            beginNode.append(i)
                elif x[1] == 'LL_CONTEXT_SOURCE':
                    source = getPureRule(x[0])
                    for i in source[1]:
                        if i != 'LL_CONTEXT_SOURCE':
                            beginNode.append(i)
    return(beginNode)

def agressiveRecursive(ruleNumber):
    for i in traversalLimited(ruleNumber):
            if isinstance(i[1], int) is True:
                agressiveRecursive(i[1])
            else:
                if i[0] not in alist:
                    alist.append(i[0])
    return(alist)

def passiveRecursive(ruleNumber):
    for i in (traversalLimited(ruleNumber)):
        if isinstance(i[1], int) is True:
            passiveRecursive(i[1])
        else:
            if ( i[1] != "'('" ) and ( i[1] != "')'"):
                    blist.append(i[1])
    return blist

def dictCreator():
    stack = {}
    alist.clear()
    aggResult = agressiveRecursive(findNode('http_destination'))
    for i in aggResult:
        if terminalControl( getPureRule(i)[1][0] ) is not True:
            validrules = []
            for x in getPureRule(i)[1]:
                if x != "'('" and x != "')'" and "$@" not in x:
                    validrules.append(x)
            stack.update({validrules[0]:validrules[1]})
            del validrules
    return(stack)

def output():
    stack = dictCreator()
    lastDict = []

    for k in stack.items():
        blist.clear()
        for Node in findNodeDetailed(k[1]):
            dummy = k[0] + " : " + Node
            if dummy not in lastDict:
                lastDict.append(dummy)
    return(lastDict)

def firstParser():

    laststack = []
    datas = output()
    dummyDatas = datas
    stack = []
    for i in datas:
        for j in dummyDatas:
            if i.split(":")[1].strip() == j.split(":")[0].strip():
                if i.split(":")[0].strip() not in stack:
                    stack.append("{}".format(i.split(":")[0].strip()))

    for key in stack:
        newObj = {}
        x = datas
        for line1 in x:
            key1 = line1.strip().split(" : ")[0]
            value1 = line1.strip().split(" : ")[1]
            if key1 not in newObj:
                newObj[key1] = {}
            for line2 in x:
                key2 = line2.strip().split(" : ")[0]
                value2 = line2.strip().split(" : ")[1]
                if key2 == value1:
                    if value1 not in newObj[key1]:
                        newObj[key1][value1] = []
                    newObj[key1][value1].append(value2)
        laststack.append(key)
        laststack.append((newObj[key]))
    return laststack

def cleaner():
    stacks = firstParser()
    for stack in stacks:
        if (stacks.index(stack) % 2 == 0):
            print(stack)
        else:
            datas = stack
            pile = []

            for i in datas.items():
                for x in i[1]:
                    if x in datas:
                        pile.append(x)
                        if i[0] not in pile:
                            pile.append(i[0])
            for i in pile:
                del datas[i]
                
            for i in datas.items():
                for sub in i[1]:
                    filename = "./modules/http/http-parser.c" #/TODO could be parameter
                    for line in open(filename, 'r'):
                        if i[0] in line:
                            rString = (re.search('{(.*),', line))

                            print("\t{} : {}".format(rString.group(1).split(",")[0],sub))

start = time.time()
cleaner()
end = time.time()
print(end-start)

"""
KW_HTTP
         "url" : LL_IDENTIFIER
         "url" : LL_STRING
         "user" : LL_IDENTIFIER
         "user_agent" : LL_IDENTIFIER
         "user" : LL_STRING
         "user_agent" : LL_STRING
         "password" : LL_IDENTIFIER
         "password" : LL_STRING
         "user_agent" : LL_IDENTIFIER
         "user_agent" : LL_STRING
         "headers" : LL_IDENTIFIER
         "headers" : LL_STRING
         "auth_header" : LL_IDENTIFIER
         "method" : LL_IDENTIFIER
         "method" : LL_STRING
         "body_prefix" : LL_IDENTIFIER
         "body_prefix" : LL_STRING
         "body_suffix" : LL_IDENTIFIER
         "body_suffix" : LL_STRING
         "delimiter" : LL_IDENTIFIER
         "delimiter" : LL_STRING
         "body" : LL_IDENTIFIER
         "body_prefix" : LL_IDENTIFIER
         "body_suffix" : LL_IDENTIFIER
         "body" : LL_STRING
         "body_prefix" : LL_STRING
         "body_suffix" : LL_STRING
         "accept_redirects" : KW_YES
         "accept_redirects" : KW_NO
         "accept_redirects" : LL_NUMBER
         "timeout" : LL_NUMBER
         "flush_bytes" : LL_NUMBER
         "batch_bytes" : LL_NUMBER
         "workers" : LL_NUMBER
         "flush_lines" : LL_NUMBER
         "flush_timeout" : LL_NUMBER
KW_TLS
         "ca_dir" : LL_IDENTIFIER
         "ca_dir" : LL_STRING
         "ca_file" : LL_IDENTIFIER
         "ca_file" : LL_STRING
         "cert_file" : LL_IDENTIFIER
         "cert_file" : LL_STRING
         "key_file" : LL_IDENTIFIER
         "key_file" : LL_STRING
         "cipher_suite" : LL_IDENTIFIER
         "cipher_suite" : LL_STRING
         "use_system_cert_store" : KW_YES
         "use_system_cert_store" : KW_NO
         "use_system_cert_store" : LL_NUMBER
         "ssl_version" : LL_IDENTIFIER
         "ssl_version" : LL_STRING
         "peer_verify" : KW_YES
         "peer_verify" : KW_NO
         "peer_verify" : LL_NUMBER
         
"""
"""
Running Measure : 133 sec
"""