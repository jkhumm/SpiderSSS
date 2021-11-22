import json

from urllib import request, parse

import pymysql
import requests
import urllib

from bs4 import BeautifulSoup
from lxml import etree

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import *

print("------- requests包学习 --------")

# 1.get请求
# token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzY3ODQyNDUsIm1lbWJlcklkIjoyMDAxMDAxMX0.8FI_1lYM' \
#         '-rwKHy77PaABnI7lWdi4_aQBSsIK7cBaO44 '
# payload = {'key1': 'value1', 'key2': 'value2'}
# headers = {'content-type': 'application/json', 'token': token}
# url = "http://192.168.1.148:30020/api/app/testDemo/testGetWay"
# res = requests.get(url, params=payload, headers=headers)
# print("结果：" + res.text)
# # 如果返回的是json数据，可以通过r.json()进行解析
# print(res.json())

# 2.post请求
# url = 'http://httpbin.org/post'
# # 最基本的传参方法可以利用 data 这个参数
# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.post(url, data=payload)
# print(r.text)
# # 有时候我们需要传送的信息不是表单形式的，需要我们传JSON格式的数据过去，
# # 所以我们可以用json.dumps()方法把表单数据序列化。
# payload = {'some': 'data'}
# r = requests.post(url, data=json.dumps(payload))
# print(r.text)

# 直接用urllib.request模块的urlopen()获取页面，page的数据格式为bytes类型，需要decode()解码，转换成str类型。
# response = urllib.request.urlopen("http://www.baidu.com")
# page = response.read()
# page = page.decode('utf-8')

# - read() , readline() ,readlines() , fileno() , close() ：对HTTPResponse类型数据进行操作
# - info()：返回HTTPMessage对象，表示远程服务器返回的头信息
# - getcode()：返回Http状态码。如果是http请求，200请求成功完成;404网址未找到
# - geturl()：返回请求的url


url = 'http://www.lagou.com/zhaopin/Python/?labelWords=label'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    # - User-Agent ：这个头部可以携带如下几条信息：浏览器名和版本号、操作系统名和版本号、默认语言
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    # - Referer：可以用来防止盗链，有一些网站图片显示来源http://***.com，就是检查Referer来鉴定的
    'Connection': 'keep-alive'  # - Connection：表示连接状态，记录Session的状态。
}
# req = request.Request(url, headers=headers)
# page = request.urlopen(req).read()
# page = page.decode('utf-8')


url = 'http://httpbin.org/post'
data = {
    'first': 'true',
    'pn': 1,
    'kd': 'Python'
}
# urlencode()主要作用就是将url附上要提交的数据。 Post的数据必须是bytes或者iterable of bytes，不能是str，因此需要进行encode()编码。
# data = parse.urlencode(data).encode('utf-8')
# req = request.Request(url, data=data)
# page = request.urlopen(req).read()
# page = page.decode('utf-8')


# 当需要抓取的网站设置了访问限制，这时就需要用到代理来抓取数据。
data = {
    'first': 'true',
    'pn': 1,
    'kd': 'Python'
}
# proxy = request.ProxyHandler({'http': 'ip:port'})  # 设置proxy
# opener = request.build_opener(proxy)  # 挂载opener
# request.install_opener(opener)  # 安装opener
# data = parse.urlencode(data).encode('utf-8')
# page = opener.open(url, data).read()
# page = page.decode('utf-8')
# print(page)


# BeautifulSoup

html = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
<body>
    <p class="title1" name="dromouse">
        <b>The Dormouse's story</b>
    </p>
    <p class="story">
        Once upon a time there were three little sisters; and their names were
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
    </p>
    <p class="story">...</p>
</body>
"""

# soup = BeautifulSoup(html)
# # 打印一下 soup 对象的内容，格式化输出
# print(soup.prettify)
#
# # 结构化数据解析
# print(soup.title)  # 获取title   <title>The Dormouse's story</title>
# print(soup.title.name)  # title标签名称   title
# print(soup.title.string)  # title标签内容  The Dormouse's story
# print(soup.title.parent.name)  # 父标签名称  head
# print(soup.p['class'])  # 属性获取  ['title']   ['title']
# print(soup.find_all('a'))  # 查找所有标签  [<a>content1<a/>,<a>content2<a/>,...]
# print(soup.find(id="link3"))  # 通过id查找  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
# for link in soup.find_all('a'):  # 遍历获取所有a标签
#     print(link.get(
#         'href'))  # 获取a标签href属性   http://example.com/elsie'  http://example.com/lacie  http://example.com/tillie


text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
html = etree.HTML(text)  # 自动补全缺失
# result = etree.tostring(html)
# print(result)
# # xpath
# result = html.xpath('//li')
# print(result)
# print(len(result))
# print(type(result))
# print(type(result[0]))
# # 获取 <li> 标签下 href 为 link1.html 的 <a> 标签
# result = html.xpath('//li/a[@href="link1.html"]')
# print(result)
# # 获取倒数第二个元素的内容
# result = html.xpath('//li[last()-1]/a')
# print(result[0].text)
# # 获取 class 为 item-0 的标签名
# result = html.xpath('//*[@class="item-0"]')
# print(result[0].tag)

# Selenium库基本使用


# driver = webdriver.Chrome()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")  # 根据name查找元素
# elem.send_keys("pycon")  # 输入内容
# elem.send_keys(Keys.RETURN)  # 回车
# print(driver.page_source)  # 返回浏览器渲染后页面
# # driver.close()  # 并不会退出模拟程序，只是关闭了窗口
# driver.quit()  # 真正退出

driver = webdriver.Chrome()
driver.get("http://somedomain/url_that_delays_loading")
try:
    # 如果前面网站不可访问 net::ERR_NAME_NOT_RESOLVED，也就不会走这里了，会直接抛错，下面代码一概不执行
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))
finally:
    print("退出")
    driver.quit()
    driver.close()
# print("-----")


# 访问数据库

con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
cue = con.cursor()

print("------- end --------")
