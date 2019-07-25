import time
import paramiko

cmdtext = 'id'

def verification_ssh(host,username,password,port,root_pwd,cmd):

    s=paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname = host,port=int(port),username=username, password=password)
    if username != 'root':
        ssh = s.invoke_shell()
        time.sleep(0.1)
        ssh.send('su -\n')
        buff = ''
        while not buff.endswith('Password: '):
            resp = ssh.recv(9999)
            buff +=resp
        ssh.send(root_pwd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            buff +=resp
        ssh.send(cmd)
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            buff +=resp
        s.close()
        result = buff
    else:
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.read()
        s.close()
    return result
#hostname=ssh_list[0], port=ssh_list[1], username=ssh_list[2], password=ssh_list[3]
if __name__ == "__main__":
    for i in open('ssh.txt'):
        if '#' in i[0]:
            pass
        else:
            ssh_list = i.strip().split(':')

            result = verification_ssh(host=ssh_list[0], username=ssh_list[2],password=ssh_list[3],port=ssh_list[1],root_pwd=ssh_list[4],cmd=cmdtext)
            if 'Install G01 success' in result:
                print ssh_list[0],'Install G01 Success!'
                with open('install_log.txt','a') as f:
                    text = ssh_list[0]+"-----------------------\n"+result+"-----------------------\n"
                    f.write(text)
            elif 'FAILED' in result:
                print ssh_list[0],'FAILED'
                with open('FAILED_log.txt', 'a') as f:
                    text = ssh_list[0] + "-----------------------\n" + result + "-----------------------\n"
                    f.write(text)
            else:
                print ssh_list[0],'Install Error'
                with open('error.txt', 'a') as f:
                    text = ssh_list[0] + "-----------------------\n" + result + "-----------------------\n"
                    f.write(text)
            # except:
            #     print ssh_list[0],'ssh error'
            #     #exit()