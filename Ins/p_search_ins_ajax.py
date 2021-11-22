import datetime
import json
import re
import urllib.parse

import eventlet
import time
import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected_conditions

from config import *

eventlet.monkey_patch()

print("---------------init-------------")
chrome_options = Options()
chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式，如你要调试请注释
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--proxy-server=" + proxy_server)
driver = webdriver.Chrome(options=chrome_options)

base_url = 'https://www.instagram.com/'


# ------------------------------------------------ 数据库操作层开始 ------------------------------------------------

def update_ins_account_enums(ins_account,ins_tag_count,followers_count,follow_count,full_name,ins_id):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("更新用户粉丝数和帖子数")
    try:
        sql = "update ins_account_enums set ins_tag_count=%s,followers_count=%s,follow_count=%s,full_name=%s,ins_id=%s,update_time=%s where ins_account=%s"
        cue.execute(sql,[ins_tag_count,followers_count,follow_count,full_name,ins_id,time.localtime(),ins_account])
    except Exception as e:
        print('update_ins_account_enums error:', e)
        con.rollback()
    else:
        con.commit()

def batch_insert_ins_tag_info(ins_info_list,photo_info_list,video_info_list):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    try:
        print("开始执行插入 帖子信息 到数据库")
        sql = "insert into ins_tag_info (ins_tag_link,ins_account,media_type,likes_count,comments_count,publish_time,author_speak,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        cue.executemany(sql, ins_info_list)
        if len(photo_info_list) > 0:
            print("开始执行插入 图片信息 到数据库")
            sql2 = "insert into ins_tag_info_photo (ins_tag_link,photo_index,photo_url,photo_height,photo_width,create_time) values (%s,%s,%s,%s,%s,%s)"
            cue.executemany(sql2, photo_info_list)
        if len(video_info_list) > 0:
            print("开始执行插入 视频信息 到数据库")
            sql3 = "insert into ins_tag_info_video (ins_tag_link,thumbnail_url,photo_height,photo_width,video_url,create_time) values (%s,%s,%s,%s,%s,%s)"
            cue.executemany(sql3, video_info_list)
    except Exception as e:
        print('batch_insert_ins_tag_info error:', e)
        con.rollback()
    else:
        con.commit()

def query_one_by_ins_account(ins_account):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询明星的帖子的信息")
    try:
        cue.execute("select * from ins_account_enums where ins_account = '" + ins_account + "'")
        return cue.fetchone()
    except Exception as e:
        print('query_one_by_ins_account error:', e)

def query_newest_one(ins_account):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询该账号最新的一条帖子")
    try:
        cue.execute("SELECT * FROM ins_tag_info WHERE ins_account='" + ins_account +"' ORDER BY publish_time DESC LIMIT 0,1")
        return cue.fetchone()
    except Exception as e:
        print('query_newest_one error:', e)

def query_all_ins_account():
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询所有的所需爬取的ins账号")
    try:
        cue.execute("select * from ins_account_enums where account_type=3")
        return cue.fetchall()
    except Exception as e:
        print('query_all_ins_account error:', e)
# ------------------------------------------------ 数据库操作层结束 ------------------------------------------------
# ------------------------------------------------ 公共模块层开始 ------------------------------------------------
def getProxy():
    return {
        'http': 'http://192.168.1.148:7890',
        'https': 'http://192.168.1.148:7890'
    }
def getHeaders():


    # cookie_list = driver.get_cookies()
    # str_list = []
    # size = len(cookie_list)
    # for i in range(size):
    #     key = cookie_list[i]['name']
    #     value = cookie_list[i]['value']
    #     single = key + "=" + value
    #     if i != size - 1:
    #         single = single + ";"
    #     str_list.append(single)
    cookie_str = ''
    s='mid=YYOjugALAAHSnFfx3CKUjQ1rWvgB; ig_did=619086B5-DBC4-46B9-94DE-03573234571E; ig_nrcb=1; shbid="15883\05450238238285\0541668499338:01f7008e294c5a39b9b41373cbaf59d7795e7bfaffe2a806d37d8da47dfb4703140da9c8"; shbts="1636963338\05450238238285\0541668499338:01f7df11b396371f500d284530dda13bd618aaf96e0800bdd354ed12cd47e6dd3e3cdefb"; ds_user_id=50290853753; csrftoken=nobEQadsFZth1QJdgyagdOI6ly4wcRcg; sessionid=50290853753:f0bMp7w9si8LnG:11; rur="VLL\05450290853753\0541668845536:01f791f5ca5b7e0df003140fe32af00e48eaabc1bec27d8b8080011b85d43901b9d6e9e8"'

    headers = {}
    headers.setdefault('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36')
    # headers.setdefault('cookie',cookie_str.join(str_list))
    headers.setdefault('cookie', s)
    return headers


