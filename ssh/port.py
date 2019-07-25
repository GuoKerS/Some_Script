import telnetlib

def t(ip):
    try:
        telnetlib.Telnet(ip,3389)
        print ip+'22 open'
        with open('22.txt'+,'a') as f:
            f.write(ip)
    except:print ip,'22 close'

for i in open('ip.txt'):
    ip = i.strip()
    t(ip)