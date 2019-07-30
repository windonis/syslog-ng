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
                    print(i[1])

def dictCreator():
    stack = {}
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

for k in dummyStack.items():
    print(k)

'''

('KW_URL', 'string_list')
('KW_USER', 'string')
('KW_PASSWORD', 'string')
('KW_USER_AGENT', 'string')
('KW_HEADERS', 'string_list')
('KW_AUTH_HEADER', 'http_auth_header_plugin')
('KW_METHOD', 'string')
('KW_BODY_PREFIX', 'string')
('KW_BODY_SUFFIX', 'string')
('KW_DELIMITER', 'string')
('KW_BODY', 'template_content')
('KW_ACCEPT_REDIRECTS', 'yesno')
('KW_TIMEOUT', 'nonnegative_integer')
('KW_BATCH_BYTES', 'nonnegative_integer')
('KW_WORKERS', 'nonnegative_integer')
('KW_RETRIES', 'positive_integer')
('KW_BATCH_LINES', 'nonnegative_integer')
('KW_BATCH_TIMEOUT', 'positive_integer')
('KW_LOG_FIFO_SIZE', 'positive_integer')
('KW_THROTTLE', 'nonnegative_integer')
('KW_PERSIST_NAME', 'string')
('KW_CA_DIR', 'string')
('KW_CA_FILE', 'string')
('KW_CERT_FILE', 'string')
('KW_KEY_FILE', 'string')
('KW_CIPHER_SUITE', 'string')
('KW_USE_SYSTEM_CERT_STORE', 'yesno')
('KW_SSL_VERSION', 'string')
('KW_PEER_VERIFY', 'yesno')
('KW_TS_FORMAT', 'string')
('KW_FRAC_DIGITS', 'nonnegative_integer')
('KW_TIME_ZONE', 'string')
('KW_SEND_TIME_ZONE', 'string')
('KW_LOCAL_TIME_ZONE', 'string')
('KW_ON_ERROR', 'string')

'''