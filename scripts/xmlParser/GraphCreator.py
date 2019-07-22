import ObjectCreator as parser

data = parser.xmltoobject()

def EdgeAdder():
    for i in data:
        count = 1
        for symbol in i.rhs:
            if symbol is not None:
                parser.G.add_edge(i.lhs, symbol, weight=count )
                count = count + 1
