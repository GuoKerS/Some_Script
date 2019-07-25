import requests
from lxml import etree

headers = {
    "User-Agent" : "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding" : "gzip, deflate",
    "Accept-Language" : "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "x-forwarded-for" : "123.125.66.120",
    "referer" : "https://www.baidu.com",
}
xpath1 = '/html/head/title/text()'

for url in open('urls.txt'):
    try:
        url = 'http://'+url
        request = requests.get(url=url.strip(), headers=headers,timeout=1)
        request.encoding = 'utf-8'
        html = request.text
        con = etree.HTML(html)
        title = con.xpath(xpath1)
        text = '{}<---------------->{}\n'.format(url.strip(),title)
        print(title)
        with open('titles.txt','a') as f:
            f.write(text)
    except:
        print('{}<--------->error'.format(url))