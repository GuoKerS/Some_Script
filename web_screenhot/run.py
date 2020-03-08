import re,time
import queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class web_screenhot:
    def __init__(self):
        #self.url = url
        self.q = queue.Queue()
        self.re_str = '\w+\.\w+\.\w+.|\w+\.\w+'
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.get('https://www.baidu.com')
        print('[*]对象初始化完毕..')

    def url_list_load(self,url):
        # [self.q.put(i.strip()) for i in open(url)]
        for i in open(url):
            #url_tmp = 'http://'+i.strip()
            url_tmp = i.strip()
            self.q.put(url_tmp)
        print('[*]url列表载入完成..')


    def screenhots(self):
        url = self.q.get()
        self.driver.get(url)
        try:
            title_tmp = re.search(self.re_str,url)
            title = './screenhot/'+title_tmp.group()+'.png'
            self.driver.save_screenshot(title)
            print('[*]%s保存成功'%(title))
            #self.driver.close()
        except:
            print('error')
            self.driver.close()

    def run(self):
        self.url_list_load('url.txt')
        while not self.q.empty():
            self.screenhots()
        self.driver.quit()


if __name__ == '__main__':
    now = lambda :time.time()
    s_time = now()
    save = web_screenhot()
    save.run()
    del save
    print('程序共耗时: %s 秒'%(now() - s_time))