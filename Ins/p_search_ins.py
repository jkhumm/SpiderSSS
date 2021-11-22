from datetime import date

import eventlet
import time
import pymysql
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected_conditions

from config import *

eventlet.monkey_patch()

print("---------------init-------------")
chrome_options = Options()
#chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式，如你要调试请注释
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--proxy-server=" + proxy_server)
driver = webdriver.Chrome(options=chrome_options)

base_url = 'https://www.instagram.com/'
total_href_list = []

# ------------------------------------------------ 数据库操作层开始 ------------------------------------------------

def batch_insert_tag_task(ins_tag_task):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()  # 创建游标
    print("批量插入帖子任务到数据库")
    try:
        cue.executemany("insert ignore into ins_tag_task (ins_tag_link,ins_account,extra_index,create_time) values (%s,%s,%s,%s)",ins_tag_task)
    except Exception as e:
        print('batch_insert_tag_task error:', e)
        con.rollback()
    else:
        con.commit()

def insert_ins_tag_info(ins_tag_link,ins_account,publish_time,like_count,media_type,author_speak,create_time,media_url_ary):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()  # 创建游标
    print("帖子信息插入到数据库")
    try:
        cue.execute("insert ignore into ins_tag_info (ins_tag_link,ins_account,publish_time,like_count,media_type,author_speak,create_time) values (%s,%s,%s,%s,%s,%s,%s)",
                        [ins_tag_link,ins_account,publish_time,like_count,media_type,author_speak,create_time])
        for media_url in media_url_ary:
            cue.execute("insert ignore into ins_tag_info_media (ins_tag_link,media_url,create_time) values (%s,%s,%s)",[ins_tag_link, media_url, create_time])
        cue.execute("update ins_tag_task set is_crawled = 1 where ins_tag_link = (%s)", ins_tag_link)
    except Exception as e:
        print('insert_ins_tag_info error:', e)
        con.rollback()
    else:
        con.commit()

def query_star_tag_db_count(star_account):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()  # 创建游标
    print("查询明星存在数据库中的帖子数")
    try:
        cue.execute("select count(1) from ins_tag_task where ins_account = '" + star_account + "'")
        return cue.fetchone()[0]
    except Exception as e:
        print('query_star_tag_db_count error:', e)

def query_ins_tag_by_account_in_db(ins_account):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()  # 创建游标
    print("查询明星存在数据库中的帖子链接地址")
    try:
        cue.execute("select ins_tag_link from ins_tag_task where ins_account = '" + ins_account + "'")
        return cue.fetchall()
    except Exception as e:
        print('query_star_tag_info_in_db error:', e)

def query_ins_tag_task_newest_one(ins_account):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询该账号最新的一条数据")
    try:
        cue.execute("SELECT * FROM ins_tag_task WHERE ins_account='" + ins_account +"' ORDER BY create_time DESC,extra_index ASC LIMIT 0,1")
        return cue.fetchone()
    except Exception as e:
        print('query_ins_tag_task_newest_one error:', e)

def query_ins_tag_task_not_crawled_count():
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询未被爬取任务的数量")
    try:
        cue.execute("SELECT count(1) FROM ins_tag_task WHERE is_crawled=0")
        return cue.fetchone()[0]
    except Exception as e:
        print('query_ins_tag_task_not_crawled_count error:', e)

def query_ins_tag_task_not_crawled(start,end):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询未被爬取任务的数量")
    try:
        cue.execute("SELECT * FROM ins_tag_task WHERE is_crawled=0 limit " + str(start) + "," + str(end))
        return cue.fetchall()
    except Exception as e:
        print('query_ins_tag_task_not_crawled_count error:', e)

def query_all_ins_account():
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询所有的所需爬取的ins账号")
    try:
        cue.execute("select * from ins_account_enums where account_type=4")
        return cue.fetchall()
    except Exception as e:
        print('query_all_ins_account error:', e)
# ------------------------------------------------ 数据库操作层结束 ------------------------------------------------

#下面方法暂时没被用到
month_ary = ["January","February","March","April","May","June","July","August","September","Octorber","November","December"]
def get_Publish_time(img_alt_str):
    year,month,day = 0,0,0
    s1 = img_alt_str.split(".")[0].split("on")[1][1:]
    data_array = s1.replace(",", "").split(" ")  # ['February', '01', '2021']
    year = int(data_array[2])
    day = int(data_array[1])
    for i in range(len(month_ary)):
        if month_ary[i].__eq__(data_array[0]):
            month = i+1
            break
    return date(year,month,day)

def dateStr_to_datetime(dateStr):
    ary1 = dateStr.split('年')
    ary2 = ary1[1].split('月')
    year,month,day = ary1[0], ary2[0], ary2[1].replace('日','')
    return date(int(year), int(month), int(day))

# ------------------------------------------------ 爬取帖子操作 开始 ------------------------------------------------

