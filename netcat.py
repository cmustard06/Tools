#coding:utf-8

__author__= 'cmustard'
"""
python版netcat
"""

import sys
import socket
import getopt
import subprocess
import threading


#定义一些全局变量
listen = False
command = False
upload = False
excute = ""
target = ""
upload_destination = r""
port = 0

def usage():
    print "BHP Net Tool"
    print 
    print "Usage:netcat.py -t  target_host  -p  port"
    print "-l --listen\n\t\t\t-listen  on [host]:[port] for incomming connection"
    print "-e --excute=file_to_run\n\t\t\t-excute the given file upon receiving a connection"
    print "-c --command\n \t\t\t-initialize a conection shell"
    print "-u --upload=destination\n \t\t\t-upon receiving connection upload a file and write to [destination]"
    print 
    print 
    print "Example:"
    print "netcat.py -t 192.168.0.1 -p 5555 -l -c"
    print "netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "netcat.py -t 192.168.0.1 -p 5555 -l -e='cat /etc/passwd'"
    print "echo 'ABCDEFGI' | ./netcat.py -t 192.168.11.12 -p 135"
    sys.exit(0)





def client_sender(buffer):
    global target
    global port
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #connecting
    try:
        client.connect((target,int(port)))

        if len(buffer):
            client.send(buffer)

        while True:
            #现在等待数据回传
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response+=data

                if recv_len < 4096:
                    break

            print response,

            #等待更多的输入
            buffer = raw_input("")
            buffer+="\n"

            #发出去
            client.send(buffer)

    except:
        print "[*]Exception!Exiting"
        #关闭链接
        client.close()









def server_loop():
    global target
    global port
    #如果没有定义目标，那么我们监听所有端口
    if not len(target):
        target="0.0.0.0"

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,int(port)))

    server.listen(5)

    while True:
        client_socket,addr = server.accept()

        #分拆一个线程处理新的客户端
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()








def run_command(command):
    #换行
    command = command.rstrip()
    
    #运行命令并将输出返回
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output = "Failed to excute command.\r\n"

    #将输出发送
    return str(output)







def client_handler(client_socket):
    global upload
    global excute
    global command

    #检查上传文件
    if len(upload_destination):
        #读取所有的字符并写下目标
        file_buffer=""

        #持续读取数据直到没有符合的数据
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer+=data

            #现在我们接受这些数据并将他们写出来
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(buffer)
            file_descriptor.close()

            #确认文件已经写出来
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Faild to save file to %s \r\n" %upload_destination)

    #检查执行命令
    if len(excute):

        #运行命令
        output = run_command(excute)

        client_socket.send(output)

    #如果需要一个命令行shell,那么我们进入另一个循环
    if command:
        while True:
            #跳出一个窗口
            client_socket.send("<BPH:#> ")

            #现在我们接受文件直接发现换行符（enter key）
            cmd_buffer =""
            while "\n" not in cmd_buffer:
                cmd_buffer+= client_socket.recv(1024)
                #返回命令输出
                response = run_command(cmd_buffer)

                #返回响应数据
                client_socket.send(str(response))










def main():
    #从命令行接受参数并进行判断
    if not len(sys.argv[1:]):
        usage()
    global listen
    global command
    global excute
    global target
    global port
    global upload_destination
    #读取命令行参数
    try:
        opts,args = getopt.getopt(sys.argv[1:],'hle:t:p:cu:',["help","listen=","excute=","target=","port=","command","upload="])

    except getopt.GetoptError ,err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-c","--command"):
            command = True
        elif o in ("-l","--listen"):
            listen = True

        elif o in ("-e","--excute"):
            excute=a

        elif o in ("-t","--target"):
            target = a

        elif o in ('-p',"--port"):
            port = a

        elif o in ("-u","--upload"):
            upload_destination = a
        else:
            assert False,"unhandled option"
        
        #我们是进行监听还是仅从标准输入发生数据？
    if not listen and len(target) and port>0:
        #从命令行读取内存数据
        #这里将阻塞，所以不在向标准输入发送数据时  发送CTRL+D
        #这个sys.stdin.readline()[:-1](由于最后一个是换行符)与raw_input（）等价
        buffer = sys.stdin.read()

        #发送数据
        client_sender(buffer)

    # 我们开始监听并准备上传文件，执行命令
    # 放置一个反弹Shell
    # 取决于上面的命令行选项
    if listen:
        server_loop()
    





if __name__ == '__main__':
    main()
