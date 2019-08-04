import networkx as nx
import GraphCreator as graph
import ObjectCreator as parser
import matplotlib.pyplot as plt
import re
import time
import itertools

#alist = [] #using at agressiveRecursive()
blist = [] #using at passiveRecursive()
graph.EdgeAdder()
gettingRules = parser.xmltoobject()
parseFile = "./modules/http/http-parser.c"


def getPureRule(ruleNumber):
    store = []
    for i in gettingRules:
        if ( i.number == ruleNumber):
            store.append(i.lhs)
            store.append(i.rhs)
    return(store)

def traversalUnlimeted(beginstate):
    return list(nx.dfs_edges(parser.G, source=beginstate))

def traversalLimited(beginstate):
    return list(nx.dfs_edges(parser.G, source=beginstate, depth_limit=0))

def findNode(lhs):
    newBorn = []
    for x in parser.G.nodes.data('lhs'):
        if x[1] == lhs:
            newBorn.append(x[0])
    return newBorn

def findNodeDetailed(lhs):
    listed = []
    stored = []
    for x in parser.G.nodes.data('lhs'):
        if x[1] is not None and x[1] == lhs:
            listed.append(x[0])
    for li in listed:
        stored = passiveRecursive(li)
    return(stored)
    
def terminalControl(name):
    stored = []
    for x in parser.G.node.data('terminalName'):
        if x[1] is not None:
            if x[0] < 0:
                if x[1] not in stored:
                    stored.append(x[1])

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

def oppositeFindBeginState(state):
    allRuleNumber = gettingRules
    for i in allRuleNumber:
        gettingDetail = getPureRule(i.number)
        if state in gettingDetail[1]:
            for x in gettingDetail[1]:
                if "LL_CONTEXT_" in x:
                    return x.replace("LL_CONTEXT_","").lower()
        
def agressiveRecursive(ruleNumber):
    havuz = []
    havuz.append(ruleNumber)
    count = 0
    previousLen = 0
    alist = []
    while True:
        if count != 100:
            if len(havuz) != 0:
                fikri = havuz[0]
                for x in traversalLimited(fikri):
                    if isinstance(x[1], int) is True:
                        if x[1] not in havuz:
                            if x[1] > min(havuz):
                                havuz.append(x[1])
                    else:
                        if x[0] not in alist and x[1] is not None:
                            alist.append(x[0])
                havuz.remove(fikri)
                if len(alist) == previousLen:
                    count = count + 1
                else:
                    previousLen = len(alist)          
            else:
                break
        else:
            break
    return(alist)

def passiveRecursive(ruleNumber):
    havuz = []
    havuz.append(ruleNumber)
    count = 0
    previousLen = 0
    while True:
        if count != 100:
            if len(havuz) != 0:
                fikri = havuz[0]
                for x in traversalLimited(fikri):
                    if isinstance(x[1], int) is True:
                        if x[1] not in havuz:
                            #if x[1] > min(havuz):
                            havuz.append(x[1]) 
                    else:
                        if ( x[1] != "'('" ) and ( x[1] != "')'"):
                            blist.append(x[1])
                havuz.remove(fikri)
                if len(blist) == previousLen:
                    count = count + 1
                else:
                    previousLen = len(blist)          
            else:
                break
        else:
            break
    return(blist)

def findTerminalState(lhs):
    if terminalControl(lhs) is True:
        return lhs
    terminalState = []
    nodes = findNode(lhs)
    for i in nodes:
        i = getPureRule(i)
        if len(i) == 1:
            if terminalControl(i) is True:
                terminalState.append(i)
    return(terminalState)

def dictCreator(beginning):
    #Parser Files
    allStack = {}
    newBorn = (findNode(beginning))
    for born in newBorn:
        stack = {}
        aggResult = agressiveRecursive(born)
        for i in aggResult:
            if terminalControl( getPureRule(i)[1][0] ) is not True:
                validrules = []
                for x in getPureRule(i)[1]:
                    if x != "'('" and x != "')'" and "$@" not in x:
                        validrules.append(x)
                        if len(validrules) == 2:
                            stack[validrules[0]] = validrules[1]
                del validrules
        allStack[getPureRule(born)[1][0]] = stack
        del stack
    return(allStack)

