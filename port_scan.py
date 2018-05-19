#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
import nmap
import multiprocessing
from datetime import datetime
from urlparse import urlparse

target_ports = [20, 21, 22, 23, 80, 81, 443, 445, 544, 873, 1080, 1433, 1434, 1521, 2100, 3306, 3389, 4440, 5671, 5672,
                5900, 5984, 6379, 7001, 8080, 8081, 8089, 8888, 9090, 9200, 11211, 15672, 27017, 50070]
PROCESS_COUNT = 50


def nmap_scanner(target_host):
    """
    对目标主机的指定断开进行扫描，返回扫描结果
    :param target_host:
    :return: [{'host': '192.168.1.1', 'banner': 'cpe:/o:linux:linux_kernel', 'port': 80, 'port_server': 'BusyBox http'},]
    """

    result_list = []
    port_scanner = nmap.PortScanner()
    try:
        # 对目标进行端口探测
        port_scanner.scan(target_host, ','.join('%s' % port for port in target_ports))
        # 遍历存活端口
        for i in port_scanner[target_host].all_tcp():
            if port_scanner[target_host]['tcp'][i]['state'] == 'open':
                port_server_data = {
                    'host': target_host,
                    'port': i,
                    'port_server': port_scanner[target_host]['tcp'][i]['product'],
                    'banner': port_scanner[target_host]['tcp'][i]['cpe'],
                }
                result_list.append(port_server_data)
    except Exception as e:
        print e
        print target_host, e
    return result_list


class MultiProcess:
    def __init__(self):
        self.target_list = []
        self.asset_id = ''
        self.asset_name = ''
        self.processes_count = PROCESS_COUNT

    def scan_pool(self):
        """
        不同目标多进程端口扫描，将结果更新到数据库中
        :return:
        """
        target_list = []
        for target in self.target_list:
            target_list.append(target.strip())
        scanner_pool = multiprocessing.Pool(processes=self.processes_count)
        # 目前只能等待一个资产库资产扫描完毕返回结果 出现意外中断 结果没有办法保存 后期要解决掉
        result = scanner_pool.map(nmap_scanner, target_list)
        scanner_pool.close()
        scanner_pool.join()
        if result:
            # 删除旧数据
            for scan_result in result:
                self.printinfo(scan_result)

    def start_port_scan(self, target_hosts):
        """
        从数据库中取出数据，调用start_pool函数
        :return:
        """

        for target_host in target_hosts:
            # 处理资产库中 以URL形式存在的资产
            if 'http://' in target_host or 'https://' in target_host:
                target_host = urlparse(target_host).netloc.split(':')[0]
                self.target_list.append(target_host)
            else:
                self.target_list = target_hosts
        self.scan_pool()

    def printinfo(self, data):
        if not isinstance(data, list):
            return None
        for i in data:
            if not isinstance(i, dict):
                continue
            for key in i:
                print("{}:{}".format(key, i[key]))
            print("**************************************\n")


def main():
    global target_ports, PROCESS_COUNT
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="targets", help="target host address")
    parser.add_option("-p", "--port", dest="port", help="special port")
    parser.add_option("--thread", dest="threads", help="threads number")
    options, args = parser.parse_args()
    targets = options.targets
    port = options.port
    threads = options.threads
    target_hosts = []
    if not targets:
        print("Not target host specialed!!!")
        exit(0)
    if "," in targets:
        target_hosts = targets.split(",")
    else:
        target_hosts.append(targets)

    if not port:
        port = target_ports
    else:
        port = port.split(",")
    target_ports = port
    if not threads:
        PROCESS_COUNT = threads
    print target_ports
    print target_hosts

    print("++++++++++ Scan Start! ++++++++++\n")
    start_date = datetime.now()
    start_port_scan = MultiProcess()
    start_port_scan.start_port_scan(target_hosts)
    scan_time = datetime.now() - start_date
    print("++++++++++ Scan Done! ++++++++++", scan_time.total_seconds())


if __name__ == '__main__':
    main()
    # nmap_scanner("192.168.1.1")
