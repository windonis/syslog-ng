import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

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

def Output():
    stack = dictCreator()
    dummyStack = stack
    deletedLines = []

    for x in stack.items():
        for v in traversalLimited(findNode(x[1])):
            try:
                if getPureRule(v[1])[1][0] in dummyStack:
                    if x[0] not in deletedLines:
                        deletedLines.append(x[0])
            except:
                pass

    for line in deletedLines:
        dummyStack.pop(line,None)
    lastDict = []

    for k in dummyStack.items():
        blist.clear()
        print(findNodeDetailed(k[1]))
        for Node in findNodeDetailed(k[1]):
            dummy = k[0] + " : " + Node
            if dummy not in lastDict:
                lastDict.append(dummy)

    for n in lastDict:
        print(n)

Output()

#stdout

'''
KW_URL : LL_IDENTIFIER
KW_URL : LL_STRING
KW_USER : LL_IDENTIFIER
KW_USER : LL_STRING
KW_PASSWORD : LL_IDENTIFIER
KW_PASSWORD : LL_STRING
KW_USER_AGENT : LL_IDENTIFIER
KW_USER_AGENT : LL_STRING
KW_HEADERS : LL_IDENTIFIER
KW_HEADERS : LL_STRING
KW_AUTH_HEADER : LL_IDENTIFIER
KW_METHOD : LL_IDENTIFIER
KW_METHOD : LL_STRING
KW_BODY_PREFIX : LL_IDENTIFIER
KW_BODY_PREFIX : LL_STRING
KW_BODY_SUFFIX : LL_IDENTIFIER
KW_BODY_SUFFIX : LL_STRING
KW_DELIMITER : LL_IDENTIFIER
KW_DELIMITER : LL_STRING
KW_BODY : LL_IDENTIFIER
KW_BODY : LL_STRING
KW_ACCEPT_REDIRECTS : KW_YES
KW_ACCEPT_REDIRECTS : KW_NO
KW_ACCEPT_REDIRECTS : LL_NUMBER
KW_TIMEOUT : LL_NUMBER
KW_BATCH_BYTES : LL_NUMBER
KW_WORKERS : LL_NUMBER
KW_RETRIES : LL_NUMBER
KW_BATCH_LINES : LL_NUMBER
KW_BATCH_TIMEOUT : LL_NUMBER
KW_LOG_FIFO_SIZE : LL_NUMBER
KW_THROTTLE : LL_NUMBER
KW_PERSIST_NAME : LL_IDENTIFIER
KW_PERSIST_NAME : LL_STRING
KW_CA_DIR : LL_IDENTIFIER
KW_CA_DIR : LL_STRING
KW_CA_FILE : LL_IDENTIFIER
KW_CA_FILE : LL_STRING
KW_CERT_FILE : LL_IDENTIFIER
KW_CERT_FILE : LL_STRING
KW_KEY_FILE : LL_IDENTIFIER
KW_KEY_FILE : LL_STRING
KW_CIPHER_SUITE : LL_IDENTIFIER
KW_CIPHER_SUITE : LL_STRING
KW_USE_SYSTEM_CERT_STORE : KW_YES
KW_USE_SYSTEM_CERT_STORE : KW_NO
KW_USE_SYSTEM_CERT_STORE : LL_NUMBER
KW_SSL_VERSION : LL_IDENTIFIER
KW_SSL_VERSION : LL_STRING
KW_PEER_VERIFY : KW_YES
KW_PEER_VERIFY : KW_NO
KW_PEER_VERIFY : LL_NUMBER
KW_TS_FORMAT : LL_IDENTIFIER
KW_TS_FORMAT : LL_STRING
KW_FRAC_DIGITS : LL_NUMBER
KW_TIME_ZONE : LL_IDENTIFIER
KW_TIME_ZONE : LL_STRING
KW_SEND_TIME_ZONE : LL_IDENTIFIER
KW_SEND_TIME_ZONE : LL_STRING
KW_LOCAL_TIME_ZONE : LL_IDENTIFIER
KW_LOCAL_TIME_ZONE : LL_STRING
KW_ON_ERROR : LL_IDENTIFIER
KW_ON_ERROR : LL_STRING
'''