import xml.etree.ElementTree as syslog

filePath = input('Please specify file path. (Full path) :')
tree = syslog.parse(filePath)
root = tree.getroot()


def lhsfinder(nameoflhs):
    lhslist = []
    for rule in root.iter('rule'):
        lhs = rule.find('lhs').text
        lhslist.append(lhs)
        res_list = []
        for i, value in enumerate(lhslist):
            if nameoflhs == value:
                res_list.append(i)
    return res_list


def xmlparser():
    for rule in root.iter('rule'):
        number = rule.get('number')
        print("\nnumber:{}".format(number))
        usefulness = rule.get('usefulness')
        print("usefulness:{}".format(usefulness))
        lhs = rule.find('lhs').text
        print("lhs:{}".format(lhs))
        for rhs in rule.iter('rhs'):
            symbol = rhs.findall('symbol')
            print("rhs:")
            for i in symbol:
                if i is not None:
                    returnable = lhsfinder(i.text)
                    if len(returnable) != 0:
                        print("{}:{}".format(returnable, i.text))
                    else:
                        print("[x] {}".format(i.text))


xmlparser()
