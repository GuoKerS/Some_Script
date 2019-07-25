import paramiko
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname='192.168.80.129', port=22, username='root', password='guoker97')
# stdin, stdout, stderr = ssh.exec_command('uname -a')
# res, err = stdout.read(), stderr.read()
# result = res if res else err
# print res
# test = raw_input('Are you OK?>')
# if test == 'yes':
#     stdin, stdout, stderr = ssh.exec_command('ifconfig')
#     res, err = stdout.read(), stderr.read()
#     result = res if res else err
#     print result
# elif test == 'no':
#     print 886

for i in open('ssh.txt'):
    if '#' in i[0]:
        print '-----'
    else:print i