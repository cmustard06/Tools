# coding:utf-8

__author__ = 'cmustard'
"""
用于下载扫描器文档
"""

import subprocess
import sys
import os


def main():
    if os.name !='posix':
        print "the system is not supported!!! Please change your system environment"
        exit(0)
    try:
        url = raw_input("Please input aiscanner address,ep http://192.168.1.1/:")
        start = input("Please input start id:")
        end = input("Please input end id:")
        cookie = raw_input("Please input login cookie:")
        if start>end:
            end,start = start,end
    except:
        print "help:\n  python downWorld start[int] end[int] cookie [path]"
        exit(0)
    path = raw_input("Please input save path(default is chdir):")
    print "path"+path
    if path is not "":
        # 更改当前路径
        try:
            os.chdir(path)
            #print os.getcwd()
        except Exception as e:
            print "path is not exist!!"
            exit(0)
    # 无法下载的world文档
    errorId = []

    for id in xrange(start, end+1):
        # 下载
        print "[==>]starting downloading id=%s"%id
        command ="""curl -JOL "%s/aiscanner/report.php?id=%s&tpl=word" --cookie "%s" """%(url,id,cookie)
        # print command
        try:
            subprocess.check_call(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        except subprocess.CalledProcessError as e:
            print "[==!]id=%s error"%id
            errorId.append(id)
            continue
        except Exception as e:
            print e
            print "[==!]id=%s error"%id
            errorId.append(id)
            continue

    if len(errorId)>0:
        print "[==!]not finish down:"
        print errorId

    print "finish"

if __name__ == '__main__':
    main()