def resolve_account_data(account_data):
    account = {
        'country': account_data['country_code'],
        'language': account_data['language_code'],
        'followers_count': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'], # 粉丝数
        'follow_count': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count'], # 关注数
        'full_name': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name'], # 全名：张子枫
        'ins_id': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['id'], # 张子枫的id
        'profile_pic_url': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd'], # ins账号高清头像
        'username': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['username'], # ins的账号
        'media_obj': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'],  # 首次加载的12张图片信息和分页信息
        'ins_tag_count': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
    }
    return account
# 从node（每个帖子）中提取我们所需业务信息
def general_resolve_media(media):
    res = {
        'tag_id': media['id'], # 帖子id
        'type': media['__typename'][5:].lower(), # GraphImage 单张 GraphSidecar 多张图片
        'comments_count': media['edge_media_to_comment']['count'], # 评论数
        'likes_count': media['edge_media_preview_like']['count'], # 点赞数
        'publish_time':time.localtime(media['taken_at_timestamp']), # 发布时间
        'tag_link': 'https://www.instagram.com/p/' + media['shortcode'] + '/?taken-by=' + media['owner']['username']
    }
    # 说说
    if len(media['edge_media_to_caption']['edges']) == 0:
        res.setdefault('speak','')
    else:
        res.setdefault('speak', media['edge_media_to_caption']['edges'][0]['node']['text'])
    # 图片数据源集合[{帖子的第一张}，{帖子的第二张}]      [{node_index:0,display_resource:[第一张帖子跌一张图片的地址]},{帖子的第二章图片}.....]
    photo_info_ary = []
    video_info = {}
    if res['type'] == 'image':
        photo_info = {}
        display_resources = []  # 该图片的所有src地址-->需求改为只取一张

        obj = {'height': media['dimensions']['height'], 'width': media['dimensions']['width'],'src': media['display_url']}
        display_resources.append(obj)

        # if 'display_resources' in media.keys():
        #     for p in media['display_resources']:
        #         obj = {'height': p['config_height'], 'width': p['config_width'], 'src': p['src']}
        #         display_resources.append(obj)
        # else:
        #     # 图片数据源只有单张情况，则另辟字段
        #     obj = {'height': media['dimensions']['height'], 'width': media['dimensions']['width'],'src': media['display_url']}
        #     display_resources.append(obj)

        photo_info.setdefault("node_index", 0)
        photo_info.setdefault("display_resources",display_resources)
        photo_info_ary.append(photo_info)
    elif res['type'] == 'sidecar':
        edges = media['edge_sidecar_to_children']['edges']
        # 遍历某个帖子的下多张的图片
        for i in range(len(edges)):
            photo_info = {}
            display_resources = []

            obj = {'height': edges[i]['node']['dimensions']['height'], 'width': edges[i]['node']['dimensions']['width'],'src': edges[i]['node']['display_url']}
            display_resources.append(obj)

            # if 'display_resources' in edges[i]['node'].keys():
            #     for p in edges[i]['node']['display_resources']:
            #         obj = {'height': p['config_height'], 'width': p['config_width'], 'src': p['src']}
            #         display_resources.append(obj)
            # else:
            #     # 图片数据源只有单张情况，则另辟字段
            #     obj = {'height': edges[i]['node']['dimensions']['height'], 'width': edges[i]['node']['dimensions']['width'], 'src': edges[i]['node']['display_url']}
            #     display_resources.append(obj)

            photo_info.setdefault("node_index", i)
            photo_info.setdefault("display_resources", display_resources)
            photo_info_ary.append(photo_info)
    elif res['type'] == 'video':
        video_info = {'video_url': media['video_url'],'height': media['dimensions']['height'], 'width': media['dimensions']['width'],'src': media['display_url']}

    res.setdefault('photo_info',photo_info_ary)
    res.setdefault('video_info', video_info)
    return res
