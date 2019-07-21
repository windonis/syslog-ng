#Bison create xml file current directory.
import os
import shutil

path = os.getcwd()
os.chdir(path)


cmd = 'bison -x /var/syslog-ng/modules/http/http-grammar.y > /dev/null 2>&1'
os.system(cmd)

shutil.move('http-grammar.tab.c','./scripts/xmlParser')
shutil.move('http-grammar.xml','./scripts/xmlParser/')


import ObjectCreator as parser
import xml.etree.ElementTree as ET

#Parse http-grammar.xml file only include <rules> ... </rules> part.
context = ET.iterparse('./scripts/xmlParser/http-grammar.xml', events=('end', ))
for event, elem in context:
    if elem.tag == "rules":
        #Output file Father.xml
        filename = format("./scripts/xmlParser/Father" + ".xml")
        with open(filename, 'wb') as f:
            f.write(ET.tostring(elem))


#Creating xml file with my RULE's array.
data = parser.xmltoobject()
#This xml file named Son.xml
f = open('./scripts/xmlParser/Son.xml', 'w')
f.write('<rules>\n')
for d in data:
    f.write('      <rule number="{}" usefulness="{}">\n'.format(d.number,d.usefulness))
    f.write('        <lhs>{}</lhs>\n'.format(d.lhs))
    f.write('        <rhs>\n')
    if (len(d.rhs) != 0):
        for x in d.rhs:
            f.write('          <symbol>{}</symbol>\n'.format(x))
    else:
        f.write('          <empty />\n')
    f.write('        </rhs>\n')
    f.write('      </rule>\n')
f.write('    </rules>\n')
f.write('    ')


