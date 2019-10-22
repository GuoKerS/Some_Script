from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_Options = Options()
    chrome_Options.add_argument('--headless') #设置无头模式
    chrome_Options.add_argument('--disable-gpu') #禁用GPU
    driver = webdriver.Chrome(options=chrome_Options) #创建实例，并加载配置
    driver.maximize_window()  # 最大化窗口
    print('正在打开baidu....')
    driver.get("https://baidu.com") #打开页面
    driver.save_screenshot('./baidu.png')  #截图
    print(driver.get_cookies())
    #driver.close()
    print('正在打开138....')
    driver.get("http://ip138.com")
    print(driver.get_cookies())
    driver.save_screenshot('./138.png')
    # driver.close()

    driver.quit() #退出浏览器



if __name__ == '__main__':
    main()

# [print(i) for i in range(10)]