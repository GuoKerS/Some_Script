import os
import time
import smtplib
import requests
from email.header import Header
from email.mime.text import MIMEText
from optparse import OptionParser
#第二版，增加微信提醒功能
logo = '''
  _____        _____        __        _            
 / ____|      |_   _|      / _|      | |           
| |  ____  __   | |  _ __ | |_ ___   | |_ ___  ___ 
| | |_ \ \/ /   | | | '_ \|  _/ _ \  | __/ _ \/ __|
| |__| |>  <   _| |_| | | | || (_) | | ||  __/ (__ 
 \_____/_/\_\ |_____|_| |_|_| \___/   \__\___|\___|
										from guoker
'''

data = "10994-47f71e1d70276add4875623d45142826"
# 延迟函数
def delay(int):
    time.sleep(int)


# 获取域名
def get_urls(test_file):
    try:
        with open(test_file, "r") as f:
            url_list = [line.strip("\n") for line in f.readlines()]
            return url_list
    except:
        print('*** file open error,Please check filename and try again!')


# 监测请求
def httpsend(urls):
    tar_url = get_urls(urls)
    times = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    for urlsend in tar_url:
        try:
            requests.adapters.DEFAULT_RETRIES = 2
            s = requests.session()
            s.keep_alive = False
            if "http://" in urlsend:
                pass
            else:
                urlsend = 'http://'+urlsend
            response = requests.get(url=urlsend, timeout=5, stream=False, verify=False)
            code = response.status_code
            response.close()
            if code == 200:
                print('Domain name:%s >>>>>>>>>>>>>>> %s' % (urlsend, code))
        except requests.RequestException as e:
            print('Domain name:%s >>>>>>>>>>>>>>> error' % (urlsend))
            # 先判断是否开启邮件功能，再接收错误url并发送邮件
            if sendmail_how == '1':
                sendmail_go1(receivers, urlsend)
            elif sendmail_how == '2' :
                urlsend = '>>网站监测异常请检测---->%s'%(urlsend)
                send_wechat(urlsend)



# 循环函数
def sendloop(urls, time_int):
    i = 1
    while True:
        try:
            httpsend(urls)
            print('第%s次监测结束,等待%s秒后进入下次监测' % (i, time_int))
            i += 1
            delay(time_int)
            clear = os.system("clear||cls")
            print(logo)
        except Exception as e:
            print('Exit monitoring ' + e)


# zhuang 13

def animate_banner(tick=0.001):
    import time
    for c in logo:
        time.sleep(tick)
        print(c, end="")


# 邮件发送
def sendmail_go1(receivers, urltext):
    mail_host = 'smtp.exmail.qq.com'
    mail_user = 'xxxx'
    mail_pass = 'xxxxx'

    sender = 'xxxxx'
    # receivers = ['9644395@qq.com']  # 参数1 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    times = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    message = MIMEText('>>%s网站监测异常请检测---->%s' % (times, urltext), 'plain', 'utf-8')  # 参数2
    message['From'] = Header("这是发件人", 'utf-8')
    message['To'] = Header("这是收件人", 'utf-8')

    subject = '<<-----xxxxx网站监测详情----->>'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        # print ("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# 微信发送
def send_wechat(text):
    headers = {
        "Host": "pushbear.ftqq.com",
        "Connection": "keep-alive",
        "Content-Length": "60",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://pushbear.ftqq.com",
        "X-Requested-With": "XMLHttpRequest",
        "LP4-Request-Type": "json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://pushbear.ftqq.com/admin/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "PHPSESSID=2e04c458959c483d8b565a99eb708e1a",
    }
    url = 'https://pushbear.ftqq.com/sub?sendkey={sendkey}&text=网站监控告警&desp={desp}'.format(sendkey=data, desp=text)
    request = requests.get(url=url)
    request.encoding = 'utf8'



if __name__ == "__main__":
    animate_banner()
    urls = str(input('Please enter the list of domain names.(url.txt)\n>>'))
    time_int = int(input('Please enter the interval time.(120) \n>>'))
    sendmail_how = str(input('Do you want to open the mail(1) delivery function or wechat(2) ?(1 or 2) \n>>'))
    # urls = 'url.txt'
    # time_int = 120
    # sendmail_how = 'yes'
    if sendmail_how == '1':
        receivers = str(input('Please enter your mailbox.(xxx@qq.com)\n>>'))
    sendloop(urls, time_int)

