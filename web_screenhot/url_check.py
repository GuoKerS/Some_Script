import gevent
from gevent import monkey;

monkey.patch_all()
import requests, queue, time, re

requests.packages.urllib3.disable_warnings()

timeout = 3  # 设置超时
jobs = []
q = queue.Queue()

xpath = '//*/head/title'  # title


# 检查网站存活
def check_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    }
    try:
        r = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
        if 200 or 302 in r.status_code:
            print('[*] Site %s Successful connection.' % url)
            try:
                t = re.search("<title>(.*)</title>", r.text)
                title = t.group().strip('</title>')
            except:
                title = '无标题'
            #wite_title(url, title)
            wite_url(url)

    except:
        print('[-]Site %s error.' % url)


def wite_url(text):
    text = text + '\n'
    with open('url.txt', 'a') as f:
        f.write(text)


def wite_title(text, title):
    text = '{}<-------->{}\n'.format(text, title)
    with open('url_title.txt', 'a') as f:
        f.write(text)


if __name__ == '__main__':
    start = time.time()
    print('[**]正在加载url，请稍后')
    for i in open('urls.txt', encoding='utf8'):
        if 'http' not in i:
            i = 'http://' + i.strip()
            q.put(i)
        else:
            q.put(i.strip())
    count = q.qsize()
    while not q.empty():
        jobs.append(gevent.spawn(check_url, q.get()))
    gevent.joinall(jobs)
    for i in jobs:
        i.join()
    print('\r\r\r\r\r\r\HTTP检测完成，正在加载检测HTTPS。。。')
    ###########################################################
    for i in open('urls.txt', encoding='utf8'):
        if 'http' not in i:
            i = 'https://' + i.strip()
            q.put(i)
        else:
            q.put(i.strip())
    count = q.qsize()
    while not q.empty():
        jobs.append(gevent.spawn(check_url, q.get()))
    gevent.joinall(jobs)
    for i in jobs:
        i.join()

    print("[**]任务完成！队列长度为%s条共耗时%s" % (count, time.time() - start))