# ------------------------------------------------ 公共模块层 结束 ------------------------------------------------
# ------------------------------------------------ 爬取帖子操作 开始 ------------------------------------------------

def searchUser(ins_account):
    print("-------准备进入 " + ins_account + " 明星主页面-------")
    response = requests.get("https://www.instagram.com/" + ins_account + "/", proxies=getProxy(), headers=getHeaders())
    regex = r"\s*.*\s*<script.*?>.*_sharedData\s*=\s*(.*?);<\/script>"

    # driver.get(base_url + ins_account)
    #match_result = re.match(regex, driver.page_source, re.S)
    match_result = re.match(regex, response.text, re.S)
    data = json.loads(match_result.group(1))

    account = resolve_account_data(data)

    one = query_one_by_ins_account(ins_account=ins_account)
    # 查询帖子数是否存在更新
    if account['ins_tag_count'] == one[3]:
        print("do nothing")
    else:
        node_list = []
        first = 200
        if one[3] is None:
            print("全量插入")
            # 首次加载的数据放入到总的集合中
            for node in account['media_obj']['edges']:
                node_info = general_resolve_media(node['node'])
                node_list.append(node_info)
            total_count = account['media_obj']['count']
            user_id = account['ins_id']
            end_cursor = account['media_obj']['page_info']['end_cursor']
            has_next_page = account['media_obj']['page_info']['has_next_page']
            # 不断的查询
            node_list = get_media_by_user_id(user_id, first, end_cursor, has_next_page, node_list, False, None, total_count)
            print("最终集合大小：" + str(len(node_list)))
            batch_insert_data(ins_account, node_list)
        else:
            print("增量插入")
            one = query_newest_one(ins_account=ins_account)
            if one is None:
                print("warn------：数据异常")
                return
            is_go_on_query = True
            total_count = account['media_obj']['count']
            for node in account['media_obj']['edges']:
                node_info = general_resolve_media(node['node'])
                if struct_time_to_datetime(node_info['publish_time']) > one[6]:
                    node_list.append(node_info)
                else:
                    is_go_on_query = False
                    break
            if is_go_on_query:
                user_id = account['ins_id']
                end_cursor = account['media_obj']['page_info']['end_cursor']
                has_next_page = account['media_obj']['page_info']['has_next_page']
                node_list = get_media_by_user_id(user_id, first, end_cursor, has_next_page, node_list, True, one[6], total_count)
                print("最终集合大小：" + str(len(node_list)))
            # 如果发现首次加载中已经找到了增量的数据，并且其中也出现了我们中的老数据，则无需循环访问接口
            print("最终集合大小：" + str(len(node_list)))
            batch_insert_data(ins_account,node_list)

        # 完成后更新对应账号的信息
        update_ins_account_enums(ins_account, account['ins_tag_count'], account['followers_count'],account['follow_count'], account['full_name'], account['ins_id'])

def struct_time_to_datetime(struct_time):
    year = struct_time.tm_year
    month = struct_time.tm_mon
    day = struct_time.tm_mday
    hour = struct_time.tm_hour
    min = struct_time.tm_min
    sec = struct_time.tm_sec

    date_time = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=min, second=sec)
    return date_time





