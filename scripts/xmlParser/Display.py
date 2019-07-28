import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

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
                    if i[1] != 'LL_CONTEXT_SOURCE':
                        beginNode.append(i[1])
            return(beginNode)

def snippetOutput():
    for state in findBeginState():
        nodeNumber = findNode(state)
        for part in traversalLimited(nodeNumber):
            if isinstance(part[1], int) is True:
                if len(traversalLimited(part[1])) != 0:
                    for x in (traversalLimited(part[1])):
                        if len(traversalLimited(x[1])) != 0:
                            if isinstance((traversalLimited(x[1]))[0][1], int) is False:
                                print("{} : {}".format((traversalLimited(x[1])[0][1]), (getPureRule((traversalLimited(x[1]))[0][0]))[1][2]))
                            else:
                                for p in (traversalLimited((traversalLimited(x[1]))[0][0])):
                                    try:
                                        print("{} : {}".format(getPureRule(p[1])[1][0], getPureRule(p[1])[1][2]))
                                    except:
                                        print(traversalLimited(p[1]))
                                        pass
                                    
#/TODO this method must be recursive. I will give only begin node.                     
snippetOutput()

'''

KW_URL : string_list
KW_USER : string
KW_PASSWORD : string
KW_USER_AGENT : string
KW_HEADERS : string_list
KW_AUTH_HEADER : http_auth_header_plugin
KW_METHOD : string
KW_BODY_PREFIX : string
KW_BODY_SUFFIX : string
KW_DELIMITER : string
KW_BODY : template_content
KW_ACCEPT_REDIRECTS : yesno
KW_TIMEOUT : nonnegative_integer
KW_BATCH_BYTES : nonnegative_integer
KW_WORKERS : nonnegative_integer
KW_RETRIES : positive_integer
KW_BATCH_LINES : nonnegative_integer
KW_BATCH_TIMEOUT : positive_integer
[(62, 55), (62, 56), (62, 57), (62, 58)] ---> I need Recursive search.
KW_CA_DIR : string
KW_CA_FILE : string
KW_CERT_FILE : string
KW_KEY_FILE : string
KW_CIPHER_SUITE : string
KW_USE_SYSTEM_CERT_STORE : yesno
KW_SSL_VERSION : string
KW_PEER_VERIFY : yesno
KW_TLS : http_tls_options
[] ---> I need control everytime to empty list.
KW_TS_FORMAT : string
KW_FRAC_DIGITS : nonnegative_integer
KW_TIME_ZONE : string
KW_SEND_TIME_ZONE : string
KW_LOCAL_TIME_ZONE : string
KW_ON_ERROR : string 

'''