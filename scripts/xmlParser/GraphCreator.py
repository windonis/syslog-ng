import ObjectCreator as parser

data = parser.xmltoobject()

def EdgeAdder():
    for i in data:
        count = 1
        for symbol in i.rhs:
            if symbol is not None:
                terminalCheck = parser.lhsfinder(symbol)
                if len(terminalCheck) == 0:
                    parser.G.add_edge(i.number, symbol, weight=count )
                    count = count + 1
                else:
                    for d in terminalCheck:
                        parser.G.add_edge(i.number , d , weight=count )
                        count = count + 1