#!python
# -*- coding: utf-8 -*-

import sys
import re
from optparse import OptionParser


usg = \
    '''
    worker.py --path ./_posts/2020-02-28-graceful-start-and-shutdown.md --weixin
    '''

parser = OptionParser(usage=usg)
parser.add_option('--path', dest='path', help='Target page')
parser.add_option('--weixin', dest='weixin', action="store_true", default=False, help='Convert for WeChat')
(opts, args) = parser.parse_args()

if __name__ == "__main__":
    if not opts.path:
        print "--path is required"
        print parser.usage
        exit(-1)

    file = open(opts.path, 'r')

    content = file.read()

    base_url = "https://www.dozer.cc"

    link =  base_url + re.search('permalink:\s*(.*)', content).group(1)

    content = re.sub('---.*?---', '', content, flags=re.S, count=1)

    content = re.sub('<!--more-->', '', content)

    content = re.sub('\]\(/', '](%s/' % base_url, content)

    if opts.weixin:
        content += '\n&nbsp;\n\n👇更好的排版请点击原文连接👇'
    else:
        content += '\n&nbsp;\n\n源地址:[{link}]({link})'.format(link=link)

    print content