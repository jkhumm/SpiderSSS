import datetime
import json
import re
import urllib.parse

import time
import pymysql
import requests

from config import *

#eventlet.monkey_patch() https://zhuanlan.zhihu.com/p/37679547

def getProxy():
    #用户名： 912bef8175c0   授权码： b962a7c83d
    return {
        'http': 'http://127.0.0.1:7890', # http://username:password@120.24.77.37:1056   http://127.0.0.1:7890
        'https': 'http://127.0.0.1:7890'
    }

def getHeaders():
    # 163邮箱账号 humm_ins163
    #cookie = 'mid=YZxbIwALAAHm1uM2xmDj6xeSiFe8; ig_did=C85EDD35-5DA7-4932-808A-D37F9A30E3E1; ig_nrcb=1; csrftoken=4cz9koAjLOdVcRkOOdyNHsWwImj9plnB; ds_user_id=50290853753; sessionid=50290853753%3AwelLxOkpJrIQbq%3A27; rur="VLL\05450290853753\0541669172920:01f76c987245916453627b782eb2179f16f5f65890668491073675236d2406baf4b6038b"'
    # 企业邮箱账号 humm
    #cookie = 'mid=YYOjugALAAHSnFfx3CKUjQ1rWvgB; ig_did=619086B5-DBC4-46B9-94DE-03573234571E; ig_nrcb=1; shbid="15883\05450238238285\0541669084807:01f7b585d01f18ca73edfc6dbc8092c4558d8fe7b49f7f2cf5b0fc67360caf18e7748a85"; shbts="1637548807\05450238238285\0541669084807:01f70199d28af67ca9180c29e266a7008cb467dc48e3682a1f403ffdbc022c70f77c7563"; datr=34ScYXpoiE-uEQBXIdLZp9kp; csrftoken=Ya2BsPMHnvY0QBV8LchKF5jElwlnL1mX; ds_user_id=50648183942; sessionid=50648183942:cTgoeTsIyEMi2J:26; rur="VLL\05450648183942\0541669281792:01f7a094f6464ec82805e57397515d6a201243243c23b736407ddfe6111e49302786c98d"'
    # 186手机号 humm_abcd
    cookie = 'YYOjugALAAHSnFfx3CKUjQ1rWvgB; ig_did=619086B5-DBC4-46B9-94DE-03573234571E; ig_nrcb=1; shbid="15883\05450238238285\0541669084807:01f7b585d01f18ca73edfc6dbc8092c4558d8fe7b49f7f2cf5b0fc67360caf18e7748a85"; shbts="1637548807\05450238238285\0541669084807:01f70199d28af67ca9180c29e266a7008cb467dc48e3682a1f403ffdbc022c70f77c7563"; datr=34ScYXpoiE-uEQBXIdLZp9kp; csrftoken=fcZI36Wc8KtnQpIcWk5mpZnMukh1IjLX; ds_user_id=50662902597; sessionid=50662902597%3AxXLz9k0QSJ5b5F%3A22; rur="VLL\05450662902597\0541669354838:01f7f9eaa6f1bec93aa77e5000ff889768fd91251952fb6ab80b30c45154413a9ae3c7d3"'
    # 199手机号 lsp
    #cookie = 'YYOjugALAAHSnFfx3CKUjQ1rWvgB; ig_did=619086B5-DBC4-46B9-94DE-03573234571E; ig_nrcb=1; shbid="15883\05450238238285\0541669084807:01f7b585d01f18ca73edfc6dbc8092c4558d8fe7b49f7f2cf5b0fc67360caf18e7748a85"; shbts="1637548807\05450238238285\0541669084807:01f70199d28af67ca9180c29e266a7008cb467dc48e3682a1f403ffdbc022c70f77c7563"; datr=34ScYXpoiE-uEQBXIdLZp9kp; csrftoken=ig7r6qMsy9QXjnH5xeOB4r5vfrpvDA10; ds_user_id=50361064848; sessionid=50361064848:i2owbDVmHxWnAu:18; rur="PRN\05450361064848\0541669276592:01f787a6b63a6f91fc25e9ee34de64c3bf927d87d16851037dbb989aa22ef76865e8ee43"'
    user_agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                  'Opera/9.25 (Windows NT 5.1; U; en)',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                  'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                  'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                  "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                  "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "]
    headers = {}

    headers.setdefault('user-agent',user_agent[0])
    headers.setdefault('cookie', cookie)

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
    # cookie_str = ''
    # headers.setdefault('cookie',cookie_str.join(str_list))

    return headers

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
        con.close()
        cue.close()

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
        con.close()
        cue.close()

def query_one_by_ins_account(ins_account):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询明星的帖子的信息")
    try:
        cue.execute("select * from ins_account_enums where ins_account = '" + ins_account + "'")
        return cue.fetchone()
    except Exception as e:
        print('query_one_by_ins_account error:', e)
    con.close()
    cue.close()

def query_newest_one(ins_account):
    con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cue = con.cursor()
    print("查询该账号最新的一条帖子")
    try:
        cue.execute("SELECT * FROM ins_tag_info WHERE ins_account='" + ins_account +"' ORDER BY publish_time DESC LIMIT 0,1")
        return cue.fetchone()
    except Exception as e:
        print('query_newest_one error:', e)
    con.close()
    cue.close()

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
    response = requests.get("https://www.instagram.com/" + ins_account + "/", proxies=getProxy(), headers=getHeaders(),timeout=10)
    if re.search("login", response.url) is not None:
        print("访问失败的情况，账号可能存在被限制的可能")
        return
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
        first = 50
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
    num = 1
    base_query_url = "https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables="
    while has_next_page:
        variables = json.dumps({
            'id': str(user_id),
            'first': first,
            'after': str(end_cursor)
        }, separators=(',', ':'))  # 不指定separators的话key:value的:后会默认有空格，因为其默认separators为(', ', ': ')
        url = base_query_url + urllib.parse.quote(variables)
        print("分页接口之前node_list的大小：" + str(len(node_list)) + "，总计大小为：" + str(total_count) + "，访问次数：" + str(num))
        time.sleep(1)
        num = num + 1
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
        # 轮询ins账号
        # total_ins_account = query_all_ins_account()
        total_ins_account = ((1, 'natgeo'),) # __zf0827__ (2, 'mariadelaord'),(3, 'dianasilverss'),
        for singleIns in total_ins_account:
            searchUser(singleIns[1]) # 取出index=1 的字段
            print(singleIns[1] + "该明星查找完毕")

    finally:
        print("finally")
       # driver.quit()

