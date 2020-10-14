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
    'https': 'socks5://127.0.0.1:1XXX'
}#  因为一些网络特殊的原因，访问该目标FK01需要走代理，自己用的时候可以将request.post中proxies=proxies删掉

headers = {
    'accept': "application/json, text/plain, */*",
    'sec-fetch-dest': "empty",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    'content-type': "application/json;charset=UTF-8",
    'cache-control': "no-cache",
    "Cookie": "换成你的cookie",# 替换下cookie
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


def get_count():
    global all_count
    all = "{\"method\":\"RequestLogService.GetRequestLogList\",\"params\":{\"count\":1,\"offset\":0,\"timestamp\":[{\"target\":\""+ date +"\",\"oper\":\"=\"}]},\"jsonrpc\":\"2.0\",\"id\":\"0\"}"
    response = requests.request("POST", url, data=all, headers=headers, proxies=proxies, verify=False)
    ret = response.json()
    all_count = int(ret['result']['total'])
    return str(all_count)


def get_time(t):
    s_time = f"2020-{t} 00:00:00"
    e_time = f"2020-{t} 21:00:00"
    time_format = "%Y-%m%d %H:%M:%S"
    s1_array = time.strptime(s_time, time_format)
    e1_array = time.strptime(e_time, time_format)
    s1 = str(int(time.mktime(s1_array)))
    e1 = str(int(time.mktime(e1_array)))
    ret = f"{s1}-{e1}"
    return ret


if __name__ == '__main__':

    date = get_time(input(">"))
    print(date)
    print(f"all_count:{get_count()}  all_ip:{get_attackip(date)}", end="\r\n\r\n")

    for k, v in type_list.items():
        total = get_data(k)
        if total:
            # print(add_counts, total)
            print('|', v.ljust(5), str(total).center(5), '|')

    print('|', '情报模块'.ljust(5), str(all_count - add_counts).center(5), '|')
    # 75600  21小时   # 86400  24小时



