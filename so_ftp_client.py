'''
name:songbin
Email:xxxxx
introduce: ftp文件服务器_客户端
env:python3.5 
'''

from socket import *
import os,sys
import signal
import time

#基本文件操作功能
class FtpClient(object):
    def __init__(self,s):
        self.s=s
    def do_list(self):
        self.s.send(b'L')   #发送请求
        #等待回复
        data=self.s.recv(1024).decode()
        if data=='OK':
            data=self.s.recv(4096).decode()
            files=data.split("#")
            for file in files:
                print(file)
            print("文件列表展示完毕\n")
        else:
            print(data)   #即失败的原因
    def do_get(self):
        file_name=input("请输入文件名")
        self.s.send(("G "+file_name).encode())
        data0=self.s.recv(1024).decode()
        if data0=='OK':
            f=open(file_name,'wb')

            while True:
                data=self.s.recv(1024)
                if not data:    # if data ==b"##"
                    break
                f.write(data)
            f.close()
        else:
            print(data0)
    def do_quit(self):
        self.s.send(b'Q')


#网络连接
def main():
    if len(sys.argv)<3:
        print("argv is error")
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)

    s=socket()
    try:
        s.connect(ADDR)
    except:
        print("连接失败")
        return

    ftp=FtpClient(s)   #类对象
    while True:
        print("=============命令选项=============")
        print("============   list   =============")
        print("===========  get file =============")
        print("===========   put file=============")
        print("===========     quit  =============")

        cmd=input("请输入命令>>")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd.strip() == 'get':
            ftp.do_get()
        elif cmd.strip() =='quit':
            ftp.do_quit()
            s.close()
            sys.exit("谢谢使用")
        else:
            print("请输入正确命令")
            continue

if __name__=='__main__':
    main()
