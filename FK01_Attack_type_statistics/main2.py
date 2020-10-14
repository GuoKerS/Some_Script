#!/usr/bin/env python3
# encoding: utf-8
"""
@file: main.py
@time: 2020-9-13 18:53
@ide: PyCharm
@author: guoker
@contact: attackesb@gmail.com
"""
import time
import requests
requests.packages.urllib3.disable_warnings()

url = "https://XXXXX:9443/rpc"

proxies = {
    "http": "socks5://127.0.0.1:1XXX",
    'https': 'socks5://127.0.0.1:1XXXX'
}

proxies2 = {
    "http": "socks5://127.0.0.1:XX",
    'https': 'socks5://127.0.0.1:XXX'
}

headers = {
    'accept': "application/json, text/plain, */*",
    'sec-fetch-dest': "empty",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    'content-type': "application/json;charset=UTF-8",
    'cache-control': "no-cache",
    "Cookie": "替换Cookie",# 换成你的Cookie
    }

type_list = {
    0: "SQL 注入",
    1: "XSS",
    2: "CSRF",
    3: "SSRF",
    4: "拒绝服务",
    5: "后门",
    6: "反序列化",
    7: "代码执行",
    8: "代码注入",
    9: "命令注入",
    10: "文件上传",
    11: "文件包含",
    12: "重定向",
    13: "权限不当",
    14: "信息泄露",
    15: "未授权访问",
    16: "不安全的配置",
    17: "XXE",
    18: "XPath 注入",
    19: "LDAP 注入",
    20: "目录穿越",
    21: "扫描器",
    22: "水平权限绕过",
    23: "垂直权限绕过",
    24: "文件修改",
    25: "文件读取",
    26: "文件删除",
    27: "逻辑错误",
    28: "CRLF 注入",
    29: "模版注入",
    30: "点击劫持",
    31: "缓冲器溢出",
    32: "整数溢出",
    33: "格式化字符串",
    34: "条件竞争",
    61: "超时",
    62: "未知",
    -1: "非 Web 攻击"
}

add_count = int()

# all_count = int()

add_counts = 0

def get_data(targe):
    global add_counts
    payload = "{\"method\":\"RequestLogService.GetRequestLogList\",\"params\":{\"count\":1,\"offset\":0,\"timestamp\":[{\"target\":\""+ date +"\",\"oper\":\"=\"}],\"attack_type\":[{\"target\":" + str(targe) + ",\"oper\":\"=\"}]},\"jsonrpc\":\"2.0\",\"id\":\"0\"}"
    response = requests.request("POST", url, data=payload, headers=headers, proxies=proxies, verify=False)
    ret = response.json()
    total = ret['result']['total']
    # add_counts = add_counts + total
    add_counts += total
    # print(add_counts)
    return total


def get_attackip(dates):
    # date_old = int(dates) - 1
    payload = "{\"method\":\"RequestLogService.GetSrcIPAttackAnalysis\",\"params\":{\"count\":1,\"offset\":0,\"timestamp\":[{\"oper\":\"=\",\"target\":\""+ dates +"\"}]},\"jsonrpc\":\"2.0\",\"id\":\"0\"}"
    response = requests.request("POST", url, data=payload, headers=headers, proxies=proxies, verify=False)
    ret = response.json()
    old_total = ret['result']['total']
    return old_total


def get_count(date):
    global all_count
    all = "{\"method\":\"RequestLogService.GetRequestLogList\",\"params\":{\"count\":1,\"offset\":0,\"timestamp\":[{\"target\":\""+ date +"\",\"oper\":\"=\"}]},\"jsonrpc\":\"2.0\",\"id\":\"0\"}"
    response = requests.request("POST", url, data=all, headers=headers, proxies=proxies, verify=False)
    ret = response.json()
    all_count = int(ret['result']['total'])
    return str(all_count)


def get_time(t):
    s_time = f"2020-{t} 00:00:00"
    e_time = f"2020-{str(int(t) + 1)} 00:00:00"
    time_format = "%Y-%m%d %H:%M:%S"
    s1_array = time.strptime(s_time, time_format)
    e1_array = time.strptime(e_time, time_format)
    s1 = str(int(time.mktime(s1_array)))
    e1 = str(int(time.mktime(e1_array)))
    ret = f"{s1}-{e1}"
    return ret


def get_time_format(times):
    times = int(times)
    timeArray = time.localtime(times)
    otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
    return otherStyleTime

def get_location(ip):
    url = f"http://freeapi.ipip.net/{ip}"
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.3987.132 Safari/637.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    time.sleep(0.5)
    response = requests.request("GET", url, headers=headers, proxies=proxies2)
    tmp = eval(response.text)
    text = ''.join(tmp)
    return text



def format_data(data):
    src_ip = data["src_ip"]
    location = get_location(data["src_ip"])  # 物理地址---要手动查询
    type = data["type"]
    attack_count = data["attack_count"]
    ip_num = data["ip_num"]
    last_attack_time = get_time_format(data["last_attack_time"]) # 上一次攻击时间 ---需要手动转换时间
    text = f"{src_ip},{location},{type},{attack_count},{ip_num},{last_attack_time}\r"
    with open('FK01_attackIpTop.csv', 'a+', encoding='gbk') as f:
        f.write(text)


def get_attack_top(date):
    payload = "{\"method\":\"RequestLogService.GetSrcIPAttackAnalysis\",\"params\":{\"count\":10,\"offset\":0,\"timestamp\":[{\"oper\":\"=\",\"target\":\""+ date +"\"}]},\"jsonrpc\":\"2.0\",\"id\":\"0\"}"
    response = requests.request("POST", url, data=payload, headers=headers, proxies=proxies, verify=False)
    ret = response.json()
    data = ret['result']['data']
    print(data)
    with open('FK01_attackIpTop.csv', 'a+', encoding='gbk') as f:
        f.write(f"{i}\r")
    for a in data:
        format_data(a)


def test():
    times = ['0'+str(i) for i in range(911,924)]

    for i in times:
        date = get_time(i)
        # print(date)
        a = get_count(date)
        b = get_attackip(date)
        print(f'{i} :   攻击次数{a}    封禁IP{b}')


if __name__ == '__main__':

    # date = get_time(input(">"))
    # print(date)
    # print(f"all_count:{get_count()}  all_ip:{get_attackip(date)}", end="\r\n\r\n")
    #
    # for k, v in type_list.items():
    #     total = get_data(k)
    #     if total:
    #         # print(add_counts, total)
    #         print('|', v.ljust(5), str(total).center(5), '|')
    #
    # print('|', '情报模块'.ljust(5), str(all_count - add_counts).center(5), '|')
    # # 75600  21小时   # 86400  24小时
    # test()
    # get_attack_top("1599753600-1599840000")
    # times = ['0' + str(i) for i in range(911, 924)]
    times = ['0' + str(i) for i in range(911, 925)]  # 这里我想查询 9月11日-25日每日攻击IP次数排名前十的数据
    for i in times:
        date = get_time(i)
        get_attack_top(date)





