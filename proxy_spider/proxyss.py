import socket
from socket import error
import threading
import random
import time

localtime = time.asctime(time.localtime(time.time()))
#http://ip.ws.126.net/ipquery
class ProxyServerTest():
    def __init__(self, proxyip):
    # 本地socket服务
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxyip = proxyip

    def run(self):
        try:
            # 本地服务IP和端口
            self.ser.bind(('127.0.0.1', 9999))
            # 最大连接数
            self.ser.listen(20)
        except error as e:
            print("[-]The local service : " + str(e))
            return "[-]The local service : " + str(e)

        while 1:
            try:
                # 接收客户端数据
                client, addr = self.ser.accept()
                print('[*]accept %s connect' % (addr,))
                data = client.recv(1048576)
                if not data:
                    #break
                    continue
                print ('[*' + localtime + ']: Accept data...')
            except error as e:
                print("[-]Local receiving client : " + str(e))
                return "[-]Local receiving client : " + str(e)

            while 1:#第一个坑点，这里的while循环导致，接收到data一直在上面循环，发不下去,缩进！
                    # 目标代理服务器，将客户端接收数据转发给代理服务器
                mbsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                iplen = len(self.proxyip)
                proxyip = self.proxyip[random.randint(0, iplen - 1)]
                print("[!]Now proxy ip:" + str(proxyip))
                prip = proxyip[0]
                prpo = proxyip[1]
                try:
                    mbsocket.settimeout(5)
                    mbsocket.connect((prip, prpo))
                except:
                    print("[-]RE_Connect...")
                    continue
                #break
              # except :
              #     print("[-]Connect failed,change proxy ip now...")
              #    pass
                try:
                    mbsocket.send(data)#将本地监听9999端口的数据发送给代理服务器
                except error as e:
                    print("[-]Sent to the proxy server : " + str(e))
                    return "[-]Sent to the proxy server : " + str(e)

                #while True:
                try:
                    # 从代理服务器接收数据，然后转发回客户端
                    data_1 = mbsocket.recv(1048576)
                    if not data_1:
                        continue#第二个坑点，原代码使用break导致一次请求后就直接退出了整个循环，关闭连接
                    print('[*' + localtime + ']: Send data...')
                    client.send(data_1)
                    #break
                except socket.timeout as e:
                    print(proxyip)
                    print("[-]Back to the client : " + str(e))
                    continue
                    #break#第三个坑点，原代码continue只是跳出当前循环
                break
    # 关闭连接
                client.close()
                mbsocket.close()

def Loadips():
    print("[*]Loading proxy ips..")
    ip_list = []
    ip = ['ip', 'port']
    with open("check_proxy_ok.txt") as ips:
        lines = ips.readlines()
    for line in lines:
        ip[0], ip[1] = line.strip().split(":")
        ip[1] = eval(ip[1])
        nip = tuple(ip)
        ip_list.append(nip)
    return ip_list

def main():
    print('''*Atuhor : Guoker.
        ''')
    ip_list = Loadips()
    #   ip_list = [('118.89.148.92',8088)]
    #   ip_list = tuple(ip_list)
    try:
        pst = ProxyServerTest(ip_list)
        # 多线程
        t = threading.Thread(target=pst.run, name='LoopThread')
        print('[*]Waiting for connection...')
        # 关闭多线程
        t.start()
        t.join()
    except Exception as e:
        print("[-]main : " + str(e))
        return "[-]main : " + str(e)

if __name__ == '__main__':
    main()