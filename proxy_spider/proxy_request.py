import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_url(proxy):
    re = requests.get(url='http://ip.ws.126.net/ipquery', proxies=proxy, verify=False, timeout=5)
    s = re.status_code
    print(s)

if __name__ == '__main__':
    for p in open('proxy_test.txt'):
        proxys = {'http' : 'http://'+p.strip()}
        try:
            get_url(proxys)
        except:
            print(p.strip(),'失效')