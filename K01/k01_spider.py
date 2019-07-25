import json,datetime,requests
requests.packages.urllib3.disable_warnings()
_author_ = 'Guoker'
'''
	使用前自行修改k01设备ip和cookie（貌似cookie有效时间一周）
	以及user-agent（有出现过换了机器不改的话不返回数据？？黑人？？）
	0625更新后 iDisplayLength 的值不可自定义
'''

k01_ip = '10.190.19.25'
# K01 cookie.txt
cookie_txt = 'SYS_TIMEOUT=30; webray_lang=zh_CN; pwd_len=10; pwd_comp=1; reminder=0; webseclogin_adminid=1; webseclogin_adminname=admin; userauth=1; product_type=; style_color=deepblue; product_category=NoLicense; webseclogin_random=7ij7xu6nwf3sjw7rg8ofynnjzy94aq8n; session=.eJwdjkGLwjAQhf-KzNlDa7eXwh6UcUuEmaBEy-QiiN1N0-TSbpGN-N83eHsP3vfxnnD9nvrZQfM7Lf0arsMdmiesbtCAJDeyHwvqVEXmHiltkyT5Y9yW1pyTbU9eo3xwopx5IL-vrb9EG4-lxjDy5jRkvtJ4rmjzNdhOCt1SYbu8N-yoVSXjT01easYQCN0oSSUx2WEOkXAXGekh_hLEqAf5Q2You13Mm6C73FFVFo-f8FrDMvfT-z-U8PoHaK5G9A.D_Nfsw.NYQk00xGOvYJP82eCdLBoP_Y10U'
#三个被攻击IP
attacked_ip = ['10.190.16.107', '10.190.18.32', '10.190.18.34']
# 日志类型
r_types = {
    "今日总攻击数" : "",
	"僵尸网络" : '0',
    '恶意IP' : '1',
    '扫描器' : '2',
    'Webshell客户端' : '3',
    '代理' : '4',
    'TOR节点' : '5',
    '漏洞利用' : '6',
    '暴力破解' : '7',
    'CC攻击' : '8',
    '黑名单' :'250',
    "服务器非法外联" : "254",
}
headers = {
    'Connection':'close',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
i = datetime.datetime.now()
time = '{}-{}-{}'.format(i.year,i.month,i.day)
def get_cookie():
    # with open(cookie_txt,'r') as f:
    #     cookies={}
    #     for line in f.read().split(';'):
    #         name,value = line.strip().split('=',1)
    #         cookies[name] = value
    #     return cookies
    cookies={}
    for line in cookie_txt.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    return cookies

def get_logs(name,type,time):
    url = 'https://{}/logsystem/alertlogviewer/query/?startDate={}&endDate={}&iDisplayLength=15&r_type={}'.format(k01_ip, time,time,type)
    try:
        r = requests.session()
        html = r.get(url=url, cookies=get_cookie(), headers=headers, verify=False)
        text = html.content.decode()
        text = json.loads(text)
        return name , text
    except:print('[error]Please check cookie or network to get_logs')

def get_attacked_ip_logs(ip,time):
    url = 'https://{}/logsystem/alertlogviewer/query/?&startDate={}&endDate={}&r_dip={}&iDisplayLength=15'.format(k01_ip,time,time,ip)
    try:
         r = requests.session()
         html = r.get(url=url, cookies=get_cookie(), headers=headers, verify=False)
         text = html.content.decode()
         text = json.loads(text)
         return ip,text
    except:print('[error]Please check cookie or network to get_attacked_ip')
def main():
    print('当前日期为：',time)
    print("------------------------")
    for i in r_types.items():
        name,type = i
        try:
            name,log_count = get_logs(name,type,time)
            if log_count['iTotalDisplayRecords'] != 0:
                output = '{}={}'.format(name,log_count['iTotalDisplayRecords'])
                print(output)
        except:exit()
    print("------------------------")
    print("----前三IP受攻击情况-----")
    for ip in attacked_ip:
        try:
            ip,log_count = get_attacked_ip_logs(ip,time)
            print("{}={}".format(ip,log_count['iTotalDisplayRecords']))
        except:print('No ip')
    print("------------------------")

if __name__ == "__main__":
    main()