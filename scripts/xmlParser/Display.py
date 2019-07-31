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
    filename = "./modules/http/http-parser.c" #/TODO could be parameter 
    filename2 = "./lib/cfg-parser.c" #/TODO could be static
    stacks = firstParser()
    for stack in stacks:
        if (stacks.index(stack) % 2 == 0):
            for line in open(filename, 'r'):
                if stack in line:
                    rString = (re.search('{(.*),', line))
                    print((rString[1]).split(",")[0])
        else:
            datas = stack
            pile = []
            fikri = []

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
                    for line in open(filename, 'r'):
                        if i[0] in line:
                            rString = (re.search('{(.*),', line))
                            teyfik = ((rString[1]).split(",")[0]) + ":" + sub
                            fikri.append(teyfik.replace('"',''))
            for i in fikri:
                a = ""
                y = i.split(":")[1]
                if "LL_" in y:
                    y2 = y.replace("LL_"," ").lower()
                    print("\t{}".format(i.replace(y,y2)))

                for line in open(filename2, 'r'):
                    if y in line:
                        if y == (line.split(",")[1].replace(" }","").strip()):
                            a += (line.split("{")[1].strip().split(",")[0].replace('"',' ')) + " / " #TODO re.match(r'(.*), ', line) i use but not working perfect
                if len(a) != 0: 
                    print("\t{}".format(i.replace(y, a)))
                        
start = time.time()
cleaner()
end = time.time()
print(end-start)

"""
 "http"
         url: identifier
         url: string
         user: identifier
         user_agent: identifier
         user: string
         user_agent: string
         password: identifier
         password: string
         user_agent: identifier
         user_agent: string
         headers: identifier
         headers: string
         auth_header: identifier
         method: identifier
         method: string
         body_prefix: identifier
         body_prefix: string
         body_suffix: identifier
         body_suffix: string
         delimiter: identifier
         delimiter: string
         body: identifier
         body_prefix: identifier
         body_suffix: identifier
         body: string
         body_prefix: string
         body_suffix: string
         accept_redirects: yes  /  on  / 
         accept_redirects: no  /  off  / 
         accept_redirects: number
         timeout: number
         flush_bytes: number
         batch_bytes: number
         workers: number
         flush_lines: number
         flush_timeout: number
 "tls"
         ca_dir: identifier
         ca_dir: string
         ca_file: identifier
         ca_file: string
         cert_file: identifier
         cert_file: string
         key_file: identifier
         key_file: string
         cipher_suite: identifier
         cipher_suite: string
         use_system_cert_store: yes  /  on  / 
         use_system_cert_store: no  /  off  / 
         use_system_cert_store: number
         ssl_version: identifier
         ssl_version: string
         peer_verify: yes  /  on  / 
         peer_verify: no  /  off  / 
         peer_verify: number
"""
"""
121.8657238483429
"""       

