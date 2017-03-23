#coding:utf-8
__author__ = 'cmustard'

"""
网页目录扫描
"""

import os
import Queue
import urllib2
import urllib
import threading


#目标网址
target = "http://www.konzern.com.cn"

#爆破的时候需要对消息头进行一些设置
header_ua = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"}

#字典位置
dict_file = r'dict.txt'

#如果网络连接突然中断或者目标网站中断运行
#则我们设置的一些内置函数可以让我们恢复暴力破解会话
#这可以通过让resume变量接上 中断前最后一个尝试暴力破解的路径来轻松实现
#这里可以采用手动输入这个断点位置
resume = None


#导入字典
def build_dict(dict_file):
    #读入字典文件
    with open(dict_file,'r') as f:
        dict_list = f.readlines()

    found_resume=False
    #建立队列
    words_queue = Queue.Queue()

    for word in dict_list:
        '如果存在断点,那么首先通过resume与word比较，将文件中的数据重新遍历到断点，'
        '然后输出这个断点，将found_resume置为True，进行下一步将数据导入到队列中'
        if resume is not None:    
            if found_resume:        #当产生断点后，这是为了建立新的队列
                words_queue.put(word)
            else:                   
                if word == resume:   #判断遍历字典的位置是否到达了上一次的断点处
                    found_resume=True
                    print "Resuming wordlist from %d" % resume 

        else:
            words_queue.put(word)

    return words_queue

#开始爆破
def dir_bruter(words_queue,extensions=None):
    "extensions 参数类型是一个列表['.php','.asp']"
    while not words_queue.empty():
        attempt = words_queue.get()

        #创建一个可以尝试爆破的列表
        attempt_list = []
        #先检查文件是否有扩展名，如果没有
        #就是我们需要暴力破解的路径

        #根据字典的不同，这些功能需要进行改变
        if attempt.startswith('/'):
            attempt=attempt[1:]
        if '.' not in attempt:
            attempt_list.append('%s'%attempt)   #将可能的路径地址加入列表中

        else:                                     #队列中文件包含扩展名
            attempt_list.append('%s'%attempt)    #将可能的例如.php文件路径放入列表中

        #如果我们自己想暴力添加扩展名
        if extensions:

            for extension in extensions:
                if not attempt.endswith("extension"):

                    attempt_list.append("%s%s"%(attempt,extension))
                else:
                    continue

        #迭代我们要尝试的文件列表
        for brute in attempt_list:
            #传这个参数name=c&id=2你就会发现有问题了。加上quote就不会出问题了,就是将特殊字符转义 
            #编码：urllib.quote(string[, safe])，除了三个符号“_.-”外，将所有符号编码，后面的参数safe是不编码的字符，
            #使用的时候如果不设置的话，会将斜杠，冒号，等号，问号都给编码了。
            url = "%s/%s"%(target,urllib.quote(brute,"//?:="))
            try:
                r = urllib2.Request(url.rstrip('\n'),headers=header_ua)

                response = urllib2.urlopen(r) 

                if len(response.read()):
                    
                    print "[%d] => %s" %(response.code,url)

            except urllib2.URLError as e:
                #hasattr(object,string)判断object中是否有string这个属性
                if hasattr(e,'code') and e.code !=404:
                    print "!!! %d => %s" %(e.code,url)
                    pass


word_queue = build_dict(dict_file)

extensions =[".php"]

for i in range(10):
    t = threading.Thread(target=dir_bruter,args=(word_queue,))
    t.start()







    