def query_tagInfo_in_currentPage(tag_count):
    # 帖子容器有两个div取第一个，然后再取三个为一排
    total_href_len_previous = len(total_href_list)
    line_list = driver.find_element_by_tag_name("article").find_elements_by_xpath("div[1]//div[@class='Nnq7C weEfm']")
    count = len(line_list)
    for i in range(count):
        # 从一排中找到对应的帖子链接（一般是三个）
        line_href = [tagA.get_attribute('href') for tagA in line_list[i].find_elements_by_tag_name("a")]
        for href in line_href:
            if href not in total_href_list:
                total_href_list.append(href)
    total_href_len_post = len(total_href_list)
    print("共计：" + str(tag_count) + "帖子，当前页面有" + str(count) + "排，上一次帖子链接数为：" + str(total_href_len_previous) + ",相差" +(str(total_href_len_post-total_href_len_previous)) +"，现累计链接数为："+ str(total_href_len_post))
    return total_href_len_previous,total_href_len_post,total_href_list

def increment_batch_insert(href_list,ins_account):
    # (('地址1',), ('地址2',))
    db_ins_tag_link = query_ins_tag_by_account_in_db(ins_account)  # 返回的是Tuple数据结构（不可变 list）
    # ['地址1','地址2']
    lst_users = [i[0] for i in db_ins_tag_link]
    diff_list = list(set(href_list) - set(lst_users))
    if len(diff_list) > 0:
        list_task = []
        create_time = time.localtime()
        for i in range(len(diff_list)):
            list_task.append((diff_list[i], ins_account, i, create_time))
        # 求出差集后批量插入
        batch_insert_tag_task(list_task)

def searchUser(ins_account):
    driver.get(base_url + ins_account)
    print("-------准备进入 " + ins_account +" 明星主页面-------")
    # 如果规定时间没这个元素则会提示报错：selenium.common.exceptions.TimeoutException: Message:
    WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//section[@class='zwlfE']")))

    # 进入主页后找到此明星有多少个帖子
    # 问题点：1.当博主删除后新新增帖子数与数据库一致无法做到及时更新（因为我们对数据一致性要求不严格，这个可以容忍）
    # 问题点2：当是批量增新时，最新的帖子被博主删除了，此时我们会发现一直不会相等，使得程序陷入死循环
    tag_count = int(driver.find_element_by_xpath("//span[@class='g47SY ']").text)
    db_count = query_star_tag_db_count(ins_account)
    print("tag_count:" + str(tag_count) + ",db_count:" + str(db_count))
    # 可能会出现问题点一的情况
    if tag_count == db_count:
        print(ins_account + "账号暂无更新")
    else:
        print("睡眠3s等待页面加载完图片数据")
        time.sleep(3)
        count_scroll = 0
        # 全量插入
        if db_count == 0:
            while True:
                # 不断查询此明星账号的帖子
                total_href_len_previous, total_href_len_post, href_list = query_tagInfo_in_currentPage(tag_count)
                diff = total_href_len_post - total_href_len_previous
                if tag_count != total_href_len_post and (diff % 3) != 0:
                    print("-----warn:发现存在图片未加载完全的情况")
                    time.sleep(5)
                    total_href_len_previous, total_href_len_post, href_list = query_tagInfo_in_currentPage(tag_count)
                js = "window.scrollTo(0,document.body.scrollHeight)"
                driver.execute_script(js)
                count_scroll += 1
                print('滚动完毕，当前已滚动:', count_scroll)
                if count_scroll > 0:
                    time.sleep(5)
                # ins上帖子数可能与实际爬取的数量不一致
                if tag_count == total_href_len_post:
                    print("帖子滑到底了，无需继续滑动，跳出循环")
                    # 组装批量插入所需数据结构
                    list_task = []  # [('https://www.instagram.com/p/CVva4NEPIYM/','__zf0827__','2021-11-11 12:12:00')]
                    create_time = time.localtime()
                    for i in range(len(href_list)):
                        list_task.append((href_list[i], ins_account, i, create_time))
                    batch_insert_tag_task(list_task)
                    print("结束滚动了，全量插入执行完成")
                    break
                elif 1==1:
                    print(1)
        # 增量插入
        else:
            # 这里我们不一直拖动滚轮，可以预知的是我们数据库之前已经执行过跑批任务
            while True:
                total_href_len_previous, total_href_len_post, href_list = query_tagInfo_in_currentPage(tag_count)
                newest_one = query_ins_tag_task_newest_one(ins_account)
                # 如果数据库中最新的一条不在当前页面说明，此人更新了多条ins，需要不断的间歇性的滑动滚轮，直到存在（查询是否出现在当前页面最新集合中）
                # 可能会出现问题点二的情况
                if newest_one[1] in total_href_list:
                    # 组装批量插入所需数据结构

                    list_task = []  # ins_tag_task [('https://www.instagram.com/p/CVva4NEPIYM/','__zf0827__','2021-11-11 12:12:00')]
                    create_time = time.localtime()
                    for i in range(len(href_list)):
                        if href_list[i] != newest_one[1]:
                            list_task.append((href_list[i] , ins_account, i, create_time))
                        else:
                            batch_insert_tag_task(list_task)
                            break
                    break
                else:
                    js = "window.scrollTo(0,document.body.scrollHeight)"  # 滑倒底
                    driver.execute_script(js)
                    count_scroll += 1
                    print('滚动完毕，当前已滚动:', count_scroll)
                    time.sleep(5)



