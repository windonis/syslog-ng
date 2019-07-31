import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt
import re

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
    lastDict = []

    for k in stack.items():
        blist.clear()
        for Node in findNodeDetailed(k[1]):
            dummy = k[0] + " : " + Node
            if dummy not in lastDict:
                lastDict.append(dummy)

    return(lastDict)

for f in Output():
    filename = "./modules/http/http-parser.c"
    for line in open(filename, 'r'):
        dummyvalue = (f.split(":")[0]).strip()
        if dummyvalue in line:
            rString = (re.search('{(.*),', line))
            print(f.replace((f.split(":")[0]).strip(), (rString.group(1).split(",")[0])))

#/TODO if x [1] is equal to y [0] below, x [0] is parent.
'''
 "http" : KW_URL
 "http" : LL_IDENTIFIER
 "http" : LL_STRING
 "http" : KW_USER
 "http" : KW_PASSWORD
 "http" : KW_USER_AGENT
 "http" : KW_HEADERS
 "http" : KW_AUTH_HEADER
 "http" : KW_METHOD
 "http" : KW_BODY_PREFIX
 "http" : KW_BODY_SUFFIX
 "http" : KW_DELIMITER
 "http" : KW_BODY
 "http" : KW_ACCEPT_REDIRECTS
 "http" : KW_YES
 "http" : KW_NO
 "http" : LL_NUMBER
 "http" : KW_TIMEOUT
 "http" : KW_BATCH_BYTES
 "http" : KW_WORKERS
 "http" : KW_RETRIES
 "http" : KW_BATCH_LINES
 "http" : KW_BATCH_TIMEOUT
 "http" : KW_LOG_FIFO_SIZE
 "http" : KW_THROTTLE
 "http" : KW_PERSIST_NAME
 "http" : KW_CA_DIR
 "http" : KW_CA_FILE
 "http" : KW_CERT_FILE
 "http" : KW_KEY_FILE
 "http" : KW_CIPHER_SUITE
 "http" : KW_USE_SYSTEM_CERT_STORE
 "http" : KW_SSL_VERSION
 "http" : KW_PEER_VERIFY
 "http" : KW_TLS
 "http" : KW_TS_FORMAT
 "http" : KW_FRAC_DIGITS
 "http" : KW_TIME_ZONE
 "http" : KW_SEND_TIME_ZONE
 "http" : KW_LOCAL_TIME_ZONE
 "http" : KW_ON_ERROR
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
 "tls" : KW_CA_DIR
 "tls" : LL_IDENTIFIER
 "tls" : LL_STRING
 "tls" : KW_CA_FILE
 "tls" : KW_CERT_FILE
 "tls" : KW_KEY_FILE
 "tls" : KW_CIPHER_SUITE
 "tls" : KW_USE_SYSTEM_CERT_STORE
 "tls" : KW_YES
 "tls" : KW_NO
 "tls" : LL_NUMBER
 "tls" : KW_SSL_VERSION
 "tls" : KW_PEER_VERIFY
 '''