#-*- coding:utf-8 -*-
import paramiko
'''
paramiko 2.4.2 依赖 cryptography,而大于2.5会有一些弃用api
pip uninstall cryptography==2.5
pip install cryptography==2.4.2
'''
ssh = paramiko.SSHClient()  # 创建SSH对象
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
#ssh.connect(hostname='192.168.109.136', port=22, username='root', password='guoker')  # 连接服务器
cmdtext = 'uname -a'

for i in open('ssh.txt'):
    if '#' in i[0]:
        pass
    else:
        ssh_list = i.strip().split(':')
        try:
            ssh.connect(hostname=ssh_list[0], port=ssh_list[1], username=ssh_list[2], password=ssh_list[3])
            stdin, stdout, stderr = ssh.exec_command('uname -a')
            res, err = stdout.read(), stderr.read()
            result = res if res else err
            log = ssh_list[0]+'>>'+result
            print ssh_list[0],'=+=+=+=+=+=>>ok'
            with open('ok_log.txt','a') as f:
                f.write(log)
            ssh.close()
        except:
            print ssh_list[0],'ssh Not connetc'
            log = ssh_list[0]+'******!!!!!******>>No'
            with open('no_log.txt','a') as f:
                f.write(log)
            ssh.close()
# stdin为输入的命令
# stdout为命令返回的结果
# stderr为命令错误时返回的结果
#stdin, stdout, stderr = ssh.exec_command('whoami')  # 执行命令并获取命令结果

# res, err = stdout.read(), stderr.read()
# result = res if res else err
# print(result)
# ssh.close()  # 关闭连接