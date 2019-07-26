import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt

graph.EdgeAdder()


def Nameless (ruleNumber):
    store = []
    for i in (parser.G.edges.data('Nweight')):
        if ( i[0] == ruleNumber and i[2] is not None):
            lst = list(i)
            lst[0] = parser.G.node[ruleNumber]['lhs']
            store.append(lst)
    return(store)

def findLhstoNumber(lhsName):
    store = []
    for i in (parser.G.node.data('lhs')):
        if i[1] != None and i[1] == lhsName:
            result = Nameless(i[0])
            store.append(result)
    return(store)

def createFormat(lhsName):
    formatGenerator = findLhstoNumber(lhsName)
    firstTime = True
    for rule in formatGenerator:
        if (firstTime is True):
            print("driver: {}".format(rule[0][0].split("_")[0]))
            print("type: destination")
            print("options:")
            firstTime = False
        if "KW_" in rule[0][1] :
            print("\t{} : {}".format(rule[0][1].split("_")[1],rule[2][1]))


createFormat("http_option")

'''
driver: http
type: destination
options:
        URL : string_list
        USER : string
        PASSWORD : string
        USER : string
        HEADERS : string_list
        AUTH : http_auth_header_plugin
        METHOD : string
        BODY : string
        BODY : string
        DELIMITER : string
        BODY : template_content
        ACCEPT : yesno
        TIMEOUT : nonnegative_integer
        BATCH : nonnegative_integer
        WORKERS : nonnegative_integer
        TLS : http_tls_options
'''