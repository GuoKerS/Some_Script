# -*- coding:utf-8 -*-
import urllib2
import ssl
import json
import time
import hashlib
import threading
thread_max = 100  # 程序线程
threads = []
del_int = 10 #循环删除次数
URL_FILE = 'url.txt'#要扫描的url列表（不加http://）
'''
----------改动---------
1.awvs密码不需要手动进行sha256加密
2.增加六种扫描方式
----------改动---------
'''
#The second revision comes from GuoKer
# localhost:3443全部替换为awvs所在的服务器及端口
username = 'admin@admin.com'
password = 'Admin123456'
# 账号邮箱与密码明文
pw = hashlib.sha256(password).hexdigest()

try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	pass
else:
	ssl._create_default_https_context = _create_unverified_https_context

patterns = [
    '11111111-1111-1111-1111-111111111112',
    '11111111-1111-1111-1111-111111111115',
    '11111111-1111-1111-1111-111111111117',
    '11111111-1111-1111-1111-111111111116',
    '11111111-1111-1111-1111-111111111113',
    '11111111-1111-1111-1111-111111111111',
]

url_login = "https://localhost:3443/api/v1/me/login"
send_headers_login = {
    'Host': 'localhost:3443',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json;charset=utf-8'
}

data_login = '{"email":"' + username + '","password":"' + pw + '","remember_me":false}'

req_login = urllib2.Request(url_login, headers=send_headers_login)
response_login = urllib2.urlopen(req_login, data_login)
xauth = response_login.headers['X-Auth']
COOOOOOOOkie = response_login.headers['Set-Cookie']
#print"当前验证信息如下\r\n cookie : %r  \r\n X-Auth : %r  " % (COOOOOOOOkie, xauth)
send_headers2 = {
    'Host': 'localhost:3443',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'application/json;charset=utf-8',
    'X-Auth': xauth,
    'Cookie': COOOOOOOOkie
}
# 以上代码实现登录（获取cookie）和校验值
#-------------------------------------------------------------------------
url = "https://localhost:3443/api/v1/targets"
def add_exec_scan(url_txt):
    target_url = 'http://' + url_txt
    data = '{"description":"222","address":"' + target_url + '","criticality":"10"}'
    # data = urllib.urlencode(data)由于使用json格式所以不用添加
    req = urllib2.Request(url, headers=send_headers2)
    response = urllib2.urlopen(req, data)
    jo = json.loads(response.read())
    target_id = jo['target_id']  # 获取添加后的任务ID
    # 以上代码实现批量添加

    url_scan = "https://localhost:3443/api/v1/scans"
    headers_scan = {
        'Host': 'localhost:3443',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Auth': xauth,
        'Cookie': COOOOOOOOkie,
    }
    #3 = xss
    data_scan = '{"target_id":' + '\"' + target_id + '\"' + ',"profile_id":\"'+patterns[patter-1]+'\","schedule":{"disable":false,"start_date":null,"time_sensitive":false},"ui_session_id":"66666666666666666666666666666666"}'
    req_scan = urllib2.Request(url_scan, headers=headers_scan)
    response_scan = urllib2.urlopen(req_scan,str(data_scan))
    print target_url + "添加成功！"
    threads.pop(0)#线程序结束标志


def count():
    url_count = "https://localhost:3443/api/v1/notifications/count"
    req_count = urllib2.Request(url_count, headers=send_headers2)
    response_count = urllib2.urlopen(req_count)
    print"当前存在%r个通知！" % json.loads(response_count.read())['count']
    print"-" * 20
    # print"已存在以下任务"
    url_info = "https://localhost:3443/api/v1/scans"
    req_info = urllib2.Request(url_info, headers=send_headers2)
    response_info = urllib2.urlopen(req_info)
    all_info = json.loads(response_info.read())
    num = 0
    for website in all_info.get("scans"):
        num += 1
        # print
        # website.get("target").get("address") + "\n target_id:" + website.get("scan_id")
    print"共 %r个扫描任务(最多显示100个))" % num
# count()
# scan、target、notification！
def del_targets():
    url_info = "https://localhost:3443/api/v1/targets"
    req_info = urllib2.Request(url_info, headers=send_headers2)
    response_info = urllib2.urlopen(req_info)
    all_info = json.loads(response_info.read())
    for website in all_info["targets"]:
        while True:
            if thread_max > len(threads):
                threads.append(threading.Thread(target=del_tmp,args=(website,)).start())#启动子线程
                break

# del_targets()
def del_tmp(website): #删除任务
    if (website.get("description")) == "222":
        try:
            url_scan_del = "https://localhost:3443/api/v1/targets/" + str(website["target_id"])
            req_del = urllib2.Request(url_scan_del, headers=send_headers2)
            req_del.get_method = lambda: 'DELETE'
            response_del = urllib2.urlopen(req_del)
            print "ok!"
            threads.pop(0)#线程序结束标志
        except:
            exit()

if __name__ == "__main__":
    print "-" * 20
    count()
    print"""
    1、添加扫描任务并执行请输入1
    2、删除所有使用该脚本添加的任务请输入2
    """
    choice = raw_input(">")
    #	print type(choice)

    if choice == "1":
        print"""
        #1.高风险漏洞
        #2.弱密码扫描
        #3.仅爬行
        #4.XSS跨站扫描
        #5.SQL注入扫描
        #6.全扫描
        """
        patter = int(input(">>"))
        start_time = time.time()
        for url_txt in open(URL_FILE,'r').read().split():
            while True:
                if thread_max > len(threads):
                    # threads.append(threading.Thread(target=add_exec_scan,args=(url_txt,)).start())#启动线程
                    t = threading.Thread(target=add_exec_scan,args=(url_txt,))
                    t.start()
                    #t.join()
                    threads.append(t)
                    break
                t.join()
            # for i in thread_max:
            #     t = threads.append(threading.Thread(target=add_exec_scan,args=(url_txt,)))
        count()
        all_time = time.time() - start_time
        print '共用时',all_time
    elif choice == "2":
        for i in range(del_int):
            del_targets()
        count()
    else:
        print
        "请重新运行并请输入1、2选择。"