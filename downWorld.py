# coding:utf-8

__author__ = 'cmustard'
"""
用于下载扫描器文档
"""

import subprocess
import sys
import os

if os.name !='posix':
    print "the system is not supported!!! Please change your system environment"
    exit(0)

try:
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    cookie = sys.argv[3]
    if start>end:
        end,start = start,end
except:
    print "help:\n  python downWorld start end cookie [path]"
    exit(0)

if len(sys.argv) == 5:
    path = sys.argv[4]
    # 更改当前路径
    try:
        os.chdir(path)
    except Exception as e:
        print "path is not exist!!"
        exit(0)

errorId = set()





for id in xrange(start, end+1):
    print "[==>]starting downloading id=%s"%id
    command ="""curl -JOL "https://www.aisec.com/aiscanner/report.php?id=%s&tpl=word" --cookie "%s" """%(id,cookie)
    try:
        subprocess.check_call(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except subprocess.CalledProcessError as e:
        print "[==!]id=%s error"%id
        errorId.add(id)
        continue
    except Exception as e:
        print e
        print "[==!]id=%s error"%id
        errorId.add(id)
        continue

if len(errorId)>0:
    print "[==!]not finish down:"
    print errorId

print "finish"
