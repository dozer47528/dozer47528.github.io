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
(opts, args) = parser.parse_args()

if __name__ == "__main__":
    if not opts.path:
        print "--path is required"
        print parser.usage
        exit(-1)

    file = open(opts.path, 'r')

    content = file.read()

    base_url = "https://www.dozer.cc"

    content = re.sub('---.*?---', '', content, flags=re.S, count=1)

    content = re.sub('<!--more-->', '', content)

    content = re.sub('\]\(/', '](%s/' % base_url, content)

    print content