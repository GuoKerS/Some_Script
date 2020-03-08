import sys
import requests
from lxml import etree


def get_count():
    url = 'http://dc.gov110.cn/control_center/controlCenterIndex/getRegisterGovUserCount'
    req = requests.request('POST', url, headers=headers)

    if 'totalUserCount' in req.text:
        return req.json()['data']['totalUserCount']
    else:
        print('[-]请检测cookie中y值是否正确！')
        exit(1)


def get_users(count):
    url = 'http://dc.gov110.cn//usercenter/overviewUserList'
    data = {
        'currentPage': '0',
        'maxResults': count
    }
    req = requests.request('POST', url, headers=headers, data=data)
    return req.text

def print_text(text):
    html = etree.HTML(text)
    result = html.xpath('//*[@id="user_list_table"]/tbody/tr')
    for x in result:
        yield x.xpath('td[0]/text()|td[1]/text()|td[2]/text()|td[3]/text()|td[5]/text()|td[6]/text()|td[7]/text()|td[8]/text()|td[9]/text()')

def main():
    global headers
    headers ={
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'y={};'.format(sys.argv[1])
    }
    count = get_count()
    print('[*]用户总数：%s 加载中.....' % count)
    html = get_users(count)
    with open('result.csv', 'a', encoding='gbk') as f:
        f.write('注册时间,单位名称,所属地区,市,区/县,服务器数,网站数,联系电话,邮箱,联系人\n')
        print('[*]正在写入文件....', end='')
        for i in print_text(html):
            tmp = str(i).strip('[').strip(']') + '\n'
            f.write(tmp)
        print('ok')
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''
usage : main.py 51F819DC83C...

info:
请登陆dc.gov110.cn后获取cookie中的y值，并以此值作为该脚本启动参数运行
        ''')
    else:
        main()

