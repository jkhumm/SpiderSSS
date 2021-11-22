import urllib
import os
import eventlet
import time
import re
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from config import *

eventlet.monkey_patch()

print("---------------init-------------")
chrome_options = Options()
# chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
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
    driver.find_element_by_xpath('//input[@data-test-id="search-box-input"]').send_keys(search_text)
    driver.find_element_by_xpath('//input[@data-test-id="search-box-input"]').send_keys(Keys.ENTER)
    count_scroll = 0
    print("睡眠3s等待页面加载完图片数据")
    time.sleep(3)
    while count_scroll < 2:  # 限制滑动次数
        # 滑倒底
        getPhoto()
        js = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
        count_scroll += 1
        print(search_text, 'scroll:', count_scroll)
        time.sleep(3)
    print("停止滚动了，结束")

def getPhoto():
    # 获取所有图片链接
    lst_img = [img.get_attribute('src') for img in driver.find_elements_by_xpath("//div[@class='vbI XiG']//div[@data-test-id='pin']//img")]
    # lst_img = [img.get_attribute('srcset') for img in driver.find_elements_by_xpath("//div[@class='vbI XiG']//div[@data-test-id='pin']//img")]
    # 换成大图
    lst_img = [re.sub('236x', '564x', i) for i in lst_img]
    # lst_img = list(set(lst_img)) 去重但是会乱序，我这里为了对比所以暂时没检测
    count = len(lst_img)
    print(search_text, 'unique img count:', count)
    for count in range(count):
        img_src = lst_img[count]
        print(search_text, count, '/', count, img_src)
        # if img_src != None:
        #     insert_user_info(search_text, img_src)


# urllib 获取图片并保存
def save_img(path_img, url, save_name):
    print("------- save_img -------")
    file_name_full = path_img + save_name + '.png'
    if os.path.exists(file_name_full) and os.path.getsize(file_name_full) > 0:
        print('pic:' + save_name + '.png exists')
        return 1
    with eventlet.Timeout(TIME_OUT, False):  # 设置超时时间为10秒
        bytes = urllib.request.urlopen(url)
        f = open(file_name_full, 'wb')
        f.write(bytes.read())
        f.flush()
        f.close()
        print('pic:' + save_name + '.png save success...')
        return 1
    return 0


# 图片保存命名
def save_img_src(img_src):
    save_name = search_text + '_' + str(str(img_src).split('/')[-1][:-4])
    return save_img(path_img, img_src, save_name)


def down_img(search_text=None):
    if search_text:
        cue.execute("select count(*) from pinterest_img where search_text = '" + search_text + "' and is_crawled = 0")
    else:
        cue.execute("select count(*) from pinterest_img where is_crawled = 0")
    count_all = cue.fetchone()[0]
    print('down img count all:', count_all)
    count = 0
    while count < count_all:
        # 随机返回一条未爬取的图片链接
        if search_text:
            cue.execute(
                "select img_src from pinterest_img where search_text = '" + search_text + "' and is_crawled = 0 ORDER BY RAND() limit 1")
        else:
            cue.execute("select img_src from pinterest_img where is_crawled = 0 ORDER BY RAND() limit 1")
        img_src = cue.fetchone()[0]
        print(search_text, count, '/', count_all, img_src)
        r = save_img_src(img_src)
        if r:
            # 标记为已爬取
            cue.execute("update pinterest_img set is_crawled = 1 where img_src = (%s)", img_src)
            con.commit()
            count += 1


if __name__ == '__main__':
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()

    print("数据库链接上")
    # 登录
    driver.get(base_url)

    try:
        # 先找到登陆按钮，点击登录按钮弹出登陆页面，输入密码后登陆完成即可
        elem = driver.find_element_by_xpath("//div[@data-test-id='simple-login-button']")
        elem.click()  # 确定
        driver.find_element_by_id('email').send_keys(LOGIN_EMAIL)
        driver.find_element_by_id('password').send_keys(LOGIN_PASSWORD)
        driver.find_element_by_xpath('//button[@class="red SignupButton active"]').click()
        time.sleep(10)
        if TYPE_DB_OR_IMG == 1:
            for search_text in lst_search_text:
                # while True:
                search(search_text)

        elif TYPE_DB_OR_IMG == 2:
            for search_text in lst_search_text:
                path_img = PATH_IMGS + '/' + search_text + '/'
                if not os.path.exists(path_img):
                    os.makedirs(path_img)
                down_img(search_text)
    finally:
        print("finally")
        driver.quit()
        cue.close()