def output(beginning):
    stack = dictCreator(beginning)
    
    lastDict = []
    keys = []
    returnDict = {}

    for i in stack.keys():
        keys.append(i)

    for i in keys:
        for k in stack[i].items():
            blist.clear()
            for Node in findNodeDetailed(k[1]):
                dummy = k[0] + " : " + Node
                if dummy not in lastDict:
                    lastDict.append(dummy)
        returnDict[i] = lastDict
    return(returnDict)

def parserTerminal(text):
    keyword = []
    for line in open('./lib/cfg-parser.c','r'):
        if text in line:
            if text == (line.split(",")[1].replace(" }","").strip().replace('"','')):
                keyword.append((line.split(",")[0].replace("{ ","").strip().replace('"','')))
    return keyword


#/TODO this part will be function. we can divide it into more than one piece.
start = time.time()
BeginnerState = findBeginState() # ---> This place takes out the top parents. For Example at http module (http_destination)
for state in BeginnerState:
    dataFromOutput = output(state) 

    for key in dataFromOutput.keys():
        dataStore = []
        Problems = {}
        ProblemsArray = []
        Remover = []

        for line in open(parseFile,'r'):
            if key in line:
                newKey = (re.search('{(.*),', line))
                driverName = (((newKey[1]).split(",")[0]).replace('"',''))
                print("drive:{}".format( driverName ) ) #---> Each driver is marked as the key of the dictionary.
                break

        print("type: {}".format(oppositeFindBeginState(state))) 
        for x in dataFromOutput[key]:
            #ruleCounterPerDriver = 1 # ---> If option number is wanted 
            if x.split(" : ")[0].strip() not in dataFromOutput.keys():
                dataStore.append(x)

        for data1 in dataStore:
            for data2 in dataStore:
                if data1.split(" : ")[1] == data2.split(" : ")[0]:
                    ProblemsArray.append(data2)
                    if (data1.split(" : ")[0]) not in Problems:
                        Problems[data1.split(" : ")[0]] = ProblemsArray

        for removingKey in Problems.keys():
            for data3 in dataStore:
                if data3.split(" : ")[0] == removingKey:
                    Remover.append(data3)

            for items in Remover:
                dataStore.remove(items)

            """for items in Problems[removingKey]:
                dataStore.remove(items)"""

        
        check = []
        for k in dataStore:
            connector1 = []
            newValue = ""
            for p in dataStore:
                if k.split(" : ")[0] == p.split(" : ")[0]:
                    if k.split(" : ")[1] not in connector1:
                        connector1.append(k.split(" : ")[1])
                    if p.split(" : ")[1] not in connector1:
                        connector1.append(p.split(" : ")[1])
            count = 0
            for co in connector1:
                newValue += co
                if len(connector1) - 1 != count:
                    newValue += " / "
                    count = count + 1

                dummyArray = []
                newValueList = (newValue.split(" / "))
                for newValueElement in newValueList:
                    if "LL_" in newValueElement:
                        dummyArray.append(newValueElement.replace("LL_","").lower())
                    elif len(newValueElement) != 0:
                        returnValues = parserTerminal(newValueElement.strip())
                        for Values in returnValues:
                            dummyArray.append(Values)

                finalValue = ""
                arrayCount = 0
                for Array in dummyArray:
                    finalValue += Array
                    if len(dummyArray) -1 != arrayCount:
                        finalValue += " / "
                        arrayCount = arrayCount + 1
            flag = False
            if k.split(" : ")[0] not in check:
                for line in open(parseFile,'r'):
                    if k.split(" : ")[0] in line:
                        flag = True
                        newString = (re.search('{(.*),', line))
                        cleanString = ((newString[1]).split(",")[0]).replace('"','')
                        print("\t{} : {}".format(cleanString, finalValue))
                            
                if flag is not True:
                    for line in open('./lib/cfg-parser.c','r'):
                        if k.split(" : ")[0] in line:
                            newString = (re.search('{(.*),', line))
                            cleanString = ((newString[1]).split(",")[0]).replace('"','')
                            cleanString2 = (newString[1]).split(",")[1].replace(" }","").strip()
                            if k.split(" : ")[0] == cleanString2:
                                print("\t{} : {}".format(cleanString, finalValue))

                        #ruleCounterPerDriver = ruleCounterPerDriver + 1
                check.append(k.split(" : ")[0])

       
        
        for m in Problems.keys():
            check2 = []
            flag = False
            for line in open(parseFile,'r'):
                if m in line:
                    flag = True
                    newString = (re.search('{(.*),', line))
                    print("\t{}".format(((newString[1]).split(",")[0]).replace('"','')))

            if flag is not True:
                for line in open('./lib/cfg-parser.c','r'):
                    if m in line:
                        flag = True
                        newString = (re.search('{(.*),', line))
                        print("\t{}".format(((newString[1]).split(",")[0]).replace('"','')))

            for b in Problems[m]:

                connector2 = []
                newValue2 = ""
                for y in Problems[m]:
                    if b.split(" : ")[0] == y.split(" : ")[0]:
                        if b.split(" : ")[1] not in connector2:
                            connector2.append(b.split(" : ")[1])
                        if y.split(" : ")[1] not in connector2:
                            connector2.append(y.split(" : ")[1])

                count2 = 0
                for co in connector2:
                    newValue2 += co
                    if len(connector2) - 1 != count2:
                        newValue2 += " / "
                        count2 = count2 + 1

                    dummyArray2 = []
                    newValueList2 = newValue2.split(" / ")
                    for newValueElement2 in newValueList2:
                        if "LL_" in newValueElement2:
                            dummyArray2.append(newValueElement2.replace("LL_","").lower())
                        elif len(newValueElement2) != 0:
                            returnValues2 = parserTerminal(newValueElement2.strip())
                            for Values2 in returnValues2:
                                dummyArray2.append(Values2)
                    finalValue2 = ""
                    arrayCount2 = 0
                    for Array2 in dummyArray2:
                        finalValue2 += Array2
                        if len(dummyArray2) - 1 != arrayCount2:
                            finalValue2 += " / "
                            arrayCount2 = arrayCount2 + 1

                if b.split(" : ")[0] not in check2:
                    for line in open(parseFile,'r'):
                        if b.split(" : ")[0] in line:
                            newString = (re.search('{(.*),', line))
                            cleanString = ((newString[1]).split(",")[0]).replace('"','')
                            print("\t\t{} : {}".format(cleanString, finalValue2))
                            #ruleCounterPerDriver = ruleCounterPerDriver + 1
                    check2.append(b.split(" : ")[0])
end = time.time()
print(end - start)

"""
drive: http
type: destination
         url : identifier / string
         user : identifier / string       
         user_agent : identifier / string 
         password : identifier / string   
         user_agent : identifier / string 
         headers : identifier / string    
         auth_header : identifier
         method : identifier / string
         body_prefix : identifier / string
         body_suffix : identifier / string
         delimiter : identifier / string
         body : identifier / string
         body_prefix : identifier / string
         frac_digits : number
         time_zone : identifier / string
         send_time_zone : identifier / string
         local_time_zone : identifier / string
         on_error : identifier / string
         log_fifo_size : number         throttle : number         persist_name : identifier / string
         tls
                 ca_dir : identifier / string
                 ca_file : identifier / string
                 cert_file : identifier / string
                 key_file : identifier / string
                 cipher_suite : identifier / string
                 use_system_cert_store : yes / on / no / off / number
                 ssl_version : identifier / string
                 peer_verify : yes / on / no / off / number
"""