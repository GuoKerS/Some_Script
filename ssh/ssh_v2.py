#-*- coding:utf-8 -*-
import paramiko
# 实例化一个transport对象
trans = paramiko.Transport(('192.168.80.129', 22))
# 建立连接
trans.connect(username='root', password='guoker97')

# 将sshclient的对象的transport指定为以上的trans
ssh = paramiko.SSHClient()
ssh._transport = trans
# 执行命令，和传统方法一样
stdin, stdout, stderr = ssh.exec_command('uname -a')
print(stdout.read().decode())
stdin, stdout, stderr = ssh.exec_command('ifconfig')
print(stdout.read().decode())
# 关闭连接
trans.close()