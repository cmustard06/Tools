#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-25 09:36:44
# @Author  : cmustard (cmustard06@gmail.com)
# @Link    : http://www.cmustard.com
# @Version : $Id$
# @description: 用于检测网站是否有web系统

import urllib2
import threading
import time
import logging
import Queue
import ssl
import sys
import time

queue = Queue.Queue()
total = 0  # 有效的网站数量
lock = threading.Lock()
current = 0  # 当前已经检测的网站数量
number = 0  # 需要检测的目标网站数量
logFile = "logs.log"  # 日志存储路径
# 全局关闭ssl验证
ssl._create_default_https_context = ssl._create_unverified_context


def view_bar(num, total):
	# 进度条
	rate = float(num) / float(total)
	rate_num = int(rate * 100)
	r = '\r%d%%' % (rate_num, )
	sys.stdout.write(r)   # 做进度条用的
	sys.stdout.flush()    # flush这个缓冲区，意味着它将缓冲区中一切写入数据都flush
	
	
def getLogger(isRecord=False):
	# 线程安全的loggger日志处理器
	logger = logging.Logger("check-ip")
	logger.setLevel(logging.DEBUG)
	formatterch = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
	formatterfh = logging.Formatter("%(message)s")
	ch = logging.StreamHandler()
	fh = logging.FileHandler("print2.log")
	
	ch.setFormatter(formatterch)
	fh.setFormatter(formatterfh)
	
	logger.addHandler(ch)
	if isRecord:
		logger.addHandler(fh)
	
	return logger


def getUrl(filename):
	# 从文件中获取目标网站
	global number
	urls = []
	with open(filename, "r") as f:
		rawUrls = f.readlines()
	for url in rawUrls:
		temp = str(url).replace("\n", "")
		urls.append(temp)
	number = len(urls)
	return urls


def check(url):
	# 对目标网站进行检测，查看是否能够访问
	global total
	if not url.startswith("http") and not url.startswith("https"):
		url = "http://" + url
	try:
		req = urllib2.Request(url)
		req.add_header("User-Agent",
					   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
		req.add_header("Referer", "http://www.baidu.com")
		req.add_header("Cookie", "*****")
		# 关闭长连接
		req.add_header("Connection", "close")
		# 超时25s，可以适当调节
		html = urllib2.urlopen(req, timeout=25)
		logger = getLogger(isRecord=True)
		logger.debug("[==>] " + url + " is-ok!!!")
		# 加锁
		lock.acquire()
		total += 1
		lock.release()
	except urllib2.HTTPError as e:
		if e.code >= 400 and e.code < 599.:
			logger = getLogger(isRecord=True)
			logger.debug("[==>] " + url + " is-ok!!! " + str(e.code))
			lock.acquire()
			total += 1
			lock.release()
			e.close()
		else:
			logger = getLogger()
			logger.debug("[***] " + url + "  not access!!!  " + str(e.code))
			e.close()
	except Exception as e:
		if "sslv3" in str(e):
			logger = getLogger(isRecord=True)
			# 需要手工确认
			logger.debug("[==>] " + url + " need-ok!!! " + str(e))
		else:
			logger = getLogger()
			logger.debug("[***] " + url + "  not access!!!  " + str(e))


def run():
	# 运行，验证目标网站
	global total, current
	while not queue.empty():
		url = queue.get()
		lock.acquire()
		current += 1
		view_bar(current, total=number)
		lock.release()
		check(url)
		

def main():
	global number
	global logFile
	try:
		filename = raw_input("please input file path:")
		threadNum = raw_input("please threads number (default 100):")
		log = raw_input("pleaser log filename or path(default logs.log):")
	except Exception as e:
		print("appear error!!!")
		exit(0)
	if threadNum is "":
		threadNum = 100
	else:
		threadNum = int(threadNum)
	if log is not "":
		logFile = log
	
	# print filename
	# print threadNum
	# print logFile
	# exit(0)
	urls = getUrl(filename)
	for url in urls:
		queue.put(url)
	thList = []
	for i in range(threadNum):
		th = threading.Thread(target=run)
		thList.append(th)
	for th in thList:
		th.start()
	
	for th in thList:
		th.join()
	
	print
	print total/float(number)*100
	print total
	print "[###] finish!!!"


if __name__ == '__main__':
	#check("106.2.201.252")
	# print getUrl("result.txt")
	main()
