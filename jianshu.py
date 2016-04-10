# -*- coding: utf-8 -*-

import sys
import re

file_name = sys.argv[1]

file = open(file_name, 'r')

content = file.read()

link = "http://www.dozer.cc" + re.search('permalink:\s*(.*)', content).group(1)

content = re.sub('---.*---', '', content, flags=re.S)

content = re.sub('<!--more-->', '', content)

content = re.sub('\]\(/uploads/', '](http://www.dozer.cc/uploads/', content)

content += '\n&nbsp;\n\n源地址:[{link}]({link})'.format(link=link)

print content
