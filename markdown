#!python
# -*- coding: utf-8 -*-

import sys
import re
from optparse import OptionParser


usg = \
    '''
    ./markdown --path ./_posts/2020-02-28-graceful-start-and-shutdown.md --img-use-oss
    '''

parser = OptionParser(usage=usg)
parser.add_option('--path', dest='path', help='Target page')
parser.add_option('--img-use-oss', dest='img_use_oss', action="store_true", default=False, help='Use oss to fix Weixin can not fetch image issue.')
(opts, args) = parser.parse_args()

if __name__ == "__main__":
    if not opts.path:
        print "--path is required"
        print parser.usage
        exit(-1)

    file = open(opts.path, 'r')

    content = file.read()

    base_url = "https://www.dozer.cc"

    oss_url = "http://dozer47528-dl.oss-cn-shanghai.aliyuncs.com"

    content = re.sub('---.*?---', '', content, flags=re.S, count=1)

    content = re.sub('<!--more-->', '', content)

    if opts.img_use_oss:
        content = re.sub('\]\(/uploads/', '](%s/' % oss_url, content)

    content = re.sub('\]\(/', '](%s/' % base_url, content)

    print content
