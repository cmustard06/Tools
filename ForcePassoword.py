# /usr/bin/env python
#coding:utf-8

__author__ = 'cmustard'
"""
暴力破解加盐密码
"""

import crypt
import threading
import os
import sys


def load_dict(dict_path):
    "加载字典,返回字典队列"
    #判断字典是否存在
    if not os.path.exists(dict_path):
        print "not exists file"
        sys.exit(0)
    with open(dict_path,'r') as f:
        f.seek(0)
        word_list = f.readlines()
    #判断字典是否为空
    if not len(word_list):
        print "dictionary is null"
        sys.exit(0)
    dict_list=[]
    for word in word_list:
        dict_list.append(word.strip('\n'))

    return dict_list




def bruster(dict_list,bruster_word):
    "输出解密结果"
    for i in dict_list:
        salt = bruster_word[0:2]
        crypt_word = crypt.crypt(i,salt)
        if crypt_word == bruster_word:
            print "[+]>>>>success!!password is %s" % i
            break
    else:
        print "Faild"

def main():
    while True:
        try:
            dict_path=raw_input('dictionary path:')
            secu_word=raw_input('加密的字符串:')
            break
        except:
            print "please try again"
    dict_list = load_dict(dict_path)
    bruster(dict_list,secu_word)
    


if __name__ =="__main__":
    main()
