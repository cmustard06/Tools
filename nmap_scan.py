# /usr/bin/env python

#coding:utf-8

import nmap
import optparse
def nmapScan(tarhost,tarport):
    nmscan=nmap.PortScanner()
    nmscan.scan(tarhost,tarport)
    state = nmscan[tarhost]['tcp'][int(tarport)]['state']
    print "[*]"+tarhost+"tcp/"+str(tarport)+" "+state

def main():
    usage="nmap_scan.py [option]:-H 127.0.0.1 -p 22.23.24"
    parser = optparse.OptionParser(usage)
    parser.add_option("-H","--tarhost",action="store",dest="tarhost",type="string",help="target host ip")
    parser.add_option("-p","--tarport",action="store",dest="tarport",type="string",help="a")
    
    (options,args)=parser.parse_args()
    tarhost=options.tarhost
    tarport=options.tarport
    
    
    if (tarhost == None) | (tarport == None):
        print usage
        exit(0)
    tarports=tarport.split(',')
    for tarport in tarports:
        nmapScan(tarhost,tarport)


    pass


if __name__ == '__main__':
    main()
