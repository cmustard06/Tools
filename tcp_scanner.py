# /usr/bin/env python 
#coding:utf-8

__author__ = 'cmustard'
"""
TCP端口扫描
"""

import optparse
import socket
import threading
from sys import getdefaultencoding
def conScan(tarhost,tarport):
    "链接目标主机的端口，判断是否链接成功发送一些数据从而让目标主机返回一些数据"
    socket_tar = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #由于这里要使用多线程，如果不对这一部分加锁，那么输出顺序就会打乱，让人摸不着头脑
    #创建一个锁对象
    mlock=threading.Lock()
    mlock.acquire()
    try:
        socket_tar.connect((tarhost,tarport))
        socket.setdefaulttimeout(4)
        socket_tar.send("python test!!!\r\n")
        response  = socket_tar.recv(100)
        re= "[$$$]>>%s" %(str(response))
        print "[+] >>  tcp/open "+str(tarport) +re.decode('utf-8').encode(getdefaultencoding())
        
        

    except Exception as e:
        print "[-]>>  tcp/close  "+ str(tarport)+str(e)
    finally:
        socket_tar.close()
        #最后一定要释放锁，否则会成为死锁
        mlock.release()



def portScan(tarhost,tarport_list):
    "对目标主机的指定端口进行扫描，调用conScan来判断结果"
    
    try:
        #翻译的主机名IPv4地址格式。以字符串形式返回的IPv4地址，如'100.50.200.5“。
        #如果是一个IPv4地址的主机名，它原封不动地返回
        tarip = socket.gethostbyname(tarhost)
    except:
        print "不能解析域名，未知的主机 %s" % (tarhost)
        #提前结束该函数
        return 

    try:
        #socket.gethostbyaddr(ip_address)
        #返回一个三元组（hostname，aliaslist，ipaddrlist），支持IPv4和IPv6。
        tarname = socket.gethostbyaddr(tarip)
        print "Scan Result for : " + tarname[0]          #hostname

    except:
        print "Scan Result for :" + tarip

    for tarport in tarport_list:
        thread = threading.Thread(target=conScan,args=(tarhost,int(tarport)))
        thread.start()


def main():
    usage="usage:-H <target host> -p <target port1,target port2,....> "
    parser = optparse.OptionParser(usage)
    parser.add_option("-H",action="store",dest="tarhost",type="string",help="target host ip address")
    parser.add_option("-p",action="store",dest="tarport",type="string",help="The port number of the target host, if multiple ports are separated by a comma.")
    (options,args)=parser.parse_args()
    try:
        tarhost=options.tarhost
        tarport=options.tarport
        tarport_list=tarport.split(",")
    except Exception,e:
        print usage
        exit(0)
    portScan(tarhost,tarport_list)
  


if __name__=="__main__":
    main()