# ------------------------------------------------ 爬取帖子操作 结束 ------------------------------------------------

# ------------------------------------------------ 爬取帖子详情 开始 ------------------------------------------------
def fenye_query():
    count = query_ins_tag_task_not_crawled_count()
    # 以一百页为一次循环  1001 = 11页面
    if (count % 100) == 0:
        page = int(count/100)
    else:
        page = int(count/100) + 1
    for currentPage in range(1):
        start = currentPage * 100
        end = (currentPage + 1) * 100
        not_crawled_list = query_ins_tag_task_not_crawled(start=start,end=end)
        for ins_tag_task in not_crawled_list:
            print("开始访问该帖子的详情：" + ins_tag_task[1])
            query_notCrawled_tagDetails(ins_tag_task[1],ins_tag_task[2])


# 可以起个定时任务来去查询没有没有被爬虫的信息
def query_notCrawled_tagDetails(ins_tag_link,ins_account):
        # 左边部分是以图片/视频div 右边是评论div
        driver.get(ins_tag_link)
        # 存在这说明发布的是图片，否则是视频
        if len(driver.find_elements_by_tag_name("video")) == 0:
            media_type = 1
            media_url = [img.get_attribute('src') for img in driver.find_elements_by_xpath("//div[@class='ZyFrc']//img[@class='FFVAD']")]

        else:
            media_type = 2
            media_url = driver.find_elements_by_tag_name("video")[0].get_attribute("src")

        # 评论部分
        publish_time = driver.find_element_by_xpath("//div[@class='k_Q0X I0_K8  NnvRN']//time").get_attribute("title")

        try:
            like_count = driver.find_element_by_xpath("//a[@class='zV_Nj']//span").text
        except NoSuchElementException:
            like_count = '0'

        # if media_type == 1:
            # like_count 点赞数/播放量  如果不存在此标签，则是video
        #else:
           # like_count = driver.find_element_by_xpath("//span[@class='vcOH2']//span").text  次播放

        # if not driver.find_element_by_xpath("//a[@class='zV_Nj']//span"):
        # 限制了评论，所以拿不到该说说
        if len(driver.find_elements_by_xpath("//div[@class='EtaWk']//ul/child::div[@role='button']//div[@class='C4VMK']")) == 0:
            author_speak = ''
        else:
            oneTag = driver.find_elements_by_xpath("//div[@class='EtaWk']//ul/child::div[@role='button']//div[@class='C4VMK']")[0]
            try:
                oneTag.find_element_by_xpath("//h2")
                author_speak = oneTag.find_element_by_xpath("//h2/following-sibling::span").text
            except NoSuchElementException:
                # 作者用的是h2，普通用户是h3.如果不存在h2则说明作者只是发了一张图
                author_speak = ''
        print("  publish_time:" + publish_time + "\n  like_count:" + like_count + "\n  media_type：" + str(media_type) + "\n"                                                                                                            
            "  media_url:" + str(media_url) + "\n  author_speak:" + author_speak)

        insert_ins_tag_info(ins_tag_link, ins_account, dateStr_to_datetime(publish_time), like_count, media_type, author_speak, time.localtime(), media_url)

# ------------------------------------------------ 爬取帖子详情 结束 ------------------------------------------------

if __name__ == '__main__':
    try:
        print("数据库链接上，准备开始登陆ins账号")
        driver.get(base_url)
        time.sleep(1)

        # 先找到登陆按钮，点击登录按钮弹出登陆页面，输入密码后登陆完成即可
        driver.find_element_by_xpath("//input[@name='username']").send_keys(LOGIN_EMAIL)
        driver.find_element_by_xpath("//input[@name='password']").send_keys(LOGIN_PASSWORD)

        driver.find_element_by_xpath("//button[@type='submit']").click() # 点击登陆按钮

        #同步阻塞 会弹出一个遮罩层，提示你保存你的登录信息
        element = WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='cmbtv']//button"))).click() # 点击以后再说

        print("登陆完成")

        # 去除那个弹出提示框        等价 == driver.find_elements_by_xpath("//div[@role='dialog']//button")[1]
        try:
            driver.find_element_by_xpath("//div[@role='dialog']//button[last()]").click()
        except:
            # 浏览器无头模式没有此按钮
            pass
        # 轮询ins账号
        #total_ins_account = query_all_ins_account()
        total_ins_account = ((1, 'nasahubble'),)
        # searchUser("__zf0827__")
        for singleIns in total_ins_account:
            searchUser(singleIns[1]) # 取出index=1 的字段
            print(singleIns[1] + "该明星查找完毕")
            total_href_list = [] # 置空该集合
       # fenye_query()

    finally:
        print("finally")
        driver.quit()

