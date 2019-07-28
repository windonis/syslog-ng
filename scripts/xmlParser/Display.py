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
                                print(traversalLimited((traversalLimited(x[1]))[0][0]))
                     
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
[(22, 59), (22, 60), (22, 61), (22, 62)] ---> threaded_dest_driver_option
[(23, 29), (23, 30), (23, 31), (23, 32), (23, 33), (23, 34), (23, 35), (23, 36)] --> TLS RULES 
KW_TLS : http_tls_options
[(26, 25), (26, 63), (26, 64), (26, 65), (26, 66), (26, 67), (26, 68)] --> TEMPLATE OPTINO
'''