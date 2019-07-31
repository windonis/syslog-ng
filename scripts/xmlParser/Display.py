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
                print("\t{}".format(i))

start = time.time()
cleaner()
end = time.time()
print(end-start)

"""
KW_HTTP
        ('KW_URL', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_USER', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_PASSWORD', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_USER_AGENT', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_HEADERS', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_AUTH_HEADER', ['LL_IDENTIFIER'])
        ('KW_METHOD', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_BODY_PREFIX', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_BODY_SUFFIX', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_DELIMITER', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_BODY', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_ACCEPT_REDIRECTS', ['KW_YES', 'KW_NO', 'LL_NUMBER'])
        ('KW_TIMEOUT', ['LL_NUMBER'])
        ('KW_BATCH_BYTES', ['LL_NUMBER'])
        ('KW_WORKERS', ['LL_NUMBER'])
        ('KW_RETRIES', ['LL_NUMBER'])
        ('KW_BATCH_LINES', ['LL_NUMBER'])
        ('KW_BATCH_TIMEOUT', ['LL_NUMBER'])
        ('KW_LOG_FIFO_SIZE', ['LL_NUMBER'])
        ('KW_THROTTLE', ['LL_NUMBER'])
        ('KW_PERSIST_NAME', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_TS_FORMAT', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_FRAC_DIGITS', ['LL_NUMBER'])
        ('KW_TIME_ZONE', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_SEND_TIME_ZONE', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_LOCAL_TIME_ZONE', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_ON_ERROR', ['LL_IDENTIFIER', 'LL_STRING'])
KW_TLS
        ('KW_CA_DIR', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_CA_FILE', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_CERT_FILE', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_KEY_FILE', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_CIPHER_SUITE', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_USE_SYSTEM_CERT_STORE', ['KW_YES', 'KW_NO', 'LL_NUMBER'])
        ('KW_SSL_VERSION', ['LL_IDENTIFIER', 'LL_STRING'])
        ('KW_PEER_VERIFY', ['KW_YES', 'KW_NO', 'LL_NUMBER'])
"""
"""
Running Measure : 133 sec
"""