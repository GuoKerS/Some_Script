#-*- coding:utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cmdtext = 'getenforce'#检查selinux状态  enforcing开启   disabled关闭
#临时关闭setenforce 0
for i in open('ssh.txt'):
    if '#' in i[0]:
        pass
    else:
        ssh_list = i.strip().split(':')
        try:
            ssh.connect(hostname=ssh_list[0], port=ssh_list[1], username=ssh_list[2], password=ssh_list[3])
            stdin, stdout, stderr = ssh.exec_command(cmdtext)
            res, err = stdout.read(), stderr.read()
            result = res if res else err
            #log = ssh_list[0]+'>>'+result+'\n'
            if 'Enforcing' in result:
                print ssh_list[0],'Not install G01'
                tmp_selinux = raw_input('Whether to close SELinux?(yes/no)')
                if tmp_selinux == 'yes':
                    stdin, stdout, stderr = ssh.exec_command('setenforce 0')
                    res, err = stdout.read(), stderr.read()
                    result = res if res else err
                    print result,'setenforce 0'
                elif tmp_selinux == 'no':
                    print
            elif 'Disabled' in result:
                print ssh_list[0],'SELinux is off and G01 can be installed'
            elif 'Permissive' in result:
                print ssh_list[0],'Permissive and G01 can be installed'
            # with open('ok_log.txt','a') as f:
            #     f.write(log)
            ssh.close()
        except:
            print ssh_list[0],'ssh Not connetc'