def batch_insert_data(ins_account, node_list):
    # 组装批量插入所需数据结构 泛型是tuple
    ins_info_list = []  # [('https://www.instagram.com/p/CVva4NEPIYM/','__zf0827__','2021-11-11 12:12:00')]
    create_time = time.localtime()

    photo_info_list = []
    video_info_list = []
    for i in range(len(node_list)):
        ins_info_list.append((node_list[i]['tag_link'], ins_account, node_list[i]['type'], node_list[i]['likes_count'],
                              node_list[i]['comments_count'], node_list[i]['publish_time'], node_list[i]['speak'], create_time))

        if node_list[i]['type'] == 'image' or node_list[i]['type'] == 'sidecar':
            for p in node_list[i]['photo_info']:
                for pp in p['display_resources']:
                    photo_info_list.append((node_list[i]['tag_link'], p['node_index'], pp['src'], pp['height'],
                                            pp['width'], create_time))
        elif node_list[i]['type'] == 'video':
            video_info = node_list[i]['video_info']
            video_info_list.append((node_list[i]['tag_link'], video_info['src'], video_info['height'],
                                    video_info['width'], video_info['video_url'], create_time))

    batch_insert_ins_tag_info(ins_info_list, photo_info_list, video_info_list)

def get_media_by_user_id(user_id, first, end_cursor, has_next_page, node_list, is_go_on_query, last_publish_time, total_count):
    base_query_url = "https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables="
    while has_next_page:
        variables = json.dumps({
            'id': str(user_id),
            'first': first,
            'after': str(end_cursor)
        }, separators=(',', ':'))  # 不指定separators的话key:value的:后会默认有空格，因为其默认separators为(', ', ': ')
        url = base_query_url + urllib.parse.quote(variables)
        print("分页接口之前node_list的大小：" + str(len(node_list)) + "，总计大小为：" + str(total_count))

        response = requests.get(url, proxies=getProxy(), headers=getHeaders())
        media_json_data = json.loads(response.text)
        status = media_json_data['status']
        print("接口相应结果：" + status)
        if status != 'ok':
            print("warn:接口请求失败,准备再次发起调用")
        else:
            media_raw_data = media_json_data['data']['user']['edge_owner_to_timeline_media']
            data = media_raw_data['edges']
            for item in data:
                business = general_resolve_media(item['node'])
                if is_go_on_query:
                    if struct_time_to_datetime(business['publish_time']) > last_publish_time:
                        print("循环遍历:" + str(len(data)) + "次数，增加一个帖子，增加之后大小为：" + str(len(node_list)))
                        node_list.append(business)
                    else:
                        print("跳出循环，无需再次查询分页信息")
                        return node_list
                else:
                    node_list.append(business)
                    print("循环遍历:" + str(len(data)) + "次数，增加一个帖子，增加之后大小为：" + str(len(node_list)))
            end_cursor = media_raw_data['page_info']['end_cursor']
            has_next_page = media_raw_data['page_info']['has_next_page']
    return node_list


# ------------------------------------------------ 爬取帖子操作 结束 ------------------------------------------------

if __name__ == '__main__':
    try:
        print("数据库链接上，准备开始登陆ins账号")
        # driver.get(base_url)
        # time.sleep(1)
        #
        # # 先找到登陆按钮，点击登录按钮弹出登陆页面，输入密码后登陆完成即可
        # driver.find_element_by_xpath("//input[@name='username']").send_keys(LOGIN_EMAIL)
        # driver.find_element_by_xpath("//input[@name='password']").send_keys(LOGIN_PASSWORD)
        #
        # driver.find_element_by_xpath("//button[@type='submit']").click() # 点击登陆按钮
        #
        # #同步阻塞 会弹出一个遮罩层，提示你保存你的登录信息
        # element = WebDriverWait(driver, 15).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='cmbtv']//button"))).click() # 点击以后再说
        #
        # print("登陆完成")

        # 去除那个弹出提示框        等价 == driver.find_elements_by_xpath("//div[@role='dialog']//button")[1]
        # try:
        #     driver.find_element_by_xpath("//div[@role='dialog']//button[last()]").click()
        # except:
        #     # 浏览器无头模式没有此按钮
        #     pass
        # 轮询ins账号
        # total_ins_account = query_all_ins_account()
        total_ins_account = ((1, 'celine'),) # __zf0827__
        for singleIns in total_ins_account:
            searchUser(singleIns[1]) # 取出index=1 的字段
            print(singleIns[1] + "该明星查找完毕")

    finally:
        print("finally")
        driver.quit()

