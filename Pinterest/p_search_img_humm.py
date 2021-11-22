import eventlet
import time
import re
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected_conditions

from config import *

eventlet.monkey_patch()

print("---------------init-------------")
chrome_options = Options()
# chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式，如你要调试请注释
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--proxy-server=" + proxy_server)
driver = webdriver.Chrome(options=chrome_options)

base_url = 'https://www.pinterest.com/'


# 插入图片src到数据库
def insert_user_info(search_text, img_src):
    print("插入图片src到数据库")
    try:
        cue.execute("insert ignore into pinterest_img "
                    "(search_text, img_src) "
                    "values (%s,%s)",
                    [search_text, img_src])
    except Exception as e:
        print('Insert error:', e)
        con.rollback()
    else:
        con.commit()


# 搜索
def search(search_text):
    print("-------search-------")
    # 点击登陆按钮后页面可能一时半会没加载出来
    # 如果规定时间没这个元素则会提示报错：selenium.common.exceptions.TimeoutException: Message:
    element = WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.XPATH, '//input[@data-test-id="search-box-input"]')))
    element.send_keys(search_text)
    driver.find_element_by_xpath('//input[@data-test-id="search-box-input"]').send_keys(Keys.ENTER)
    count_scroll = 0
    print("睡眠3s等待页面加载完图片数据")
    time.sleep(3)
    while count_scroll < 3:  # 限制滑动次数
        # 滑倒底
        obtainPhotoSrc()
        js = "window.scrollTo(0,document.body.scrollHeight)"
        print('当前滚动，次数为:', count_scroll)
        driver.execute_script(js)
        count_scroll += 1
        print('结束滚动，次数为:', count_scroll)
        time.sleep(3)
    print("停止滚动了，结束")

def obtainPhotoSrc():
    # 获取所有图片链接  这里报错：说我递归太深
    print("进入获取图片方法")
    lst_img = [img.get_attribute('src') for img in driver.find_elements_by_xpath("//div[@class='vbI XiG']//div[@data-test-id='pin']//img")]
    lst_img = [re.sub('236x', '564x', i) for i in lst_img]  # 换成大图
    count = len(lst_img)
    print(search_text, 'unique img count:', count)
    for i in range(count):
        img_src = lst_img[i]
        print(search_text, i, '/', count, img_src)
        # if img_src != None:
        #     insert_user_info(search_text, img_src)


if __name__ == '__main__':
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()

    print("数据库链接上")
    # 登录
    driver.get(base_url)

    try:
        # 先找到登陆按钮，点击登录按钮弹出登陆页面，输入密码后登陆完成即可
        elem = driver.find_element_by_xpath("//div[@data-test-id='simple-login-button']")
        elem.click()  # 点击登陆按钮
        driver.find_element_by_id('email').send_keys(LOGIN_EMAIL)
        driver.find_element_by_id('password').send_keys(LOGIN_PASSWORD)
        driver.find_element_by_xpath('//button[@class="red SignupButton active"]').click() # 点击弹出框登录
        if TYPE_DB_OR_IMG == 1:
            for search_text in lst_search_text:
                # while True:
                search(search_text)
    finally:
        print("finally")
        driver.quit()
        cue.close()
