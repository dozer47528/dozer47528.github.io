# -*- coding: utf-8 -*-

import sys
import re
import markdown

reload(sys)
sys.setdefaultencoding('utf-8')

file_name = sys.argv[1]

file = open(file_name, 'r')

content = file.read()

content = re.sub('---.*---', '', content, flags=re.S)

content = re.sub('<!--more-->', '', content)

content = re.sub('\]\(/uploads/', '](http://www.dozer.cc/uploads/', content)

content += '\n&nbsp;\n\n👇更好的排版请点击原文连接👇'

content = unicode(content, "utf-8")

content = markdown.markdown(content)

content = re.sub('</h3>', '</b></p>', content)
content = re.sub('</h4>', '</b></p>', content)
content = re.sub('</h5>', '</b></p>', content)

content = re.sub('<h3>', '<p style="font-size:20px;"><b>', content)
content = re.sub('<h4>', '<p style="font-size:18px;"><b>', content)
content = re.sub('<h5>', '<p><b>', content)

print content
