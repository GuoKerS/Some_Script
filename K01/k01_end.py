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
cookie_txt = 'SYS_TIMEOUT=30; webray_lang=zh_CN; pwd_len=10; pwd_comp=1; reminder=0; webseclogin_random=fvusjoa225m6wavr5ent12uscr09l96f; webseclogin_adminid=1; webseclogin_adminname=admin; userauth=1; product_type=; session=.eJwdjkELgkAQRv9KzLlDbZ2EDsZmKMwuxpTsXILM0HG9WJFu9N-zDg--w-PjveF866t7DdGjf1ZzODdXiN4wu0AERmfCtBUXSoW6XE67NcWhtToOGMqXC_GAknRGUmXp6q32k5-ujRwDihdUR4W0G7HDweptbenUmr0RS75z5BZG5yNL3TDtVjz5v1-WxDMlLap0YakMrOM1F_mAKg9Gu4GLrHOBa5SJfT46whUXuIHPHJ73qv_3wxI-X8FnSC0.D_r0rg.YXFT6fcIGRrGnwd8j5f9jtgYlOc; style_color=deepblue; product_category=NoLicense'

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

def get_logs(time):
    url = 'https://{}/logsystem/alertlogviewer/query/?startDate={}&endDate={}&iDisplayLength=15&r_type='.format(k01_ip, time,time)
    try:
        r = requests.session()
        html = r.get(url=url, cookies=get_cookie(), headers=headers, verify=False)
        text = html.content.decode()
        text = json.loads(text)
        return text
    except:print('[error]Please check cookie or network to get_logs')


    url = 'https://{}/logsystem/alertlogviewer/query/?&startDate={}&endDate={}&r_dip={}&iDisplayLength=15'.format(k01_ip,time,time,ip)
    try:
         r = requests.session()
         html = r.get(url=url, cookies=get_cookie(), headers=headers, verify=False)
         text = html.content.decode()
         text = json.loads(text)
         return text
    except:print('[error]Please check cookie or network to get_attacked_ip')

def get_ip_logs(time):
    url = 'https://{}/attackipanalysis/attackipanalysis/query/?&startDate={}&endDate={}&iDisplayLength=15&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8&mDataProp_9=9&mDataProp_10=10&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&sSearch_7=&bRegex_7=false&bSearchable_7=true&sSearch_8=&bRegex_8=false&bSearchable_8=true&sSearch_9=&bRegex_9=false&bSearchable_9=true&sSearch_10=&bRegex_10=false&bSearchable_10=true&iSortCol_0=8&sSortDir_0=desc&iSortingCols=1&bSortable_0=false&bSortable_1=false&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=true&bSortable_7=true&bSortable_8=true&bSortable_9=false&bSortable_10=false&_=1561711888785'.format(k01_ip, time,time)
    try:
        r = requests.session()
        html = r.get(url=url, cookies=get_cookie(), headers=headers, verify=False)
        text = html.content.decode()
        text = json.loads(text)
        return text
    except:print('[error]Please check cookie or network to get_logs')


    url = 'https://{}/logsystem/alertlogviewer/query/?&startDate={}&endDate={}&r_dip={}&iDisplayLength=15'.format(k01_ip,time,time,ip)
    try:
         r = requests.session()
         html = r.get(url=url, cookies=get_cookie(), headers=headers, verify=False)
         text = html.content.decode()
         text = json.loads(text)
         return text
    except:print('[error]Please check cookie or network to get_attacked_ip')


def main():
    print('当前日期为：',time)
    print("------------------------")
    for i in range(10,31):
        times = '2019-6-{}'.format(i)
        try:
            log_count = get_logs(times)
            if log_count['iTotalDisplayRecords'] != 0:
                output = '{}攻击次数={}'.format(times,log_count['iTotalDisplayRecords'])
                print(output)
        except:exit()
    print("------------------------")
    for i in range(10,31):
        times = '2019-6-{}'.format(i)
        try:
            log_count = get_ip_logs(times)
            if log_count['iTotalDisplayRecords'] != 0:
                output = '{}封禁IP={}'.format(times,log_count['iTotalDisplayRecords'])
                print(output)
        except:exit()
    print("------------------------")

if __name__ == "__main__":
    main()