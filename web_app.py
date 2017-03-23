#coding:utf-8

__author__ = 'cmustard'
"""
扫描开源项目的目录是否存在
"""
import os
import urllib.request, urllib.error, urllib.parse
import threading
import queue

target = "http://www.abner.com//Joomla_3.5.1"
# 本机目录结构
directory = r"c:d\wamp\www\Joomla_3.5.1"
#filter
filters = ['.css',".gif",".png",".jpg"]
#改变当前目录
os.chdir(directory)

#加入队列
web_file = queue.Queue()
#扫描本机目录
for ori_dir,sub_dir,filename in os.walk("."):
    for file in filename:
        remote_path = "%s\\%s"%(ori_dir,file)
        if remote_path.startswith("."):
            remote_path=remote_path[1:]
        if os.path.splitext(remote_path)[1]  not in filters:
            web_file.put(remote_path)

def test_remote(web_file):
    global web_file

    url = "%s/%s"%(target,web_file.get())
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        content = response.read()

        print("[%d] => %s" % (response.code,web_file))

        response.close()

    except urllib.error.HTTPError as e:
        print("Faild %s" % e.code)



for i in range(10):
    print("Spawning thread:%d" % i)
    thread=threading.Thread(target=test_remote)
    thread.start()
    
