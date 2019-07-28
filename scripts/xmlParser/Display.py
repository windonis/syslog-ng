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

def solucan(nodeNumber):
    dictt = {}
    for nod in traversalUnlimeted(nodeNumber):
        if isinstance(nod[1], int) is True:
            if len(traversalLimited(nod[1])) != 0:
                for x in (traversalLimited(nod[1])):
                    if isinstance(x[1], int) is not True:
                        try:
                            if (getPureRule(x[0]))[1][0] not in dictt:
                                for status in (getPureRule(x[0]))[1]:
                                    returner = findNode(status)
                                    if returner is not None:
                                        if len(traversalLimited(returner)) != 0:
                                            #print("{}:{}".format(  (getPureRule(x[0]))[1][0],(getPureRule(x[0]))[1][2]  ))
                                            dictt.update( {(getPureRule(x[0]))[1][0] : status }) 
                                            #print(dictt)

                        except:
                            pass
    return dictt


def snippetOutput():
    for state in findBeginState():
        nodeNumber = findNode(state)
        return(solucan(nodeNumber))
                                   
dummy = snippetOutput()
for k, v in dummy.items():
    print("{} : {}".format(k,v))


#HTTP MODULE
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
LL_IDENTIFIER : string
KW_ACCEPT_REDIRECTS : yesno
KW_TIMEOUT : nonnegative_integer
KW_BATCH_BYTES : nonnegative_integer
KW_WORKERS : nonnegative_integer
KW_RETRIES : positive_integer
KW_BATCH_LINES : nonnegative_integer
KW_BATCH_TIMEOUT : positive_integer
KW_LOG_FIFO_SIZE : positive_integer
KW_THROTTLE : nonnegative_integer
KW_PERSIST_NAME : string
KW_CA_DIR : string
KW_CA_FILE : string
KW_CERT_FILE : string
KW_KEY_FILE : string
KW_CIPHER_SUITE : string
KW_USE_SYSTEM_CERT_STORE : yesno
KW_SSL_VERSION : string
KW_PEER_VERIFY : yesno
KW_TLS : http_tls_options
KW_TS_FORMAT : string
KW_FRAC_DIGITS : nonnegative_integer
KW_TIME_ZONE : string
KW_SEND_TIME_ZONE : string
KW_LOCAL_TIME_ZONE : string
KW_ON_ERROR : string
'''

#AFFILE MODULE
'''
KW_FILE : source_affile_params
KW_FOLLOW_FREQ : nonnegative_integer
KW_PAD_SIZE : nonnegative_integer
KW_MULTI_LINE_MODE : string
KW_MULTI_LINE_PREFIX : string
KW_MULTI_LINE_GARBAGE : string
KW_OWNER : string_or_number
KW_GROUP : string_or_number
KW_DIR_OWNER : string_or_number
KW_DIR_GROUP : string_or_number
KW_CHECK_HOSTNAME : yesno
KW_FLAGS : source_reader_option_flags
KW_LOG_FETCH_LIMIT : positive_integer
KW_FORMAT : string
KW_LOG_IW_SIZE : positive_integer
KW_CHAIN_HOSTNAMES : yesno
KW_KEEP_HOSTNAME : yesno
KW_PROGRAM_OVERRIDE : string
KW_HOST_OVERRIDE : string
KW_LOG_PREFIX : string
KW_KEEP_TIMESTAMP : yesno
KW_READ_OLD_RECORDS : yesno
KW_TAGS : string_list
KW_USE_FQDN : yesno
KW_USE_DNS : dnsmode
KW_DNS_CACHE : yesno
KW_NORMALIZE_HOSTNAMES : yesno
KW_ENCODING : string
KW_LOG_MSG_SIZE : positive_integer
KW_TRIM_LARGE_MESSAGES : yesno
KW_TIME_ZONE : string
KW_DEFAULT_LEVEL : level_string
KW_DEFAULT_FACILITY : facility_string
KW_PERSIST_NAME : string
KW_PIPE : source_afpipe_params
KW_OPTIONAL : yesno
KW_STDIN : source_stdin_params
KW_WILDCARD_FILE : source_wildcard_params
KW_BASE_DIR : string
KW_FILENAME_PATTERN : string
KW_RECURSIVE : yesno
KW_MONITOR_METHOD : string
'''