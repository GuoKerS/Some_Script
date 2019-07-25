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
cookie_txt = 'SYS_TIMEOUT=30; webray_lang=zh_CN; pwd_len=10; pwd_comp=1; reminder=0; webseclogin_random=bkdhr0lc5jsu4gvd2z7h9kv5thknn4lt; webseclogin_adminid=1; webseclogin_adminname=admin; userauth=1; product_type=; session=.eJwdjkELgkAQRv9KzLlDbZ2EDsZmKMwuxpTsXILM0HG9WJFu9N-zDg--w-PjveF866t7DdGjf1ZzODdXiN4wu0AERmfCtBUXSoW6XE67NcWhtToOGMqXC_GAknRGUmXp6q32k5-ujRwDihdUR4W0G7HDweptbenUmr0RS75z5BZG5yNL3TDtVjz5v1-WxDMlLap0YakMrOM1F_mAKg9Gu4GLrHOBa5SJfT46whUXuIHPHJ73qv_3wxI-X8FnSC0.D_tvPQ.Yz1krY0fFoKAwX1DimfgA-GBKig; style_color=deepblue; product_category=NoLicense'
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
    cookies={}
    for line in cookie_txt.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    return cookies

def get_logs(name,type,s_time,e_time):
    url = 'https://{}/logsystem/alertlogviewer/query/?startDate={}&endDate={}&iDisplayLength=15&r_type={}'.format(k01_ip, s_time,e_time,type)
    try:
        r = requests.session()
        html = r.get(url=url, cookies=get_cookie(), headers=headers, verify=False)
        text = html.content.decode()
        text = json.loads(text)
        return name , text
    except:print('[error]Please check cookie or network to get_logs')

def get_attacked_ip_logs(ip,s_time,e_time):
    url = 'https://{}/logsystem/alertlogviewer/query/?&startDate={}&endDate={}&r_dip={}&iDisplayLength=15'.format(k01_ip,s_time,e_time,ip)
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
        s = '2019-06-10'
        b = '2019-06-28'
        try:
            name,log_count = get_logs(name,type,s, b)
            if log_count['iTotalDisplayRecords'] != 0:
                output = '{}={}'.format(name,log_count['iTotalDisplayRecords'])
                print(output)
        except:exit()
    print("------------------------")
    print("----前三IP受攻击情况-----")
    for ip in attacked_ip:
        try:
            ip,log_count = get_attacked_ip_logs(ip,s,b)
            print("{}={}".format(ip,log_count['iTotalDisplayRecords']))
        except:print('No ip')
    print("------------------------")

if __name__ == "__main__":
    main()