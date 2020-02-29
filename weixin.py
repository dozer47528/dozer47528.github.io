#!python
# -*- coding: utf-8 -*-

import sys
import re

file_name = sys.argv[1]

file = open(file_name, 'r')

content = file.read()

content = re.sub('---.*?---', '', content, flags=re.S)

content = re.sub('<!--more-->', '', content)

# Replace image with base64
for img_exp in re.findall("!\[[^\]]*\]\([^\)]*\)",content):
    img_path = img_exp[:-1].split("(")[1][1:]
    with open(img_path, 'r') as img_file:
        img_base64 = img_file.read().encode('base64').replace("\n", "")
        img_ext = img_path.split(".")[-1]
        img_html = '<img src="data:image/%s;base64, %s" />' % (img_ext, img_base64)
        content = content.replace(img_exp, img_html)

# Replace external link
for url in re.findall("\[[^\]]*\]\([^\)]*\)",content):
    url_title, url_link = url[1:-1].split("](")
    if str(url_link).startswith("/"):
        url_link = "https://www.dozer.cc" + url_link
    content = content.replace(url, " %s %s " % (url_title, url_link))

content += '\n&nbsp;\n\n👇更好的排版请点击原文连接👇'

print content
